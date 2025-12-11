# test_api.py - Quick test script for the API
import requests
import json

API_BASE = "http://localhost:5000"

# Test 1: Health check
print("Test 1: Health Check")
try:
    response = requests.get(f"{API_BASE}/")
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*50 + "\n")

# Test 2: Analyze a simple meeting
print("Test 2: Analyze Meeting")
transcript = """
Meeting: Quick Standup
Date: Dec 11, 2024

Sarah: Let's do a quick standup. John, what are you working on?
John: I'm finishing the API refactoring. Should be done by Friday.
Sarah: Great. Lisa, how about you?
Lisa: Working on the dashboard mockups. Need feedback by next week.
Sarah: Perfect. Any blockers?
John: No blockers for me.
Lisa: All good here.
Sarah: Excellent. Let's connect again tomorrow.
"""

try:
    response = requests.post(
        f"{API_BASE}/summarize",
        json={"transcript": transcript, "use_docs": False},
        timeout=30
    )
    print(f"✓ Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"\n📋 Summary:\n{result.get('summary', 'N/A')}")
        print(f"\n✅ Action Items:")
        for item in result.get('action_items', []):
            print(f"  - {item.get('task', 'N/A')} (Assignee: {item.get('assignee', 'TBD')})")
        print(f"\n⚡ Decisions:")
        for decision in result.get('decisions', []):
            print(f"  - {decision}")
        print(f"\n❓ Open Questions:")
        for question in result.get('open_questions', []):
            print(f"  - {question}")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
