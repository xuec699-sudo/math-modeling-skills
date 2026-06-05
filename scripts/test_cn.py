import httpx, re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Test Baidu Scholar
try:
    r = httpx.get("https://xueshu.baidu.com/s", params={"wd": "深度学习图像分割", "pn": "0"}, headers=headers, timeout=10)
    titles = re.findall(r'<h3[^>]*class="t[^"]*"[^>]*>(.*?)</h3>', r.text, re.DOTALL)
    print(f"Baidu Scholar: status={r.status_code}, titles={len(titles)}")
    for t in titles[:3]:
        clean = re.sub(r'<[^>]+>', '', t).strip()
        print(f"  - {clean[:100]}")
except Exception as e:
    print(f"Baidu Scholar Error: {e}")

# Test CNKI Scholar
try:
    r2 = httpx.post("https://schlr.cnki.net/Home/Search", json={
        "searchType": "MulityTermsSearch",
        "searchWords": [[{"Field": "SU", "Value": "深度学习", "Operate": "=", "IsExact": "false"}]],
        "pageNum": 1, "pageSize": 5,
    }, headers=headers, timeout=15)
    print(f"\nCNKI Scholar: status={r2.status_code}")
    if r2.status_code == 200:
        data = r2.json()
        items = data.get("Data", {}).get("dataList", [])
        print(f"  Found: {len(items)} papers")
        for item in items[:3]:
            title = item.get("Title_CH", item.get("Title", ""))
            authors = item.get("Author", "")
            year = item.get("Year", "")
            abstract = item.get("Abstract", "")[:100]
            print(f"  - {title[:80]}")
            print(f"    {authors} ({year})")
            print(f"    Abstract: {abstract}...")
except Exception as e:
    print(f"CNKI Scholar Error: {e}")
