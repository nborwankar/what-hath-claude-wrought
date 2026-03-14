#!/usr/bin/env python3
"""
extract.py — Refresh git-derived columns in projects.csv

Reads the existing CSV for human-curated metadata (name, hook, domain, built,
repo, status, rank, notes).  For each project whose repo lives under
--repos-root, extracts fresh values for: commits, tests, last_active, version.

Usage:
    python extract.py \
        --csv /path/to/_data/projects.csv \
        --repos-root ~/Projects/github \
        [--dry-run]
"""

import argparse
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

# ── repo URL → local directory mapping ──────────────────────────────
# Most repos live directly under repos_root/<name>, but some are nested.
# This map handles the exceptions.  Key = last path component of the
# GitHub URL; value = relative path from repos_root.

REPO_DIR_OVERRIDES = {
    "VectorDatabasesBook": "kb/VectorDatabasesBook",
    "mlx-manopt": "mlx/mlx-manopt",
    "mlx-hyperbolic": "mlx/mlx-hyperbolic",
    "kurt": "art/kurt",
    "strictRAG": "kb/strictRAG",
    "embedding_tools": "etcprojects/embedding_tools",
    "flatoons": "art/flatoons",
    "convaix": "etcprojects/convaix",
}

# ── New CSV schema ──────────────────────────────────────────────────
OUTPUT_COLUMNS = [
    "rank",
    "name",
    "hook",
    "domain",
    "built",
    "repo",
    "status",
    "commits",
    "tests",
    "last_active",
    "version",
    "notes",
]


def repo_name_from_url(url: str) -> str:
    """Extract the repo name from a GitHub URL."""
    return url.rstrip("/").split("/")[-1]


def find_repo_dir(repo_url: str, repos_root: Path) -> Path | None:
    """Resolve a GitHub URL to a local directory."""
    name = repo_name_from_url(repo_url)
    if name in REPO_DIR_OVERRIDES:
        candidate = repos_root / REPO_DIR_OVERRIDES[name]
    else:
        candidate = repos_root / name
    if candidate.is_dir() and (candidate / ".git").exists():
        return candidate
    return None


def git_commit_count(repo: Path) -> str:
    """Return total commit count as a string."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-list", "--count", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def git_last_active(repo: Path) -> str:
    """Return date of most recent commit (YYYY-MM-DD)."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--format=%cd", "--date=short"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def git_version(repo: Path) -> str:
    """Return latest version from git tags or pyproject.toml."""
    # Try git tags first
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    # Try pyproject.toml
    pyproject = repo / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text()
        m = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
        if m:
            return m.group(1)

    # Try package.json
    pkg = repo / "package.json"
    if pkg.exists():
        import json

        try:
            data = json.loads(pkg.read_text())
            return data.get("version", "")
        except Exception:
            pass

    return ""


def _is_vendored(path: Path) -> bool:
    """Return True if path is inside a vendored/third-party directory."""
    parts = path.parts
    for part in parts:
        if part in ("node_modules", "vendor", "third_party", "dist", "build"):
            return True
        # Directories ending in -src are typically vendored source trees
        # e.g. jackson-src, commons-lang-src
        if part.endswith("-src"):
            return True
    return False


def count_tests(repo: Path) -> str:
    """Count test functions across the repo (Python, JS/TS, Java).

    Skips vendored/third-party directories (node_modules, *-src, etc.).
    """
    total = 0

    # Python: def test_ in test files
    for pattern in ("**/test_*.py", "**/*_test.py"):
        for f in repo.glob(pattern):
            if _is_vendored(f):
                continue
            try:
                text = f.read_text(errors="replace")
                total += len(re.findall(r"^\s*def\s+test_", text, re.MULTILINE))
            except Exception:
                pass

    # JS/TS: it( and test( in test/spec files
    for pattern in ("**/*.test.*", "**/*.spec.*"):
        for f in repo.glob(pattern):
            if _is_vendored(f):
                continue
            if f.suffix in (".js", ".ts", ".jsx", ".tsx", ".mjs"):
                try:
                    text = f.read_text(errors="replace")
                    total += len(re.findall(r"\b(?:it|test)\s*\(", text))
                except Exception:
                    pass

    # Java: @Test
    for f in repo.glob("**/*.java"):
        if _is_vendored(f):
            continue
        try:
            text = f.read_text(errors="replace")
            total += len(re.findall(r"@Test", text))
        except Exception:
            pass

    return str(total) if total > 0 else ""


