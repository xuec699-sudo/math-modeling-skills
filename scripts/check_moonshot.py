import requests

# Moonshot API base
url = "https://api.moonshot.cn/v1/models"
try:
    r = requests.get(url, timeout=10)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        for m in data.get("data", []):
            print(f"  {m.get('id')} - {m.get('owned_by')}")
    elif r.status_code == 401:
        print("Needs API key (expected)")
    else:
        print(r.text[:200])
except Exception as e:
    print(f"Error: {e}")

# Check docs page for web_search parameter
print("\n--- Checking public docs for web_search ---")
try:
    r = requests.get("https://platform.moonshot.cn/docs", timeout=10)
    print(f"Docs: {r.status_code}")
    if "web_search" in r.text.lower() or "search" in r.text.lower():
        print("  Mentions search!")
    else:
        print("  No search mention on main docs page")
except:
    print("  Cannot reach docs")