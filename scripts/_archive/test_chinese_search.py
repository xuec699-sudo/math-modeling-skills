# -*- coding: utf-8 -*-
"""Test: Can we get real Chinese paper metadata from public sources?"""
import httpx, asyncio, re, json

async def test_baidu_xueshu(query):
    """Test Baidu Scholar search"""
    url = "https://xueshu.baidu.com/s"
    params = {"wd": query, "pn": "0", "tn": "SE_baiduxueshu_c1g0"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params, headers=headers)
            # Check if we got results
            text = resp.text
            # Look for paper titles
            titles = re.findall(r'<h3[^>]*class="t[^"]*"[^>]*>(.*?)</h3>', text, re.DOTALL)
            print(f"[百度学术] 查询: {query}")
            print(f"  状态码: {resp.status_code}")
            print(f"  找到标题数: {len(titles)}")
            if titles:
                for t in titles[:3]:
                    clean = re.sub(r'<[^>]+>', '', t).strip()
                    print(f"  - {clean[:80]}")
            return len(titles) > 0
    except Exception as e:
        print(f"[百度学术] Error: {e}")
        return False

async def test_cnki_search(query):
    """Test CNKI Scholar search (public)"""
    url = "https://schlr.cnki.net/Home/Search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json={
                "searchType": "MulityTermsSearch",
                "searchWords": [[{"Field": "SU", "Value": query, "Operate": "'='", "IsExact": "false"}]],
                "pageNum": 1, "pageSize": 5,
            }, headers=headers)
            print(f"\n[CNKI Scholar] 查询: {query}")
            print(f"  状态码: {resp.status_code}")
            data = resp.json()
            items = data.get("Data", {}).get("dataList", [])
            print(f"  找到文献数: {len(items)}")
            for item in items[:3]:
                title = item.get("Title_CH", item.get("Title", ""))
                print(f"  - {title[:80]}")
            return len(items) > 0
    except Exception as e:
        print(f"[CNKI Scholar] Error: {e}")
        return False

asyncio.run(test_baidu_xueshu("深度学习图像分割"))
asyncio.run(test_cnki_search("深度学习"))
