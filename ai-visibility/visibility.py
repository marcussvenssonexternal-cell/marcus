#!/usr/bin/env python3
"""Weekly AI-visibility tracker for Vionlabs.

Sends the playbook's buyer prompts to AI engines that search the web
(ChatGPT, Perplexity, Gemini and Claude), records which vendors each answer
names and which pages it cites, and writes a summary with week-over-week
changes.

    python visibility.py check                       # which engines are ready
    python visibility.py run                         # the full weekly run
    python visibility.py run --engines claude --prompts 1,19 --runs 1
    python visibility.py summarize results/2026-10-26
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import datetime as dt
import json
import os
import re
import statistics
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_DIR = HERE / "config"
RESULTS_DIR = HERE / "results"

# Gemini links its grounding sources through this redirect host; the source's
# real domain is in the chunk title.
GEMINI_REDIRECT_HOST = "vertexaisearch.cloud.google.com"

# After this many network failures in a row, an engine is treated as
# unreachable and its remaining calls are skipped instead of timing out.
MAX_CONSECUTIVE_NETWORK_FAILURES = 3


def load_config(name):
    with open(CONFIG_DIR / name, encoding="utf-8") as f:
        return json.load(f)


class EngineError(Exception):
    """An engine call failed in a way the run records rather than crashes on."""


# --- HTTP --------------------------------------------------------------------

def post_json(url, headers, body, timeout=240, retries=3):
    data = json.dumps(body).encode("utf-8")
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            url, data=data, method="POST",
            headers={"Content-Type": "application/json", **headers},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(retry_delay(e.headers.get("retry-after"), attempt))
                continue
            raise EngineError(f"HTTP {e.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                time.sleep(retry_delay(None, attempt))
                continue
            raise EngineError(f"network error: {getattr(e, 'reason', e)}") from None


def retry_delay(retry_after, attempt):
    try:
        return max(1.0, float(retry_after))
    except (TypeError, ValueError):
        return 2.0 ** (attempt + 2)


# --- Engines -------------------------------------------------------------------
# Each ask_* function returns {"text", "citations": [{"url", "title"}], "model"}.

def ask_chatgpt(prompt, cfg, key):
    data = post_json(
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {key}"},
        {"model": cfg["model"], "input": prompt, "tools": [{"type": "web_search"}]},
    )
    return parse_openai(data)


def parse_openai(data):
    texts, citations = [], []
    for item in data.get("output") or []:
        if item.get("type") != "message":
            continue
        for part in item.get("content") or []:
            if part.get("type") != "output_text":
                continue
            texts.append(part.get("text") or "")
            for note in part.get("annotations") or []:
                if note.get("type") == "url_citation" and note.get("url"):
                    citations.append({"url": note["url"], "title": note.get("title") or ""})
    return {"text": "\n".join(texts), "citations": citations, "model": data.get("model")}


def ask_perplexity(prompt, cfg, key):
    data = post_json(
        "https://api.perplexity.ai/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {"model": cfg["model"], "messages": [{"role": "user", "content": prompt}]},
    )
    return parse_perplexity(data)


def parse_perplexity(data):
    choices = data.get("choices") or [{}]
    text = (choices[0].get("message") or {}).get("content") or ""
    citations = [
        {"url": r["url"], "title": r.get("title") or ""}
        for r in data.get("search_results") or [] if r.get("url")
    ]
    if not citations:
        citations = [{"url": u, "title": ""} for u in data.get("citations") or [] if u]
    return {"text": text, "citations": citations, "model": data.get("model")}


def ask_gemini(prompt, cfg, key):
    data = post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{cfg['model']}:generateContent",
        {"x-goog-api-key": key},
        {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "tools": [{"google_search": {}}]},
    )
    return parse_gemini(data)


def parse_gemini(data):
    candidate = (data.get("candidates") or [{}])[0]
    parts = (candidate.get("content") or {}).get("parts") or []
    text = "".join(p.get("text") or "" for p in parts)
    chunks = (candidate.get("groundingMetadata") or {}).get("groundingChunks") or []
    citations = [
        {"url": c["web"].get("uri") or "", "title": c["web"].get("title") or ""}
        for c in chunks if c.get("web")
    ]
    return {"text": text, "citations": citations, "model": data.get("modelVersion")}


def ask_claude(prompt, cfg, key):
    import anthropic  # only this engine needs the SDK

    # The key comes from a dedicated variable, and the public API URL is pinned:
    # Claude Code sessions set their own ANTHROPIC_* variables.
    client = anthropic.Anthropic(api_key=key, base_url="https://api.anthropic.com", max_retries=4)
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": cfg.get("max_searches", 5)}]
    messages = [{"role": "user", "content": prompt}]
    blocks = []
    for _ in range(4):
        try:
            response = client.beta.messages.create(
                model=cfg["model"],
                max_tokens=16000,
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
                output_config={"effort": cfg.get("effort", "medium")},
                tools=tools,
                messages=messages,
            )
        except anthropic.APIStatusError as e:
            raise EngineError(f"HTTP {e.status_code}: {e.message}") from None
        except anthropic.APIConnectionError as e:
            raise EngineError(f"network error: {e}") from None
        blocks.extend(response.content)
        if response.stop_reason != "pause_turn":
            break
        # The server-side search loop paused; resending lets it resume.
        messages = [messages[0], {"role": "assistant", "content": blocks}]
    if response.stop_reason == "refusal":
        raise EngineError("refused")
    return parse_claude([b.model_dump() for b in blocks], response.model)


def parse_claude(blocks, model=None):
    texts, citations = [], []
    for block in blocks:
        if block.get("type") != "text":
            continue
        texts.append(block.get("text") or "")
        for cite in block.get("citations") or []:
            if cite.get("url"):
                citations.append({"url": cite["url"], "title": cite.get("title") or ""})
    return {"text": "".join(texts), "citations": citations, "model": model}


ENGINES = {
    "chatgpt": ask_chatgpt,
    "perplexity": ask_perplexity,
    "gemini": ask_gemini,
    "claude": ask_claude,
}


# --- Scoring -------------------------------------------------------------------

def domain_of(citation):
    host = (urllib.parse.urlparse(citation.get("url") or "").hostname or "").lower()
    if host.endswith(GEMINI_REDIRECT_HOST):
        title = (citation.get("title") or "").strip().lower()
        if "." in title and " " not in title:
            host = title
    return host.removeprefix("www.")


def dedupe_citations(citations):
    seen, unique = set(), []
    for c in citations:
        if c["url"] and c["url"] not in seen:
            seen.add(c["url"])
            unique.append(c)
    return unique


class Scorer:
    def __init__(self, brands_cfg, facts_cfg):
        self.us = brands_cfg["us"]["name"]
        self.own_domains = [d.lower() for d in brands_cfg["us"]["domains"]]
        self.brands = [
            (b["name"], [re.compile(r"(?<!\w)" + re.escape(a) + r"(?!\w)", re.IGNORECASE) for a in b["aliases"]])
            for b in [brands_cfg["us"], *brands_cfg["competitors"]]
        ]
        self.red_flags = [(re.compile(f["pattern"], re.IGNORECASE), f["why"]) for f in facts_cfg.get("red_flags", [])]

    def is_own(self, domain):
        return any(domain == d or domain.endswith("." + d) for d in self.own_domains)

    def score(self, text, citations, branded=False):
        found = []
        for name, patterns in self.brands:
            starts = [m.start() for p in patterns if (m := p.search(text))]
            if starts:
                found.append((min(starts), name))
        named = [name for _, name in sorted(found)]
        mentioned = self.us in named
        domains = [domain_of(c) for c in citations]
        return {
            "brands": named,
            "mentioned": mentioned,
            "position": named.index(self.us) + 1 if mentioned else None,
            "cited_domains": domains,
            "us_cited": any(self.is_own(d) for d in domains),
            "flags": [why for rx, why in self.red_flags if (mentioned or branded) and rx.search(text)],
        }


# --- Running -------------------------------------------------------------------

def run_batch(prompts, engines, runs, out_dir, scorer, workers=4, callers=ENGINES):
    """Ask every prompt `runs` times on every engine and append to runs.jsonl.

    `engines` maps engine name -> (config, api key). Calls already recorded as
    successful in runs.jsonl are skipped, so an interrupted run can resume.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    runs_path = out_dir / "runs.jsonl"
    done = {(r["engine"], r["prompt_id"], r["run"]) for r in read_runs(runs_path) if r["ok"]}
    lock = threading.Lock()
    network_failures = collections.Counter()
    unreachable = set()
    date = out_dir.name

    def ask(engine, cfg, key, prompt, n):
        record = {"date": date, "engine": engine, "model": cfg["model"], "prompt_id": prompt["id"],
                  "stage": prompt["stage"], "run": n}
        started = time.time()
        if engine in unreachable:
            record.update(ok=False, error="skipped: engine unreachable this run")
        else:
            try:
                answer = callers[engine](prompt["text"], cfg, key)
                citations = dedupe_citations(answer["citations"])
                record.update(ok=True, model=answer.get("model") or cfg["model"], text=answer["text"],
                              citations=citations,
                              **scorer.score(answer["text"], citations, branded=prompt["stage"] == "Brand"))
                with lock:
                    network_failures[engine] = 0
            except EngineError as e:
                record.update(ok=False, error=str(e))
                if str(e).startswith("network error"):
                    with lock:
                        network_failures[engine] += 1
                        if network_failures[engine] >= MAX_CONSECUTIVE_NETWORK_FAILURES:
                            unreachable.add(engine)
            except Exception as e:  # a malformed answer must not sink the whole run
                record.update(ok=False, error=f"unexpected {type(e).__name__}: {e}")
        record["seconds"] = round(time.time() - started, 1)
        with lock, open(runs_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    pools = {name: concurrent.futures.ThreadPoolExecutor(max_workers=workers) for name in engines}
    futures = [
        pools[name].submit(ask, name, cfg, key, prompt, n)
        for n in range(1, runs + 1)
        for prompt in prompts
        for name, (cfg, key) in engines.items()
        if (name, prompt["id"], n) not in done
    ]
    for future in concurrent.futures.as_completed(futures):
        future.result()
    for pool in pools.values():
        pool.shutdown()
    return runs_path


def read_runs(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# --- Summary -------------------------------------------------------------------

def ratio(part, whole):
    return round(part / whole, 4) if whole else None


def kpis_for(ok_runs):
    unbranded = [r for r in ok_runs if r["stage"] != "Brand"]
    positions = [r["position"] for r in unbranded if r["position"]]
    named = sum(r["mentioned"] for r in unbranded)
    return {
        "runs_ok": len(ok_runs),
        "mention_rate_unbranded": ratio(named, len(unbranded)),
        "share_of_voice_unbranded": ratio(named, sum(len(r["brands"]) for r in unbranded)),
        "citation_rate": ratio(sum(r["us_cited"] for r in ok_runs), len(ok_runs)),
        "avg_position_when_named": round(statistics.mean(positions), 2) if positions else None,
        "unbranded_prompts_with_mention": len({r["prompt_id"] for r in unbranded if r["mentioned"]}),
        "prompts_with_citation": len({r["prompt_id"] for r in ok_runs if r["us_cited"]}),
    }


def find_previous(out_dir):
    earlier = sorted(
        d for d in out_dir.parent.iterdir()
        if d.is_dir() and d.name < out_dir.name and (d / "summary.json").exists()
    )
    return earlier[-1] if earlier else None


def summarize(out_dir, previous_dir=None):
    runs = read_runs(out_dir / "runs.jsonl")
    prompts = {p["id"]: p for p in load_config("prompts.json")}
    brands_cfg = load_config("brands.json")
    us = brands_cfg["us"]["name"]
    own = Scorer(brands_cfg, {}).is_own
    ok = [r for r in runs if r["ok"]]
    unbranded = [r for r in ok if r["stage"] != "Brand"]

    per_prompt = []
    for pid, prompt in prompts.items():
        rs = [r for r in ok if r["prompt_id"] == pid]
        if not rs:
            continue
        rivals = collections.Counter(b for r in rs for b in r["brands"] if b != us)
        per_prompt.append({
            "id": pid, "text": prompt["text"], "stage": prompt["stage"], "runs": len(rs),
            "mentions": sum(r["mentioned"] for r in rs),
            "engines_naming_us": sorted({r["engine"] for r in rs if r["mentioned"]}),
            "top_competitors": rivals.most_common(3),
        })

    url_prompts = collections.defaultdict(set)
    for r in ok:
        for c in r["citations"]:
            if not own(domain_of(c)):
                url_prompts[c["url"]].add(r["prompt_id"])

    if previous_dir is None:
        previous_dir = find_previous(out_dir)
    previous = None
    if previous_dir:
        with open(previous_dir / "summary.json", encoding="utf-8") as f:
            previous = json.load(f)

    kpis = kpis_for(ok)
    summary = {
        "date": out_dir.name,
        "runs_total": len(runs),
        "engines": {
            engine: {"model": next((r["model"] for r in ok if r["engine"] == engine), None),
                     **kpis_for([r for r in ok if r["engine"] == engine])}
            for engine in sorted({r["engine"] for r in runs})
        },
        "kpis": kpis,
        "previous": {"date": previous["date"], "kpis": previous["kpis"]} if previous else None,
        "per_prompt": per_prompt,
        "brands_named_unbranded": collections.Counter(b for r in unbranded for b in r["brands"]).most_common(),
        "top_cited_domains": collections.Counter(
            d for r in ok for d in set(r["cited_domains"]) if not own(d)).most_common(20),
        "top_cited_urls": sorted(
            ([url, len(pids), sorted(pids)] for url, pids in url_prompts.items()),
            key=lambda row: (-row[1], row[0]))[:25],
        "own_pages_cited": collections.Counter(
            c["url"] for r in ok for c in r["citations"] if own(domain_of(c))).most_common(),
        "flags": [{"engine": r["engine"], "prompt_id": r["prompt_id"], "run": r["run"], "flag": f}
                  for r in ok for f in r["flags"]],
        "errors": collections.Counter(f"{r['engine']}: {r['error'][:160]}" for r in runs if not r["ok"]).most_common(),
    }
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    with open(out_dir / "summary.md", "w", encoding="utf-8") as f:
        f.write(render_markdown(summary))
    return summary


# --- Markdown ------------------------------------------------------------------

KPI_LABELS = [
    ("mention_rate_unbranded", "Mention rate, unbranded prompts", "pct"),
    ("share_of_voice_unbranded", "Share of voice, unbranded prompts", "pct"),
    ("citation_rate", "Answers citing vionlabs.com", "pct"),
    ("avg_position_when_named", "Average position when named", "num"),
    ("unbranded_prompts_with_mention", "Unbranded prompts naming us (of 18)", "int"),
    ("prompts_with_citation", "Prompts citing vionlabs.com (of 21)", "int"),
    ("runs_ok", "Successful runs", "int"),
]


def fmt(value, kind):
    if value is None:
        return "n/a"
    if kind == "pct":
        return f"{value * 100:.1f}%"
    return f"{value:g}"


def fmt_change(now, before, kind):
    if now is None or before is None:
        return ""
    change = now - before
    if kind == "pct":
        return f"{change * 100:+.1f} pts"
    return f"{change:+g}"


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + " --- |" * len(header)]
    lines += ["| " + " | ".join(str(c).replace("|", "/") for c in row) + " |" for row in rows]
    return "\n".join(lines)


def render_markdown(s):
    prev = (s["previous"] or {}).get("kpis", {})
    out = [f"# AI visibility run {s['date']}", ""]
    out.append(f"{s['kpis']['runs_ok']} of {s['runs_total']} runs succeeded. "
               f"Previous run: {s['previous']['date'] if s['previous'] else 'none'}.")
    out += ["", "## Headline KPIs", "", table(
        ["KPI", "This run", "Previous", "Change"],
        [[label, fmt(s["kpis"][k], kind), fmt(prev.get(k), kind), fmt_change(s["kpis"][k], prev.get(k), kind)]
         for k, label, kind in KPI_LABELS])]
    out += ["", "## By engine", "", table(
        ["Engine", "Model", "Runs OK", "Mention rate", "Share of voice", "Citation rate", "Avg position"],
        [[e, v["model"] or "", v["runs_ok"], fmt(v["mention_rate_unbranded"], "pct"),
          fmt(v["share_of_voice_unbranded"], "pct"), fmt(v["citation_rate"], "pct"),
          fmt(v["avg_position_when_named"], "num")] for e, v in s["engines"].items()])]
    out += ["", "## By prompt", "", table(
        ["#", "Prompt", "Stage", "Named us", "Engines naming us", "Top competitors"],
        [[p["id"], p["text"], p["stage"], f"{p['mentions']}/{p['runs']}", ", ".join(p["engines_naming_us"]) or "none",
          ", ".join(f"{b} ({n})" for b, n in p["top_competitors"])] for p in s["per_prompt"]])]
    out += ["", "## Vendors named in unbranded answers", "", table(
        ["Vendor", "Runs naming it"], s["brands_named_unbranded"][:20])]
    out += ["", "## Most-cited third-party pages (outreach candidates)", "", table(
        ["URL", "Prompts citing it", "Prompt numbers"],
        [[url, n, ", ".join(map(str, pids))] for url, n, pids in s["top_cited_urls"]])]
    out += ["", "## Most-cited domains", "", table(["Domain", "Runs citing it"], s["top_cited_domains"])]
    out += ["", "## vionlabs.com pages cited", ""]
    out.append(table(["URL", "Times cited"], s["own_pages_cited"]) if s["own_pages_cited"] else "None this run.")
    out += ["", "## Red flags in answers that name us", ""]
    out.append(table(["Engine", "Prompt", "Run", "Flag"],
                     [[f["engine"], f["prompt_id"], f["run"], f["flag"]] for f in s["flags"]])
               if s["flags"] else "None.")
    out += ["", "## Errors", ""]
    out.append(table(["Error", "Count"], s["errors"]) if s["errors"] else "None.")
    return "\n".join(out) + "\n"


# --- CLI -----------------------------------------------------------------------

def configured_engines(names=None):
    """Return {name: (config, key)} for enabled engines that have a key set."""
    cfg = load_config("engines.json")
    ready = {}
    for name, engine in cfg["engines"].items():
        if not engine.get("enabled") or (names and name not in names):
            continue
        key = os.environ.get(engine["key_env"])
        if key:
            ready[name] = (engine, key)
        else:
            print(f"skipping {name}: {engine['key_env']} is not set", file=sys.stderr)
    return ready


def reachable(host):
    try:
        urllib.request.urlopen(f"https://{host}/", timeout=15)
    except urllib.error.HTTPError:
        pass  # any HTTP answer means the host is reachable
    except (urllib.error.URLError, TimeoutError) as e:
        return f"BLOCKED ({getattr(e, 'reason', e)})"
    return "reachable"


def cmd_check(_args):
    cfg = load_config("engines.json")
    all_ready = True
    for name, engine in cfg["engines"].items():
        if not engine.get("enabled"):
            print(f"{name:<11} disabled in config/engines.json")
            continue
        has_key = bool(os.environ.get(engine["key_env"]))
        network = reachable(engine["host"])
        notes = []
        if name == "claude":
            try:
                import anthropic  # noqa: F401
            except ImportError:
                notes.append("SDK missing: pip install -r requirements.txt")
        ready = has_key and network == "reachable" and not notes
        all_ready &= ready
        key_state = "set" if has_key else f"MISSING ({engine['key_env']})"
        print(f"{name:<11} key {key_state:<40} {engine['host']}: {network}  model {engine['model']}"
              + (f"  {'; '.join(notes)}" if notes else ""))
    return 0 if all_ready else 1


def cmd_run(args):
    cfg = load_config("engines.json")
    engines = configured_engines(args.engines)
    if not engines:
        print("No engine has an API key set; nothing to run. See README.md.", file=sys.stderr)
        return 1
    prompts = load_config("prompts.json")
    if args.prompts:
        prompts = [p for p in prompts if p["id"] in args.prompts]
    out_dir = RESULTS_DIR / args.date
    scorer = Scorer(load_config("brands.json"), load_config("facts.json"))
    runs = args.runs or cfg["runs_per_prompt"]
    print(f"Running {len(prompts)} prompts x {len(engines)} engines x {runs} runs into {out_dir}")
    run_batch(prompts, engines, runs, out_dir, scorer, workers=args.workers or cfg["workers_per_engine"])
    summary = summarize(out_dir)
    print_headline(summary, out_dir)
    return 0


def cmd_summarize(args):
    out_dir = Path(args.dir).resolve()
    summary = summarize(out_dir, Path(args.previous).resolve() if args.previous else None)
    print_headline(summary, out_dir)
    return 0


def print_headline(summary, out_dir):
    for key, label, kind in KPI_LABELS:
        print(f"{label:<40} {fmt(summary['kpis'][key], kind)}")
    print(f"Summary: {out_dir / 'summary.md'}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="show which engines have a key and network access")
    run = sub.add_parser("run", help="ask every prompt on every ready engine")
    run.add_argument("--engines", type=lambda s: s.split(","), help="comma-separated, e.g. chatgpt,claude")
    run.add_argument("--prompts", type=lambda s: [int(x) for x in s.split(",")], help="comma-separated prompt ids")
    run.add_argument("--runs", type=int, help="runs per prompt per engine (default from config)")
    run.add_argument("--workers", type=int, help="parallel calls per engine (default from config)")
    run.add_argument("--date", default=dt.date.today().isoformat(), help="results folder name (default today)")
    summ = sub.add_parser("summarize", help="rebuild summary.json and summary.md for a results folder")
    summ.add_argument("dir")
    summ.add_argument("--previous", help="results folder to compare against (default: the latest earlier one)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    return {"check": cmd_check, "run": cmd_run, "summarize": cmd_summarize}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
