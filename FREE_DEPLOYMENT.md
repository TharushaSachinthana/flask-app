# FREE Deployment Guide - Get Your Public URL in 10 Minutes!

## 🎯 Goal
Deploy Meeting Minder for **100% FREE** and get a public URL like:
- `https://meeting-minder.onrender.com` (backend)
- `https://meeting-minder-ui.vercel.app` (frontend)

---

## ✅ Best Option: Render (Backend) + Vercel (Frontend)

Both are **completely FREE** with free subdomains!

---

## 🚀 Step 1: Push Code to GitHub (5 minutes)

### 1.1 Initialize Git (if not already done)
```powershell
cd "C:\Users\CNN COMPUTERS\Desktop\Github\flask-app"
git init
git add .
git commit -m "Initial commit - Meeting Minder with Groq API"
```

### 1.2 Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `meeting-minder`
3. Make it **Public** (required for free tier)
4. Click "Create repository"

### 1.3 Push to GitHub
```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/meeting-minder.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy Backend to Render (3 minutes)

### 2.1 Sign Up for Render
1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest)

### 2.2 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `meeting-minder`
3. Click "Connect"

### 2.3 Configure Service
Fill in these details:

**Name**: `meeting-minder-api` (or any name you like)

**Region**: Choose closest to you

**Branch**: `main`

**Root Directory**: Leave empty

**Runtime**: `Python 3`

**Build Command**:
```
pip install -r requirements-lite.txt
```

**Start Command**:
```
gunicorn meeting_minder_groq:app --bind 0.0.0.0:$PORT
```

**Instance Type**: `Free` ⭐

### 2.4 Add Environment Variable
1. Scroll down to "Environment Variables"
2. Click "Add Environment Variable"
3. **Key**: `GROQ_API_KEY`
4. **Value**: `gsk_YOUR_ACTUAL_GROQ_API_KEY_HERE`
5. Click "Add"

### 2.5 Deploy!
1. Click "Create Web Service"
2. Wait 2-3 minutes for deployment
3. You'll get a URL like: `https://meeting-minder-api.onrender.com`

**Copy this URL - you'll need it for the frontend!**

---

## 🎨 Step 3: Deploy Frontend to Vercel (2 minutes)

### 3.1 Update Frontend API URL
Before deploying, update `index.html`:

1. Open `index.html`
2. Find line ~520: `const API_BASE = 'http://localhost:5000';`
3. Change to: `const API_BASE = 'https://YOUR-RENDER-URL.onrender.com';`
   - Replace with your actual Render URL from Step 2.5
4. Save the file
5. Commit and push:
```powershell
git add index.html
git commit -m "Update API URL for production"
git push
```

### 3.2 Sign Up for Vercel
1. Go to: https://vercel.com
2. Click "Sign Up"
3. Sign up with GitHub

### 3.3 Deploy
1. Click "Add New..." → "Project"
2. Import your `meeting-minder` repository
3. Click "Import"
4. **Framework Preset**: Other
5. **Root Directory**: Leave as `./`
6. Click "Deploy"

### 3.4 Get Your URL
- Vercel will give you a URL like: `https://meeting-minder.vercel.app`
- **This is your public URL!** 🎉

---

## ✅ Step 4: Test Your Deployment

### 4.1 Test Backend
Open in browser:
```
https://YOUR-RENDER-URL.onrender.com/
```

You should see:
```json
{
  "status": "running",
  "service": "Meeting Minder API (Groq)",
  "endpoints": ["/upload_docs", "/summarize"]
}
```

### 4.2 Test Frontend
1. Open: `https://YOUR-VERCEL-URL.vercel.app`
2. Paste sample transcript
3. Click "Analyze Meeting"
4. Wait 5-10 seconds (first request may be slow)
5. See results!

---

## 🎁 What You Get (100% FREE)

### Backend (Render)
- ✅ Free subdomain: `https://your-app.onrender.com`
- ✅ 750 hours/month (enough for always-on)
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ⚠️ Sleeps after 15 min inactivity (wakes up in ~30 seconds)

### Frontend (Vercel)
- ✅ Free subdomain: `https://your-app.vercel.app`
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ✅ Always on (no sleep)

---

## 🐛 Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify `GROQ_API_KEY` is set correctly
- Make sure `requirements-lite.txt` exists

### Frontend can't connect to backend
- Check API_BASE URL in `index.html`
- Make sure it's the Render URL (not localhost)
- Check CORS is enabled in backend

### "Service Unavailable" on first request
- Render free tier sleeps after 15 min
- First request wakes it up (~30 seconds)
- Subsequent requests are fast

---

## 💡 Pro Tips

### Keep Backend Awake
Add this free service to ping your backend every 14 minutes:
1. Go to: https://uptimerobot.com
2. Add monitor for your Render URL
3. Check every 5 minutes
4. **Result**: Backend never sleeps!

### Custom Domain (Optional)
Both Render and Vercel support custom domains for free:
1. Buy domain (e.g., from Namecheap ~$10/year)
2. Add to Render/Vercel settings
3. Update DNS records
4. Get: `https://meeting-minder.yourdomain.com`

---

## 📊 Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Deploy backend to Render
- [ ] Add GROQ_API_KEY to Render
- [ ] Copy Render URL
- [ ] Update API_BASE in index.html
- [ ] Push updated code to GitHub
- [ ] Create Vercel account
- [ ] Deploy frontend to Vercel
- [ ] Test backend health check
- [ ] Test frontend with sample transcript
- [ ] Share your public URL! 🎉

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Public backend API: `https://your-app.onrender.com`
- ✅ Public frontend UI: `https://your-app.vercel.app`
- ✅ 100% FREE hosting
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub

**Share your URL with anyone and they can use your meeting analyzer!**

---

## 📞 Need Help?

If you get stuck:
1. Check Render logs (click on your service → Logs)
2. Check Vercel deployment logs
3. Verify environment variables are set
4. Make sure API_BASE URL is correct

---

**Ready to deploy? Follow the steps above and you'll have a public URL in 10 minutes!** 🚀
