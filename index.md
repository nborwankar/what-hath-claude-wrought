---
layout: default
title: Home
---

<div class="hero">
  <h1>What Hath Claude Wrought</h1>
  <p class="tagline">A senior engineer who hasn't written a line of code in these projects — and has shipped more than ever.</p>
</div>

Senior engineer with decades in databases, search, machine learning, and systems architecture. O'Reilly author ([Vector Databases](https://github.com/nborwankar/VectorDatabasesBook)). Creator of [LearnDataScience](https://github.com/nborwankar/LearnDataScience) (3,000 stars, 1,600 forks — hand-built in 2013 when there were no such things as agents).

I have wide-scoped research ideas — hyperbolic embeddings for code search, neuro-symbolic query languages, Vonnegut's story shapes as generative constraints — and for years I lacked the execution bandwidth to pursue them all.

Claude Code changed the equation.

> I didn't write a line of code in any of these projects. I brought the research questions, the domain knowledge, the architectural vision. Claude brought systematic engineering, TDD discipline, and execution velocity. The best work happens when I stop tracking who typed what.

The collaboration has a consistent pattern:

- **I bring**: domain expertise, research hypotheses, architectural taste, quality standards
- **Claude brings**: implementation velocity, test coverage, systematic debugging, framework knowledge

The cognitive boundary between us dissolves during deep work sessions. That's not a bug — it's what effective human-AI collaboration actually looks like. Not "AI wrote my code" but genuine co-creation where the seams disappear.

Every project below was built with Claude Code as a pair programmer. Some were conceived and shipped in a single weekend. Others evolved over months of iterative sessions. All of them represent ideas I'd carried for years that I can now put into practice.

---

{% assign sorted = site.data.projects | sort: "rank" %}

{% for project in sorted %}
  {% assign rank_num = project.rank | plus: 0 %}
  {% if rank_num <= site.tier_cutoff %}
    {% include featured-card.html project=project %}
  {% endif %}
{% endfor %}

<div class="catalog-section" markdown="1">

## Also Shipped

<table class="catalog-table">
    <thead>
      <tr>
        <th>Project</th>
        <th>What it does</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {% for project in sorted %}
        {% assign rank_num = project.rank | plus: 0 %}
        {% if rank_num > site.tier_cutoff %}
          {% include catalog-row.html project=project %}
        {% endif %}
      {% endfor %}
    </tbody>
  </table>
</div>

<div class="about-links" markdown="1">

**Links**: [GitHub](https://github.com/nborwankar) · [LearnDataScience](https://github.com/nborwankar/LearnDataScience) (3K stars) · [This site's source](https://github.com/nborwankar/what-hath-claude-wrought)

</div>
