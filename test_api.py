import requests
import json

# Load from config file
with open('config.json', 'r') as f:
    config = json.load(f)

CLOUD_URL = config['cloud_url']

print(f"Testing connection to: {CLOUD_URL}")
try:
    response = requests.post(
        f"{CLOUD_URL}/query",
        json={"query": "What are the contraindications for nitroglycerin?", "device_id": "test"},
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS!\n")
        print("Response:", data['response'][:500])
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"❌ Failed: {e}")
