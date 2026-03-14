# NEXT_SESSION.md - Resume Work Here

**Last Updated**: 2026-03-14
**Current Status**: Pipeline built, site live with auto-refreshed stats
**Current Branch**: main
**Last Commit**: 00cebe4 - Add coming-soon page for unpublished repos

---

## What Was Accomplished This Session

- Built `pipeline/extract.py` — reads existing CSV for metadata, refreshes git-derived columns (commits, tests, last_active, version) from local repos
- Migrated CSV schema: replaced freetext `evidence` column with structured `commits, tests, last_active, version, notes`
- Updated Jekyll includes (`featured-card.html`, `catalog-row.html`) to render new structured columns
- Added vendored source exclusion (skips `*-src/`, `node_modules/`, etc. when counting tests)
- Created `coming-soon.md` page for repos not yet pushed to GitHub
- Pointed 3 unpublished repos (industrial-software, flatoons, n2) to coming-soon page
- Created 404.html on `nborwankar.github.io` user site
- Fixed typos on index page

---

## What to Do Next

### 1. Update extract.py — auto-detect published repos
When `extract.py` runs, it should check whether each project's GitHub repo actually exists (via `gh api` or HTTP HEAD). If a repo URL currently points to `/what-hath-claude-wrought/coming-soon.html` but the GitHub repo now exists, automatically swap the link back to the real GitHub URL. Conversely, if a repo URL points to GitHub but returns 404, swap it to the coming-soon page.

Currently affected repos (as of 2026-03-14):
- `industrial-software` → real URL: `https://github.com/nborwankar/industrial-software`
- `flatoons` → real URL: `https://github.com/nborwankar/flatoons`
- `n2` → real URL: `https://github.com/nborwankar/n2`

### 2. Visual polish
- Check mobile rendering
- Consider adding a favicon

### 3. Consider adding more projects
Current CSV has 12 projects. Could expand the catalog section.

---

## Quick Commands Reference

```bash
# Refresh git stats in CSV
cd /Users/nitin/Projects/github/what-hath-claude-wrought/pipeline
python extract.py --csv ../_data/projects.csv --repos-root ~/Projects/github

# Dry run (preview changes without writing)
python extract.py --csv ../_data/projects.csv --repos-root ~/Projects/github --dry-run

# Test locally
cd /Users/nitin/Projects/github/what-hath-claude-wrought
bundle exec jekyll serve
# Visit http://localhost:4000/what-hath-claude-wrought/

# Deploy — just push
git add -A && git commit -m "Update content" && git push
```

---

## Important Context

### Architecture
- `_data/projects.csv` is the ONLY file to edit for project content
- `pipeline/extract.py` refreshes git-derived columns from local repos
- `_config.yml` `tier_cutoff` controls featured vs catalog split
- Repos not yet on GitHub link to `/what-hath-claude-wrought/coming-soon.html`
- `nborwankar.github.io` repo has a 404.html that links back to portfolio

### Coming-soon link mapping
The CSV `repo` column holds coming-soon URLs for unpublished repos. extract.py needs to learn the real GitHub URL for each so it can swap them back when repos go live. Store the mapping in `REPO_DIR_OVERRIDES` or a new dict.
