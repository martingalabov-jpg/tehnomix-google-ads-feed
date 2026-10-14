"""Tehnomix google-new.csv -> Google Ads feed, keeping only products priced over MIN_PRICE EUR.
Price tested = Sale price when it is lower than Price, otherwise Price (what the shopper pays).
Usage: python3 build_google_ads_feed.py <google-new.csv> <out.csv>"""
import csv, sys

MIN_PRICE = 50.0
SRC, OUT = sys.argv[1], sys.argv[2]


def money(s):
    n, cur = s.split()
    return float(n), cur


with open(SRC, encoding="utf-8-sig", newline="") as f:
    rd = csv.DictReader(f)
    header = rd.fieldnames
    src = list(rd)

rows = []
for r in src:
    p, cur = money(r["Price"])
    if cur != "EUR":
        raise SystemExit("Unexpected currency %s for %s - output NOT written" % (cur, r["ID"]))
    s = money(r["Sale price"])[0] if r["Sale price"].strip() else 0
    if (s if 0 < s < p else p) > MIN_PRICE:
        rows.append([r[h] for h in header])

if len(rows) < 1500:
    raise SystemExit("Only %d rows - output NOT written" % len(rows))
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)
print("%d in, %d out, %d dropped (<= %g EUR)" % (len(src), len(rows), len(src) - len(rows), MIN_PRICE))
