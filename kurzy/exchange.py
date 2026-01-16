import httpx

r = httpx.get("https://gyarab.github.io/2025_wt_holcman/")
print(r.text)