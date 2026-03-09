# NEXT_SESSION.md - Resume Work Here

**Last Updated**: 2026-03-09
**Current Status**: Site built and deployed, placeholder content needs refinement
**Current Branch**: main
**Last Commit**: 3cffc71 - Update Vector Databases entry: accurate authorship and collaboration details

---

## What Was Accomplished This Session

- Cloned empty repo, scaffolded full Jekyll site with CSV-driven architecture
- Created `_data/projects.csv` with 12 projects (5 featured, 7 catalog)
- Built layout, CSS, Liquid templates (featured cards + catalog table)
- Wrote index page with hero + manifesto + CSV-driven rendering
- Wrote about page with collaboration philosophy
- Enabled GitHub Pages — live at https://nborwankar.github.io/what-hath-claude-wrought/
- Updated Vector Databases entry with accurate authorship details

**Key decisions made**:
- `tier_cutoff: 5` in _config.yml — top 5 get featured cards, rest get catalog rows
- Single CSV as source of truth — reorder by editing rank column in Excel
- Repo is public (needed for free GitHub Pages)

---

## What to Do Next

### 1. Review live site and fix content
- Visit https://nborwankar.github.io/what-hath-claude-wrought/
- Check all project descriptions — many are placeholder/approximate
- Fix repo URLs (some may not match actual GitHub repo names)
- Verify hook/domain/built/evidence text for each project

### 2. Fix repo URLs
Several repos may use different names on GitHub than locally. Verify each `repo` column entry in `_data/projects.csv` actually resolves.

### 3. Refine project descriptions
Read each project's actual README.md and DONE.md to write accurate, compelling 1-line descriptions. Current text was auto-generated from a scan.

### 4. Consider adding more projects
The RECENT_ACTIVITY.md in metaproject lists 49 active repos. Current CSV has 12. Add more to the "also shipped" section as desired.

### 5. Visual polish
- Check mobile rendering
- Consider adding a favicon
- Review card layout and spacing

---

## Quick Commands Reference

```bash
# Navigate to project
cd /Users/nitin/Projects/github/what-hath-claude-wrought

# Edit projects — open in Excel/Numbers then save
open _data/projects.csv

# Change how many are featured vs catalog
# Edit tier_cutoff in _config.yml

# Test locally (requires bundler)
bundle install
bundle exec jekyll serve
# Visit http://localhost:4000/what-hath-claude-wrought/

# Deploy — just push
git add -A && git commit -m "Update content" && git push
```

---

## Important Context to Remember

### Architecture
- `_data/projects.csv` is the ONLY file to edit for project content
- `_config.yml` `tier_cutoff` controls featured vs catalog split
- Liquid templates in `_includes/` render the cards and rows
- No JS, no build step — pure Jekyll + GitHub Pages

### Plan document
- Full design plan at `/Users/nitin/Projects/metaproject/docs/plans/2026-03-09-what-hath-claude-wrought.md`
- Activity scan at `/Users/nitin/Projects/metaproject/docs/RECENT_ACTIVITY.md`

### Target audience
- Anthropic engineers and leadership
- Substance over flash, demonstrated depth over breadth
- Dual narrative: what YOU brought (domain) + what collaboration produced

---

## Session Handoff to Claude Code

> "Resume what-hath-claude-wrought — check NEXT_SESSION.md. Review the live site and refine project descriptions in _data/projects.csv."
