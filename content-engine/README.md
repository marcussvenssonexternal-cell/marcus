# Content Radar

A weekly research run for the Vionlabs content team. Every Monday it scans what competitors
and adjacent players published, what the streaming trade press is talking about, what's coming
up at the events Vionlabs attends, and who mentioned Vionlabs. It turns that into gaps worth
owning and ready-to-draft LinkedIn ideas for Arash's two posts a week.

**Live page:** https://claude.ai/artifact/UKwTmC8DtVMasqkdp3Xa2f (private until shared from the page's Share menu)

## Schedule

A Claude Routine, **Weekly Content Radar**, runs every Monday at 07:41 Stockholm time in a
fresh cloud session. It follows `.claude/skills/content-radar/SKILL.md`, adds the new week to
the live page (older weeks stay in the week picker), pushes the week's files to this repo, and
sends a push + email summary. Edit or pause it under Routines on claude.ai.

To run it by hand from any Claude Code session in this repo: "run the content radar".

## What's here

| Path | What it is |
| --- | --- |
| `config/brand.md` | Positioning, products, ICPs, pillars and voice rules (from Notion). Read by every run. |
| `config/watchlist.yaml` | Companies (by group), trade press, topics, mention keywords, search budget, page URL |
| `config/events.yaml` | Snapshot of the Notion Event Calendar, used when a run can't reach Notion |
| `reports/<ISO week>.json` | One file per week: ideas, gaps, themes, events, mentions, stats, competitor feed |
| `reports/<ISO week>.md` | The same week as a readable brief (generated) |
| `radar/template.html` | The page design |
| `radar/build.py` | Validates the weeks and builds `radar/index.html` and the briefs; `--recover` pulls past weeks back out of a published page |

## Changing what it watches

- **Add or drop a competitor:** edit `config/watchlist.yaml`. Fill in `site` when you know the
  blog or newsroom URL.
- **New positioning or voice rules:** edit `config/brand.md`.
- **Events:** keep the Notion Event Calendar up to date. Runs that can't reach Notion fall back
  to `config/events.yaml`, so refresh that snapshot when plans change.

## Limits to know about

- **Page fetches are blocked** by this cloud environment's network policy (blogs return 403 at
  the proxy), so research works from search-result summaries, each with a dated URL. Check exact
  quotes and numbers on the source page before publishing a post. Allowing general internet
  access in the environment's network settings lets runs read full articles.
- **Web searches are capped per turn** and shared across the run's research agents. The run
  budgets them (`search_budget`), so coverage of quiet companies can be thin in a given week.
- **LinkedIn is login-walled.** Mentions and competitor social activity are limited to what search
  engines index. For complete mention tracking, use LinkedIn page notifications or a social
  listening tool alongside this.
