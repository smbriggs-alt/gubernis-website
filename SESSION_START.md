# SESSION_START — gubernis-website

Quick orientation for picking up work on this repo. Read `README.md` and `CLAUDE.md` for the substance; this file is just for the *what now* question.

## ✅ Live — as of 2026-05-24

**gubernis.com is live.** Engine running daily on Railway, marketing site
deployed to IONOS, waitlist working end-to-end, legal floor in place,
search engines verified.

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
- Watch counter: **auto-patched at deploy time** from the live engine's
  public `/gubernis/watch-counter` endpoint (`scripts/patch_watch_counter.py`
  runs in the deploy workflow). Fail-soft — if the endpoint is
  unreachable, deploy proceeds with whatever numbers are baked into the
  repo. The numbers in `index.html` source are therefore stale by
  design; what's served is always fresh.
- HTTPS canonicalisation: `.htaccess` forces HTTPS + apex (strips
  `www.`). SSL cert provisioned via Let's Encrypt at IONOS.
- Samples: five Watch Forward sample dispatches live at `/samples/`.
  Marked explicitly as illustrative (commit `eae22ed` rewrote the
  earlier fabricated ambiguity flags after a traceability review —
  every claim now ties to a real ingest or primary source, or is
  labelled illustrative).
- Search engines: Google Search Console verified; sitemap
  (`/privacy/`, `/terms/`, `/samples/` included) submitted.
- Security disclosure: RFC 9116 `security.txt` published at
  `/.well-known/security.txt`.
- Legal floor: privacy notice at `/privacy/` (commit `903a11b`),
  subscription agreement at `/terms/` (commit `7ed2e81`). Footer
  carries Companies House No. 17207406 + ICO ZC134066 + Privacy +
  Terms links. Named contacts: `privacy@gubernis.com` (UK GDPR
  data-subject requests), `legal@gubernis.com` (legal notices,
  complaints). Watch Forward IP-protection clauses in §8 of the
  terms — named-seat enforcement, no verbatim client retransmission,
  no syndication, no derivative database, 1-yr confidentiality
  survival.

**Follow-ups worth doing when you pick this up:**

1. **Automate "What changed this week" cards (goal, not built).** Watch-counter
   numbers are already auto-patched at deploy from the live engine.
   Cards are not — they're still editorial via the interactive picker
   in `scripts/refresh_this_week_cards.py`. The goal is to **automate
   card selection with firm rules** so the homepage doesn't go stale
   between manual refreshes. Open design questions to settle before
   building:
   - **Selection ruleset.** What counts as "newsworthy this week"?
     Combination of: ambiguity-flagged > substantive > other; jurisdiction
     balance (don't show three EU items if a US or UK alternative is
     comparable); topic spread (don't show three sanctions stories);
     freshness (last N days, configurable); de-dupe against identities
     already shown in the previous N rotations.
   - **Summary generation.** Hard problem — `feedback_dispatch_
     traceability.md` forbids fabricated specifics. Options: (a) use
     the engine's own structured fields (issuing agency, severity,
     ambiguity reason, affected HS chapters where available) to build
     templated summaries that cite the source; (b) LLM-draft against a
     constrained prompt that's only allowed to paraphrase the title +
     structured fields, never invent. Either way, a "no fabrication"
     contract is the load-bearing constraint.
   - **Human-in-the-loop or not.** Cron + auto-commit? Cron + open a
     PR for approval? Daily auto-commit with weekly human override?
     The dispatch-traceability rule probably argues for at least a
     review checkpoint before the page changes.
   - **Cadence.** Daily refresh? Weekly? Triggered by ambiguity-flag
     volume?

2. **Manual cards refresh in the meantime.** Until item 1 lands, run
   the picker weekly during the marketing push:

   ```
   cd gubernis-website
   python3 scripts/refresh_this_week_cards.py
   # — pick 3, write a sentence each, review with `git diff`
   git commit -am "this-week: refresh cards"
   git push    # → auto-deploys, picks up live Watch-counter too
   ```

   The script needs no env vars; the endpoint is public read-only.
   Defaults to 10 candidates from the last 7 days. Override with
   `--limit 20 --days 14` if the week was quiet.

