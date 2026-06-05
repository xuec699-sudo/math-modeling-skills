import httpx, re
h = {"User-Agent": "Mozilla/5.0"}

try:
    r = httpx.post("https://schlr.cnki.net/Home/Search", json={
        "searchType": "MulityTermsSearch",
        "searchWords": [[{"Field": "SU", "Value": "深度学习", "Operate": "=", "IsExact": "false"}]],
        "pageNum": 1, "pageSize": 5
    }, headers=h, timeout=15)
    print(f"CNKI Scholar: {r.status_code}")
    if r.status_code == 200:
        d = r.json()
        items = d.get("Data", {}).get("dataList", [])
        print(f"Papers: {len(items)}")
        for it in items[:3]:
            t = it.get("Title_CH", it.get("Title", ""))
            a = it.get("Author", "")
            y = it.get("Year", "")
            ab = (it.get("Abstract", "") or "")[:120]
            print(f"  [{y}] {t[:60]}")
            print(f"       {a}")
            if ab: print(f"       {ab}")
except Exception as e:
    print(f"CNKI Error: {e}")

try:
    r = httpx.get("https://xueshu.baidu.com/s", params={"wd": "深度学习", "pn": "0"}, headers=h, timeout=10)
    print(f"\nBaidu Scholar: {r.status_code}, len={len(r.text)}")
    if "verify" not in r.text.lower():
        for p in [r'<h3[^>]*>(.*?)</h3>', r'class="title"[^>]*>(.*?)<']:
            m = re.findall(p, r.text, re.DOTALL)
            if m:
                print(f"  Found {len(m)} titles")
                for x in m[:2]:
                    print(f"    {re.sub(r'<[^>]+>','',x)[:80]}")
                break
    else:
        print("  BLOCKED")
except Exception as e:
    print(f"Baidu Error: {e}")