# Meeting Minder - Setup & Deployment Guide

## ⚠️ Important: Two Versions Available

Due to Microsoft Visual C++ Redistributable dependency issues with PyTorch on Windows, I've created **two versions**:

### Version 1: Full Version (meeting_minder.py)
- ✅ Uses local sentence-transformers for embeddings
- ✅ FAISS vector database
- ❌ Requires Microsoft Visual C++ Redistributable
- ❌ Requires PyTorch (large download ~110MB)
- **Use this for**: Production deployment on Linux/Mac or Windows with VC++ installed

### Version 2: Lite Version (meeting_minder_lite.py) ⭐ **RECOMMENDED FOR WINDOWS**
- ✅ Uses HF Inference API for both embeddings and generation
- ✅ No PyTorch dependency
- ✅ No Visual C++ Redistributable needed
- ✅ Smaller install size
- ❌ Slightly slower (API calls for embeddings)
- ❌ Uses more HF API quota
- **Use this for**: Windows development, quick testing, or if you don't want to install VC++

---

## 🚀 Quick Start (Lite Version - Windows)

### Step 1: Get Your HF Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name: "meeting-minder"
4. Select "Read" access
5. Copy the token

### Step 2: Install Dependencies
```powershell
# Make sure you're in the project directory
cd "C:\Users\CNN COMPUTERS\Desktop\Github\flask-app"

# Install lite version dependencies (no PyTorch)
pip install -r requirements-lite.txt
```

### Step 3: Set Your HF Token
```powershell
# Replace YOUR_TOKEN_HERE with your actual token
$env:HF_TOKEN="YOUR_TOKEN_HERE"
```

### Step 4: Run the Server
```powershell
python meeting_minder_lite.py
```

You should see:
```
✓ HF_TOKEN found

🚀 Starting Meeting Minder API (Lite) on http://localhost:5000
   This version uses HF Inference API for all operations (no local models)
```

### Step 5: Open the Frontend
- Open `index.html` in your browser
- Or run: `python -m http.server 8000` and visit http://localhost:8000

### Step 6: Test It!
1. Copy the content from `sample_transcript.txt`
2. Paste it into the Meeting Transcript field
3. Click "Analyze Meeting"
4. Wait 10-15 seconds for results

---

## 🧪 Testing the API

### Option 1: Use the Test Script
```powershell
# Make sure the server is running first
python test_api.py
```

This will:
- Test the health check endpoint
- Analyze a sample meeting
- Display formatted results

### Option 2: Use the Web Interface
1. Open `index.html` in browser
2. Paste a meeting transcript
3. Click "Analyze Meeting"
4. View results

### Option 3: Use curl/Postman
```powershell
# Health check
curl http://localhost:5000/

# Analyze meeting
curl -X POST http://localhost:5000/summarize `
  -H "Content-Type: application/json" `
  -d '{"transcript": "Meeting notes here...", "use_docs": false}'
```

---

## 📦 Deployment Options

### Option 1: Railway (Backend) + Vercel (Frontend) ⭐ Recommended

#### Deploy Backend to Railway:
1. Push code to GitHub
2. Go to https://railway.app
3. Create new project → Deploy from GitHub
4. Select your repository
5. Railway will auto-detect Python
6. Add environment variable:
   - Key: `HF_TOKEN`
   - Value: Your HF token
7. Change start command to: `python meeting_minder_lite.py`
8. Deploy!
9. Copy your Railway URL (e.g., `https://your-app.railway.app`)

#### Deploy Frontend to Vercel:
1. Open `index.html`
2. Find line with `const API_BASE = 'http://localhost:5000';`
3. Change it to: `const API_BASE = 'https://your-app.railway.app';`
4. Push to GitHub
5. Go to https://vercel.com
6. Import your repository
7. Deploy!

---

### Option 2: Render (Full-Stack)

1. Push code to GitHub
2. Go to https://render.com
3. Create new "Web Service"
4. Connect your repository
5. Configure:
   - **Build Command**: `pip install -r requirements-lite.txt`
   - **Start Command**: `python meeting_minder_lite.py`
   - **Environment Variables**: Add `HF_TOKEN`
6. Deploy!
7. For frontend:
   - Create new "Static Site"
   - Point to same repository
   - Update `API_BASE` in `index.html` to your backend URL

---

