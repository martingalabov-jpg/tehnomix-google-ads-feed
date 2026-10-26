# Tehnomix - Google Ads product feed

`tehnomix-google-ads-feed.csv` is https://www.tehnomix.bg/media/feed/google-new.csv filtered to products over 50 EUR
by `build_google_ads_feed.py` (columns unchanged: ID, Item title, Final URL, Image URL, item description, Item category, Price, Sale price).
The price tested is the Sale price when it is lower than Price, otherwise Price (what the shopper pays). Change `MIN_PRICE` in the script to move the threshold.
Products with no image (empty or `no_selection` placeholder Image URL) are dropped.
`Formatted price` / `Formatted sale price` are added in the JTclima style (euro sign first, no cents on whole prices, e.g. `€1 779`, `€659,50`); `Sale price` and `Formatted sale price` are empty unless the product is really discounted.

    python3 build_google_ads_feed.py <google-new.csv> <out.csv>

Stable raw URL for Google Sheets (`IMPORTDATA`), Merchant Center or Google Ads scheduled fetch:

    https://raw.githubusercontent.com/martingalabov-jpg/tehnomix-google-ads-feed/main/tehnomix-google-ads-feed.csv

Refreshed every 6 hours by the GitHub Actions workflow `.github/workflows/refresh-feed.yml` (cron 00:00, 06:00, 12:00 and 18:00 UTC; GitHub often starts scheduled runs late).
Cloudflare stopped blocking GitHub's runners on 2026-10-14; before that the refresh ran on Martin's PC. `refresh.ps1` is that old Task Scheduler version, kept as a fallback (its task is disabled; `git pull` before re-enabling).
The run aborts without publishing if the download is not the feed CSV, the source has fewer than 3000 products, or fewer than 1500 remain after filtering.
Sibling repo: `tehnomix-feed` (OpenAI Ads feed).

## PMax category feeds (`pmax/`)

One feed per category asset group in `Tehnomix -- General-Pmax`, split from `tehnomix-google-ads-feed.csv` by
`build_pmax_category_feeds.py` in the same run, so they refresh every 6 hours too and carry the same columns and rules
(over 50 EUR, has an image). The file name is the asset group's `utm_content` tag.

| Asset group | Feed |
|---|---|
| Tehnomix -- Кухненски уреди | `pmax/kuhnenski-uredi.csv` |
| Tehnomix -- Роботи прахосмукачки | `pmax/roboti-prahosmukachki.csv` |
| Tehnomix -- Безжични прахосмукачки | `pmax/bezzhichni-prahosmukachki.csv` |
| Tehnomix -- Красота и грижа | `pmax/krasota-i-grizha.csv` |
| Tehnomix -- Перални и сушилни | `pmax/peralni-i-sushilni.csv` |
| Tehnomix -- Хладилници | `pmax/hladilnici.csv` |
| Tehnomix -- Уреди за вграждане | `pmax/uredi-za-vgrazhdane.csv` |
| Tehnomix -- Климатици | `pmax/klimatici.csv` |
| Tehnomix -- Пречистватели за въздух | `pmax/prechistvateli.csv` |
| Tehnomix -- Кафемашини | `pmax/kafemashini.csv` |
| Tehnomix -- Телевизори (Tehnomix -- Pmax TV) | `pmax/televizori.csv` |

Raw URL: `https://raw.githubusercontent.com/martingalabov-jpg/tehnomix-google-ads-feed/main/pmax/<file>.csv`

A product is placed by its `Item category` path. Products the site parks in promo buckets (Liebherr 2+8, Miele 25 years,
"Shark & Ninja", "Нови продукти" ...) are placed by their title instead, with built-in appliances going to
Уреди за вграждане. Accessories, consumables, wine coolers, stain cleaners, window robots and mobile ACs never go in.
A category feed that would drop below 5 products is not overwritten, so the last good file stays.

### Page feeds (`pmax-pages/`)

The same split as Google Ads **page feeds**: exactly two columns, `Page URL` and `Custom label` (the slug with
underscores, e.g. `kuhnenski_uredi`). The asset group's category page comes first, then every product page.
In Google Ads (Tools ▸ Business data) each `20261026-<Category>` page feed has an HTTPS schedule pointing at
`https://raw.githubusercontent.com/martingalabov-jpg/tehnomix-google-ads-feed/main/pmax-pages/<slug>.csv`.
Do not upload the `pmax/` product files into a page feed - they have no `Page URL` header and every row fails.
