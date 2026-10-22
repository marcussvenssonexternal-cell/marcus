# AI visibility tracker

Measures how often AI engines name Vionlabs when buyers ask about our
category, and which pages those answers cite. It backs the weekly agent
described in [AGENT.md](AGENT.md), which writes its readout into the
[Vionlabs AI Visibility Playbook](https://claude.ai/artifact/6wcCXKjTxoMy6RRQRoMY5u).

Each run sends the 21 playbook prompts (`config/prompts.json`) three times to
each engine, with web search on:

| Engine | API | Key variable | Host to allow |
| --- | --- | --- | --- |
| ChatGPT | OpenAI Responses API, `web_search` tool | `OPENAI_API_KEY` | `api.openai.com` |
| Perplexity | Sonar chat completions | `PERPLEXITY_API_KEY` | `api.perplexity.ai` |
| Gemini | `generateContent` with Google Search grounding | `GEMINI_API_KEY` | `generativelanguage.googleapis.com` |
| Claude | Messages API, web search tool | `VISIBILITY_ANTHROPIC_API_KEY` | `api.anthropic.com` |

The API answers are close to, but not identical to, what the consumer apps
show; treat trends as the signal. Microsoft Copilot has no comparable API, so
it is covered by the Bing Webmaster Tools AI Performance report instead. The
Claude key uses its own variable name because Claude Code sessions set their
own `ANTHROPIC_*` variables.

## Setup

1. Create an API key with each provider and add it as an environment secret
   in the Claude Code cloud environment, under the variable names above.
2. Allow the hosts above under the environment's Network access settings.
   `www.vionlabs.com` is worth adding too, so the agent can check robots.txt
   and the sitemap.
3. Check: `python3 visibility.py check` prints, per engine, whether the key is
   set and the host is reachable.

The model names in `config/engines.json` are defaults; update them to the
models that power each consumer app when those change.

## Running it by hand

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python visibility.py run                                  # full run
.venv/bin/python visibility.py run --engines claude --prompts 1,19 --runs 1   # quick test
.venv/bin/python visibility.py summarize results/2026-10-26          # rebuild a summary
.venv/bin/python -m unittest discover -s tests                      # offline tests
```

A run that stops partway can be restarted with the same command; finished
calls are skipped.

## Output

`results/<date>/` holds:

- `runs.jsonl`: one line per engine call, with the answer text, cited URLs,
  vendors named in order, and our position.
- `summary.json` and `summary.md`: the KPIs, with changes against the latest
  earlier run, broken down by engine and by prompt, plus the most-cited
  third-party pages (the outreach list), red flags and errors.

| KPI | Definition |
| --- | --- |
| Mention rate | Share of answers to unbranded prompts (1 to 18) that name Vionlabs |
| Share of voice | Vionlabs mentions divided by all vendor mentions in those answers |
| Citation rate | Share of all answers that cite a vionlabs.com page |
| Average position | Where Vionlabs comes in the order vendors are named, when it is named |

Vendor names and aliases are in `config/brands.json`; canonical facts and the
red-flag patterns that catch confused answers are in `config/facts.json`.
