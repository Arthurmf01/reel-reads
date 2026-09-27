# Reel Reads — Specifications

## What this is

Reel Reads is a Gen AI course final project for INSEAD (the deliverable is a business pitch, not a shipped company). The product concept: an infinite, TikTok-style swipe-feed where every card is a 20-second idea from a book. The catalogue is seeded with the books MBA professors recommend plus the canonical MBA reading list. The differentiator is not the cards (several apps already do cards) but the **feed**: an adaptive recommender that chooses your next card from what you dwell on, swipe past, and save, the same mechanic as TikTok's For You page, with a payload that compounds instead of rotting attention.

Tagline: same dopamine as TikTok, opposite outcome.

## Goal

Produce a pitch package that wins in this specific professor's class, backed by a working technical proof:

1. A 1-pager.
2. A draft pitch deck (7 to 10 slides).
3. A 7 to 10 minute pitch video (script plus a filmed hero visual).
4. A Jupyter notebook that demonstrates the AI core end to end: books atomised into idea-cards, then an adaptive recommender that visibly re-ranks the feed as it learns simulated swipes.

"Done" = all four exist, the deck and 1-pager cover every required session-5 element plus a moat slide and an evals slide, and the notebook runs top to bottom and produces the adaptation visual.

## Non-goals

- Not a shipped app. No real users, no accounts, no payments, no app-store build.
- Not a full catalogue. The seed is roughly 15 books, roughly 75 cards.
- Not a live production recommender. The notebook is a convincing proof on a small card bank, not a scalable service.
- Not a legal ingestion pipeline for copyrighted full text. Cards are generated from the model's own knowledge of famous books (transformative summarisation), not from ingested book files.

## Constraints

- **Deadline sequence:** the 1-pager plus draft pitch deck are due before session 7 (the pitch session). The polished video plus deck plus optional notebook are the final submission.
- **Course lens (this drives what scores):** the professor emphasises The Mom Test (validate the problem by customer discovery, never lead with the solution), moats for AI-native products (he called the moat question "the hardest question"), product-market fit ("no market = no product"), and evals ("the R-squared of AI, the metric everything ties back to"). The pitch must answer all four visibly.
- **Notebook must run for a grader with zero API keys.** The roughly 75 generated cards ship as JSON in the repo so the recommender runs fully offline. A separate, clearly optional cell regenerates cards live via the Anthropic API for anyone who supplies a key.
- **British English, no em-dashes, no fabricated figures.** Any market number carries a source and is marked to verify before the deck is final.

## The pitch content (canonical answers)

This section is the single source of truth for the substance. The 1-pager, deck, and video all draw from here so they never disagree. Every session-5 required element is answered.

### 1. Problem and importance

- People lose hours a day to doomscrolling. The habit (swiping for a dopamine hit) is not the problem and is not going away. The content is the problem: it leaves nothing behind.
- The pain is near-universal and self-aware: most people actively regret their screen time. Attention is the scarce resource of the decade.
- Sharpened for the beachhead: MBA students carry long reading lists, have no time, feel guilt about screen time, want to learn, and default to Instagram or TikTok anyway. They are the clearest case of the wider problem.
- Importance framing for the deck: this is not "another learning app", it is a redirection of an existing compulsive behaviour toward a compounding outcome.

### 2. Clients and segments

- **Beachhead:** MBA students and the business-school community. Defined, reachable, high willingness to pay, shared reading lists, dense word-of-mouth. Arthur can run real Mom Test interviews inside his own cohort.
- **Adjacent expansion:** ambitious knowledge workers and the self-improvement segment (the Blinkist and Headway audience), lifelong learners, professionals prepping for a domain.
- **B2B or B2B2C later:** business schools, corporate learning and development, publishers.

### 3. Market size

Structure as TAM, SAM, SOM. Figures below are directional and each must be re-checked against its named source before the final deck (grounding rule).

- **TAM:** the microlearning market, roughly 3.83 billion USD in 2026, projected to roughly 8.64 billion USD by 2032 at roughly 14 percent CAGR (market-research aggregators, to verify the primary source). Wider reference point: global e-learning is in the hundreds of billions.
- **SAM:** English-speaking mobile microlearning and book-summary users. Anchor with real incumbents: Headway reports 55 million-plus users and is the most-downloaded book-summary app; Blinkist condenses 8,000-plus titles. These prove an audience at scale exists and is monetising.
- **SOM (beachhead):** MBA students plus adjacent early-career professionals. Roughly 250,000-plus MBA students enrolled worldwide at any time (to verify), a wedge, not the ceiling.

### 4. Technical challenges

