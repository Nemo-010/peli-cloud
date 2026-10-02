#!/usr/bin/env python3
"""check-strip-selftest.py - prove the claim-stripper, and prove the proof.

The catalogue reads a vendor's own words out of fetched HTML to decide two
things: whether a page can be read at all, and whether a provider's page states
an idle-billing policy. Both are only as good as the function that turns HTML
into text. This repository did not have one of its own, so it had no way to see
the class of defect that `talaria0101/peli-cloud` found in its stripper on
2026-10-02: stripping every `<script>` discarded a JSON-LD pricing block, the
page looked empty, and the verdict became the confident false statement "no
price rendered in the HTML (client-side)".

This is that reader, and its self-test.

Usage:
  python3 tools/check-strip-selftest.py             # run the known-answer cases
  python3 tools/check-strip-selftest.py --naive     # run them against the naive
                                                    # stripper, and expect failures
Exit 0 when every case holds, 1 when one does not.
"""
import html
import re
import sys

# A <script> with a type is data the vendor published on purpose; without one it
# is code, and code has no text a reader would see. JSON-LD is the case that
# matters because schema.org pricing blocks carry the very sentences a pricing
# page is being read for.
JSONLD = re.compile(
    r'<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.S | re.I)


def strip_markup(body, naive=False):
    """Visible text, with executable scripts and styles removed.

    JSON-LD is extracted first and appended, so a page that renders its prices
    inside a schema.org block is not mistaken for a client-side shell.
    `naive=True` reproduces the one-liner this replaced, which is what the
    --naive mode needs to demonstrate that the cases can fail.
    """
    if naive:
        t = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
        t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        return re.sub(r"\s+", " ", html.unescape(t))

    kept = []

    def _keep_jsonld(m):
        kept.append(m.group(1))
        return " "

    t = JSONLD.sub(_keep_jsonld, body)
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", html.unescape(t))
    for k in kept:
        t += " " + re.sub(r"\s+", " ", html.unescape(k))
    return t


# A page whose visible text carries no money figure is called unreadable. This
# is the predicate both this repository and the sibling use; the defect was that
# a readable page fell through it once the JSON-LD had been thrown away.
MONEY = re.compile(r"\$\s?\d|\d\s?")


def readable(body, naive=False):
    return bool(MONEY.search(strip_markup(body, naive=naive)))


# (id, html, must the stripped text be readable?)
CASES = [
    ("json-ld price survives",
     '<html><body><script type="application/ld+json">'
     '{"@type":"Product","offers":{"price":"499","priceCurrency":"USD",'
     '"description":"Dedicated stack. Starting at $499/month."}}'
     '</script></body></html>', True),
    ("ordinary script is dropped",
     '<html><body><script>var price = "$999";</script>'
     '<p>$10 per month</p></body></html>', True),
    ("genuinely empty page stays empty",
     '<html><body><div id="root"></div></body></html>', False),
    ("json-ld below the fold is kept",
     '<html><body><div id="root">Pricing</div>'
     '<script type="application/ld+json">{"name":"X","offers":"$0.009/hour"}</script>'
     '</body></html>', True),
    ("json-ld with attributes order reversed is kept",
     '<html><body><script data-x="1" type="application/ld+json">'
     '{"offers":"$20/month"}</script></body></html>', True),
    ("a script with no type is still dropped even if it quotes a price",
     '<html><body><script>document.write("$1,234")</script>'
     '<div id="root"></div></body></html>', False),
    ("escaped entities in the visible text are decoded",
     '<html><body><p>$5 &amp; up</p></body></html>', True),
    ("a comment carrying a price is not evidence",
     '<html><body><!-- $999/month --><div id="root"></div></body></html>', False),
]


def main():
    naive = "--naive" in sys.argv
    mode = "naive (pre-fix)" if naive else "JSON-LD aware"
    bad = []
    for cid, src, want in CASES:
        got = readable(src, naive=naive)
        mark = "ok  " if got == want else "FAIL"
        print(f"{mark} {cid}: readable={got} want={want}")
        if got != want:
            bad.append(cid)
    print(f"\nstripper={mode} cases={len(CASES)} failed={len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
