# SESSION_START — gubernis-website

Quick orientation for picking up work on this repo. Read `README.md` and `CLAUDE.md` for the substance; this file is just for the *what now* question.

## Where this repo sits

| | Location |
|---|---|
| This repo (the marketing site) | `gubernis-website/` |
| The engine | `pragticality/gubernis/` (on `gubernis-poc` branch) |
| The strategic docs | `pragticality-docs/gubernis/` |
| The holding-co site (sibling) | `pragticality-website/` |
| The other product site (sibling) | `gnomon-website/` |

## How the site works

- Single-page HTML at `index.html`
- One stylesheet at `styles.css`
- Section anchors handle all in-page navigation
- No build step, no JavaScript framework
- Hostable anywhere static files run

## Deploying

The `gubernis.com` domain was registered 2026-05-12. Host setup is pending. When deployment lands, two probable paths:

### Option A — IONOS (same pattern as `pragticality.com`)

The Pragticality Ltd holding-company site is hosted on IONOS and deployed via GitHub Actions (workflow at `pragticality-website/.github/workflows/deploy.yml`). Same approach could apply here:

1. Set DNS for `gubernis.com` to IONOS
2. Add `IONOS_FTP_HOST`, `IONOS_FTP_USER`, `IONOS_FTP_PASS` secrets to this repo on GitHub
3. Add a `.github/workflows/deploy.yml` analogous to the one in `pragticality-website` (lftp-based SFTP push to IONOS document root)
4. Push to `main` triggers deploy

### Option B — Fasthosts (same pattern as `gnomon.info` was meant to)

The Gnomon marketing site was scoped to deploy to Fasthosts per `gnomon-website/DEPLOY.md`. Same registrar may apply to `gubernis.com` (it was registered there too — confirm via `whois gubernis.com`). If so:

1. Configure Fasthosts hosting for `gubernis.com`
2. Upload repo contents via SFTP / FileZilla / lftp
3. Verify `https://gubernis.com/` and `https://gubernis.com/sitemap.xml`

### Either way

- After deploy, submit `sitemap.xml` to Google Search Console (URL-prefix property; HTML file verification method like `pragticality.com` used)
- Set up Bing Webmaster Tools via "Import from Google"
- Add `Organization` JSON-LD to `<head>` (optional SEO refinement; deferred)
- Configure `www → root` 301 redirect at the DNS / host level

## What to do first when picking this up

1. **Read `README.md`** for the broader context — Gubernis as a product, the wedge → destination architecture, what this site is and isn't.
2. **Read `CLAUDE.md`** for the brand voice rules — what language is allowed, what's forbidden, what register to write in.
3. **Open `index.html` in a browser** to see the current state. Three things to check first:
   - The Watch counter — is it showing reasonable numbers or are they obviously stale?
   - The "What changed this week" cards — are the dates current?
   - The Ambiguity Watch section copy — does it still read as sharp, or has it drifted toward generic SaaS?
4. **Check open decisions** at the bottom of `CLAUDE.md` — most are still unresolved as of the initial commit.

## Common edits and how to make them safely

### Refreshing the Watch counter

Numbers in `index.html` lines around the `.ledger-grid` are placeholders. To refresh:

- Get current counts from the engine: `python3 -m gubernis.scripts.inspect_store` (in the `pragticality` repo on `gubernis-poc` branch) — provides total docs by source
- Compute today / 7d / 28d windows
- Update the `<div class="ledger-number">` values in the five cells
- Update the `ledger-time` text to current time

Or wire up a small endpoint and fetch dynamically — V2 work.

### Refreshing the "What changed this week" cards

Run `python3 -m gubernis.scripts.inspect_store --list --limit 10` in the engine repo to see recent ingests. Pick the three most substantive and update the three cards in `index.html` (around the `featured-grid` section).

### Adding a new section

1. Sketch in `pragticality-docs/strategic_package/website/gubernis-brand-direction.html` first
2. Port to `index.html` once the design is stable
3. Add styles to `styles.css` (single shared stylesheet, no per-page styles)
4. Add anchor link to the `site-nav` if it's a major section

### Adjusting pricing tiers

Pricing is in the `.pricing-grid` section. Four tiers: Free Watch / Starter / **Pro (recommended)** / Enterprise. The Ambiguity Watch sits in Pro as the upgrade gate — be deliberate about moving it.

## What this session is NOT for

- Implementing the engine — that's the `pragticality` repo, `gubernis-poc` branch.
- Strategic direction — that's `pragticality-docs/gubernis/`.
- Building a blog / multi-page expansion — deferred until V1 is validated.
- Adding tracking / analytics without explicit privacy review.
- Anything that adds JavaScript frameworks or a build step.

## Auto-memory rules that apply here

If you're Claude Code, the following auto-memory entries are load-bearing for this repo:

- `feedback_gubernis_customer_copy.md` — never describe mechanism in customer copy
- `feedback_marketing_claim_defensibility.md` — no unsupported competitive claims
- `feedback_drive_terminal_ops.md` — drive multi-step terminal work via Bash tool, don't paste copy-paste lists
- `feedback_ground_rules.md` — ask before push / deploy / delete

## Pairs with

- `README.md` (this repo)
- `CLAUDE.md` (this repo)
- `pragticality-docs/gubernis/06_brand_direction.md` (the brand spec)
- `pragticality-docs/gubernis/05_product_thesis.md` (the product thesis)
- `pragticality-website/SESSION_START.md` (the sibling site's session-start; similar structure)
