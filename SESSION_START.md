# SESSION_START — gubernis-website

Quick orientation for picking up work on this repo. Read `README.md` and `CLAUDE.md` for the substance; this file is just for the *what now* question.

## ✅ Live — as of 2026-05-21

**gubernis.com is live.** Engine running daily on Railway, marketing site
deployed to IONOS, waitlist working end-to-end.

**What's wired up:**

- DNS: gubernis.com nameservers at IONOS (`ns1045.ui-dns.*`); A record
  auto-set to `217.160.0.23` by IONOS once domain was connected to
  webspace under `/Gubernis/`
- Hosting: IONOS web space, contract 107127470, host
  `access-5018101164.webspace-host.com`
- SFTP user: `a2016447` (chrooted to `/Gubernis/`) — created via the
  IONOS panel
- Auto-deploy: GitHub Actions workflow at `.github/workflows/deploy.yml`
  uses `lftp` over SFTP port 22. Mirror of the gnomon-website pattern.
  Three secrets in the repo: `IONOS_FTP_HOST`, `IONOS_FTP_USER`,
  `IONOS_FTP_PASS`. lftp uploads to `/` (chroot root IS `/Gubernis/`).
  Every push to `main` redeploys.
- Form: Formspree endpoint `https://formspree.io/f/xwvzopqy` wired into
  `#sign-up`. Submissions land in the Formspree dashboard and forward
  to Stephen's email. End-to-end tested 2026-05-21.
- Watch counter: numbers refreshed from real engine data on
  2026-05-21 (24 changes today / 31 last 7d / 407 docs tracked / 11
  sources / § 8 ambiguity flags). Manual refresh for now — see the
  follow-up below.
- SSL: Let's Encrypt cert via IONOS — provisioning kicked off when
  domain was connected. May still be propagating through their edge
  even after IONOS marks it "issued" (their platform had system
  issues 2026-05-21). HTTP works regardless.

**Follow-ups worth doing when you pick this up:**

1. **Watch counter auto-refresh.** Wire a `/gubernis/watch-counter`
   JSON endpoint on the Railway FastAPI app that returns current
   counts. Then either (a) have the deploy workflow `curl` that
   endpoint and `sed`-patch index.html before lftp upload, or (b)
   add a client-side `fetch()` in index.html that calls the endpoint
   on page load. (b) is more dynamic but adds CORS surface. (a)
   freezes the numbers per-deploy but is simpler. ~30 minutes either
   way.
2. **HTTPS verification.** Run `curl -I https://gubernis.com` and
   confirm `200 OK` with a valid Let's Encrypt cert. If not, check
   the IONOS SSL panel for the gubernis.com cert status and trigger
   re-issue if needed.
3. **Sources section refresh.** The "Watching · eleven sources today"
   caption is right but the source cards in the row still list only
   6 (FR / OFAC SDN / gov.uk / HMRC Tariff / EU Sanctions / EUR-Lex).
   Add cards for USTR Section 301, BIS Section 232, Congress.gov,
   EU Legislative Train, UK Parliament — or split the row into
   "Published" + "Pipeline" subgroups (V2 of the section).
4. **"What changed this week" cards.** The current three cards are
   strong illustrative copy. As real, narrative-strong changes flow
   in, replace with actual ingested items (e.g. real OFAC SDN delta
   entries, real EU CFSP decisions). Refresh maybe weekly.

---

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
