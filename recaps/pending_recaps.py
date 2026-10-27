"""Generate the Reel Reads audio recaps still missing, once ElevenLabs quota allows.

Run daily by launchd (com.arthur.reel-reads-recaps via cal-dispatch). Each run tries every
recap in scripts.json that has no MP3 yet. A quota refusal costs nothing, so the run just stops
and waits for tomorrow. When at least one recap is generated, it refreshes durations.json and the
recap data embedded in the mockup pages, then pings Arthur on Telegram. It never commits or
publishes: publishing the artifact needs a Claude session ("publish reel reads").
"""
from __future__ import annotations

import json
import logging
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RECAPS = REPO / "recaps"
AUDIO = RECAPS / "audio"
PAGES = [REPO / "mockup/reel-reads-mockup.html", REPO / "mockup/reel-reads-mockup.template.html"]
KEY_FILE = Path.home() / ".claude/skills/reading-agent/.elevenlabs_key"
DIGEST_DIR = Path.home() / ".claude/skills/morning-digest"
VOICE = "EXAVITQu4vr4xnSDxMaL"  # Sarah, premade (works on the free tier)
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_22050_32"
DATA_RE = re.compile(r'(<script type="application/json" id="recapData">)(.*?)(</script>)', re.S)

log = logging.getLogger("reel-reads-recaps")


class QuotaExceeded(Exception):
    pass


def load_scripts() -> list[dict]:
    return json.loads((RECAPS / "scripts.json").read_text())["recaps"]


def pending(scripts: list[dict], audio_dir: Path = AUDIO) -> list[dict]:
    return [r for r in scripts if not (audio_dir / f"{r['slug']}.mp3").exists()]


def synthesise(text: str, key: str) -> bytes:
    body = json.dumps({"text": text, "model_id": "eleven_flash_v2_5"}).encode()
    req = urllib.request.Request(TTS_URL, data=body, method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        if "quota_exceeded" in detail:
            raise QuotaExceeded(detail[:200]) from e
        raise RuntimeError(f"HTTP {e.code}: {detail[:200]}") from e


def duration(mp3: Path) -> str:
    out = subprocess.run(["afinfo", str(mp3)], capture_output=True, text=True).stdout
    secs = float(next(l for l in out.splitlines() if "estimated duration" in l).split()[2])
    return f"{int(secs // 60)}:{int(secs % 60):02d}"


def recap_data(scripts: list[dict], durations: dict[str, str], audio_dir: Path = AUDIO) -> str:
    """The JSON the page's player reads; title must match the card's <b> title."""
    out = []
    for r in scripts:
        has = (audio_dir / f"{r['slug']}.mp3").exists()
        out.append({"title": "Power" if r["slug"] == "power-pfeffer" else r["title"],
                    "author": r["author"], "text": r["text"],
                    "audio": f"audio/{r['slug']}.mp3" if has else None,
                    "duration": durations.get(r["slug"])})
    return json.dumps(out, ensure_ascii=False).replace("</", "<\\/")


def replace_data(html: str, data: str) -> str:
    new, n = DATA_RE.subn(lambda m: m.group(1) + data + m.group(3), html)
    if n != 1:
        raise ValueError(f"expected one recapData block, found {n}")
    return new


def send_telegram(text: str) -> None:
    token = (DIGEST_DIR / ".bot_token").read_text().strip()
    chat_id = (DIGEST_DIR / "chat_id.txt").read_text().strip()
    subprocess.run(["curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{token}/sendMessage",
                    "-d", f"chat_id={chat_id}", "--data-urlencode", f"text={text}"],
                   capture_output=True, timeout=30, check=False)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    scripts = load_scripts()
    todo = pending(scripts)
    if not todo:
        log.info("all recaps generated; this job can be removed")
        return
    key = KEY_FILE.read_text().strip()
    made: list[str] = []
    for r in todo:
        try:
            mp3 = synthesise(r["text"], key)
        except QuotaExceeded as e:
            log.info("quota not available yet, stopping (%s)", e)
            break
        (AUDIO / f"{r['slug']}.mp3").write_bytes(mp3)
        made.append(r["title"])
        log.info("generated %s", r["slug"])
    if not made:
        return
    durations = {p.stem: duration(p) for p in sorted(AUDIO.glob("*.mp3"))}
    (RECAPS / "durations.json").write_text(json.dumps(durations, indent=1))
    data = recap_data(scripts, durations)
    for page in PAGES:
        page.write_text(replace_data(page.read_text(), data))
    left = len(pending(scripts))
    send_telegram(f"Reel Reads: {len(made)} new audio recap(s) ready ({', '.join(made)}). "
                  f"{left} still pending. Tell Claude 'publish reel reads' to put them live.")


if __name__ == "__main__":
    main()
