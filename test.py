import requests
import json

payload = {"message": "Hi, I need a personal loan of 2.5L"}
master_url = "https://curly-space-garbanzo-7vx6j5596jw9fp764-8000.app.github.dev/"
r = requests.post(master_url, json=payload, timeout=10)
print("HTTP", r.status_code)
print(json.dumps(r.json(), indent=2))
