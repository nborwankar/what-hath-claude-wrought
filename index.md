---
layout: default
title: Home
---

<div class="hero">
  <h1>What Hath Claude Wrought</h1>
  <p class="tagline">I'm Nitin Borwankar, a senior engineer who hasn't written a line of code in these projects — and has shipped more than ever.</p>
</div>

* Senior engineer with decades in databases, some machine learning and enterprise application development roles in QA, dev, technical management, architecture and product management. 

* O'Reilly author ([Vector Databases](https://github.com/nborwankar/VectorDatabasesBook)). 

* Creator of [LearnDataScience](https://github.com/nborwankar/LearnDataScience) (3,000 stars, 1,600 forks — hand-built in 2013 when there were no such things as agents).

I have wide-ranging and sometimes wild-eyed research ideas — hyperbolic embeddings for code search, neuro-symbolic query languages, Vonnegut's story shapes as generative constraints, geometric analysis of code hierarchies and the transition to industrial development of software that will emerge after this current phase of agentic development  — and for years I lacked the execution bandwidth to pursue them all. 

Claude Code changed the equation. The projects mentioned here were all initiated in the last year. Many were shipped. Many are in progress — often the needle will move forward on 3-5 of them over a weekend. Initially I would do a deep dive on a single project over a weekend and the first cut was published by the end of the weekend. As time went by and Claude became more capable, I was able to run 3-5 projects in parallel, constantly pushing myself to the edge of my knowledge and letting Claude go into areas I didn't at first understand. Then I would ask Claude to explain what was just done — and so I expanded my knowledge about multiple subjects a little more every day. What a time to be alive!

> I didn't write a line of code in any of these projects. I brought the research questions, the domain knowledge, the architectural vision - what I wanted and what I didn't want. Claude brought systematic engineering, TDD discipline, and execution velocity. The best work happens when I stop tracking who typed what.

The cognitive boundary between Claude and me dissolves during deep work sessions. That's not a bug — it's what effective human-AI collaboration actually looks like. Not "AI wrote my code" but genuine co-creation where the seams disappear.

The collaboration has a consistent pattern:

- **I bring**: domain expertise, research hypotheses, architectural taste, quality standards, opinionatedness - and an open question which I keep drilling down on - "how about this, what if we tried that, no no not that way - this is better"
- **Claude brings**: implementation velocity, test coverage, systematic debugging, framework knowledge and just enough random behavior to keep things interesting.

Every project below was built with Claude Code as a pair programmer. Some were conceived and shipped in a single weekend. Others evolved over months of iterative sessions sometimes with dead-ends. Most of them represent ideas I'd carried for years that I can now put into practice but some of them, like mcpmon, came out of an issue that needed a tool to fix and I said hey why not we just build the tool.

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
<th>Stats</th>
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
