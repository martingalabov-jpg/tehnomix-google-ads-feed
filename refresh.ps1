# Daily refresh of tehnomix-google-ads-feed.csv. Run by Task Scheduler; see README.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$log = Join-Path $PSScriptRoot 'refresh.log'
function Log($m) { "$(Get-Date -Format s)  $m" | Add-Content $log -Encoding utf8 }
try {
    git pull -q --rebase origin main
    $ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    curl.exe -sSf --retry 3 --retry-delay 20 -o google-new.csv -A $ua -H 'Accept: text/csv,*/*' https://www.tehnomix.bg/media/feed/google-new.csv
    if ($LASTEXITCODE -ne 0) { throw "download failed (curl exit $LASTEXITCODE)" }
    if ((Get-Content google-new.csv -TotalCount 1) -notmatch '^ID,Item title,Final URL') { throw 'download is not the feed CSV (challenge page?)' }
    $rows = python -I -c "import csv;print(sum(1 for _ in csv.DictReader(open('google-new.csv',encoding='utf-8-sig'))))"
    if ([int]$rows -lt 3000) { throw "only $rows products - refusing to publish" }
    Copy-Item google-new.csv tehnomix-google-ads-feed.csv -Force
    (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ') | Set-Content last_run.txt -Encoding ascii
    git add tehnomix-google-ads-feed.csv last_run.txt
    git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) { git commit -q -m "Refresh feed $(Get-Date -Format yyyy-MM-dd)"; git push -q origin main }
    Log "OK  rows=$rows"
} catch { Log "FAIL  $_"; exit 1 }
