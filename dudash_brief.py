"""
Daily CEO Podcast for Steve Dudash — automation script.

Runs once per weekday via GitHub Actions. Pulls the last 24 hours of
headlines from verified free sources, pulls verified figures from FRED,
sends both to the Anthropic API to write the script, converts the script
to audio with ElevenLabs, and emails the result.

All credentials are read from environment variables (set as GitHub
Secrets — see README / setup doc for the full list). Nothing is
hardcoded here.
"""

import os
import re
import smtplib
import datetime
from email.message import EmailMessage

import requests
import feedparser

# ---------------------------------------------------------------------
# Configuration — all values below are read from environment variables.
# See the setup document for exactly what each one is and where it
# comes from. Nothing here needs to be edited by hand.
# ---------------------------------------------------------------------

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
ELEVENLABS_VOICE_ID = os.environ["ELEVENLABS_VOICE_ID"]
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

ANTHROPIC_MODEL = "claude-sonnet-5"

# Verified, free, working RSS feeds (confirmed live — see project spec doc)
RSS_FEEDS = {
    "CNBC Top News": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "CNBC Business": "https://www.cnbc.com/id/15837362/device/rss/rss.html",
    "CNBC Markets": "https://www.cnbc.com/id/15838459/device/rss/rss.html",
    "CNBC Finance/Wall Street": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    "CNBC Economy": "https://www.cnbc.com/id/20910258/device/rss/rss.html",
    "Federal Reserve Press Releases": "https://www.federalreserve.gov/feeds/press_all.xml",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "TechCrunch (VC/startups)": "https://techcrunch.com/feed/",
    "Crunchbase News (VC/startups)": "https://news.crunchbase.com/feed/",
}

# FRED series used to ground any macro figure the script states out loud
FRED_SERIES = {
    "Unemployment rate": "UNRATE",
    "CPI (inflation index)": "CPIAUCSL",
    "Fed funds rate": "FEDFUNDS",
    "10-year Treasury yield": "DGS10",
}

PROJECT_INSTRUCTIONS = """
Goal: Produce a short daily audio-podcast SCRIPT for Steve Dudash, a CEO.
Cover markets, finance, business, industry, VC, and wealth management.

Audience: Steve wants signal, not noise. Give him what moves markets,
what affects his clients and his business, and what he needs to sound
sharp in a morning meeting. Skip filler. Skip anything he already knows.

Rules on the markets snapshot: Do NOT narrate routine index moves
("the S&P closed up 0.3%"). Only mention an index level or move if it
was unusual or directly tied to one of today's larger stories. If
nothing stands out, skip the markets snapshot section entirely.

Every story must clear this bar: would this change how a CEO or wealth
advisor talks to a client this week? If not, leave it out.

Structure:
1. Cold open: one line on the single biggest story of the day.
2. Markets snapshot: only if warranted (see rule above).
3. Three to five stories, 30-60 seconds each read aloud. Lead with why
   it matters, not what happened.
4. One VC or deal item.
5. One wealth management item.
6. Close: one takeaway or thing to watch today.

Length and pace: Target 12-15 minutes of spoken audio. Short sentences.
Active voice. Talk like a person, not a report.

Tone: Direct and confident. No hype. No jargon a CEO wouldn't use.
Explain any number in terms of impact, not just magnitude. Never give
financial advice. Report the news only.

Sources and accuracy: Only use the headlines and verified figures
provided below. Every figure you state must come from the verified
figures block. If a number is not in that block, do not state a
specific figure — describe the direction or event in words instead.
Never invent quotes, prices, or data of any kind.

Number formatting for text-to-speech: Write every number as words, not
digits, so the voice engine pronounces it correctly and naturally.
This includes percentages, dollar amounts, dates, and counts.
Examples: "four point two five percent" not "4.25%"; "two hundred
fifty thousand jobs" not "250,000 jobs"; "six billion dollars" not
"$6 billion"; "July twenty-ninth" not "July 29"; "ten year Treasury
yield" not "10-year Treasury yield". Do not use any digits, percent
signs, dollar signs, or numerals anywhere in the script.

Output format: You must return TWO parts, in this exact order, separated
by a line containing only ===BULLETS===

Part 1 — the spoken script. Written to be read aloud by a text-to-speech
voice. No section headers, no labels, no markdown, no stage directions,
no numerals or symbols of any kind (see number formatting rule above).

Part 2 — three to five short headline bullets summarizing the episode,
one per line, each starting with "- ". These are for an email a CEO
will scan before listening, NOT spoken aloud, so write them the normal
written way: use ordinary digits and symbols here (e.g. "4.25%", "$6B",
"250,000 jobs"), not spelled-out words. Keep each bullet under 12 words.

Do not add any other text, headers, or commentary outside these two parts.""".strip()


