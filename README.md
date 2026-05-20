# gubernis-website

Source files for the **Gubernis** marketing website at [gubernis.com](https://gubernis.com).

Static HTML/CSS — no build step, no JavaScript framework, no dependencies beyond Google Fonts. Sibling to [`pragticality-website`](https://github.com/smbriggs-alt/pragticality-website) (the holding-company site) and [`gnomon-website`](https://github.com/smbriggs-alt/gnomon-website) (the sibling product site).

## What Gubernis is

The regulatory watch for UK, EU, and US trade compliance. Surfaces what changed in regulation; flags ambiguity where careful readings diverge. A Pragticality Ltd product alongside Gnomon (classification) — the wedge in the wedge → destination product architecture.

Brand kernel: **Surfaces change. You decide.**

Strategic context: `pragticality-docs/gubernis/` in the [`pragticality-docs`](https://github.com/smbriggs-alt/pragticality-docs) repo, particularly:

- `00_README.md` — what Gubernis is, naming rationale, relationship to Gnomon
- `05_product_thesis.md` — Gubernis-as-product wedge → destination thesis
- `06_brand_direction.md` — kernel, voice, palette, ornament, three tones explored
- `strategic_package/website/gubernis-brand-direction.html` — the design exploration that became this site

## Read first

1. **[`SESSION_START.md`](./SESSION_START.md)** — quick orientation, deploy workflow
2. **[`CLAUDE.md`](./CLAUDE.md)** — guidance for AI assistants editing this repo (brand voice rules, the hard "do not"s)
3. The strategic docs above

## Repo structure

```
gubernis-website/
├── README.md           this file
├── SESSION_START.md    quick orientation + deploy workflow
├── CLAUDE.md           guidance for AI editing this repo
├── .gitignore
├── styles.css          single shared stylesheet
├── robots.txt
├── sitemap.xml
├── favicon.svg         the § mark in oxblood
└── index.html          single-page landing site
```

Multi-page expansion (e.g. `/about/`, `/pricing/`, `/how-it-works/`) is deferred to a later session. The single-page V1 is enough to validate willingness-to-pay via the LinkedIn survey planned in `pragticality-docs/gubernis/05_product_thesis.md` §6.

## How it deploys

Same pattern as `pragticality-website` and `gnomon-website`: static files, hostable anywhere.

The `gubernis.com` domain was registered on 2026-05-12 (initially as defensive insurance for the runner-up name in the product-naming session). DNS pointing and hosting setup are pending; deployment notes will land here once the host is chosen. Likely path: Fasthosts (same as `gnomon.info`) or IONOS (same as `pragticality.com`) — the deployment muscle for both is already in this house.

When deploying:

1. Ensure `index.html` references absolute paths (`/styles.css`, `/favicon.svg`) — they already do.
2. Upload the whole repo contents to the document root of `gubernis.com`.
3. Verify with `curl -I https://gubernis.com/sitemap.xml` and `curl -I https://gubernis.com/robots.txt`.
4. Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools (same convention as `pragticality.com` per its `SESSION_LOG`).

## What this isn't

- **The Gubernis engine** — that's the `gubernis/` module in [`pragticality`](https://github.com/smbriggs-alt/pragticality) (currently on the `gubernis-poc` branch; not yet merged to main). 18+ commits of working code: connectors for US Federal Register, OFAC SDN, UK gov.uk, UK HMRC Trade Tariff, EU Consolidated Sanctions, and EUR-Lex; dual-LLM cross-check tagger; semantic diff engine; automated smoke test. See `pragticality-docs/gubernis/04_poc_report.md` for the PoC verdict.
- **The Gubernis sub-brand assets** (logo SVG variants, social-share images, business cards). Those don't yet exist; only the `§` wordmark and oxblood palette are defined. Add when needed.
- **The Pragticality Ltd holding-company site** — that's [`pragticality-website`](https://github.com/smbriggs-alt/pragticality-website).
- **The Gnomon product site** — that's [`gnomon-website`](https://github.com/smbriggs-alt/gnomon-website).

## Conventions (inherited from sibling repos)

- **Markdown for guides, HTML for the site itself.** No SCSS, no preprocessors, no JS toolchain.
- **One stylesheet** (`styles.css`) shared across all pages. Per-page styles are forbidden.
- **Internal links use absolute paths** (`/about/`, `/pricing/`) so they work whether deployed at root or a subpath.
- **External links** open in a new tab with `rel="noopener"`.
- **Brand voice rules** are enforced in `CLAUDE.md` for AI assistants editing the repo. The hard ones: no "AI-powered" language, no mechanism description in customer copy, no unsupported competitive claims.

## Notes on brand voice

Gubernis copy is **trusted-advisor-with-skin-in-the-game**. Quiet authority, plain English, no SaaS marketing tells. Specifically:

- **Never** describe the dual-LLM cross-check mechanism in customer copy. The Ambiguity Watch is the *outcome* the customer sees; the engine architecture is invisible infrastructure. Memory rule: *"saying 'dual AI' might convince some people it can go wrong twice as fast."*
- **Never** make unsupported competitive claims like "no other regulatory monitor offers this." Either verify with research, or describe the product and let readers infer differentiation.
- **Never** use words like *empower, harness, transform, next-generation, AI-powered, intelligence platform.* These tells mark generic-SaaS-marketing voice that Gubernis explicitly opposes.

See `CLAUDE.md` for the full voice guide.
