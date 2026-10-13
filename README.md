# Tehnomix - Google Ads product feed

`tehnomix-google-ads-feed.csv` is an unmodified copy of https://www.tehnomix.bg/media/feed/google-new.csv
(columns: ID, Item title, Final URL, Image URL, item description, Item category, Price, Sale price).
The source is already in Google Ads custom-feed format, so there is no converter step.

Stable raw URL for Google Sheets (`IMPORTDATA`), Merchant Center or Google Ads scheduled fetch:

    https://raw.githubusercontent.com/martingalabov-jpg/tehnomix-google-ads-feed/main/tehnomix-google-ads-feed.csv

Refreshed daily by `refresh.ps1`, run from Windows Task Scheduler ("Tehnomix Google Ads feed refresh", 09:40) on Martin's PC.
It cannot run in GitHub Actions: Cloudflare returns 403 to GitHub's datacenter IPs even with a browser User-Agent.
From the office connection a browser User-Agent passes (curl's default UA gets 403).
The run aborts without publishing if the download is not the feed CSV or yields fewer than 3000 products.
Log: `refresh.log` next to the script (not committed). Sibling repo: `tehnomix-feed` (OpenAI Ads feed, 09:30).