def fetch_headlines(max_per_feed: int = 8) -> str:
    """Pull recent headlines from each RSS feed. Feed-level failures are
    logged and skipped rather than stopping the whole run."""
    lines = []
    for name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_per_feed]:
                summary = entry.get("summary", "")[:200]
                lines.append(f"[{name}] {entry.title} — {summary}")
        except Exception as exc:
            print(f"WARNING: could not fetch {name}: {exc}")
    return "\n".join(lines)


def fetch_fred_block() -> str:
    """Pull the latest value for each FRED series. Returns a plain-text
    block the model is told to treat as ground truth."""
    if not FRED_API_KEY:
        return "No FRED API key configured — no verified macro figures available this run."

    lines = []
    for label, series_id in FRED_SERIES.items():
        try:
            resp = requests.get(
                "https://api.stlouisfed.org/fred/series/observations",
                params={
                    "series_id": series_id,
                    "api_key": FRED_API_KEY,
                    "file_type": "json",
                    "sort_order": "desc",
                    "limit": 1,
                },
                timeout=15,
            )
            resp.raise_for_status()
            obs = resp.json()["observations"][0]
            lines.append(f"{label}: {obs['value']} (as of {obs['date']})")
        except Exception as exc:
            print(f"WARNING: FRED fetch failed for {label}: {exc}")
    return "\n".join(lines) if lines else "No FRED figures retrieved this run."


def generate_script(headlines: str, fred_block: str) -> tuple:
    """Returns (script_text, bullets) — the spoken script with numbers
    spelled out for text-to-speech, and a separate list of email
    headline bullets that use normal digits/symbols instead."""
    today_str = datetime.date.today().strftime("%B %d, %Y")
    prompt = f"""{PROJECT_INSTRUCTIONS}

Today's date: {today_str}

Verified macro figures (from FRED — the only figures you may state as numbers):
{fred_block}

Raw headlines from the last 24 hours, multiple sources, unverified beyond
the source itself:
{headlines}

Write today's script and bullets now."""

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": ANTHROPIC_MODEL,
            "max_tokens": 2200,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    full_text = "".join(
        block["text"] for block in data["content"] if block["type"] == "text"
    ).strip()

    if "===BULLETS===" in full_text:
        script_part, bullets_part = full_text.split("===BULLETS===", 1)
    else:
        # Fallback: model didn't follow the delimiter format. Use the
        # whole response as the script and fall back to a simple
        # sentence-based summary for bullets rather than failing the run.
        print("WARNING: '===BULLETS===' delimiter not found in model output; falling back to sentence extraction for bullets.")
        script_part, bullets_part = full_text, ""

    script_text = script_part.strip()

    bullets = [
        line.strip().lstrip("- ").strip()
        for line in bullets_part.strip().splitlines()
        if line.strip()
    ]
    if not bullets:
        sentences = re.split(r"(?<=[.!?])\s+", script_text)
        bullets = [s.strip() for s in sentences[:5] if s.strip()]

    return script_text, bullets


def generate_audio(script_text: str, out_path: str) -> None:
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "content-type": "application/json",
        },
        json={
            "text": script_text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        },
        timeout=180,
    )
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)


def send_email(mp3_path: str, bullets: list, date_str: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"Your Daily Brief — {date_str}"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    bullet_block = "\n".join(f"- {b}" for b in bullets)
    msg.set_content(
        f"""Steve,

Today's brief, ready to listen:

{bullet_block}

Audio attached.
"""
    )

    with open(mp3_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="audio",
            subtype="mpeg",
            filename=os.path.basename(mp3_path),
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)


def main() -> None:
    today = datetime.date.today()
    date_str = today.strftime("%B %d, %Y")
    mp3_path = f"dudash-brief-{today.isoformat()}.mp3"

    print("Fetching headlines...")
    headlines = fetch_headlines()

    print("Fetching verified FRED figures...")
    fred_block = fetch_fred_block()

    print("Generating script and bullets...")
    script_text, bullets = generate_script(headlines, fred_block)

    print("Generating audio...")
    generate_audio(script_text, mp3_path)

    print("Sending email...")
    send_email(mp3_path, bullets, date_str)

    print(f"Done. Brief sent for {date_str}.")


if __name__ == "__main__":
    main()
