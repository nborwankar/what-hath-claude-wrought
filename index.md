---
layout: default
title: Home
---

<div class="hero">
  <h1>What Hath Claude Wrought</h1>
  <p class="tagline">A senior engineer who hasn't written a line of code in these projects — and has shipped more than ever.</p>
</div>

Senior engineer with decades in databases, machine learning, and enterprise application development roles in QA, dev, technical management, architecture and product management. 

O'Reilly author ([Vector Databases](https://github.com/nborwankar/VectorDatabasesBook)). 

Creator of [LearnDataScience](https://github.com/nborwankar/LearnDataScience) (3,000 stars, 1,600 forks — hand-built in 2013 when there were no such things as agents).

I have wide-scoped research ideas — hyperbolic embeddings for code search, neuro-symbolic query languages, Vonnegut's story shapes as generative constraints, geometric ananlysis of code hierarchies and the transition to industrial development of software that will emerge after this current phase of agentic development  — and for years I lacked the execution bandwidth to pursue them all.

Claude Code changed the equation.

> I didn't write a line of code in any of these projects. I brought the research questions, the domain knowledge, the architectural vision - what I wanted and what I didnt want. Claude brought systematic engineering, TDD discipline, and execution velocity. The best work happens when I stop tracking who typed what.

The cognitive boundary between us dissolves during deep work sessions. That's not a bug — it's what effective human-AI collaboration actually looks like. Not "AI wrote my code" but genuine co-creation where the seams disappear.

The collaboration has a consistent pattern:

- **I bring**: domain expertise, research hypotheses, architectural taste, quality standards, opinionatedness
- **Claude brings**: implementation velocity, test coverage, systematic debugging, framework knowledge and just enough randomw behavior to keep things interesting


Every project below was built with Claude Code as a pair programmer. Some were conceived and shipped in a single weekend. Others evolved over months of iterative sessions. Most of them represent ideas I'd carried for years that I can now put into practice bt some of them, like mcpmon, came out of an issue that needed a tool to fix.

The [portfolio]({{ '/' | relative_url }}) showcases the range: from Riemannian geometry on Apple Silicon to MCP protocol monitoring to Vonnegut-inspired story generation. The common thread is depth — these aren't toy demos, they're real systems with real tests solving real problems.

---

{% assign projects = site.data.projects %}
{% for project in projects %}
{% if forloop.index <= site.tier_cutoff %}
{% include featured-card.html project=project %}
{% endif %}
{% endfor %}

<div class="catalog-section">
<h2>Also Working On</h2>
<table class="catalog-table">
<thead>
<tr>
<th>Project</th>
<th>What it does</th>
<th>Status</th>
</tr>
</thead>
<tbody>
{% for project in projects %}
{% if forloop.index > site.tier_cutoff %}
{% include catalog-row.html project=project %}
{% endif %}
{% endfor %}
</tbody>
</table>
</div>

**Links**: [GitHub](https://github.com/nborwankar) · [LearnDataScience](https://github.com/nborwankar/LearnDataScience) (3K stars) · [This site's source](https://github.com/nborwankar/what-hath-claude-wrought)