def migrate_notes_from_evidence(evidence: str) -> str:
    """Extract non-numeric narrative from old evidence field for notes column.

    The structured columns (commits, tests, version) now hold the numbers.
    Keep only the descriptive parts that can't be auto-extracted.
    """
    if not evidence:
        return ""
    # Remove patterns like "N commits", "N tests", "N/N tests", "vX.Y.Z"
    notes = evidence
    notes = re.sub(r"\d+\s+commits?\s*;?\s*", "", notes)
    notes = re.sub(r"\d+/\d+\s+tests?\s*;?\s*", "", notes)
    notes = re.sub(r"\d+\s+tests?\s*;?\s*", "", notes)
    notes = re.sub(r"v\d+\.\d+[\.\d]*\s*;?\s*", "", notes)
    notes = notes.strip().rstrip(";").strip()
    return notes


def load_existing_csv(csv_path: Path) -> list[dict]:
    """Load the existing CSV into a list of dicts."""
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def refresh_row(row: dict, repos_root: Path) -> dict:
    """Return a new row dict with refreshed git-derived columns."""
    out = {}
    # Carry forward human-curated fields
    for col in ("rank", "name", "hook", "domain", "built", "repo", "status"):
        out[col] = row.get(col, "").strip()

    # Find local repo
    repo_dir = find_repo_dir(out["repo"], repos_root) if out["repo"] else None

    if repo_dir:
        out["commits"] = git_commit_count(repo_dir)
        out["tests"] = count_tests(repo_dir)
        out["last_active"] = git_last_active(repo_dir)
        out["version"] = git_version(repo_dir)
    else:
        # Carry forward existing values if repo not found locally
        out["commits"] = row.get("commits", "")
        out["tests"] = row.get("tests", "")
        out["last_active"] = row.get("last_active", "")
        out["version"] = row.get("version", "")

    # Notes: carry forward if it exists, otherwise migrate from evidence
    if "notes" in row and row["notes"].strip():
        out["notes"] = row["notes"].strip()
    elif "evidence" in row:
        out["notes"] = migrate_notes_from_evidence(row["evidence"])
    else:
        out["notes"] = ""

    return out


def write_csv(rows: list[dict], path: Path):
    """Write rows to CSV with the target schema."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def print_diff(old_rows: list[dict], new_rows: list[dict]):
    """Print a summary of what changed."""
    print("\n── Changes ─────────────────────────────────")
    for old, new in zip(old_rows, new_rows):
        name = new["name"]
        changes = []
        for col in ("commits", "tests", "last_active", "version"):
            old_val = old.get(col, "")
            new_val = new.get(col, "")
            if old_val != new_val:
                changes.append(f"  {col}: {old_val!r} → {new_val!r}")
        if changes:
            print(f"\n{name}:")
            print("\n".join(changes))
    if not any(
        old.get(col, "") != new.get(col, "")
        for old, new in zip(old_rows, new_rows)
        for col in ("commits", "tests", "last_active", "version")
    ):
        print("  (no changes)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Refresh git-derived columns in projects.csv"
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to _data/projects.csv",
    )
    parser.add_argument(
        "--repos-root",
        required=True,
        help="Root directory containing git repos",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print changes without writing",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv).expanduser().resolve()
    repos_root = Path(args.repos_root).expanduser().resolve()

    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    if not repos_root.is_dir():
        print(f"ERROR: repos root not found: {repos_root}", file=sys.stderr)
        sys.exit(1)

    old_rows = load_existing_csv(csv_path)
    new_rows = [refresh_row(row, repos_root) for row in old_rows]

    print_diff(old_rows, new_rows)

    if args.dry_run:
        print("(dry run — no files written)")
    else:
        write_csv(new_rows, csv_path)
        print(f"Wrote {len(new_rows)} rows to {csv_path}")


if __name__ == "__main__":
    main()