1. **Card quality at scale.** Atomising a book into self-contained, accurate, non-obvious idea-cards without blandness or hallucination. This is what the evals measure.
2. **Faithfulness.** Cards must not misrepresent the book. Getting an author's idea wrong is a trust and reputation risk, not just a quality nit.
3. **The recommender.** Cold-start for a brand-new user with no history; balancing exploration against exploitation; avoiding an echo-chamber that only ever serves one topic; extracting signal from noisy implicit feedback (dwell time is a weak label).
4. **Copyright and licensing.** Generating from copyrighted books legally. Parametric summarisation is transformative and defensible; full-text ingestion is the risky path and is avoided.
5. **Cost and latency at feed scale.** Real-time generation for an infinite feed has a unit-economics question behind it. Video makes this sharper: ambient backgrounds and AI author-explainer clips add generation and streaming cost per card that text does not.
6. **AI video generation and likeness.** Producing author-explainer clips (for example via a HeyGen-style avatar API) is technically feasible but raises two issues: cost per generated minute at catalogue scale, and the likeness and consent question when the avatar depicts a real or deceased author. Mitigation: label every AI clip clearly, and use consenting authors, licensed likenesses, or a neutral AI narrator rather than an unlicensed real person.

### 5. MVP shape

- A mobile-first, full-screen, **video-native** swipe feed with roughly 75 pre-generated cards from roughly 15 MBA books. The medium is video, not static cards: this is a feed you scroll like TikTok, not a stack of flashcards.
- Each card has two video layers: an **ambient motion background** (footage or generated motion themed to the idea, keeping the feed alive) and an optional **AI author-explainer clip**, a short talking-head avatar of the author (or a labelled AI narrator) delivering the idea in their own voice. The author-explainer is the video hook that a text summary cannot match.
- Implicit feedback capture: dwell time, watch-through on the author clip, swipe direction, save.
- A content-based adaptive recommender that re-ranks the feed from that feedback.
- Two concrete proofs stand in for the MVP in this project: the **notebook** proves the AI core (atomiser plus adaptive recommender), and the **clickable mockup** proves the swipe UX.
- Explicitly out of the MVP: accounts, payments, full catalogue, social features.

### 6. Competition and alternatives

Present as a table plus the honest "do nothing" alternative.

| Player | What it is | What it leaves open |
| --- | --- | --- |
| LeafTok | Turns any book (PDF or EPUB) into swipeable cards, free. The closest thing to this concept already shipped | No real recommender; generic feel; unproven business |
| ScrollEd | Textbooks and PDFs into a short-form study feed | Study material, not a doomscroll replacement for adults |
| Blinkist, Shortform | Long-form written summaries, human editorial team | Not feed-native, not swipe-first, finite curated catalogue |
| Headway, Uptime, Imprint | Curated bite-size insights with swipe UX, often illustrated | Hand-curated, so catalogue is finite and slow and costly to grow |
| The real alternative | Instagram, TikTok, and doing nothing; or buying the book and not reading it | The behaviour we redirect |

Wedge versus all of them: generated on demand (infinite catalogue at near-zero marginal cost) plus a genuine adaptive feed plus an editorial-calm anti-doomscroll design. Being honest that LeafTok exists is itself a credibility slide.

### 7. Team needed

- Founder or founders with product plus domain: Arthur brings MBA plus enterprise-software background.
- An ML or AI engineer for the recommender, the LLM pipeline, and the eval harness.
- A full-stack or mobile engineer.
- A content or editorial lead who owns the quality bar and, later, licensing relationships.
- Later: growth and business development for school and publisher partnerships.

### 8. Moat (the professor's "hardest question")

Be honest that the early moat is thin, then show what compounds:

- **Data and network effect:** proprietary engagement data becomes a taste graph (which ideas hook which kinds of people). It compounds with use and is hard to replicate. This is the real long-run moat.
- **Process IP:** the editorial plus eval pipeline that keeps card quality high.
- **Distribution:** embedding in the MBA and university funnel, then publisher partnerships.
- **Not a moat:** the LLM itself is a commodity. Saying this out loud scores better than pretending otherwise.

### 9. Evals (the professor's "R-squared of AI")

Two evals, both demonstrated in the notebook:

- **Card-quality eval:** a rubric (accurate, self-contained, non-obvious, faithful to source) scored by an LLM judge plus a human spot-check. Target: a stated pass rate, for example 90 percent or higher.
- **Recommender eval:** does the adaptive feed beat a random-order feed on simulated engagement? Measure dwell and save uplift of adaptive versus random over simulated user personas, and report the lift as a single number. This is the metric everything ties back to, and it is the money chart in the deck.

### 10. Business model and why now

