"""Tehnomix google-new.csv -> Google Ads feed, keeping only products priced over MIN_PRICE EUR.
Price tested = Sale price when it is lower than Price, otherwise Price (what the shopper pays).
Adds 'Formatted price' / 'Formatted sale price' (same display style as the JTclima feed) and leaves
Sale price empty when the product is not actually discounted.
Usage: python3 build_google_ads_feed.py <google-new.csv> <out.csv>"""
import csv, sys

MIN_PRICE = 50.0
SRC, OUT = sys.argv[1], sys.argv[2]
EURO, NBSP = chr(0x20AC), chr(0xA0)


def money(s):
    n, cur = s.split()
    return float(n), cur


def fmt(v):
    """Euro sign in front, no cents when whole, nbsp thousands, comma decimal: EUR1 779 / EUR659,50."""
    dec = 0 if round(v * 100) % 100 == 0 else 2
    return EURO + "{:,.{p}f}".format(v, p=dec).replace(",", NBSP).replace(".", ",")


with open(SRC, encoding="utf-8-sig", newline="") as f:
    rd = csv.DictReader(f)
    header = rd.fieldnames
    src = list(rd)
sale_col = header.index("Sale price")

rows, no_image = [], 0
for r in src:
    if not r["Image URL"].strip() or "no_selection" in r["Image URL"]:
        no_image += 1
        continue
    p, cur = money(r["Price"])
    if cur != "EUR":
        raise SystemExit("Unexpected currency %s for %s - output NOT written" % (cur, r["ID"]))
    s = money(r["Sale price"])[0] if r["Sale price"].strip() else 0
    on_sale = 0 < s < p
    if (s if on_sale else p) > MIN_PRICE:
        row = [r[h] for h in header]
        if not on_sale:
            row[sale_col] = ""
        rows.append(row + [fmt(p), fmt(s) if on_sale else ""])

if len(rows) < 1500:
    raise SystemExit("Only %d rows - output NOT written" % len(rows))
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header + ["Formatted price", "Formatted sale price"])
    w.writerows(rows)
print("%d in, %d out, %d dropped (%d no image, rest <= %g EUR)" % (
    len(src), len(rows), len(src) - len(rows), no_image, MIN_PRICE))