3. **Legal stack — future work** (low urgency, the floor is laid):
   - **Informal lawyer-friend review.** Worth getting a sanity-check
     read-through from a UK B2B-SaaS lawyer-friend (NOT a billable
     engagement, per Stephen's in-house drafting discipline). Look
     specifically at the liability cap, governing law, and §8
     enforcement clauses.
   - **Data Processing Addendum (DPA).** Stub-referenced in §15 of
     the terms but not actually written. Only needed when a customer
     puts us in a processor relationship — i.e. they provide us
     personal data to process on their behalf. Today none of the
     tiers contemplate that.
   - **Acceptable Use Policy.** Currently the prohibitions live in
     §7 of terms. If the misuse landscape gets richer (e.g. specific
     scraping patterns emerge), break out into a separate AUP linked
     from §7.
   - ~~`security.txt`~~ — **DONE** (commit `9d272f8`). Published at
     `/.well-known/security.txt` per RFC 9116. The
     `security@gubernis.com` mailbox itself is still TBC.

---

## Where this repo sits

| | Location |
|---|---|
| This repo (the marketing site) | `gubernis-website/` |
| The engine | `pragticality/gubernis/` (on `main` as of 2026-05-21, commit `f73bf05`) |
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

Deploy is live and automated. Push to `main` → GitHub Actions
(`.github/workflows/deploy.yml`) runs lftp over SFTP to IONOS. See the
"What's wired up" section at the top for hosting / DNS / SFTP details.

What happens on each push:

1. Stage public files (`index.html`, `styles.css`, legal pages,
   `samples/`, `.well-known/`, sitemap, etc.) into `dist/`.
2. Patch the Watch counter in `dist/index.html` from the live engine's
   `/gubernis/watch-counter` endpoint (`scripts/patch_watch_counter.py`,
   fail-soft).
3. lftp mirror `dist/` to the IONOS chroot root (no `--delete` — manually
   placed files like Google verification HTML and Let's Encrypt
   challenges are left alone).

Search-engine and canonicalisation setup are already done:
- Google Search Console — verified (HTML file at repo root).
- Sitemap — `sitemap.xml` includes `/privacy/`, `/terms/`, `/samples/`.
- `.htaccess` — forces HTTPS, canonicalises `www.gubernis.com` → apex.

Outstanding deploy-adjacent items:
- Bing Webmaster Tools — set up via "Import from Google" (deferred).
- `Organization` JSON-LD in `<head>` — optional SEO refinement (deferred).

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

Don't. It's auto-patched at deploy time from the live engine's public
`/gubernis/watch-counter` endpoint (`scripts/patch_watch_counter.py`,
called from the deploy workflow). The numbers in `index.html` source
are intentionally stale; what's served is fresh on every push.

If the deployed numbers look wrong, debug the endpoint, not the HTML:
```
curl -s https://pragticality-production.up.railway.app/gubernis/watch-counter | python3 -m json.tool
```

### Refreshing the "What changed this week" cards

Currently manual / editorial. Use the picker:

```
cd gubernis-website
python3 scripts/refresh_this_week_cards.py
# — pick 3, write a sentence each, review with `git diff`
git commit -am "this-week: refresh cards"
git push    # → auto-deploys, picks up live Watch-counter too
```

The script fetches from `/gubernis/recent-changes` (public, no auth).
Defaults to 10 candidates from the last 7 days; override with
`--limit 20 --days 14` if the week was quiet.

Per `feedback_dispatch_traceability.md`, summary copy must tie to the
real ingest — no fabricated specifics. The script's interactive prompt
makes this explicit ("editorial pick step" is the whole point of
keeping it human).

Automation of this step is a stated goal — see follow-up #1 at the
top of this file.

### Adding a new section

1. Sketch in `pragticality-docs/strategic_package/website/gubernis-brand-direction.html` first
2. Port to `index.html` once the design is stable
3. Add styles to `styles.css` (single shared stylesheet, no per-page styles)
4. Add anchor link to the `site-nav` if it's a major section

### Adjusting pricing tiers

Pricing is in the `.pricing-grid` section. **Five tiers** (as of
2026-05-24): Free Watch (£0) / Starter (£200) / Pro (£800) /
**Watch Forward (£1,800)** / Enterprise (£30k+/yr). The Ambiguity
Watch sits in Pro as the upgrade gate; Watch Forward adds
pipeline-tracking on top. Watch Forward at £21,600/yr sits ~£3.4k
under the £25k procurement-threshold from
`feedback_procurement_threshold_pricing.md` — adding features that
push the price up risks crossing into procurement-friction land.

## What this session is NOT for

- Implementing the engine — that's the `pragticality` repo, on `main`
  branch (in `gubernis/`).
- Strategic direction — that's `pragticality-docs/gubernis/`.
- Building a blog / multi-page expansion — deferred until V1 is validated.
- Adding tracking / analytics without explicit privacy review.
- Anything that adds JavaScript frameworks or a build step.

## Auto-memory rules that apply here

If you're Claude Code, the following auto-memory entries are load-bearing for this repo:

- `feedback_gubernis_customer_copy.md` — never describe mechanism in customer copy
- `feedback_marketing_claim_defensibility.md` — no unsupported competitive claims
- `feedback_dispatch_traceability.md` — no fabricated specifics in cards / Watch Forward dispatches; every claim cites engine ingest or primary source
- `feedback_procurement_threshold_pricing.md` — keep wedge-tier annual spend below £25k
- `feedback_gubernis_scope_discipline.md` — goods-affecting regulation only; not insurance, sales tax, freight
- `feedback_drive_terminal_ops.md` — drive multi-step terminal work via Bash tool, don't paste copy-paste lists
- `feedback_ground_rules.md` — ask before push / deploy / delete

## Pairs with

- `README.md` (this repo)
- `CLAUDE.md` (this repo)
- `pragticality-docs/gubernis/06_brand_direction.md` (the brand spec)
- `pragticality-docs/gubernis/05_product_thesis.md` (the product thesis)
- `pragticality-website/SESSION_START.md` (the sibling site's session-start; similar structure)
