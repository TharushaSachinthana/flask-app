# quick_test.py - Direct HF API test
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
print(f"Token set: {HF_TOKEN[:10]}..." if HF_TOKEN else "No token!")

# Test the embedding endpoint
print("\n1. Testing embedding endpoint (BAAI/bge-large-en-v1.5)...")
url = "https://api-inference.huggingface.co/models/BAAI/bge-large-en-v1.5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
payload = {"inputs": "Hello world"}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Embedding works!")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")

# Test the generation endpoint
print("\n2. Testing generation endpoint (facebook/bart-large-cnn)...")
url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
payload = {
    "inputs": "The meeting was about Q4 planning. Sarah discussed priorities with the team. John will handle API refactoring by end of December. Lisa will create dashboard mockups by Dec 20th. The team decided to use React Native for the mobile app.",
    "parameters": {"max_length": 100}
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Generation works!")
        print(f"Response: {response.json()}")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Exception: {e}")
