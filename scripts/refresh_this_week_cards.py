"""Interactive refresh of the "What changed this week" cards in index.html.

Fetches recent trade-relevant ingests from the Railway-hosted Gubernis
engine, prints a numbered candidate list, lets you pick three, prompts
for a custom summary line per pick, and rewrites the .featured-grid
block in index.html in place.

Runs locally on the user's machine — NOT as part of the deploy
workflow. The whole point is the editorial pick step.

Usage:
    python3 scripts/refresh_this_week_cards.py
    python3 scripts/refresh_this_week_cards.py --limit 20 --days 14

After it finishes, review and ship:
    git diff index.html
    git commit -am "this-week: refresh cards" && git push
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_ENDPOINT = (
    "https://pragticality-production.up.railway.app/gubernis/recent-changes"
)

# Pretty-print map from raw source_id to short jurisdiction-and-issuer label.
SOURCE_LABELS = {
    "federal_register":          "US FR",
    "ofac_sdn":                  "US OFAC",
    "ustr_section_301":          "US USTR",
    "bis_section_232":           "US BIS",
    "congress_bills":            "US Congress",
    "hmrc_trade_tariff_news":    "UK HMRC",
    "gov_uk_publications":       "UK gov.uk",
    "uk_parliament_bills":       "UK Parliament",
    "eu_sanctions_consolidated": "EU Sanctions",
    "eur_lex":                   "EU EUR-Lex",
    "eu_legislative_train":      "EU LegTrain",
}

# Map source_id to which two-letter jurisdiction tag goes on the card.
JURISDICTION_TAGS = {
    "federal_register": "US", "ofac_sdn": "US", "ustr_section_301": "US",
    "bis_section_232": "US", "congress_bills": "US",
    "hmrc_trade_tariff_news": "UK", "gov_uk_publications": "UK",
    "uk_parliament_bills": "UK",
    "eu_sanctions_consolidated": "EU", "eur_lex": "EU",
    "eu_legislative_train": "EU",
}

# Light topic inference based on title keywords. The picker uses this for
# the second card-tag pill. Order matters — first match wins.
TOPIC_RULES = [
    (re.compile(r"\bsanctions?\b|\bembargo\b|\bSDN\b|\bCFSP\b", re.I), "sanctions"),
    (re.compile(r"\banti.?dumping\b|\bdumping\b|\bsubsidy\b|\bcountervailing\b", re.I), "trade defence"),
    (re.compile(r"\bSection 301\b|\bSection 232\b|\bSection 201\b", re.I), "trade defence"),
    (re.compile(r"\btariff\b|\bcustoms\b|\bduty\b|\bquota\b", re.I), "tariff"),
    (re.compile(r"\bexport control\b|\bECRA\b|\bITAR\b|\bEAR\b", re.I), "export control"),
    (re.compile(r"\bimport\b|\bexport\b|\borigin\b", re.I), "trade"),
    (re.compile(r"\bsteel\b|\baluminium\b|\baluminum\b", re.I), "metals"),
    (re.compile(r"\bpharmaceutical\b|\bmedical\b", re.I), "pharma"),
    (re.compile(r"\bsemiconductor\b|\baircraft\b|\bUAV\b|\bunmanned\b", re.I), "tech"),
]


def fetch_candidates(endpoint: str, limit: int, days: int, timeout: float = 15.0) -> list[dict]:
    """Fetch via curl rather than urllib — macOS Python's urllib often
    can't verify SSL (no CA bundle wired up); curl has a proper one."""
    url = f"{endpoint}?limit={limit}&days={days}&include_noisy=false"
    try:
        result = subprocess.run(
            ["curl", "-sf", "-m", str(int(timeout)),
             "-A", "refresh_this_week_cards.py",
             url],
            capture_output=True, text=True, check=True,
        )
        payload = json.loads(result.stdout)
    except FileNotFoundError:
        print("curl not found in PATH; install curl or run on a machine that has it.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"curl failed against {url}:\n  stderr: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Response wasn't JSON: {e}\n{result.stdout[:200]}", file=sys.stderr)
        sys.exit(1)
    return payload.get("items", [])


def format_date(item: dict) -> str:
    raw = item.get("publication_date") or item.get("fetched_at") or ""
    if not raw:
        return "????-??-??"
    try:
        d = datetime.fromisoformat(raw.replace("Z", "").split(".")[0])
        return d.strftime("%d %b %Y")
    except ValueError:
        return raw[:10]


def topic_for(title: str) -> str:
    for pat, tag in TOPIC_RULES:
        if pat.search(title or ""):
            return tag
    return "trade"


def render_candidates(items: list[dict]) -> None:
    print()
    print("Recent trade-relevant changes — newest first:\n")
    for i, item in enumerate(items, 1):
        date = format_date(item)
        source = SOURCE_LABELS.get(item["source_id"], item["source_id"])
        flags = []
        if item.get("ambiguity"):
            flags.append("AMBIG")
        if item.get("severity"):
            flags.append(item["severity"].upper())
        if item.get("version_number", 1) > 1:
            flags.append(f"v{item['version_number']}")
        flag_str = (" " + " ".join(flags)) if flags else ""
        title = (item.get("title") or "")[:90]
        print(f"  {i:2d}) [{source:14s}] {date}{flag_str}")
        print(f"       {item['identity']}")
        print(f"       {title}")
        print()


def pick_three(items: list[dict]) -> list[dict]:
    while True:
        raw = input("Pick 3 by number (space-separated, e.g. \"1 3 5\"):\n> ").strip()
        try:
            nums = [int(x) for x in raw.split()]
        except ValueError:
            print("Please enter 3 numbers separated by spaces.")
            continue
        if len(nums) != 3:
            print(f"Need exactly 3 picks; got {len(nums)}.")
            continue
        if any(n < 1 or n > len(items) for n in nums):
            print(f"Numbers must be between 1 and {len(items)}.")
            continue
        return [items[n - 1] for n in nums]


def prompt_summary(item: dict, label: str) -> str:
    print()
    print(f"=== {label} ===")
    print(f"  {item['identity']}")
    print(f"  {(item.get('title') or '')[:120]}")
    raw = input(
        "Summary (one sentence on why this matters; "
        "Enter to leave [WRITE SUMMARY] placeholder):\n> "
    ).strip()
    return raw or "[WRITE SUMMARY]"


def build_card_html(item: dict, summary: str) -> str:
    date = format_date(item)
    source = SOURCE_LABELS.get(item["source_id"], item["source_id"])
    jurisdiction = JURISDICTION_TAGS.get(item["source_id"], "")
    topic = topic_for(item.get("title") or "")
    severity = item.get("severity") or "substantive"

    is_ambig = item.get("ambiguity", False)
    article_class = "card ambiguous" if is_ambig else "card"
    sev_tag = f"{severity} · grey edge" if is_ambig else severity

    # Encode &, <, > in title/summary for HTML safety (light pass).
    title_safe = (item.get("title") or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    summary_safe = summary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    identity_safe = (item.get("identity") or "").replace("&", "&amp;")

    parts = [f'      <article class="{article_class}">']
    if is_ambig:
        parts.append('        <span class="watch-flag">§ ambiguity flag</span>')
    parts += [
        f'        <div class="ts">{date} · {source}</div>',
        f'        <div class="id">{identity_safe}</div>',
        f'        <h3 class="card-title">{title_safe}</h3>',
        f'        <p class="card-summary">{summary_safe}</p>',
        '        <div class="card-tags">',
        f'          <span class="tag">{jurisdiction}</span>' if jurisdiction else "",
        f'          <span class="tag">{topic}</span>',
        f'          <span class="tag sev">{sev_tag}</span>',
        '        </div>',
        '      </article>',
    ]
    return "\n".join(p for p in parts if p)


def patch_index_html(path: Path, cards_html: list[str]) -> None:
    start_marker = "<!-- featured-cards: start (managed by scripts/refresh_this_week_cards.py) -->"
    end_marker = "<!-- featured-cards: end -->"

    html = path.read_text(encoding="utf-8")
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx + 1 if start_idx >= 0 else 0)
    if start_idx < 0 or end_idx < 0:
        print(
            "Could not find the featured-cards start/end markers in index.html.\n"
            "Looking for:\n"
            f"  {start_marker}\n"
            f"  {end_marker}\n"
            "Make sure those exist around the .featured-grid contents.",
            file=sys.stderr,
        )
        sys.exit(2)

    new_inner = "\n\n" + "\n\n".join(cards_html) + "\n\n      "
    new_html = (
        html[: start_idx + len(start_marker)]
        + new_inner
        + html[end_idx:]
    )
    path.write_text(new_html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Pick 3 recent changes and rewrite the featured-cards block.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--limit", type=int, default=10, help="How many candidates to show")
    parser.add_argument("--days",  type=int, default=7,  help="How many days back to scan")
    parser.add_argument("--html",  default="index.html", help="Path to index.html (default: cwd)")
    args = parser.parse_args()

    items = fetch_candidates(args.endpoint, limit=args.limit, days=args.days)
    if not items:
        print("No candidates returned. Try widening --days or --limit.", file=sys.stderr)
        return 1

    render_candidates(items)
    picks = pick_three(items)

    cards = []
    for idx, item in enumerate(picks, 1):
        summary = prompt_summary(item, label=f"Card {idx} summary")
        cards.append(build_card_html(item, summary))

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"index.html not found at {html_path.resolve()}", file=sys.stderr)
        return 1
    patch_index_html(html_path, cards)

    print()
    print(f"Updated {html_path}.")
    print("Review:  git diff index.html")
    print("Ship:    git commit -am 'this-week: refresh cards' && git push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
