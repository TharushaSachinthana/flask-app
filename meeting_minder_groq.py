# meeting_minder_groq.py - Free version using Groq API
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import re
from typing import List

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE = "https://api.groq.com/openai/v1"
MODEL = "llama-3.3-70b-versatile"  # Fast and free on Groq

app = Flask(__name__)
CORS(app)

# ----------------- Simple document store (no embeddings for simplicity) -----------------
doc_texts = []

def build_index(text_chunks: List[str]):
    """Store document chunks for keyword-based retrieval"""
    global doc_texts
    doc_texts = text_chunks.copy()
    print(f"✓ Stored {len(doc_texts)} document chunks")

def query_index(query: str, k=3):
    """Simple keyword-based retrieval"""
    if not doc_texts:
        return []
    
    # Simple keyword matching (case-insensitive)
    query_words = set(query.lower().split())
    
    # Score each document by keyword overlap
    scored_docs = []
    for doc in doc_texts:
        doc_words = set(doc.lower().split())
        overlap = len(query_words & doc_words)
        if overlap > 0:
            scored_docs.append((overlap, doc))
    
    # Sort by score and return top-k
    scored_docs.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in scored_docs[:k]]

# ----------------- Groq API helpers -----------------
def groq_chat(messages: List[dict], max_tokens=1000):
    """Call Groq Chat Completion API"""
    url = f"{GROQ_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        result = r.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        raise

# ----------------- API Endpoints -----------------
@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "service": "Meeting Minder API (Groq)",
        "endpoints": ["/upload_docs", "/summarize"],
        "version": "groq-free"
    })

@app.route("/upload_docs", methods=["POST"])
def upload_docs():
    """Upload documents for RAG context"""
    try:
        docs = request.json.get("docs", [])
        
        if not docs:
            return jsonify({"error": "No documents provided"}), 400
        
        # Chunk docs (split by paragraphs)
        chunks = []
        for d in docs:
            for p in d.split("\n\n"):
                p = p.strip()
                if p and len(p) > 20:
                    chunks.append(p)
        
        if not chunks:
            return jsonify({"error": "No valid chunks extracted"}), 400
        
        build_index(chunks)
        return jsonify({
            "status": "indexed",
            "chunks": len(chunks),
            "message": f"Successfully indexed {len(chunks)} document chunks"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    """Analyze meeting transcript"""
    try:
        data = request.json
        transcript = data.get("transcript", "").strip()
        include_docs = data.get("use_docs", True)
        
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
        
        # Retrieve RAG context if enabled
        rag_context = ""
        if include_docs and doc_texts:
            print("Retrieving context...")
            top = query_index(transcript, k=3)
            if top:
                rag_context = "\n\n".join([f"[Context {i+1}]: {chunk}" for i, chunk in enumerate(top)])
        
        # Construct messages for Groq
        system_message = """You are MeetingMinder, an AI assistant that analyzes meeting transcripts.

Your task is to analyze the meeting and provide a structured response in JSON format with these exact keys:
- summary: A concise 3-4 sentence summary of the meeting
- action_items: Array of objects with keys: task, assignee, due
- decisions: Array of key decisions made
- open_questions: Array of unresolved questions

Return ONLY valid JSON, no other text."""

        # Build user message with optional RAG context
        context_prefix = ""
        if rag_context:
            context_prefix = "Relevant context from company documents:\n" + rag_context + "\n\n"
        
        user_message = f"{context_prefix}Meeting Transcript:\n{transcript}\n\nAnalyze this meeting and return a JSON response with: summary, action_items (with task/assignee/due), decisions, and open_questions."

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Call Groq API
        print("Calling Groq API...")
        generated = groq_chat(messages, max_tokens=1000)
        print(f"Generated response: {generated[:200]}...")
        
        # Parse the response
        result = parse_model_output(generated)
        
        # Add email-ready summary
        result["email_summary"] = generate_email_summary(result)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in summarize: {e}")
        return jsonify({"error": str(e)}), 500

def parse_model_output(generated: str):
    """Parse model output and extract structured data"""
    # Try to find JSON in the response
    json_match = re.search(r'\{[\s\S]*\}', generated)
    
    if json_match:
        try:
            result = json.loads(json_match.group(0))
            # Validate required keys
            if all(k in result for k in ["summary", "action_items", "decisions", "open_questions"]):
                return result
        except json.JSONDecodeError:
            pass
    
    # Fallback: parse manually
    result = {
        "summary": extract_section(generated, ["summary", "Summary"], default="Meeting analysis completed."),
        "action_items": extract_action_items(generated),
        "decisions": extract_list(generated, ["decisions", "Decisions"]),
        "open_questions": extract_list(generated, ["open_questions", "Open Questions", "questions"])
    }
    
    return result

def extract_section(text: str, headers: List[str], default: str = "") -> str:
    """Extract text under a specific header"""
    for header in headers:
        pattern = rf'"{header}":\s*"([^"]*)"'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return default

def extract_list(text: str, headers: List[str]) -> List[str]:
    """Extract list under a header"""
    for header in headers:
        pattern = rf'"{header}":\s*\[(.*?)\]'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1)
            # Extract quoted strings
            items = re.findall(r'"([^"]*)"', content)
            if items:
                return items
    return []

def extract_action_items(text: str) -> List[dict]:
    """Extract action items from text"""
    # Try to find JSON array
    pattern = r'"action_items":\s*\[(.*?)\]'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    
    if match:
        try:
            items_str = "[" + match.group(1) + "]"
            items = json.loads(items_str)
            if isinstance(items, list) and all(isinstance(i, dict) for i in items):
                return items
        except json.JSONDecodeError:
            pass
    
    # Fallback
    return [{
        "task": "Review meeting transcript",
        "assignee": "TBD",
        "due": "TBD"
    }]

def generate_email_summary(result: dict) -> str:
    """Generate email-ready summary"""
    email = f"""Meeting Summary

{result.get('summary', 'No summary available.')}

Action Items:
"""
    for i, action in enumerate(result.get('action_items', []), 1):
        task = action.get('task', 'N/A')
        assignee = action.get('assignee', 'TBD')
        due = action.get('due', 'TBD')
        email += f"{i}. {task} (Assignee: {assignee}, Due: {due})\n"
    
    if result.get('decisions'):
        email += f"\nKey Decisions:\n"
        for i, decision in enumerate(result.get('decisions', []), 1):
            email += f"{i}. {decision}\n"
    
    if result.get('open_questions'):
        email += f"\nOpen Questions:\n"
        for i, question in enumerate(result.get('open_questions', []), 1):
            email += f"{i}. {question}\n"
    
    return email

# ----------------- Main -----------------
if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("⚠️  WARNING: GROQ_API_KEY environment variable not set!")
        print("   Get your key at: https://console.groq.com")
        print("   Set it with: $env:GROQ_API_KEY=\"your_key_here\"")
    else:
        print("✓ GROQ_API_KEY found")
    
    # Get port from environment (for deployment) or use 5000 for local
    port = int(os.getenv("PORT", 5000))
    
    print(f"\n🚀 Starting Meeting Minder API (Groq - FREE) on port {port}")
    print(f"   Using model: {MODEL}")
    app.run(host="0.0.0.0", port=port, debug=False)
