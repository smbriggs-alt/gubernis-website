# Document Watch — change **and** absence, one signal stream

> **Staging note.** Engine spec parked in the marketing-site repo for
> versioning. Final home: the Gubernis engine (`pragticality`,
> `gubernis-poc`). Not deployed to the live site. Pairs with
> `expected_cadence.yaml` in this folder.

## The idea

The engine already watches for **change** — a new or amended document. Document
Watch adds the mirror half: watching for **expected-but-absent** — the release
that should have happened and didn't. For a regulatory watch, silence is
information. A working-day publisher going quiet can mean a delayed rule, a
government shutdown, a missed statutory deadline — or our own ingestion quietly
breaking. All four are worth knowing; only the first three are worth telling the
customer.

Per Stephen's steer, this is **not a separate feature** — it folds into the
existing change-alert pipeline as additional `signal_type`s on one stream.

## Unified signal model

Every watch output — change or absence — is one `watch_signal`:

```jsonc
{
  "source_id": "federal_register",
  "signal_type": "change | overdue | statutory_deadline | pipeline_suspect",
  "observed_at": "2026-05-26T13:05:00Z",
  "severity": "info | substantive | high",
  "detail": "...",                  // human-readable line for the dispatch
  "evidence": { /* doc id / url for change; expected-window math for absence */ },
  "customer_facing": true            // pipeline_suspect → false (ops only)
}
```

- `change` — existing behaviour: a new/amended doc was seen.
- `overdue` — a `scheduled_working_days` / `periodic` / `session_days` source
  produced nothing inside its expected window (per `expected_cadence.yaml`).
- `statutory_deadline` — a tracked clock fired: a §232 investigation passed its
  270-day report mark, a §301 review window opened. This is the *only* absence
  analog for the event-driven sources.
- `pipeline_suspect` — **the guard** (below). Overdue, but probably us, not them.

## What the detector needs

Two timestamps per source, kept distinct — this distinction is the whole ballgame:

- `last_successful_fetch` — we reached the source and parsed it OK.
- `last_new_document` — we actually saw something new.

A daily evaluator walks each source and asks, using its cadence entry:

1. Is a release **expected** by now? (working/sitting-day calendar + window, or
   periodic staleness, or a statutory clock.) If not → do nothing.
2. If expected and `last_new_document` is inside the window → healthy.
3. If expected and nothing new:
   - `last_successful_fetch` **also** stale → `pipeline_suspect` (our scraper or
     the source endpoint is down). Route to ops; **not** customer-facing.
   - `last_successful_fetch` fresh (we looked, there was genuinely nothing) →
     `overdue`. This is the real signal.

> **The one subtlety that makes or breaks it:** never conflate "the source
> released nothing" with "we failed to fetch." Splitting those two timestamps
> is what stops the feature crying wolf — and it doubles as free monitoring of
> our own ingestion health.

## Scope across the eleven

- **Absence-capable (7):** `federal_register`, `eur_lex`, `gov_uk_publications`,
  `congress_bills`, `uk_parliament_bills` (calendar-bound), `eu_legislative_train`
  (periodic). These can be genuinely "overdue."
- **Statutory-clock analog (2):** `bis_section_232`, `ustr_section_301` — can't
  be calendar-overdue, but their statutory deadlines are trackable and fire
  `statutory_deadline`.
- **Presence-only (2):** `ofac_sdn`, `eu_sanctions_consolidated`,
  `hmrc_trade_tariff_news` are unscheduled — watch for change, never for absence.
  (Note: that's 3 presence-only; sanctions get the hardest poll cadence instead.)

## How it surfaces

- **Engine output:** `overdue` / `statutory_deadline` ride the same dispatch
  stream as change alerts, tagged by `signal_type`.
- **Site:** a distinct flag from the oxblood `§` ambiguity flag — absence is a
  different category of signal and shouldn't dilute the ambiguity mark. It does,
  though, literally deliver the supporting line: *"when the rules move, we're
  already telling you"* — including when they conspicuously don't.

## Open questions (for Stephen)

1. **Customer threshold.** Is a single working-day FR gap worth a customer
   dispatch, or only N-day / multi-source silence? (Avoid alarm fatigue.)
2. **§232/§301 clock data.** Where does the engine learn of *open* investigations
   and their initiation dates — scraped from FR notices, or a hand-maintained
   register to start?
3. **pipeline_suspect routing.** Ops channel only, or also a quiet "data health"
   line on the internal dashboard?
4. **Calendar feeds.** Confirm sources for US federal holidays, EU institution
   holidays, UK bank holidays, and the Congress/Parliament sitting calendars.
