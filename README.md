# Tehnomix - Google Ads product feed

`tehnomix-google-ads-feed.csv` is https://www.tehnomix.bg/media/feed/google-new.csv filtered to products over 50 EUR
by `build_google_ads_feed.py` (columns unchanged: ID, Item title, Final URL, Image URL, item description, Item category, Price, Sale price).
The price tested is the Sale price when it is lower than Price, otherwise Price (what the shopper pays). Change `MIN_PRICE` in the script to move the threshold.
Products with no image (empty or `no_selection` placeholder Image URL) are dropped.

    python3 build_google_ads_feed.py <google-new.csv> <out.csv>

Stable raw URL for Google Sheets (`IMPORTDATA`), Merchant Center or Google Ads scheduled fetch:

    https://raw.githubusercontent.com/martingalabov-jpg/tehnomix-google-ads-feed/main/tehnomix-google-ads-feed.csv

Refreshed every 6 hours by the GitHub Actions workflow `.github/workflows/refresh-feed.yml` (cron 00:00, 06:00, 12:00 and 18:00 UTC; GitHub often starts scheduled runs late).
Cloudflare stopped blocking GitHub's runners on 2026-10-14; before that the refresh ran on Martin's PC. `refresh.ps1` is that old Task Scheduler version, kept as a fallback (its task is disabled; `git pull` before re-enabling).
The run aborts without publishing if the download is not the feed CSV, the source has fewer than 3000 products, or fewer than 1500 remain after filtering.
Sibling repo: `tehnomix-feed` (OpenAI Ads feed).
