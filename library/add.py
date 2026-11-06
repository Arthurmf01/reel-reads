"""Add one title to the Reel Reads library (library.json), skipping duplicates.

Called by ambidex-agent when a capture says "add X to Reel Reads" or names a book,
film, TV series or documentary to read/watch. Runs on /usr/bin/python3 (3.9).

    /usr/bin/python3 library/add.py --type film --title "The Alabama Solution" \
        --creator "Andrew Jarecki, Charlotte Kaufman" --year 2025 \
        --domain "Justice" --source "Ambidex capture T-0166, 05/11/2026"

Screen items take --note: the "why watch" line shown on the Library shelf (premise,
where it streams, why it is on the list). After an add, the shelf data embedded in
both mockup pages is refreshed (republishing the artifact stays a manual step).

--rating is a public rating WITH its source, e.g. "IMDb 7.1 (imdb.com, 06/11/2026)";
only pass one you actually looked up. Re-running on an existing title fills in a
missing note or rating (never overwrites) and prints `updated:`.

Prints `added:`, `updated:` or `exists: <title>` and exits 0; exits 2 on bad input.
It never commits: the repo is public, a human reviews and commits.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

LIBRARY = Path(__file__).resolve().parent / "library.json"
MOCKUP = Path(__file__).resolve().parent.parent / "mockup"
PAGES = (MOCKUP / "reel-reads-mockup.html", MOCKUP / "reel-reads-mockup.template.html")
DATA_RE = re.compile(r'(<script type="application/json" id="libraryData">)(.*?)(</script>)', re.S)
SHELF_FIELDS = ("title", "type", "author", "creator", "year", "domain", "status", "note", "rating")
TYPES = ("book", "film", "series", "documentary")
SCREEN = ("film", "series", "documentary")


def norm(title: str) -> str:
    """Comparable key: no accents, case, punctuation or leading article; subtitle dropped."""
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    t = t.split(":")[0]
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"^(the|a|an|le|la|les)\s+", "", t.strip())
    return re.sub(r"\s+", " ", t).strip()


def item_type(entry: Dict) -> str:
    return str(entry.get("type") or "book")  # entries written before 06/11/2026 are books


def find(books: List[Dict], title: str, kind: str) -> Optional[Dict]:
    key = norm(title)
    return next((b for b in books if norm(str(b.get("title", ""))) == key and item_type(b) == kind), None)


def add(library: Path, kind: str, title: str, creator: str, source: str,
        year: Optional[int] = None, domain: Optional[str] = None,
        today: Optional[str] = None, note: Optional[str] = None,
        rating: Optional[str] = None) -> str:
    """Append a queued entry: "added". An existing entry only gains a missing note or
    rating: "updated"; otherwise nothing is written: "exists"."""
    if kind not in TYPES:
        raise ValueError(f"type must be one of {TYPES}")
    if not title.strip() or not source.strip():
        raise ValueError("title and source are required (only add traceable titles)")
    data = json.loads(library.read_text(encoding="utf-8"))
    books = data["books"]
    found = find(books, title, kind)
    if found:
        extra = {k: v.strip() for k, v in (("note", note), ("rating", rating)) if v and v.strip() and not found.get(k)}
        if not extra:
            return "exists"
        found.update(extra)
        _write(library, data)
        return "updated"
    entry: Dict = {"title": title.strip(), "type": kind}
    entry["creator" if kind in SCREEN else "author"] = creator.strip()
    if year:
        entry["year"] = year
    if domain:
        entry["domain"] = domain.strip()
    if note:
        entry["note"] = note.strip()
    if rating:
        entry["rating"] = rating.strip()
    entry.update(source=source.strip(), added=today or date.today().isoformat(), status="queued")
    books.append(entry)
    _write(library, data)
    return "added"


def _write(library: Path, data: Dict) -> None:
    tmp = library.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(library)


def shelf_json(library: Path) -> str:
    """Public subset of the library for the page (no capture ids or sources)."""
    books = json.loads(library.read_text(encoding="utf-8"))["books"]
    rows = [{k: b[k] for k in SHELF_FIELDS if b.get(k) not in (None, "")} for b in books]
    # "</" would close the <script> element early.
    return json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")


def embed(library: Path, pages=PAGES) -> int:
    """Write the shelf data into every page that has a libraryData block. Returns pages updated."""
    data, done = shelf_json(library), 0
    for page in pages:
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        new, n = DATA_RE.subn(lambda m: m.group(1) + data + m.group(3), html)
        if n == 1 and new != html:
            page.write_text(new, encoding="utf-8")
            done += 1
    return done


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--type", required=True, choices=TYPES)
    ap.add_argument("--title", required=True)
    ap.add_argument("--creator", required=True, help="author for a book, director/creator for screen")
    ap.add_argument("--source", required=True, help="e.g. 'Ambidex capture T-0166, 05/11/2026'")
    ap.add_argument("--year", type=int)
    ap.add_argument("--domain")
    ap.add_argument("--note", help="screen items: premise, where it streams, why it is on the list")
    ap.add_argument("--rating", help='public rating with its source, e.g. "IMDb 7.1 (imdb.com, 06/11/2026)"')
    ap.add_argument("--embed-only", action="store_true", help="just refresh the shelf data in the pages")
    ap.add_argument("--library", type=Path, default=LIBRARY)
    if argv is None and "--embed-only" in sys.argv:
        print(f"embedded in {embed(LIBRARY)} page(s)")
        return 0
    a = ap.parse_args(argv)
    try:
        result = add(a.library, a.type, a.title, a.creator, a.source, a.year, a.domain,
                     note=a.note, rating=a.rating)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if result != "exists" and a.library == LIBRARY:
        embed(a.library)
    print(f"{result}: {a.title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
