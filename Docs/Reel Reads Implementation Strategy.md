# Reel Reads — Implementation Strategy

The runbook. Ordered phases, each marked automated (Claude does it) or manual (Arthur does it), with dependencies. Single version. The canonical "what" and acceptance criteria live in `Reel Reads Specifications.md`; the visual bar lives in `Reel Reads Design.md`.

## Stack decisions (verify-before-use noted where relevant)

- **Notebook:** Python 3.11, Jupyter or Google Colab. Follows the Python default stack (type hints, no hardcoded secrets, `logging` over `print` in any helper module).
- **Atomiser LLM:** Anthropic Claude, Haiku tier for cost (cheap, fast; confirm the current Haiku model id via the `claude-api` skill at build time rather than hardcoding from memory). Key via environment variable, never committed.
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`), run locally. Free, no API key, reproducible for a grader. Chosen over a hosted embeddings API precisely so the notebook runs offline. This is a new dependency, flagged deliberately.
- **Recommender:** content-based taste vector over card embeddings, cosine similarity for the next-card pick, epsilon-greedy for exploration. No heavy ML framework needed (numpy plus sentence-transformers).
- **Plotting:** matplotlib. 2D projection via PCA (scikit-learn) or UMAP; prefer PCA to avoid a heavy dependency unless UMAP clearly reads better.
- **Mockup:** self-contained HTML or CSS (headless-Chrome-printable, same pattern as Arthur's other one-pagers) or Figma Make (demoed in class). Decide at Phase 3 based on which films better.
- **Deck:** self-contained HTML or CSS artifact in the product identity, printable to PDF. Not the INSEAD-brand deck skill (this is a startup pitch, product branding wins).

## Phase 0: Setup

- **Manual (Arthur):** confirm Python or Colab is available. If regenerating cards live, obtain and export an Anthropic API key (`ANTHROPIC_API_KEY`); this is optional because cards ship pre-generated.
- **Automated:** scaffold the repo: `notebook/`, `data/` (for `cards.json`), `deck/`, `assets/`, a `.gitignore` that excludes any key file, environment or `.env`, and generated media, and a `README.md`. Add `requirements.txt`.
- Depends on: nothing.

## Phase 1: Content seed and card generation

- **Automated:** seed with the verified top-ten catalogue from the Specifications ("Seed catalogue" section): Blue Ocean Strategy, The Lean Startup, The Innovator's Dilemma, Thinking Fast and Slow, The Goal, The Black Swan, Against the Gods, Freakonomics, The Art of Strategy, Effectuation. All ten are traceable to Arthur's own INSEAD course notes (textbook, recommended reading, or repeatedly-cited slide concept). Expand toward roughly 15 only from the verified bench list in the Spec, not from a generic web list.
- **Automated:** define the card schema: id, book, author, topic tag, hook (one line), idea (roughly 40 words), why-it-matters (one line). Generate roughly 5 cards per book with Claude Haiku from parametric knowledge (no full-text ingestion). Save to `data/cards.json`.
- **Manual (Arthur):** spot-check a sample of cards for faithfulness and quality (5 minutes). This is the human half of the card-quality eval.
- Depends on: Phase 0.

## Phase 2: Card-quality eval

- **Automated:** build the rubric eval (accurate, self-contained, non-obvious, faithful). Score the card bank with an LLM judge (optional, needs key) and or a rule-based proxy (length, self-containment, topic-tag agreement) so it also runs offline. Print a pass rate. Target 90 percent or higher; regenerate weak cards until met.
- Depends on: Phase 1.

## Phase 3: The recommender notebook (centrepiece)

- **Automated:** embed all cards with sentence-transformers. Implement the taste vector (engagement-weighted mean of embeddings of cards the user liked or dwelled on, down-weighted for skips). Implement next-card selection (max cosine similarity among unseen) with epsilon-greedy exploration and a cold-start rule.
- **Automated:** simulate at least two distinct personas (for example a "behavioural psychology" lover and a "corporate strategy" lover) as latent preference vectors that generate swipe or dwell signals. Run each through a feed session.
- **Automated:** produce the two required outputs inline: the **adaptation visual** (2D PCA map of cards coloured by topic, with the served sequence traced, showing convergence toward the persona's interest) and the **uplift number** (mean simulated engagement of the adaptive feed versus a random-order baseline, reported as a percentage lift).
- Depends on: Phase 1 (cards) and ideally Phase 2 (clean bank).

## Phase 4: Clickable product mockup

- **Automated:** build a swipeable feed of roughly 10 cards in the Legora-inspired identity from the Design doc (full-screen cards, serif idea-hooks, forest-green accents). It is video-native: each card carries an ambient motion background and a visible AI author-explainer control (the point where a HeyGen-style clip plays), plus the adaptive "served because" line. HTML or Figma Make. It must look filmable on a phone-shaped frame. A working first version already exists at `mockup/reel-reads-mockup.html` (canvas motion, author-explainer pills, nine seed cards); extend or restyle from there.
- **Manual (Arthur):** review the look on device, then screen-record or film a swipe-through for the video and for deck screenshots.
- Depends on: Design doc; can run in parallel with Phases 2 and 3.

## Phase 5: Market-size verification

- **Automated:** verify the TAM, SAM, SOM figures against named primary sources (microlearning market value and CAGR, incumbent user and revenue numbers, MBA enrolment). Replace any figure that cannot be sourced.
- **Manual (Arthur):** sign off the numbers he is willing to defend on stage.
- Depends on: nothing; do before Phase 6.

## Phase 6: The pitch deck

- **Automated:** draft 7 to 10 slides in the product identity, mapping one slide to each required element plus the dedicated moat and evals slides. Open on problem plus customer evidence, not the solution. Embed the notebook uplift chart on the evals slide and the mockup screens on the MVP slide. Name LeafTok on the competition slide. Cite sources on the market slide.
- **Manual (Arthur):** run real Mom Test interviews inside his cohort and drop the evidence into the problem and customer slides. Edit voice and claims.
- Depends on: Phases 3, 4, 5.

## Phase 7: The 1-pager

- **Automated:** condense the deck into a single-page PDF in the product identity, all seven elements plus one-line moat and evals.
- Depends on: Phase 6.

## Phase 8: The video

- **Automated:** write the 7 to 10 minute script from the deck, with the hero-visual cues marked (where the notebook recording and mockup swipe appear).
- **Manual (Arthur):** record the pitch; capture the screen-recordings; optionally produce one sub-one-minute HeyGen author-avatar teaser on the free tier, clearly labelled as AI and framed as a future feature.
- Depends on: Phases 3, 4, 6.

## Sequencing summary

- Critical path: Phase 0 to 1 to 2 to 3 (the notebook), then 6 to 7 to 8.
- Parallel: Phase 4 (mockup) and Phase 5 (market check) can run alongside Phases 2 and 3.
- The two graded-first items (1-pager plus draft deck) come out of Phases 6 and 7; the notebook (Phase 3) is the proof that makes the deck believable and should not be cut.
