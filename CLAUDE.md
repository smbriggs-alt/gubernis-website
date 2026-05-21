# CLAUDE.md — gubernis-website

Guidance for Claude Code (or any AI assistant) editing the source files of [gubernis.com](https://gubernis.com).

## What this site is

The marketing front-end for **Gubernis**, a Pragticality Ltd product. Gubernis is a regulatory watch product — it surfaces what changed in UK / EU / US trade compliance regulation and flags where careful readings of the published text diverge.

Kernel: **Surfaces change. You decide.**
Supporting line: *When the rules move, we're already telling you.*

Strategic context lives in `pragticality-docs/gubernis/`. Read `06_brand_direction.md` before making any voice or visual changes here.

## Brand voice — hard rules

The Gubernis voice is **trusted-advisor-with-skin-in-the-game.** Like a senior counsel: quiet, considered, accountable, plain-spoken. Stakes credibility on judgement; no hedging to meaninglessness.

### Forbidden language (this is non-negotiable)

The following words and patterns must never appear in customer-facing copy on this site. They are generic-SaaS-marketing tells that signal the opposite of trusted-advisor register:

| Forbidden | Why | Use instead |
|---|---|---|
| *AI-powered* / *AI-native* (as marketing claim) | Cheapens the product; signals "another wrapper" | Describe what the product does — never the technology |
| *Next-generation* / *cutting-edge* / *revolutionary* | Hyperbole tells | Describe the work plainly |
| *Empower* / *harness* / *transform* / *unlock* | Marketing-bingo verbs | Use concrete verbs: *watches, surfaces, flags, dispatches, reads* |
| *Intelligence platform* / *intelligence layer* | Abstract puffery | *Regulatory watch* — the literal product category |
| *Hey there!* / *Welcome to the future!* | Fake warmth | Warmth comes from precision and accountability, not chirp |
| *Dual-LLM* / *two AI systems* / *Claude + OpenAI* | The mechanism is internal | *"Multiple independent reading paths"* / *"where readings diverge"* |
| *No other X does this* / *Only X in the market* | Unsupported competitive claims (per `feedback_marketing_claim_defensibility.md` in auto-memory) | Describe the feature; let readers infer differentiation |

### Required register

- **Plain English.** Regulatory citations render cleanly (e.g. *§ 15 CFR 740.3(a)*), with one-sentence explanations.
- **Brevity over completeness.** Two crisp paragraphs beat one comprehensive page.
- **Wire-service dispatches**, not essays. The voice of the analyst who writes the morning brief, not the consultant who writes the white paper.
- **Customer agency.** Gubernis surfaces; the customer decides. Never *"Gubernis recommends"* or *"the AI advises"*.
- **Honest hedging when warranted.** *"Readings diverge on whether..."* is good. *"This may or may not be relevant"* is bad. Hedge with precision, not with vagueness.

### Visual rules

- **No AI imagery.** No circuits, neural nets, glowing networks, neon, gradients suggesting flow.
- **No SaaS marketing imagery.** No abstract 3D shapes, no faceless silhouettes around laptops, no hand-drawn diagrams of interlocking circles.
- **Editorial register only.** Source Serif 4 body, JetBrains Mono for technical content (citations, timestamps, identifiers), Inter for UI chrome.
- **Oxblood `#7A2632`** as the signal accent. Used for the § ornament, headline numbers, the Ambiguity Watch flag colour, and emphasis.
- **The § mark** is the wordmark ornament. Set in oxblood, before the typographic word.

## The Ambiguity Watch — special handling

The Ambiguity Watch is the differentiated Pro-tier feature. When writing about it:

- **Describe the customer outcome** (surfaces grey-edge regulatory changes; flags rules where readings diverge) — *never* the mechanism.
- **Lean into "where the bills come from"** language. Stephen's framing 2026-05-20: *"ambiguity is the boogie man and we don't need to hide it."* Sharp consequence-language is welcome; melodrama is not.
- **Don't make competitive claims** about what other products do or don't offer until we've researched and documented those claims. Stephen's discipline 2026-05-20: *"we need to be very careful about statements like 'no other offers this' unless we have done some dope/hallucination checks."*

## The Watch — the live ledger

The Watch counter sits below the hero. It carries **two messages at once**:

1. *Selling*: the engine is working; numbers tick up; the watch is happening.
2. *Warning*: 287 changes in 28 days across 6 sources — the volume of regulatory activity the customer would miss alone.

The ambiguity-flag cell in oxblood is the headline metric. The other four (Changes today / 7d / 28d / Sources) are supporting evidence.

Numbers shown on the site are illustrative placeholders. In production they would be read from the engine's live data via a small endpoint. Update them periodically (manually for V1; via a tiny script for V2) so the ledger isn't visibly stale.

## Site structure

Single-page V1. All sections accessible via anchor links from the top nav.

| Anchor | Section |
|---|---|
| (top) | Hero — kernel + supporting line |
| (below hero) | The Watch — live ledger |
| `#ambiguity-watch` | The Ambiguity Watch feature section (navy background) |
| `#how-it-works` | What Gubernis does — intro with ontology callout |
| `#this-week` | What changed this week — three cards |
| `#sources` | Sources covered — six-source proof bar |
| `#pricing` | Four-tier pricing (Free / Starter / Pro-recommended / Enterprise) |
| `#sign-up` | Final CTA — email capture for early-access list |

Multi-page expansion (`/about/`, `/pricing/`, `/how-it-works/`) is deferred. Anchor links on the single page are V1's answer.

## How to edit safely

1. **Read `06_brand_direction.md` in `pragticality-docs/gubernis/`** before any voice or visual change. The doc is the spec; this site implements it.
2. **Run `feedback_gubernis_customer_copy.md`** (in auto-memory) as a checklist after any copy change. Common slip: AI-mechanism language sneaking back in.
3. **For Ambiguity Watch copy changes**: describe outcomes, never mechanisms; let readers infer differentiation; no competitive claims without research.
4. **For Watch ledger numbers**: replace placeholder values with current engine counts where possible; otherwise refresh the timestamp so the ledger isn't visibly stale.
5. **For new sections or pages**: start by sketching in the design-direction mockup at `pragticality-docs/strategic_package/website/gubernis-brand-direction.html` first; only port to this site once the design is stable.

## What this repo is not

- The Gubernis engine itself — that's `gubernis/` inside [`pragticality`](https://github.com/smbriggs-alt/pragticality) (`gubernis-poc` branch).
- The Gubernis strategic docs — those live in `pragticality-docs/gubernis/`.
- The Pragticality Ltd holding-company site — that's `pragticality-website`.
- The Gnomon product site — that's `gnomon-website`.
- A blog. (Not yet. Maybe later — `gubernis.com/this-week/` could become a public weekly digest as a lead-gen channel per the product thesis.)

## Hard "do not"s

- **Do not** add JavaScript frameworks. Vanilla JS for tiny interactions only (e.g. updating the Watch timestamp).
- **Do not** add a tracker pixel or analytics SDK without checking the privacy posture first. If/when added, document it visibly in the footer.
- **Do not** add a build step. Static HTML + one CSS file is the discipline.
- **Do not** invent claims, certifications, customer logos, testimonials, or quantitative metrics that aren't backed by real data. The Watch counter is the only metric on the site; it's illustrative until production data is wired.
- **Do not** describe the engine's mechanism in customer copy. (Repeating because this is the one most likely to be slipped back in.)

## Deploy + form handling

- **Hosting:** IONOS web hosting (same vendor as `pragticality.com`).
- **DNS:** `gubernis.com` is managed in the IONOS control panel.
- **Auto-deploy:** GitHub Actions workflow at `.github/workflows/deploy.yml`
  uses `lftp` to mirror the staged `dist/` directory to IONOS over SFTP
  (port 22) on every push to `main`. Same pattern as
  `gnomon-website/.github/workflows/deploy.yml`. The IONOS SFTP user is
  chrooted to `/Gubernis/`, so lftp uploads to `/` (which from the user's
  perspective is the webspace's `/Gubernis/`). The workflow needs three
  repository secrets matching the estate-wide convention:
  `IONOS_FTP_HOST`, `IONOS_FTP_USER`, `IONOS_FTP_PASS` — set them in
  Settings → Secrets and variables → Actions.
- **Form handling:** Formspree free tier (50 submissions/mo). The endpoint
  ID goes into the `<form action>` attribute on `#sign-up`. If Gubernis
  starts pulling enough signups to exceed the free tier, replace the
  Formspree endpoint with either a paid Formspree plan or a tiny PHP
  mailer hosted alongside the static files on IONOS.

## Open decisions (carried forward)

- Final tone selection (currently the "Watch House" / Tone C from v1 of the brand direction)
- Exact oxblood hex (currently `#7A2632`; could shift `±` 10 units after print-style testing)
- Wordmark spacing (currently `§ Gubernis` with single space)
- Whether to add a public `/this-week/` weekly-digest page as a lead-gen tool
