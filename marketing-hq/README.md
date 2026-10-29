# Marketing HQ: Atlas

Atlas is the orchestrator for Vionlabs marketing. It turns the strategy into a weekly plan, briefs
the agent that owns each piece, keeps the fleet of agents healthy and keeps one scoreboard.
Marcus approves anything public, paid or sent outside.

**Strategy doc:** https://claude.ai/artifact/Lwk7SRf92iaZpJZdWzDTuZ (private). It holds the goal,
the one story, the six plays, who owns what, the KPIs and targets, the roadmap and open decisions,
plus a **Weekly plans** tab and a **Scoreboard log** tab.

## The team

| Play | Agent |
| --- | --- |
| Foundation: one story, plan, scoreboard | Atlas, Mason (website) |
| Founder voice | Iris (Content Radar), Content bot |
| Earned media | Guest-post agent |
| Search and AI answers | AI visibility agent |
| Proof | Content bot, with sales |
| Paid amplification | Vera (ads creative), Ads optimization |
| Events and partners | Events agent (proposed; Atlas covers it until then) |

Sessions, routines and outputs for each are in `config/agents.yaml`.

## Schedule

Two scheduled tasks fire into Atlas's own session, so it keeps its context and Marcus can talk to
it there between runs:

- **Marketing HQ weekly plan**, Monday 08:38 Stockholm time. It runs after the AI visibility
  (06:33) and Content Radar (07:41) runs. Atlas checks every agent, adds a scoreboard row, writes
  the week's plan tab, sends the briefs and messages Marcus.
- **Marketing HQ Friday wrap**, Friday 14:38. It covers what shipped, what slipped and what is
  blocked.

Edit or pause them under Scheduled tasks on claude.ai.

## Talking to Atlas

Open the session "Atlas – Marketing director" and ask, for example:

- "status": where every brief and agent stands;
- "brief Vera on a DPP invite ad";
- "switch to propose mode": briefs then wait for your go;
- "add the new events agent to the roster".

## Files

| Path | What it is |
| --- | --- |
| `AGENT.md` | Atlas's procedure: Monday plan, Friday wrap, between runs, brief format, rules |
| `config/agents.yaml` | The roster: each agent's play, the session to brief, routines, outputs, health check |
| `config/operating.yaml` | Dispatch mode, schedule, limits, and the strategy doc's tab, table and enum ids |

This repository is public. Budgets, spend, MQLs, ad account IDs and target companies stay in the
strategy doc, never here.
