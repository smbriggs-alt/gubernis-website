# Session handoff — Document Watch, source cadence, deploy cron

**Read this first if you're picking up branch `claude/gubernis-website-jobs-review-VY4Sr`.**
Last updated: 2026-05-26.

This is the "start here" briefing for the engine-spec work staged in this
folder, plus the unmerged deploy change that rode along on the same branch.
The two spec files beside it (`expected_cadence.yaml`, `document-watch.md`)
are the substance; this file is the map and the backlog.

---

## Where things stand (branch state)

`main` HEAD is `4601a41` — the Watch ledger already carries its honest framing
(site snapshot + timestamp + daily cadence). This branch is **two commits ahead
of `main`, neither merged**:

| Commit | What | Ships to site? | Merged? |
|---|---|---|---|
| `d1280a5` | Daily cron in `.github/workflows/deploy.yml` so the Watch ledger refreshes without a manual push | Yes (workflow) | No |
| `159e396` | `engine-spec/` — `expected_cadence.yaml` + `document-watch.md` | **No** (engine-bound; deploy only stages `index.html`/`styles.css` + privacy/terms/about/samples) | No |

No PR has been opened for either. Nothing here is live.

---

## What this work is

Document Watch is the mirror half of the engine's existing change-alert: the
engine watches for *change*; this adds watching for *expected-but-absent*. For
a regulatory watch, a working-day publisher going quiet is itself a signal — a
delayed rule, a shutdown, a missed statutory deadline. Per the steer, it is
**not a separate feature**: absence folds into the same alert stream as change,
as additional `signal_type`s.

### Decisions locked this session
- **One signal stream.** Change and absence both emit a single `watch_signal`,
  differentiated by `signal_type`: `change` / `overdue` / `statutory_deadline`
  / `pipeline_suspect`. Document Watch is wired *into* the change-alert flow,
  not bolted beside it.
- **Two timestamps per source** (`last_successful_fetch` vs `last_new_document`)
  — the load-bearing distinction that stops "the source released nothing" being
  confused with "our scraper broke." The latter routes to ops as
  `pipeline_suspect`, never to the customer.
- **Cadence drives both poller and detector.** `expected_cadence.yaml` is the
  single source of truth for poll frequency *and* the expected-release window.
- **tz-aware local times**, resolved at runtime — not baked to UTC (US/EU/UK
  DST transitions don't align and would drift every window twice a year).
- **Scope across the eleven sources:** 7 are absence-capable (calendar/periodic);
  §232 and §301 get the *statutory-clock* analog (270+90-day and 4-yr review
  windows); the sanctions + HMRC feeds are presence-only (poll hardest, never
  flag silence).
- **Staging location.** Specs live here for versioning while we iterate; the
  clean home is the Gubernis engine (`pragticality`, `gubernis-poc`).

---

## Backlog (ordered)

### Needs Stephen's call before build
1. **Customer threshold.** Does a single missed working day warrant a customer
   dispatch, or only N-day / multi-source silence? (Alarm-fatigue tradeoff.)
2. **§232/§301 investigation feed.** Where does the engine learn of *open*
   investigations + their initiation dates — scraped from FR notices, or a
   hand-kept register to start?
3. **`pipeline_suspect` routing.** Ops channel only, or also a quiet data-health
   line on the internal dashboard?
4. **Calendar feeds.** Confirm sources for US federal holidays, EU institution
   holidays, UK bank holidays, and the Congress/Parliament sitting calendars.

### Engineering next steps
5. **Relocate `engine-spec/` into `pragticality` (`gubernis-poc`)** and wire
   `expected_cadence.yaml` to the live poller. Best done in a session opened on
   that repo so the spec can be checked against the current polling code.
6. **Implement the daily absence evaluator** per `document-watch.md` (two-
   timestamp logic + the `pipeline_suspect` guard).
7. **Site surfacing.** Decide the visual treatment for an absence/overdue flag —
   it must be *distinct* from the oxblood `§` ambiguity flag so it doesn't
   dilute the ambiguity mark. (Deferred until the engine emits the signal.)

### Loose ends on this branch
8. **Decide the fate of `d1280a5` (deploy cron).** Either fold it into a PR to
   `main` or drop it — it's currently stranded on this branch.
9. **Decide whether `engine-spec/` belongs in this repo at all**, or should be
   moved out wholesale once pragticality is ready (it's the boundary smudge
   flagged when it was staged — acceptable as temporary, not as a home).

---

## Files
- `expected_cadence.yaml` — per-source cadence for all 11 sources (validated).
- `document-watch.md` — the absence-detection design + unified signal model.
- this file — handoff / backlog.
