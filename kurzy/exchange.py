import httpx

r = httpx.get("https://www.youtube.com/")
print(r.text)