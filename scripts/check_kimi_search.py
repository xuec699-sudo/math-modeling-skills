import requests

# Check the API reference / chat completions docs
urls = [
    "https://platform.moonshot.cn/docs/api/chat",
    "https://platform.moonshot.cn/docs/api-reference",
    "https://platform.moonshot.cn/docs/guide/use-kimi-api",
]

for url in urls:
    try:
        r = requests.get(url, timeout=10)
        text = r.text.lower()
        has_search = "web_search" in text or "search" in text
        has_tool = "tool" in text and "search" in text
        print(f"{url}: {r.status_code} | search={'YES' if has_search else 'no'} | tool_search={'YES' if has_tool else 'no'}")
    except Exception as e:
        print(f"{url}: Error {e}")

# Try to find the specific API parameter docs
try:
    r = requests.get("https://platform.moonshot.cn/docs", timeout=10)
    # Find all links
    import re
    links = re.findall(r'href="([^"]*)"', r.text)
    search_links = [l for l in links if 'search' in l.lower() or 'tool' in l.lower()]
    print(f"\nSearch-related links found: {len(search_links)}")
    for l in search_links[:5]:
        print(f"  {l}")
except:
    pass