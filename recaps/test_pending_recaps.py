import json
from pathlib import Path

import pytest

from pending_recaps import pending, recap_data, replace_data

SCRIPTS = [
    {"slug": "a", "title": "Book A", "author": "X", "text": "t"},
    {"slug": "power-pfeffer", "title": "Power", "author": "Pfeffer", "text": "</script> inside"},
]


def test_pending_skips_books_with_audio(tmp_path: Path) -> None:
    (tmp_path / "a.mp3").write_bytes(b"x")
    assert [r["slug"] for r in pending(SCRIPTS, tmp_path)] == ["power-pfeffer"]


def test_recap_data_marks_audio_and_escapes_script_end(tmp_path: Path) -> None:
    (tmp_path / "a.mp3").write_bytes(b"x")
    data = recap_data(SCRIPTS, {"a": "2:01"}, tmp_path)
    assert "</script>" not in data
    rows = json.loads(data.replace("<\\/", "</"))
    assert rows[0]["audio"] == "audio/a.mp3" and rows[0]["duration"] == "2:01"
    assert rows[1]["audio"] is None and rows[1]["title"] == "Power"


def test_replace_data_swaps_only_the_block() -> None:
    html = '<p>x</p><script type="application/json" id="recapData">[1]</script><script>y</script>'
    assert replace_data(html, "[2]") == '<p>x</p><script type="application/json" id="recapData">[2]</script><script>y</script>'


def test_replace_data_refuses_missing_block() -> None:
    with pytest.raises(ValueError):
        replace_data("<p>no data</p>", "[]")