### Option 3: Ngrok (Quick Demo)

```powershell
# Terminal 1: Run Flask
python meeting_minder_lite.py

# Terminal 2: Run ngrok
ngrok http 5000
```

Then:
1. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
2. Update `API_BASE` in `index.html` to this URL
3. Open `index.html` in browser
4. Share the ngrok URL with others!

---

## 🔧 Troubleshooting

### "HF_TOKEN not set" Error
**Problem**: Environment variable not set
**Solution**:
```powershell
$env:HF_TOKEN="your_token_here"
# Run this in the SAME terminal where you run python
```

### CORS Error in Browser
**Problem**: Frontend can't connect to backend
**Solution**:
- Make sure Flask is running
- Check that `flask-cors` is installed: `pip install flask-cors`
- Verify `API_BASE` in `index.html` matches your server URL

### "Could not find a version that satisfies the requirement faiss-cpu==1.7.4"
**Problem**: Old version specified
**Solution**: Use `requirements-lite.txt` instead (no FAISS needed)

### Slow First Request
**Problem**: HF API model loading
**Solution**: This is normal! First request takes 10-15 seconds. Subsequent requests are faster.

### Empty or Error Results
**Problem**: HF API error or invalid token
**Solution**:
- Check Flask terminal for error messages
- Verify HF token is valid at https://huggingface.co/settings/tokens
- Check HF API status at https://status.huggingface.co

---

## 📊 API Usage & Costs

### Hugging Face Inference API

**Free Tier**:
- 30,000 characters/month
- ~6-10 meetings (depending on length)

**Pro Tier** ($9/month):
- 3,000,000 characters/month
- ~600-1000 meetings

### Lite Version vs Full Version

| Feature | Lite Version | Full Version |
|---------|-------------|--------------|
| HF API calls per meeting | 4-6 | 1 |
| Local model size | 0 MB | ~500 MB |
| First request time | 10-15s | 5-10s |
| Subsequent requests | 5-8s | 2-3s |
| Windows compatibility | ✅ Perfect | ⚠️ Needs VC++ |
| Deployment | ✅ Easy | ✅ Easy |

---

## 📁 Project Files

```
flask-app/
├── meeting_minder.py          # Full version (with PyTorch)
├── meeting_minder_lite.py     # Lite version (API only) ⭐
├── index.html                 # Frontend UI
├── requirements.txt           # Full version dependencies
├── requirements-lite.txt      # Lite version dependencies ⭐
├── test_api.py               # API test script
├── sample_transcript.txt      # Sample data
├── .env.example              # Environment template
├── Procfile                  # Railway/Render config
├── runtime.txt               # Python version
├── vercel.json               # Vercel config
├── render.yaml               # Render blueprint
├── README.md                 # Full documentation
├── QUICKSTART.md             # Quick start guide
└── DEPLOYMENT.md             # This file
```

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] Get HF API token
- [ ] Test locally with `meeting_minder_lite.py`
- [ ] Test with `sample_transcript.txt`
- [ ] Test RAG (upload documents)
- [ ] Update `API_BASE` in `index.html` to production URL
- [ ] Push to GitHub
- [ ] Deploy backend (Railway/Render)
- [ ] Add `HF_TOKEN` environment variable
- [ ] Test backend health check
- [ ] Deploy frontend (Vercel/Render)
- [ ] Test end-to-end flow
- [ ] Monitor HF API usage

---

## 🎯 Next Steps

1. **Test locally** with the lite version
2. **Choose deployment platform** (Railway + Vercel recommended)
3. **Deploy backend** and get URL
4. **Update frontend** with backend URL
5. **Deploy frontend**
6. **Test production** deployment
7. **Monitor usage** in HF dashboard

---

## 💡 Tips

1. **Save your HF token** in a password manager
2. **Monitor API usage** at https://huggingface.co/settings/billing
3. **Use caching** for repeated transcripts (future enhancement)
4. **Start with lite version** on Windows, switch to full version on Linux if needed
5. **Test with short transcripts first** to save API quota

---

## 📞 Support

If you encounter issues:
1. Check Flask terminal logs
2. Check browser console (F12)
3. Verify HF token is valid
4. Test with `test_api.py` script
5. Check HF API status

---

**Ready to deploy? Start with the lite version and Railway + Vercel!** 🚀