- **Model:** freemium (free feed; premium unlocks unlimited, offline, and deeper personalisation), B2B2C via schools and corporate learning and development, and a publisher revenue share.
- **Why now:** two capabilities matured at once. LLMs atomise any book into feed-native content at near-zero marginal cost, and AI video (talking-head avatars, generated motion) can now put an author on screen explaining the idea, also at near-zero marginal cost. The curated, human-produced incumbents cannot grow a video catalogue the way a generative pipeline can. This is the "now possible" claim, stated as unit economics, not hype.

## Seed catalogue (verified from Arthur's INSEAD course notes)

The v1 feed is seeded with these ten books. Each was verified as a course textbook, a professor's recommended reading, or a repeatedly-cited slide concept in Arthur's own INSEAD course notes (not a generic web list). This is the key content data for the notebook and mockup.

| Book | Author | Domain | Source in the course notes |
| --- | --- | --- | --- |
| Blue Ocean Strategy | Kim and Mauborgne | Strategy | Introduction to Strategy, Technology and Innovation Strategy |
| The Lean Startup | Eric Ries | Entrepreneurship | Corporate Entrepreneurship |
| The Innovator's Dilemma | Clayton Christensen | Innovation | Technology and Innovation Strategy |
| Thinking, Fast and Slow | Daniel Kahneman | Behavioural and judgment | Prices and Markets (recommended), Uncertainty Data and Judgment |
| The Goal | Eliyahu Goldratt | Operations | Process and Operations Management (textbook) |
| The Black Swan | Nassim Taleb | Risk and uncertainty | Understanding and Managing Risk |
| Against the Gods | Peter Bernstein | Risk (history of) | Understanding and Managing Risk (recommended reading) |
| Freakonomics | Levitt and Dubner | Economics | Prices and Markets (recommended and Sessions 1 to 2) |
| The Art of Strategy | Dixit and Nalebuff | Game theory | Prices and Markets (recommended) |
| Effectuation | Saras Sarasvathy | Entrepreneurship | Corporate Entrepreneurship, Realising Entrepreneurial Potential (ETA) |

Bench (verified alternates, swap in as needed): The Undoing Project (Michael Lewis), Zero to One (Peter Thiel), The Strategy of Conflict (Schelling), Antifragile (Taleb), Prisoner's Dilemma (Poundstone), Matching Supply with Demand (Cachon and Terwiesch).

Deliberately excluded: dry academic textbooks cited in the notes (Pindyck and Rubinfeld Microeconomics, Makridakis and Winkler Basic Statistics, Puranam and Vanneste Corporate Strategy). They do not atomise into compelling 20-second idea-cards.

## Deliverables and acceptance criteria

### Deliverable 1: The 1-pager

- Acceptance: a single page (PDF) that covers all seven session-5 elements plus a one-line moat and a one-line evals statement, in the product's visual identity (see Design doc). Readable in under two minutes. No element missing.

### Deliverable 2: The pitch deck

- Acceptance: 7 to 10 slides, product-branded per the Design doc. There is a distinct slide for each of: problem, clients and segments, market size, competition, MVP, team, plus a dedicated moat slide and a dedicated evals slide. The market-size slide cites sources. The competition slide names LeafTok. The evals slide shows the adaptive-versus-random uplift chart produced by the notebook.
- Acceptance: opens on the problem and customer evidence (Mom Test framing), not on the solution.

### Deliverable 3: The pitch video

- Acceptance: a 7 to 10 minute script exists and, when delivered, covers the same content as the deck.
- Acceptance: at least one hero visual is filmed: a screen-recording of the notebook recommender adapting, and or the clickable mockup being swiped.
- Acceptance (optional element): if the HeyGen author-avatar teaser is included, it is under one minute, clearly labelled as AI-generated, and framed as an illustrative future feature.

### Deliverable 4: The notebook (confirmed in scope)

- Acceptance: the notebook runs top to bottom in a fresh environment with **no API key set**, using the shipped `cards.json`.
- Acceptance: it contains an **Atomiser** section that shows the book-to-cards prompt and schema, and (in an optional, clearly-marked cell) can regenerate cards live via the Anthropic API when a key is present.
- Acceptance: it contains a **Recommender** section that embeds the cards, maintains an engagement-weighted taste vector, serves next cards with an explore-exploit rule, and simulates at least two distinct user personas.
- Acceptance: it produces the **adaptation visual** (a 2D map of cards coloured by topic with the served sequence traced toward the persona's interest) and the **uplift number** (adaptive feed versus random-order baseline on simulated engagement), both rendered inline.
- Acceptance: it prints the **card-quality eval** result (LLM-judge or rule-based rubric pass rate over the card bank).
