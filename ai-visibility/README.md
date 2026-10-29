# AI visibility agent

A weekly agent that finds ways to make Vionlabs more visible in AI answers and
search, and turns them into tasks in the
[Vionlabs AI Visibility Playbook](https://claude.ai/artifact/6wcCXKjTxoMy6RRQRoMY5u).
It runs as the Claude Code routine "Vionlabs AI visibility weekly" every
Monday at 06:33 Stockholm time and follows [AGENT.md](AGENT.md).

Each run it:

1. Measures brand and non-branded searches (Search Console, through
   Supermetrics), and AI citations for Vionlabs and six competitors, Domain
   Rating, referring domains and non-branded rankings (Ahrefs).
2. Finds outreach targets: sites that started linking to competitors but not
   to us, and pages ranking for our buyer prompts that leave us out (Ahrefs
   and web search).
3. Finds content gaps from competitors' rankings, monthly (Ahrefs).
4. Audits vionlabs.com (Webflow) and scans the news.
5. Does the backlog tasks people have set to "Approved: agent does it" in the
   Agent column, publishing on vionlabs.com within the rules in AGENT.md.
6. Drafts up to two "Agent drafts" tasks a week: content as Webflow CMS drafts,
   outreach as ready-to-copy text.
7. Adds up to 8 new tasks to the backlog and writes a readout tab plus a KPI
   row in the Tracking log, listing every site change so it can be undone.

It needs no API keys. The routine needs four connectors attached (Ahrefs,
Webflow, Claude Docs and Supermetrics, for Google Search Console) and this
repository. `.claude/settings.json` at the
repository root pre-approves the tools it uses, so an unattended run does not
stop at permission prompts, and denies the Webflow Designer and element tools. A run uses about 6,000 of the
200,000 monthly units on the Ahrefs Lite plan.

## Files

- `config/brands.json`: Vionlabs and the competitors whose citations and
  links are tracked. Change the list here.
- `config/prompts.json`: the 21 buyer prompts from the playbook.
- `config/facts.json`: canonical facts and the red flags that catch confused
  descriptions.
- `results/<date>/snapshot.json`: what each run measured and found.

Ahrefs counts AI answers that link to a site. Unlinked mentions need its Brand
Radar add-on, which the Lite plan does not include.
