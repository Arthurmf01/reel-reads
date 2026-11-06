"""Tests for library/add.py (stdlib unittest): run `/usr/bin/python3 -m unittest library/test_add.py`."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import add  # noqa: E402


class TestAdd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.lib = Path(self._tmp.name) / "library.json"
        self.lib.write_text(json.dumps({"_doc": "x", "books": [
            {"title": "Quiet", "author": "Susan Cain", "status": "queued"},
        ]}), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def books(self):
        return json.loads(self.lib.read_text(encoding="utf-8"))["books"]

    def test_same_book_not_added_twice(self):
        self.assertEqual('exists', add.add(self.lib, "book", "Quiet: The Power of Introverts", "Susan Cain", "T-1"))
        self.assertEqual('exists', add.add(self.lib, "book", "quiet", "Susan Cain", "T-1"))
        self.assertEqual(len(self.books()), 1)

    def test_film_added_with_creator(self):
        self.assertEqual('added', add.add(self.lib, "documentary", "The Alabama Solution", "Andrew Jarecki",
                                "Ambidex capture T-0166", 2025, today="2026-11-06"))
        e = self.books()[-1]
        self.assertEqual((e["type"], e["creator"], e["status"], e["added"]),
                         ("documentary", "Andrew Jarecki", "queued", "2026-11-06"))
        self.assertNotIn("author", e)
        self.assertEqual('exists', add.add(self.lib, "documentary", "Alabama Solution", "x", "T-2"))

    def test_book_and_film_of_same_title_coexist(self):
        self.assertEqual('added', add.add(self.lib, "film", "Quiet", "someone", "T-3"))
        self.assertEqual(len(self.books()), 2)

    def test_accents_and_articles_ignored(self):
        self.assertEqual('added', add.add(self.lib, "book", "Jacaranda", "Gaël Faye", "T-4"))
        self.assertEqual('exists', add.add(self.lib, "book", "JACARANDA", "Gael Faye", "T-4"))

    def test_rejects_untraceable_or_bad_type(self):
        with self.assertRaises(ValueError):
            add.add(self.lib, "book", "X", "Y", " ")
        with self.assertRaises(ValueError):
            add.add(self.lib, "podcast", "X", "Y", "T-5")
        self.assertEqual(len(self.books()), 1)

    def test_note_and_embed_into_page(self):
        add.add(self.lib, "series", "Tip Toe", "Russell T Davies", "T-6", note="Thriller. </script> safe")
        page = Path(self._tmp.name) / "page.html"
        page.write_text('<p>x</p><script type="application/json" id="libraryData">[]</script>', encoding="utf-8")
        self.assertEqual(add.embed(self.lib, pages=(page, Path(self._tmp.name) / "missing.html")), 1)
        html = page.read_text(encoding="utf-8")
        payload = html.split('id="libraryData">', 1)[1].rsplit("</script>", 1)[0]
        rows = json.loads(payload)
        self.assertEqual(rows[-1]["note"], "Thriller. </script> safe")
        self.assertNotIn("source", rows[-1])  # capture ids stay out of the public page
        self.assertEqual(html.count("</script>"), 1)

    def test_rating_fills_missing_never_overwrites(self):
        add.add(self.lib, "series", "Singapura", "Elsa Marpeau", "T-0168", note="Canal+ thriller.")
        self.assertEqual(add.add(self.lib, "series", "Singapura", "x", "T-0168", rating="IMDb 7.0 (imdb.com)"), "updated")
        self.assertEqual(add.add(self.lib, "series", "Singapura", "x", "T-0168", note="other", rating="IMDb 9"), "exists")
        e = self.books()[-1]
        self.assertEqual((e["note"], e["rating"]), ("Canal+ thriller.", "IMDb 7.0 (imdb.com)"))


if __name__ == "__main__":
    unittest.main()
