# Meeting Minder - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your Hugging Face Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "meeting-minder")
4. Select "Read" access
5. Copy the token

### Step 2: Set Environment Variable

**Windows PowerShell**:
```powershell
$env:HF_TOKEN="paste_your_token_here"
```

**Windows Command Prompt**:
```cmd
set HF_TOKEN=paste_your_token_here
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web server)
- FAISS (vector search)
- sentence-transformers (embeddings)
- And other dependencies

**Note**: First install may take 2-3 minutes to download models.

### Step 4: Run the Backend
```bash
python meeting_minder.py
```

You should see:
```
✓ HF_TOKEN found
✓ Loading sentence transformer model...
✓ Model loaded successfully

🚀 Starting Meeting Minder API on http://localhost:5000
```

### Step 5: Open the Frontend

**Option A - Direct Open**:
- Double-click `index.html`
- It will open in your default browser

**Option B - Local Server** (recommended):
```bash
# In a new terminal
python -m http.server 8000
```
Then visit: http://localhost:8000

### Step 6: Test with Sample Data

1. Open `sample_transcript.txt`
2. Copy the entire content
3. In the web interface, paste it into the "Meeting Transcript" field
4. Click "Analyze Meeting"
5. Wait 5-10 seconds for results

You should see:
- ✅ Meeting summary
- ✅ Action items with assignees and due dates
- ✅ Key decisions
- ✅ Open questions
- ✅ Email-ready summary

### Step 7: Test RAG (Optional)

1. Create a text file with company info (e.g., `company_policy.txt`):
   ```
   Company Policy on Remote Work:
   All employees are allowed to work remotely up to 3 days per week.
   Managers must approve remote work schedules in advance.
   ```

2. In the web interface, click "Choose Files" under "Upload Context Documents"
3. Select your policy file
4. Click "Upload Documents"
5. Now analyze a meeting - the system will use this context!

---

## 🎯 What to Try

### Test Case 1: Basic Analysis
Use the provided `sample_transcript.txt` to see:
- Summary extraction
- Action item parsing
- Decision tracking

### Test Case 2: RAG Context
1. Upload a document about your project
2. Analyze a meeting about that project
3. See how the context improves the analysis

### Test Case 3: Email Summary
1. Analyze any meeting
2. Scroll to "Email-Ready Summary"
3. Click "Copy to Clipboard"
4. Paste into your email client

---

## 🐛 Troubleshooting

### "HF_TOKEN not set" Error
- Make sure you ran the `set` or `$env:` command
- Run it in the SAME terminal where you run `python meeting_minder.py`
- Check the token at https://huggingface.co/settings/tokens

### CORS Error in Browser
- Make sure Flask is running (`python meeting_minder.py`)
- Check that `flask-cors` is installed: `pip install flask-cors`
- Try opening `index.html` via `python -m http.server 8000`

### Slow First Request
- First request loads the model (~5-10 seconds)
- Subsequent requests are much faster (~2-3 seconds)
- This is normal!

### Empty Results
- Check Flask terminal for error messages
- Verify HF_TOKEN is valid
- Try with `sample_transcript.txt` first

---

## 📦 Next Steps: Deployment

Once you've tested locally, deploy to production:

### Option 1: Vercel + Railway (Recommended)
- **Backend**: Push to GitHub → Deploy on Railway → Add HF_TOKEN
- **Frontend**: Update API_BASE in index.html → Deploy on Vercel

### Option 2: Render (Easiest)
- Push to GitHub → Create Render Blueprint → Add HF_TOKEN
- Both frontend and backend deploy automatically

### Option 3: Ngrok (Quick Demo)
- Keep Flask running locally
- Run `ngrok http 5000`
- Update API_BASE in index.html to ngrok URL
- Share the ngrok URL with others

See `README.md` for detailed deployment instructions.

---

## 💡 Tips

1. **Save your HF_TOKEN**: Add it to a `.env` file (don't commit!)
2. **Test incrementally**: Start with sample transcript, then try your own
3. **Monitor usage**: Check HF dashboard for API usage (free tier = 30k chars/month)
4. **Optimize prompts**: Edit the prompt in `meeting_minder.py` for better results
5. **Cache results**: For repeated transcripts, consider adding caching

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Implementation Details**: See `walkthrough.md` in `.gemini/antigravity/brain/`
- **API Reference**: See README.md "API Documentation" section

---

**Ready to analyze meetings? Let's go! 🚀**
