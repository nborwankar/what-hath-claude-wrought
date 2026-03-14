# metaproject — CLAUDE.md

## Purpose

Extract per-project stats from local git repos and emit a structured CSV that feeds the Jekyll portfolio site at `what-hath-claude-wrought`.

---

## Target Output Schema

`_data/projects.csv` — consumed directly by Jekyll. Column order matters.

```
rank, name, hook, domain, built, repo, status,
commits, tests, last_active, version, notes
```

| Column | Source | Notes |
|---|---|---|
| rank | manual / metaproject.md | Display order; CSV row order is what Jekyll uses |
| name | metaproject.md | Short display name |
| hook | metaproject.md | One-line pitch |
| domain | metaproject.md | Expertise areas |
| built | metaproject.md | What was actually constructed |
| repo | metaproject.md | Full GitHub URL |
| status | metaproject.md | One of: `pre-release`, `published`, `active`, `early` |
| commits | git log | `git rev-list --count HEAD` in repo dir |
| tests | file scan | Count of test functions — see extraction rules below |
| last_active | git log | `git log -1 --format=%cd --date=short` |
| version | git tags / pyproject.toml | Latest tag or version string; empty if none |
| notes | derived | Human-readable summary e.g. "91/91 tests; 50-200x speedup" — rendered by Jekyll include |

The `evidence` freetext column from the old CSV is **replaced** by structured columns above. The Jekyll include assembles the human-readable string from them at render time.

---

## Extraction Rules

### Commits
```bash
git -C <repo_path> rev-list --count HEAD
```

### Last Active
```bash
git -C <repo_path> log -1 --format=%cd --date=short
```

### Version
Check in order:
1. Latest git tag: `git -C <repo_path> describe --tags --abbrev=0`
2. `pyproject.toml` → `version`
3. `package.json` → `version`
4. Empty string if none found

### Test Count
Count test functions across the repo — language-aware:

- **Python**: grep `def test_` across `**/test_*.py` and `**/*_test.py`
- **JavaScript/TypeScript**: grep `it(` and `test(` across `**/*.test.*` and `**/*.spec.*`
- **Java**: grep `@Test` across `**/*.java`

Return total count as integer. If no test files found, return empty string.

---

## Source: metaproject.md

The input is `metaproject.md` — a loose markdown file with one section per project.
Each section has some or all of: name, repo URL, status, hook, domain, built description.

Parse strategy:
- Split on `##` headings — each heading is a project
- Extract repo URL via regex on `github.com/nborwankar/` pattern
- Extract status from a line containing `status:` or infer from context
- For fields not found in the MD, leave blank — do not hallucinate values

---

## Scripts to Build

### `extract.py`
Main extraction script.

```
python extract.py \
  --metaproject /path/to/metaproject.md \
  --repos-root /path/to/repos \
  --output /path/to/what-hath-claude-wrought/_data/projects.csv
```

- Reads metaproject.md for metadata fields
- For each project with a known repo name, looks for matching dir under `--repos-root`
- Runs git commands to extract commits, last_active, version
- Runs test count extraction
- Writes CSV preserving row order from metaproject.md (rank column is informational only)
- Prints a summary diff of what changed vs the existing CSV

### `cron_update.sh`
Wrapper for cron.

```bash
#!/bin/bash
set -e

REPOS_ROOT="$HOME/code"
METAPROJECT="$HOME/code/metaproject/metaproject.md"
PORTFOLIO="$HOME/code/what-hath-claude-wrought"

python "$PORTFOLIO/pipeline/extract.py" \
  --metaproject "$METAPROJECT" \
  --repos-root "$REPOS_ROOT" \
  --output "$PORTFOLIO/_data/projects.csv"

cd "$PORTFOLIO"
git add _data/projects.csv
git diff --cached --quiet || git commit -m "chore: weekly stats update $(date +%Y-%m-%d)"
git push
```

Add to crontab:
```
0 9 * * 1  /path/to/what-hath-claude-wrought/pipeline/cron_update.sh >> /tmp/portfolio-update.log 2>&1
```
(Runs Monday 9am — adjust to taste)

---

## Jekyll Include Changes Needed

After the CSV schema change, update `_includes/featured-card.html` and `_includes/catalog-row.html` to render structured fields:

```liquid
<!-- Example: render evidence line from structured columns -->
{% assign evidence_parts = "" %}
{% if project.commits != "" %}{% assign evidence_parts = evidence_parts | append: project.commits | append: " commits; " %}{% endif %}
{% if project.tests != "" %}{% assign evidence_parts = evidence_parts | append: project.tests | append: " tests; " %}{% endif %}
{% if project.version != "" %}{% assign evidence_parts = evidence_parts | append: project.version %}{% endif %}
<span class="evidence">{{ evidence_parts }}</span>
```

---

## Repo Layout

```
what-hath-claude-wrought/
  pipeline/
    extract.py
    cron_update.sh
    requirements.txt      # standard library only if possible
  _data/
    projects.csv
  _includes/
    featured-card.html
    catalog-row.html
```

---

## Notes for Claude Code

- Do not modify `index.md` or any layout files unless explicitly asked
- Do not reorder rows in the CSV — row order = display order
- If a repo directory is not found locally, emit a warning but do not skip the row — carry forward existing values from the current CSV
- The `rank` column is preserved as-is from metaproject.md; it is informational only
- Prefer stdlib over third-party for extract.py (csv, subprocess, pathlib, re) — this runs in cron, no venv activation guaranteed unless explicitly set up
