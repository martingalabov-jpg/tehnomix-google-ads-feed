# Tehnomix - Google Ads product feed

`tehnomix-google-ads-feed.csv` is https://www.tehnomix.bg/media/feed/google-new.csv filtered to products over 50 EUR
by `build_google_ads_feed.py` (columns unchanged: ID, Item title, Final URL, Image URL, item description, Item category, Price, Sale price).
The price tested is the Sale price when it is lower than Price, otherwise Price (what the shopper pays). Change `MIN_PRICE` in the script to move the threshold.
Products with no image (empty or `no_selection` placeholder Image URL) are dropped.

    python3 build_google_ads_feed.py <google-new.csv> <out.csv>

Stable raw URL for Google Sheets (`IMPORTDATA`), Merchant Center or Google Ads scheduled fetch:

    https://raw.githubusercontent.com/martingalabov-jpg/tehnomix-google-ads-feed/main/tehnomix-google-ads-feed.csv

Refreshed daily by `refresh.ps1`, run from Windows Task Scheduler ("Tehnomix Google Ads feed refresh", 09:00) on Martin's PC.
It cannot run in GitHub Actions: Cloudflare returns 403 to GitHub's datacenter IPs even with a browser User-Agent.
From the office connection a browser User-Agent passes (curl's default UA gets 403).
The run aborts without publishing if the download is not the feed CSV or yields fewer than 3000 products.
Log: `refresh.log` next to the script (not committed). Sibling repo: `tehnomix-feed` (OpenAI Ads feed, 09:30).
