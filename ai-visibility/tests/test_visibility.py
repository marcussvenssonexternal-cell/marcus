"""Offline tests: parsers, scoring and a full run with stubbed engines."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import visibility as v  # noqa: E402

BRANDS = v.load_config("brands.json")
FACTS = v.load_config("facts.json")


class ParserTests(unittest.TestCase):
    def test_openai_reads_text_and_url_citations(self):
        data = {
            "model": "gpt-5",
            "output": [
                {"type": "web_search_call", "status": "completed"},
                {"type": "message", "content": [{
                    "type": "output_text",
                    "text": "Try Vionlabs or Gracenote.",
                    "annotations": [
                        {"type": "url_citation", "url": "https://www.vionlabs.com/curio", "title": "Curio"},
                        {"type": "file_citation", "file_id": "x"},
                    ],
                }]},
            ],
        }
        parsed = v.parse_openai(data)
        self.assertEqual(parsed["text"], "Try Vionlabs or Gracenote.")
        self.assertEqual(parsed["citations"], [{"url": "https://www.vionlabs.com/curio", "title": "Curio"}])

    def test_perplexity_prefers_search_results_then_citations(self):
        with_results = {"choices": [{"message": {"content": "Answer"}}],
                        "search_results": [{"url": "https://a.com/x", "title": "A"}],
                        "citations": ["https://b.com"]}
        self.assertEqual(v.parse_perplexity(with_results)["citations"], [{"url": "https://a.com/x", "title": "A"}])
        only_citations = {"choices": [{"message": {"content": "Answer"}}], "citations": ["https://b.com"]}
        self.assertEqual(v.parse_perplexity(only_citations)["citations"], [{"url": "https://b.com", "title": ""}])

    def test_gemini_joins_parts_and_reads_grounding_chunks(self):
        data = {"modelVersion": "gemini-2.5-flash", "candidates": [{
            "content": {"parts": [{"text": "Part one. "}, {"text": "Part two."}]},
            "groundingMetadata": {"groundingChunks": [
                {"web": {"uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/abc", "title": "vionlabs.com"}},
            ]},
        }]}
        parsed = v.parse_gemini(data)
        self.assertEqual(parsed["text"], "Part one. Part two.")
        self.assertEqual(v.domain_of(parsed["citations"][0]), "vionlabs.com")

    def test_claude_joins_text_blocks_and_reads_citations(self):
        blocks = [
            {"type": "server_tool_use", "name": "web_search", "input": {"query": "q"}},
            {"type": "web_search_tool_result", "content": [{"type": "web_search_result", "url": "https://x.com", "title": "X"}]},
            {"type": "text", "text": "Vionlabs ", "citations": [
                {"type": "web_search_result_location", "url": "https://vionlabs.com/our-ai", "title": "Our AI", "cited_text": "..."}]},
            {"type": "text", "text": "is one option.", "citations": None},
        ]
        parsed = v.parse_claude(blocks, "claude-opus-5-5")
        self.assertEqual(parsed["text"], "Vionlabs is one option.")
        self.assertEqual([c["url"] for c in parsed["citations"]], ["https://vionlabs.com/our-ai"])


class ScorerTests(unittest.TestCase):
    def setUp(self):
        self.scorer = v.Scorer(BRANDS, FACTS)

    def test_orders_brands_by_first_mention_and_finds_our_position(self):
        text = "Top picks: Gracenote, then TwelveLabs, and Vion Labs for mood-based discovery."
        result = self.scorer.score(text, [])
        self.assertEqual(result["brands"], ["Gracenote", "TwelveLabs", "Vionlabs"])
        self.assertTrue(result["mentioned"])
        self.assertEqual(result["position"], 3)

    def test_counts_our_domain_in_text_and_citations(self):
        result = self.scorer.score("See vionlabs.com for details.", [{"url": "https://www.vionlabs.com/api", "title": ""}])
        self.assertTrue(result["mentioned"])
        self.assertTrue(result["us_cited"])
        self.assertEqual(result["cited_domains"], ["vionlabs.com"])

    def test_alias_needs_word_boundaries(self):
        result = self.scorer.score("Recombeeish tools and Netrality are not vendors.", [])
        self.assertEqual(result["brands"], [])
        self.assertIsNone(result["position"])

    def test_red_flags_only_on_answers_about_us_or_branded_prompts(self):
        text = "Vionlabs builds smart building sensors."
        self.assertEqual(self.scorer.score(text, [])["flags"], ["Confused with Vion Labs, a smart-buildings company"])
        unrelated = "Some vendors make smart buildings."
        self.assertEqual(self.scorer.score(unrelated, [])["flags"], [])
        self.assertEqual(len(self.scorer.score("VisionLabs is a face recognition firm.", [], branded=True)["flags"]), 1)


class RunTests(unittest.TestCase):
    def test_full_run_with_stubbed_engines_writes_summary_and_deltas(self):
        prompts = [p for p in v.load_config("prompts.json") if p["id"] in (1, 19)]

        def good_engine(prompt, cfg, key):
            if "Vionlabs" in prompt:  # branded prompt
                return {"text": "Vionlabs is a Stockholm company.", "citations": [{"url": "https://vionlabs.com/company", "title": ""}], "model": "stub-1"}
            return {"text": "Gracenote and Vionlabs lead.", "citations": [
                {"url": "https://lists.example.com/best", "title": ""},
                {"url": "https://lists.example.com/best", "title": ""}], "model": "stub-1"}

        def blocked_engine(prompt, cfg, key):
            raise v.EngineError("network error: Tunnel connection failed: 403")

        callers = {"good": good_engine, "blocked": blocked_engine}
        engines = {"good": ({"model": "stub-1"}, "k"), "blocked": ({"model": "stub-2"}, "k")}
        scorer = v.Scorer(BRANDS, FACTS)
        with tempfile.TemporaryDirectory() as tmp:
            earlier = Path(tmp) / "2026-10-19"
            earlier.mkdir()
            (earlier / "summary.json").write_text(json.dumps({"date": "2026-10-19", "kpis": {"mention_rate_unbranded": 0.25}}))
            out = Path(tmp) / "2026-10-26"
            v.run_batch(prompts, engines, runs=3, out_dir=out, scorer=scorer, workers=1, callers=callers)
            summary = v.summarize(out)

            runs = v.read_runs(out / "runs.jsonl")
            self.assertEqual(len(runs), 12)
            blocked = [r for r in runs if r["engine"] == "blocked"]
            self.assertTrue(all(not r["ok"] for r in blocked))
            self.assertTrue(any(r["error"].startswith("skipped") for r in blocked))

            kpis = summary["kpis"]
            self.assertEqual(kpis["runs_ok"], 6)
            self.assertEqual(kpis["mention_rate_unbranded"], 1.0)
            self.assertEqual(kpis["share_of_voice_unbranded"], 0.5)
            self.assertEqual(kpis["avg_position_when_named"], 2)
            self.assertEqual(kpis["citation_rate"], 0.5)
            self.assertEqual(summary["previous"]["date"], "2026-10-19")
            self.assertEqual(summary["top_cited_urls"][0][:2], ["https://lists.example.com/best", 1])
            self.assertIn("+75.0 pts", (out / "summary.md").read_text())

            # A second call resumes: successful runs are not asked again.
            calls = []
            callers["good"] = lambda *a: calls.append(a) or good_engine(*a)
            v.run_batch(prompts, {"good": engines["good"]}, runs=3, out_dir=out, scorer=scorer, workers=1, callers=callers)
            self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
