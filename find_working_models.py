# find_working_models.py - Test multiple models to find working ones
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# List of models to test for text generation/summarization
generation_models = [
    "facebook/bart-large-cnn",
    "google/flan-t5-base",
    "t5-small",
    "gpt2",
    "distilgpt2",
    "facebook/opt-350m",
    "bigscience/bloom-560m",
    "microsoft/DialoGPT-medium"
]

# List of models to test for embeddings
embedding_models = [
    "BAAI/bge-large-en-v1.5",
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "BAAI/bge-small-en-v1.5",
    "thenlper/gte-small"
]

print("Testing Generation Models...")
print("=" * 50)
for model in generation_models:
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": "Summarize this text: The meeting was about planning."}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ {model} - WORKS!")
        else:
            print(f"❌ {model} - Status {response.status_code}")
    except Exception as e:
        print(f"❌ {model} - Error: {str(e)[:50]}")

print("\n" + "=" * 50)
print("Testing Embedding Models...")
print("=" * 50)
for model in embedding_models:
    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": "Hello world"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ {model} - WORKS!")
        else:
            print(f"❌ {model} - Status {response.status_code}")
    except Exception as e:
        print(f"❌ {model} - Error: {str(e)[:50]}")
