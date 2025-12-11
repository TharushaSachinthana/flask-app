# 🎯 Meeting Minder - AI-Powered Meeting Assistant

Transform your meeting transcripts into actionable insights with AI-powered summarization, action item extraction, and RAG capabilities.

## 🌐 Live Demo

**Try it now:** [https://tharusha-meeting-minder.vercel.app/](https://tharusha-meeting-minder.vercel.app/)

**Backend API:** [https://Tharusha614.pythonanywhere.com](https://Tharusha614.pythonanywhere.com)

---

## ✨ Features

- **📋 Smart Summarization** - Get concise 3-4 sentence meeting summaries
- **✅ Action Item Extraction** - Automatically identify tasks, assignees, and due dates
- **⚡ Decision Tracking** - Capture key decisions made during meetings
- **❓ Open Questions** - Track unresolved questions and blockers
- **📚 RAG Capabilities** - Upload company documents for context-aware analysis
- **📧 Email-Ready Summaries** - One-click copy for easy sharing
- **🎨 Premium UI** - Beautiful dark theme with glassmorphism effects
- **🚀 100% FREE** - No credit card required, powered by Groq API

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask (Python)
- **AI Model:** Llama 3.3 70B (via Groq API)
- **RAG:** Keyword-based document retrieval
- **Hosting:** PythonAnywhere (Free Tier)

### Frontend
- **Tech:** HTML, CSS, JavaScript (Vanilla)
- **Styling:** Custom CSS with glassmorphism
- **Hosting:** Vercel (Free Tier)

---

## 🚀 Quick Start

### Option 1: Use the Live App (Easiest)

Just visit: **[https://tharusha-meeting-minder.vercel.app/](https://tharusha-meeting-minder.vercel.app/)**

1. Paste your meeting transcript
2. Click "Analyze Meeting"
3. Get instant AI-powered insights!

### Option 2: Run Locally

#### Prerequisites
- Python 3.10+
- Groq API key (free from [console.groq.com](https://console.groq.com))

#### Setup
```bash
# Clone the repository
git clone https://github.com/TharushaSachinthana/flask-app.git
cd flask-app

# Install dependencies
pip install -r requirements-lite.txt

# Set your Groq API key
export GROQ_API_KEY="your_groq_api_key_here"  # Linux/Mac
$env:GROQ_API_KEY="your_groq_api_key_here"   # Windows

# Run the backend
python meeting_minder_groq.py

# Open index.html in your browser
```

---

## 📖 How to Use

### 1. Upload Context Documents (Optional)
Upload company policies, contracts, or meeting notes to enhance analysis with relevant context.

### 2. Paste Meeting Transcript
Copy your meeting notes or transcript into the text area.

### 3. Analyze
Click "Analyze Meeting" and wait 5-10 seconds for AI processing.

### 4. Review Results
Get:
- **Summary:** Concise overview of the meeting
- **Action Items:** Tasks with assignees and due dates
- **Decisions:** Key decisions made
- **Open Questions:** Unresolved issues
- **Email Summary:** Ready-to-share format

---

## 🎨 Screenshots

### Main Interface
![Meeting Minder UI](https://tharusha-meeting-minder.vercel.app/)

### Features
- ✨ Premium dark theme with gradient accents
- 🔍 Real-time analysis with loading states
- 📋 Structured, easy-to-read results
- 📧 One-click copy to clipboard

---

## 🔧 API Documentation

### Base URL
```
https://Tharusha614.pythonanywhere.com
```

### Endpoints

#### Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "running",
  "service": "Meeting Minder API (Groq)",
  "endpoints": ["/upload_docs", "/summarize"],
  "version": "groq-free"
}
```

#### Upload Documents (RAG)
```http
POST /upload_docs
Content-Type: application/json

{
  "docs": ["document text 1", "document text 2"]
}
```

**Response:**
```json
{
  "status": "indexed",
  "chunks": 15,
  "message": "Successfully indexed 15 document chunks"
}
```

#### Analyze Meeting
```http
POST /summarize
Content-Type: application/json

{
  "transcript": "Meeting transcript here...",
  "use_docs": true
}
```

**Response:**
```json
{
  "summary": "Meeting summary...",
  "action_items": [
    {
      "task": "Complete API refactoring",
      "assignee": "John",
      "due": "Dec 31"
    }
  ],
  "decisions": ["Decision 1", "Decision 2"],
  "open_questions": ["Question 1"],
  "email_summary": "Email-ready text..."
}
```

---

## 🌟 Key Highlights

### Why Meeting Minder?

1. **100% Free** - No credit card required, ever
2. **Powerful AI** - Uses Llama 3.3 70B (70 billion parameters)
3. **Fast** - Results in 5-10 seconds
4. **Privacy-Focused** - Your data isn't stored
5. **Easy to Use** - No signup, just paste and analyze
6. **Production-Ready** - Deployed and accessible 24/7

### Use Cases

- 📊 **Team Standups** - Track action items and blockers
- 🤝 **Client Meetings** - Document decisions and next steps
- 📈 **Planning Sessions** - Capture priorities and timelines
- 🎓 **Lectures/Workshops** - Extract key points and takeaways
- 💼 **Board Meetings** - Summarize discussions and resolutions

---

## 🚀 Deployment

### Backend (PythonAnywhere)
- **URL:** https://Tharusha614.pythonanywhere.com
- **Hosting:** PythonAnywhere Free Tier
- **Features:** Always-on, automatic HTTPS

### Frontend (Vercel)
- **URL:** https://tharusha-meeting-minder.vercel.app
- **Hosting:** Vercel Free Tier
- **Features:** CDN, automatic deployments, custom domains

---

## 📊 Performance

- **Response Time:** 5-10 seconds (first request), 2-5 seconds (subsequent)
- **Model:** Llama 3.3 70B (70 billion parameters)
- **Accuracy:** High-quality summaries and extraction
- **Limits:** 14,400 requests/day (Groq free tier)

---

## 🛡️ Privacy & Security

- ✅ No data storage - transcripts are processed in real-time
- ✅ HTTPS encryption for all communications
- ✅ No user tracking or analytics
- ✅ Open source - inspect the code yourself

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **Groq** - For providing free, fast AI inference
- **PythonAnywhere** - For free Python hosting
- **Vercel** - For free frontend hosting
- **Llama 3.3** - For powerful language understanding

---

## 📞 Support

- **Live App:** [https://tharusha-meeting-minder.vercel.app/](https://tharusha-meeting-minder.vercel.app/)
- **GitHub:** [https://github.com/TharushaSachinthana/flask-app](https://github.com/TharushaSachinthana/flask-app)
- **Issues:** Report bugs on GitHub Issues

---

## 🎉 Try It Now!

**[Launch Meeting Minder →](https://tharusha-meeting-minder.vercel.app/)**

Transform your meetings into actionable insights in seconds!

---

<div align="center">

**Made with ❤️ using AI**

[Live Demo](https://tharusha-meeting-minder.vercel.app/) • [API Docs](#-api-documentation) • [GitHub](https://github.com/TharushaSachinthana/flask-app)

</div>
