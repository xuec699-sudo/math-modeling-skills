import requests

r = requests.get("https://platform.moonshot.cn/docs/api/chat", timeout=10)
text = r.text

# Find sections mentioning search or tool
import re
# Extract sections with "search" or "tool"
for keyword in ["web_search", "tool", "search", "internet"]:
    idx = text.lower().find(keyword)
    if idx > 0:
        snippet = text[max(0,idx-200):idx+400]
        # Clean HTML
        clean = re.sub(r'<[^>]+>', ' ', snippet)
        clean = re.sub(r'\s+', ' ', clean)
        print(f"\n--- Found '{keyword}' at pos {idx} ---")
        print(clean[:600])
        print("...")