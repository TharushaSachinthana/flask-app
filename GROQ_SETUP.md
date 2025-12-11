# Meeting Minder - Groq Setup Guide

## 🎉 Free Version with Groq API

This version uses Groq's **free API** - no credit card required!

### Why Groq?
- ✅ **100% Free** - No credit card needed
- ✅ **Fast** - Optimized inference
- ✅ **Powerful** - Uses Llama 3.3 70B model
- ✅ **Reliable** - Production-ready API

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Your Free Groq API Key

1. Go to: **https://console.groq.com**
2. Sign up (free, no credit card)
3. Click "API Keys" in the left sidebar
4. Click "Create API Key"
5. Give it a name: "meeting-minder"
6. **Copy the key** (starts with `gsk_...`)

### Step 2: Set the API Key

**PowerShell:**
```powershell
$env:GROQ_API_KEY="gsk_YourKeyHere"
```

**Verify it's set:**
```powershell
echo $env:GROQ_API_KEY
```

### Step 3: Run the Server

```powershell
cd "C:\Users\CNN COMPUTERS\Desktop\Github\flask-app"
python meeting_minder_groq.py
```

**Expected output:**
```
✓ GROQ_API_KEY found

🚀 Starting Meeting Minder API (Groq - FREE) on http://localhost:5000
   Using model: llama-3.3-70b-versatile
```

### Step 4: Test It!

**Option A - Web Interface:**
1. Open `index.html` in your browser
2. Paste content from `sample_transcript.txt`
3. Click "Analyze Meeting"
4. Wait 5-10 seconds for results

**Option B - Test Script:**
```powershell
python test_api.py
```

---

## 📊 What's Different from HF Version?

| Feature | HF Version | Groq Version |
|---------|-----------|--------------|
| Cost | Free (deprecated) | **Free (working!)** |
| Model | flan-t5 | **Llama 3.3 70B** |
| Speed | Slow | **Very Fast** |
| Quality | Good | **Excellent** |
| RAG | Vector embeddings | Keyword matching |
| Status | ❌ Broken | ✅ **Working** |

---

## 🔧 Technical Details

### Model Used
- **llama-3.3-70b-versatile**
- 70 billion parameters
- Optimized for speed
- Excellent at structured output

### RAG Implementation
- Simple keyword-based matching (no embeddings needed)
- Fast and effective for most use cases
- No additional API calls required

### API Limits (Free Tier)
- **Requests**: 30 requests/minute
- **Tokens**: 6,000 tokens/minute
- **Daily**: 14,400 requests/day

This is **more than enough** for typical usage!

---

## 🧪 Testing

### Test with Sample Transcript

```powershell
# Make sure server is running
python meeting_minder_groq.py

# In another terminal
python test_api.py
```

### Expected Results
- ✅ Health check passes
- ✅ Meeting analyzed successfully
- ✅ Summary generated
- ✅ Action items extracted
- ✅ Decisions listed
- ✅ Open questions identified

---

## 🌐 Deployment

### Update for Production

1. **Update `index.html`**:
   - Find: `const API_BASE = 'http://localhost:5000';`
   - Change to your production URL

2. **Deploy Backend** (Railway/Render):
   - Use `meeting_minder_groq.py` instead of `meeting_minder_lite.py`
   - Set environment variable: `GROQ_API_KEY`
   - Update Procfile: `web: python meeting_minder_groq.py`

3. **Deploy Frontend** (Vercel):
   - Same as before
   - Update `API_BASE` to backend URL

---

## 💡 Tips

1. **Save your Groq API key** securely
2. **Monitor usage** at https://console.groq.com
3. **Free tier is generous** - 14,400 requests/day
4. **Llama 3.3 is powerful** - better than flan-t5
5. **No embeddings needed** - simpler architecture

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not set"
```powershell
$env:GROQ_API_KEY="gsk_YourKeyHere"
```

### "401 Unauthorized"
- Check your API key at https://console.groq.com
- Make sure you copied the full key (starts with `gsk_`)

### "429 Rate Limit"
- Free tier: 30 requests/minute
- Wait a minute and try again
- Or upgrade to paid tier for higher limits

### Slow Response
- First request may take 5-10 seconds (model loading)
- Subsequent requests are faster (2-3 seconds)

---

## 📈 Comparison: Groq vs OpenAI

| Feature | Groq (Free) | OpenAI (Paid) |
|---------|-------------|---------------|
| Cost | **$0** | ~$0.002/meeting |
| Speed | Very Fast | Fast |
| Quality | Excellent | Excellent |
| Setup | 5 minutes | 5 minutes |
| Limits | 14.4K req/day | Pay-as-you-go |

**Verdict**: Start with Groq (free), upgrade to OpenAI if you need higher limits.

---

## ✅ Ready to Use!

1. Get Groq API key: https://console.groq.com
2. Set it: `$env:GROQ_API_KEY="gsk_..."`
3. Run: `python meeting_minder_groq.py`
4. Test: Open `index.html` or run `python test_api.py`

**It's that simple!** 🚀

---

## 📞 Support

- **Groq Docs**: https://console.groq.com/docs
- **API Status**: https://status.groq.com
- **Community**: https://groq.com/community

---

**Enjoy your FREE, fast, and powerful meeting assistant!** 🎉
