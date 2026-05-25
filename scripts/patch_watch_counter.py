"""Patch the Watch ledger in dist/index.html with live engine numbers.

Run during the GitHub Actions deploy workflow, after the index.html has
been copied into dist/ but before lftp uploads it to IONOS. Fetches
the public /gubernis/watch-counter JSON from the Railway-hosted FastAPI
app and substitutes the ledger values in the staged HTML.

Fail-soft posture: if the endpoint is unreachable, returns non-JSON,
or any field is missing, this script prints a warning and exits 0
so the deploy proceeds with whatever numbers are already in the file.
A stale-but-deployed site is better than a failed deploy.

Usage:
    python3 scripts/patch_watch_counter.py \\
        --endpoint https://pragticality-production.up.railway.app/gubernis/watch-counter \\
        --html dist/index.html
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request


def _format_as_of(ts: str) -> str:
    """Format ISO-8601 timestamp from the endpoint as '25 May 2026 15:14 UTC'
    for display. The endpoint's as_of is the moment the response was generated
    (effectively deploy time). Falls back to first 16 chars if parsing fails."""
    from datetime import datetime
    try:
        clean = ts.replace("Z", "").split(".")[0]
        dt = datetime.fromisoformat(clean)
        return dt.strftime("%d %b %Y %H:%M UTC")
    except (ValueError, AttributeError):
        return (ts or "")[:16] or "—"


# Map the JSON field returned by the endpoint to the data-count attribute
# value in index.html, plus a formatter for the displayed value. Keep this
# in sync with the ledger-cell + ledger-label structures in index.html.
FIELD_MAP = [
    ("changes_today",       "changes-today",       lambda n: str(n)),
    ("changes_7d",          "changes-7d",          lambda n: str(n)),
    ("documents_tracked",   "documents-tracked",   lambda n: str(n)),
    ("sources_watched",     "sources",             lambda n: str(n)),
    ("ambiguity_flags_7d",  "ambiguity-7d",        lambda n: f"&sect; {n}"),
    ("as_of",               "as-of",               _format_as_of),
]


def fetch_counter(endpoint: str, timeout: float = 10.0) -> dict | None:
    """GET the endpoint, return the parsed JSON dict, or None on any failure."""
    try:
        req = urllib.request.Request(
            endpoint,
            headers={"User-Agent": "gubernis-website-deploy (curl-equivalent)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
        print(f"watch-counter fetch failed: {type(e).__name__}: {e}", file=sys.stderr)
        return None
    return payload


def patch_html(html: str, counter: dict) -> tuple[str, list[str]]:
    """Substitute values into elements carrying a `data-count` attribute.
    Returns (new_html, notes). Matches either `</div>` or `</span>` so the
    same machinery can patch ledger-cell numbers and the ledger-label
    timestamp (which is in a <span>)."""
    notes: list[str] = []
    out = html
    for json_field, attr_value, fmt in FIELD_MAP:
        if json_field not in counter:
            notes.append(f"  - {json_field}: missing from endpoint payload, left as-is")
            continue
        new_text = fmt(counter[json_field])
        pattern = rf'(data-count="{re.escape(attr_value)}"[^>]*>)([^<]*)(</[a-z]+>)'
        replacement = rf"\g<1>{new_text}\g<3>"
        new_out, count = re.subn(pattern, replacement, out)
        if count == 0:
            notes.append(f"  - data-count=\"{attr_value}\" marker not found in HTML")
        else:
            notes.append(f"  - {attr_value} -> {new_text}")
            out = new_out
    return out, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch Watch ledger in deploy-time HTML.")
    parser.add_argument("--endpoint", required=True,
                        help="URL of /gubernis/watch-counter on the Railway app")
    parser.add_argument("--html", required=True,
                        help="Path to the staged index.html to patch in place")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    counter = fetch_counter(args.endpoint, timeout=args.timeout)
    if counter is None:
        print("Proceeding with deploy using static numbers in repo.", file=sys.stderr)
        return 0  # fail-soft

    print(f"Fetched watch-counter (as_of={counter.get('as_of', '?')}):")

    with open(args.html, "r", encoding="utf-8") as f:
        html = f.read()
    new_html, notes = patch_html(html, counter)
    for n in notes:
        print(n)
    if new_html == html:
        print("No substitutions applied; HTML unchanged.")
        return 0

    with open(args.html, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Patched {args.html}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
