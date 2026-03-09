# CLAUDE.md — What Hath Claude Wrought

## Overview
CSV-driven Jekyll portfolio site for GitHub Pages. Showcases Claude Code collaboration projects.

## Architecture
- `_data/projects.csv` is the single source of truth for all project content
- `_config.yml` has `tier_cutoff` — rows with rank <= cutoff are featured, rest are catalog
- To reorder: edit rank column in CSV (open in Excel/Numbers), save, commit, push
- GitHub Pages auto-builds on push to main

## No conda env needed
This is a static Jekyll site. No Python.

## Key files
- `_data/projects.csv` — all project data
- `_config.yml` — site config + tier_cutoff
- `_layouts/default.html` — page layout
- `_includes/featured-card.html` — featured project card template
- `_includes/catalog-row.html` — compact catalog row template
- `index.md` — landing page
- `about.md` — about page

## Reordering workflow
1. Open `_data/projects.csv` in Excel/Numbers
2. Change rank numbers
3. Save, commit, push
4. Site rebuilds automatically
