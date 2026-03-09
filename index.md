---
layout: default
title: Home
---

<div class="hero">
  <h1>What Hath Claude Wrought</h1>
  <p class="tagline">A senior engineer who hasn't written a line of code in these projects — and has shipped more than ever.</p>
</div>

I've spent decades in databases, search, ML, and systems architecture. I have wide-scoped research ideas that I could never execute alone. Claude Code changed that equation.

I didn't write a line of code in any of these projects. I brought the domain knowledge, the research questions, the architectural taste. Claude brought the systematic engineering. The result is a body of work I couldn't have built in ten years on my own.

{% assign sorted = site.data.projects | sort: "rank" %}

{% for project in sorted %}
  {% assign rank_num = project.rank | plus: 0 %}
  {% if rank_num <= site.tier_cutoff %}
    {% include featured-card.html project=project %}
  {% endif %}
{% endfor %}

<div class="catalog-section">
  <h2>Also Shipped</h2>
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
