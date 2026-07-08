# What Hath Claude Wrought

**A CSV-driven Jekyll portfolio of projects built in collaboration with Claude Code** —
research, developer tools, libraries, books, and generative art, in one browsable site.

Live site: https://nborwankar.github.io/what-hath-claude-wrought/

## How it works

- `_data/projects.csv` is the **single source of truth** for all project content — row order
  in the CSV is display order on the site
- `_config.yml` sets `tier_cutoff`: the first N rows render as featured cards, the rest as
  compact catalog rows
- GitHub Pages auto-builds on every push to `main` — reordering the portfolio is: edit CSV,
  save, commit, push

## Key files

| File | Role |
|---|---|
| `_data/projects.csv` | all project data |
| `_config.yml` | site config + `tier_cutoff` |
| `_layouts/default.html` | page layout |
| `_includes/featured-card.html` | featured project card |
| `_includes/catalog-row.html` | compact catalog row |
| `index.md` / `about.md` | landing and about pages |

No build tooling needed locally — it's a static Jekyll site (no Python, no conda).
