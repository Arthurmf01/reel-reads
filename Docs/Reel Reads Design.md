# Reel Reads — Design

The visual acceptance bar for every surface a viewer sees: the card and feed identity, the clickable mockup, and the pitch deck. This is the design-critic's contract, the look-and-feel counterpart to the Specifications' acceptance criteria.

## Creative direction

**The one feeling:** quiet-luxury editorial calm. The feed should feel expensive, considered, and adult, the way a beautifully typeset book or a premium print magazine feels. This is the deliberate opposite of the loud, gamified, neon look of TikTok and Duolingo.

**Why this feeling and not the obvious one:** the pitch line is "same dopamine, opposite outcome." A dark-neon TikTok clone would visually say "same as TikTok". A calm editorial surface visually argues the opposite outcome before a word is spoken. The design does pitch work.

**The concrete reference:** [legora.com](https://legora.com), the legal-AI product. Copy its **aesthetic language**, not its layout (Legora is a dense document workspace, which is irrelevant to a swipe feed). What to take from it:

- A deep forest or pine green as the single signature accent.
- Warm, cinematic, golden-hour photography as imagery, not flat illustration or stock-tech gradients.
- A refined serif for display type, set large and confident, paired with a clean humanist sans for everything functional.
- Warm off-white and bone backgrounds, near-black text, generous whitespace.
- Soft pill buttons carrying a small circular-arrow icon; large rounded cards; restrained, subtle motion.

## Palette

- Accent (forest green): approximately `#1E4A38`. One accent, used for actions and the wordmark, not spread across many hues.
- Background (bone or warm off-white): approximately `#F7F6F2`.
- Text (near-black): approximately `#1A1A1A`, with a warm mid-grey for secondary text.
- Topic imagery: warm golden-hour photographic tones behind or beside each card, with a wash that keeps text legible. Topic tags may use a muted tint of the accent, not a rainbow of colours.

Exact hex values are a starting point captured from the live site; the design-critic ranks against real Legora screenshots, so match the *feel*, and refine the values against those screenshots rather than treating these as fixed.

## Typography

- **Display and idea-hooks:** a refined serif (transitional or humanist serif), set large. Each card's idea reads as a beautifully set line from a book. This is the emotional core of the identity.
- **UI, metadata, buttons, book and author lines:** a clean humanist sans.
- **Wordmark:** "REEL READS" in a letter-spaced serif, echoing Legora's wordmark treatment.

## Design principles (guardrails, decided now)

- Restraint over addition. Polish by subtraction. If a decorative element does not earn its place, remove it.
- No decorative gradients, glows, or drop-shadow stacks for their own sake. Depth comes from whitespace and one soft shadow at most.
- One accent colour. Resist the urge to colour-code every topic with its own bright hue.
- Native, standard components. No bespoke widgets where a plain one reads cleaner.
- Type does the work. The identity is carried by the serif or sans pairing and the whitespace, not by ornament.

## Variety strategy

The direction is committed (Legora-inspired), so exploration is narrow, not open. For the card and feed, produce two or three quick variants that differ only in: serif choice, how imagery meets text (full-bleed wash versus a framed image band), and card density. Rank against the moodboard, pick one, and hold it across the mockup and the deck so the whole package reads as one product.

## Design-critic rubric and moodboard

- **Quality target:** 8 out of 10 or higher against the moodboard. Below that, iterate.
- **Moodboard (rank against these):** live screenshots of legora.com (hero, the "Introducing the aOS" section, and a product-UI section); one premium editorial reference (a Penguin Classics cover or a New Yorker layout) for the serif-plus-whitespace feel; one calm reading-app reference for the card framing. Capture the Legora screenshots fresh during the build so the critic ranks against current pixels.
- **Stopping criterion:** the card and feed read as calm, premium, and editorial (not gamified, not neon, not generic-SaaS-blue); the serif idea-hook is the clear focal point; the forest-green accent is the only strong colour; a stranger shown the mockup would describe it as "expensive" or "considered" before "fun".
- **Failure signals to catch:** rainbow topic colours; a dark-neon TikTok pastiche; flat tech illustration instead of warm photography; the serif reduced to a timid subheading instead of the hero.

## Motion and video

The feed is video-native, so motion is part of the identity, not decoration. Two layers:

- **Ambient background motion** behind every card: slow, cinematic golden-hour movement themed to the idea (drifting light, gentle Ken Burns, or short looping footage). It must stay calm and never fight the text, restraint is the rule. In the self-contained mockup this is a live canvas animation (real video files cannot be embedded under the artifact CSP without bloating the page); in the product and the filmed demo it is actual footage or generated video. The two look the same to a viewer.
- **AI author-explainer clip** as the video hook: a short talking-head avatar of the author, or a clearly-labelled AI narrator, delivering the idea. Every AI clip carries a visible "AI" label. Free-tier avatar tools (HeyGen and similar) suffice for one labelled teaser clip (roughly one minute, watermarked); an avatar API is the path for a per-card clip at catalogue scale. Never depict a real or deceased author without a licence or consent; prefer consenting authors or a neutral narrator.
- Respect `prefers-reduced-motion`: fall back to a still frame for both layers.

## Asset plan

- **Topic imagery and footage:** warm golden-hour photography or short video loops per topic or book. Source from a permissively-licensed stock set, or generate; either way keep any generation key gitignored and never ship a key in the product or the notebook.
- **Wordmark and icons:** set in type plus a simple circular-arrow glyph; no custom logo commission needed for a course pitch.
- **Deck and mockup screenshots:** exported into `assets/` for reuse across the deck, 1-pager, and video.
- Keys and any generated media that is large or licence-encumbered stay out of git.
