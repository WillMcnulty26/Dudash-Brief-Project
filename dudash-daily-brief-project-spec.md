# Daily CEO Podcast for Steve Dudash — Project Spec v2
Revised to incorporate feedback: cut minute-by-minute market moves, favor larger stories, prioritize free sources, prepare for automated scheduling and delivery.

---

## 1. Revised Project Instructions (the prompt for script generation)

**Goal**
Every weekday, produce a short audio podcast for Steve Dudash. Cover markets, finance, business, industry, VC, and wealth management. Write it for a busy CEO. Deliver the finished audio by 6:30am Central.

**Audience**
Steve is a CEO. He wants signal, not noise. Give him what moves markets, what affects his clients and his business, and what he needs to sound sharp in a morning meeting. Skip filler. Skip anything he already knows.

**What changed from v1**
- Do not narrate routine index moves ("the S&P closed up 0.3%, the Dow was flat"). Only mention an index level or move if it was unusual (a swing large enough to be a talking point) or directly tied to one of the day's larger stories.
- Every story must clear a bar: would this change how a CEO or wealth advisor talks to a client this week? If not, cut it.
- Favor stories with a clear "why it matters for a client conversation" angle over stories that are simply large in the news cycle.
- Match the tone and pacing of the stronger back half of the July 21 test recording: calmer, more explanatory, fewer transitions that sound like a list being read.

**What to cover each day**
- Markets snapshot: only if something notable happened (a real move in rates, a currency swing, an outlier day). Otherwise, skip straight past this section.
- Finance and macro: Fed decisions or signals, inflation and jobs data (only on release days or when a figure surprises), earnings that matter to a CEO audience.
- Business and industry: major corporate news, deals, layoffs, product launches.
- Venture capital: one notable round, exit, fund close, or startup trend.
- Wealth management: one item affecting advisors, clients, or high-net-worth investors.
- One broader story: policy, tech shift, geopolitics, or trend a CEO should know about, even outside finance.

**Structure**
1. Cold open: one line on the single biggest story of the day.
2. Markets snapshot: only if warranted (see above). If nothing stands out, skip this section entirely rather than filling it with routine numbers.
3. Three to five stories, 30–60 seconds each. Lead with why it matters, not what happened.
4. One VC or deal item.
5. One wealth management item.
6. Close: one takeaway or thing to watch today.

**Length and pace**
- Target 12–15 minutes of audio.
- Short sentences. Active voice. Talk like a person, not a report.

**Tone**
- Direct and confident. No hype. No jargon a CEO wouldn't use.
- Explain any number in terms of impact, not just magnitude.
- Never give financial advice. Report the news.

**Sources**
- Pull only from the verified source list below (Section 2).
- Prioritize items from the last 24 hours.
- Every figure must trace back to a specific source pulled that morning. If a number can't be verified against a fetched source, drop it — do not estimate, round from memory, or infer.
- Never invent quotes, prices, or data of any kind.

**Number formatting**
- Write every number as words, not digits, so the text-to-speech voice pronounces it correctly. This applies to percentages, dollar amounts, dates, and counts.
- Examples: "four point two five percent," not "4.25%"; "six billion dollars," not "$6 billion"; "July twenty-ninth," not "July 29."
- No digits, percent signs, dollar signs, or numerals should appear anywhere in the *spoken script*.
- This rule does not apply to the email headline bullets in Section 3 below — those are read on screen, not spoken aloud, so they use normal digits and symbols (e.g. "4.25%," "$6B") for quick scanning.

**Rules**
- Accuracy beats speed.
- If a source is unclear, paywalled, or contradicted by another source, leave the item out.
- Keep it tight. If it doesn't help a CEO, cut it.

---

## 2. Verified News Sources

A note on reality first: several outlets that used to offer simple public RSS feeds (Reuters, MarketWatch, AP News) have largely discontinued easy public feeds in recent years. Rather than hand you dead links, here's what's actually live and free right now, verified today.

### Confirmed working, free, official feeds

**CNBC** (has real official feeds)
- Top News: `https://www.cnbc.com/id/100727362/device/rss/rss.html`
- Business: `https://www.cnbc.com/id/15837362/device/rss/rss.html`
- Markets: `https://www.cnbc.com/id/15838459/device/rss/rss.html`
- Finance/Wall Street: `https://www.cnbc.com/id/10000664/device/rss/rss.html`
- Economy: `https://www.cnbc.com/id/20910258/device/rss/rss.html`

**Federal Reserve Board (federalreserve.gov)** — official, confirmed live today
- All Press Releases: `https://www.federalreserve.gov/feeds/press_all.xml`
- Monetary Policy releases only: `https://www.federalreserve.gov/feeds/press_monetary.xml`
- All Speeches & Testimony: `https://www.federalreserve.gov/feeds/speeches_and_testimony.xml`
- Selected Interest Rates (H.15): `https://www.federalreserve.gov/feeds/h15.xml`

**FRED (Federal Reserve Bank of St. Louis)** — not RSS, but a free data API, more reliable for verified numbers
- Base API: `https://api.stlouisfed.org/fred/`
- Requires a free API key from `https://fred.stlouisfed.org`
- Use `fred/series/observations` with series IDs like `UNRATE` (unemployment), `CPIAUCSL` (inflation), `FEDFUNDS` (fed funds rate), `DGS10` (10-year Treasury yield)
- This is the right tool for grounding any number the script states out loud. Pull the actual figure here rather than trusting the model to recall it.

### Gaps to fill with alternatives (Reuters, AP, MarketWatch don't offer clean public feeds anymore)

- **Yahoo Finance** does still publish a working feed and covers markets/business broadly: `https://finance.yahoo.com/news/rssindex`
- **TechCrunch** (free, official, good for VC): `https://techcrunch.com/feed/`
- **Crunchbase News** (free, official, VC-focused): `https://news.crunchbase.com/feed/`
- For Reuters/AP/MarketWatch-equivalent coverage without paying for a terminal, the practical free substitute is Yahoo Finance's feed above, since it aggregates wire content from multiple sources, plus CNBC directly.

### Recommendation
Build the news-gathering step to pull from: CNBC (4–5 feeds above), Federal Reserve official feeds, FRED API for verified figures, Yahoo Finance, TechCrunch, and Crunchbase News. That's six free, working sources covering markets, macro, business, VC, and policy. Re-verify each URL once when you build the script, since outlets do change feed paths without much notice.

---

## 3. Email Delivery Template

**Subject line:**
`Your Daily Brief — [Month Day, Year]`

**Body:**

```
Steve,

Today's brief, ready to listen:

• [Headline 1 — the cold open story]
• [Headline 2]
• [Headline 3]
• [Headline 4, if applicable]
• [Headline 5, if applicable]

Audio attached ([X] min).

—
```

**Attachment naming:** `dudash-brief-YYYY-MM-DD.mp3`

**Notes for whoever wires this up:**
- Bullets should be pulled directly from the script's own section headers/topic sentences, not re-summarized separately — keeps the email and audio in sync.
- Keep the body genuinely scannable: five bullets max, no additional commentary in the email itself.
- During the test phase (sending to your boss instead of Steve), consider adding a line at the bottom noting it's a test send, so it's clearly distinguishable from the eventual live version.
