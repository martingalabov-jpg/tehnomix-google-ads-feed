"""Split the Google Ads feed into one feed per PMax category asset group (Tehnomix -- General-Pmax).
Input is the already-filtered feed (tehnomix-google-ads-feed.csv: > 50 EUR, has image, formatted prices),
so every category feed keeps the same columns and rules. Output: pmax/<slug>.csv, slug = the asset group's
utm_content tag.

A product goes to a group by its 'Item category' path. Products parked in promo buckets (Liebherr 2+8,
Miele 25 years, "Shark & Ninja", "Нови продукти" ...) carry no real category there, so those are placed
by their title instead. Accessories, consumables, wine coolers, stain cleaners and window robots never go in.
Usage: python3 build_pmax_category_feeds.py <tehnomix-google-ads-feed.csv> <out_dir>"""
import csv, os, re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
MIN_ROWS = 5   # a category feed that would drop below this is not overwritten (keeps the last good one)

K = 'Малки електроуреди > Уреди за кухня > '
P = 'Малки електроуреди > Прахосмукачки > '
B = 'Малки електроуреди > Грижа за тялото > '
V = 'Уреди за вграждане > '
GROUPS = [   # slug, category prefixes, title regex for promo buckets
    ('kuhnenski-uredi',
     [K + x for x in ('Фритюрници', 'Уреди за готвене', 'Грилове и скари', 'Блендери', 'Кухненски роботи', 'Миксери',
                      'Пасатори', 'Сокоизстисквачки', 'Цитрус преси', 'Кухненски чопъри', 'Хлебопекарни',
                      'Сандвич мейкъри', 'Тостери', 'Електрически кани', 'Месомелачки', 'Ледогенератори',
                      'Уреди за вакуумиране', 'Микровълнови фурни')],
     r'фритюрник|мултикукър|грил|блендер|уред за сладолед|кухненски робот|миксер|тостер|сокоизстисквачка'),
    ('roboti-prahosmukachki', [P + 'Прахосмукачки робот'], r'прахосмукачка робот|робот прахосмукачка'),
    ('bezzhichni-prahosmukachki', [P + 'Вертикални прахосмукачки'], r'безжична прахосмукачка|вертикална прахосмукачка'),
    ('krasota-i-grizha', [B + x for x in ('Перфектен стил', 'Сешоари', 'Маши за коса', 'Преси за коса')],
     r'сешоар|маша за коса|стилизатор|преса за коса'),
    ('peralni-i-sushilni',
     ['Едра бяла техника > Перални > Перални с предно зареждане', 'Едра бяла техника > Перални > Перални със сушилня',
      'Едра бяла техника > Сушилни'],
     r'^(пералня|сушилня)'),
    ('hladilnici',
     ['Едра бяла техника > Хладилници > Хладилници с фризер', 'Едра бяла техника > Хладилници > Хладилници Side by Side',
      'Едра бяла техника > Хладилници > Хладилници с една врата', 'Едра бяла техника > Хладилници > Хладилници с горна камера'],
     r'^хладилник'),
    ('uredi-za-vgrazhdane',
     [V + x for x in ('Хладилници за вграждане > Хладилници за вграждане', 'Фурни за вграждане > Стандартни',
                      'Фурни за вграждане > Фурни с пиролиза', 'Фурни за вграждане > Комбинирани', 'Фурни за вграждане > Парови',
                      'Фурни за вграждане > Микровълнови', 'Съдомиялни за вграждане', 'Плотове за вграждане > Индукционни',
                      'Плотове за вграждане > Стъклокерамични', 'Плотове за вграждане > Газови', 'Плотове за вграждане > Комбинирани',
                      'Абсорбатори за вграждане', 'Фризери за вграждане', 'Перални за вграждане', 'Кафемашини за вграждане')],
     r'за вграждане'),
    ('klimatici', ['Климатизация/Отопление > Климатици'], r'климатик'),
    ('prechistvateli',
     ['Климатизация/Отопление > Пречистватели и Овлажнители', 'Климатизация/Отопление > Грижа за въздуха с Dyson > Пречистватели'],
     r'пречиствател|овлажнител'),
    ('kafemashini',
     ['Малки електроуреди > Кафемашини > ' + x for x in ('Кафеавтомати', 'Кафемашини еспресо', 'Кафемашини с капсули', 'Шварц кафемашини')],
     r'кафемашина|кафеавтомат'),
]
PROMO = re.compile(r'гаранция|Shark & Ninja|Нови продукти|Последни бройки|Специални оферти|Philips I Disney|Перални и сушилни BOSCH|FreshCare|MIELE пералня')
NEVER = re.compile(r'аксесоар|консуматив|филтър|препарат|виноохладител|витрин|съдове|торбичк|петна|парочистачка|мобилен климатик|за прозорци', re.I)
BUILT_IN = re.compile(r'за вграждане', re.I)

with open(SRC, encoding='utf-8-sig', newline='') as f:
    rd = csv.DictReader(f)
    header, rows = rd.fieldnames, list(rd)

out = {g[0]: [] for g in GROUPS}
for r in rows:
    cat, title = r['Item category'], r['Item title']
    if NEVER.search(title) or NEVER.search(cat):
        continue
    hit = None
    if PROMO.search(cat):                       # promo bucket: place by title, built-in first
        t = title.lower()
        for slug, _, rx in GROUPS:
            if slug != 'uredi-za-vgrazhdane' and BUILT_IN.search(t):
                continue                        # "Хладилник за вграждане" is built-in, not a fridge
            if re.search(rx, t):
                hit = slug
                break
        if BUILT_IN.search(t) and re.search(r'^(хладилник|фризер|фурна|съдомиялна|плот|абсорбатор|пералня|кафемашина)', t):
            hit = 'uredi-za-vgrazhdane'
    else:
        for slug, prefixes, _ in GROUPS:
            if any(cat.startswith(p) for p in prefixes):
                hit = slug
                break
    if hit:
        out[hit].append(r)

os.makedirs(OUT, exist_ok=True)
for slug, items in out.items():
    path = os.path.join(OUT, slug + '.csv')
    if len(items) < MIN_ROWS:
        print('%-26s %4d rows - NOT written (kept last good file)' % (slug, len(items)))
        continue
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(items)
    print('%-26s %4d rows' % (slug, len(items)))
