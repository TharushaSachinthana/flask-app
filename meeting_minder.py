# meeting_minder.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
import re
from typing import List
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Configuration
HF_TOKEN = os.getenv("HF_TOKEN")
HF_BASE = "https://api-inference.huggingface.co/models"
GEN_MODEL = "facebook/bart-large-cnn"  # Updated: Using BART for summarization
EMBED_MODEL = "BAAI/bge-large-en-v1.5"  # Updated: Using BGE for embeddings

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# ----------------- Simple in-memory FAISS (for RAG) -----------------
embedder = SentenceTransformer(EMBED_MODEL)
index = None
index_texts = []

def build_index(text_chunks: List[str]):
    """Build FAISS index from text chunks"""
    global index, index_texts
    if not text_chunks:
        return
    
    vectors = embedder.encode(text_chunks, show_progress_bar=False, convert_to_numpy=True)
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    index_texts = text_chunks.copy()
    print(f"✓ Built FAISS index with {len(text_chunks)} chunks")

def query_index(query: str, k=3):
    """Query FAISS index for top-k relevant chunks"""
    if index is None or index.ntotal == 0:
        return []
    
    qv = embedder.encode([query], convert_to_numpy=True)
    D, I = index.search(qv, k)
    results = []
    for idx in I[0]:
        if idx < len(index_texts):
            results.append(index_texts[idx])
    return results

# ----------------- HF Inference helpers -----------------
def hf_generate(prompt: str, max_new_tokens=400):
    """Call Hugging Face Inference API for text generation"""
    url = f"{HF_BASE}/{GEN_MODEL}"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=60)
        r.raise_for_status()
        out = r.json()
        
        # Parse output; flan-t5 often returns list with 'generated_text'
        if isinstance(out, list) and len(out) > 0:
            if "generated_text" in out[0]:
                return out[0]["generated_text"]
            return str(out[0])
        return str(out)
    except Exception as e:
        print(f"Error calling HF API: {e}")
        raise

# ----------------- API Endpoints -----------------
@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "service": "Meeting Minder API",
        "endpoints": ["/upload_docs", "/summarize"]
    })

@app.route("/upload_docs", methods=["POST"])
def upload_docs():
    """
    Upload documents for RAG context
    Expects JSON: { "docs": ["text1", "text2", ...] }
    """
    try:
        docs = request.json.get("docs", [])
        
        if not docs:
            return jsonify({"error": "No documents provided"}), 400
        
        # Chunk docs (naive: split by paragraphs)
        chunks = []
        for d in docs:
            # Split by double newlines (paragraphs)
            for p in d.split("\n\n"):
                p = p.strip()
                if p and len(p) > 20:  # Ignore very short chunks
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
    """
    Analyze meeting transcript and extract insights
    Expects JSON: {
        "transcript": "meeting text...",
        "use_docs": true/false (optional, default: true)
    }
    """
    try:
        data = request.json
        transcript = data.get("transcript", "").strip()
        include_docs = data.get("use_docs", True)
        
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
        
        # Retrieve RAG context if enabled
        rag_context = ""
        if include_docs and index is not None and index.ntotal > 0:
            top = query_index(transcript, k=3)
            if top:
                rag_context = "\n\n".join([f"[Context {i+1}]: {chunk}" for i, chunk in enumerate(top)])
        
        # Construct prompt for the model
        prompt = f"""You are MeetingMinder, an AI assistant that analyzes meeting transcripts.

{f"Relevant context from company documents:\n{rag_context}\n" if rag_context else ""}
Meeting Transcript:
{transcript}

Please analyze this meeting and provide:

1. SUMMARY: A concise 3-4 sentence summary of the meeting
2. ACTION_ITEMS: List of action items in this exact JSON format:
   [{{"task": "description", "assignee": "person name", "due": "suggested date"}}]
3. DECISIONS: Key decisions made during the meeting
4. OPEN_QUESTIONS: Unresolved questions or topics for follow-up

Format your response as valid JSON with these exact keys: summary, action_items, decisions, open_questions
"""

        # Call HF Inference API
        print("Calling HF Inference API...")
        generated = hf_generate(prompt, max_new_tokens=500)
        print(f"Generated response: {generated[:200]}...")
        
        # Try to extract JSON from response
        result = parse_model_output(generated, transcript)
        
        # Add email-ready summary
        result["email_summary"] = generate_email_summary(result)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in summarize: {e}")
        return jsonify({"error": str(e)}), 500

def parse_model_output(generated: str, transcript: str):
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
        "summary": extract_section(generated, ["SUMMARY", "Summary"], default="Meeting analysis completed."),
        "action_items": extract_action_items(generated),
        "decisions": extract_list(generated, ["DECISIONS", "Decisions"]),
        "open_questions": extract_list(generated, ["OPEN_QUESTIONS", "Open Questions", "QUESTIONS"])
    }
    
    return result

def extract_section(text: str, headers: List[str], default: str = "") -> str:
    """Extract text under a specific header"""
    for header in headers:
        pattern = rf"{header}:?\s*(.+?)(?=\n[A-Z_]+:|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    return default

def extract_list(text: str, headers: List[str]) -> List[str]:
    """Extract bullet list under a header"""
    for header in headers:
        pattern = rf"{header}:?\s*(.+?)(?=\n[A-Z_]+:|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Extract bullet points
            items = re.findall(r'[-•*]\s*(.+)', content)
            if items:
                return [item.strip() for item in items]
            # Fallback: split by newlines
            return [line.strip() for line in content.split('\n') if line.strip()]
    return []

def extract_action_items(text: str) -> List[dict]:
    """Extract action items from text"""
    # Try to find JSON array
    json_match = re.search(r'\[[\s\S]*?\]', text)
    if json_match:
        try:
            items = json.loads(json_match.group(0))
            if isinstance(items, list) and all(isinstance(i, dict) for i in items):
                return items
        except json.JSONDecodeError:
            pass
    
    # Fallback: extract from bullet points
    action_items = []
    items = extract_list(text, ["ACTION_ITEMS", "Action Items", "ACTIONS"])
    for item in items:
        action_items.append({
            "task": item,
            "assignee": "TBD",
            "due": "TBD"
        })
    
    return action_items

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
    if not HF_TOKEN:
        print("⚠️  WARNING: HF_TOKEN environment variable not set!")
        print("   Set it with: set HF_TOKEN=your_token_here")
    else:
        print("✓ HF_TOKEN found")
    
    print("✓ Loading sentence transformer model...")
    # Warm up the embedder
    _ = embedder.encode(["test"], show_progress_bar=False)
    print("✓ Model loaded successfully")
    
    print("\n🚀 Starting Meeting Minder API on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
