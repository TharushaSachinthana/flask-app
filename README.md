# Meeting Minder 🎯

AI-powered meeting minutes and action-item extractor that combines summarization, structured information extraction, and RAG (Retrieval-Augmented Generation) capabilities using Hugging Face Inference API.

## Features

✨ **Smart Meeting Analysis**
- 3-4 sentence meeting summary (TL;DR)
- Automatic action item extraction with assignees and due dates
- Key decisions tracking
- Open questions identification
- Email-ready summary generation

🔍 **RAG-Powered Context**
- Upload company documents, policies, or contracts
- Semantic search with FAISS vector database
- Context-aware analysis using relevant document chunks

🚀 **Fast & Cost-Effective**
- Uses `google/flan-t5-small` for generation (CPU-friendly)
- `sentence-transformers/all-MiniLM-L6-v2` for embeddings
- Optimized for speed and low latency

🎨 **Premium UI**
- Dark theme with glassmorphism effects
- Responsive design
- Real-time processing with loading states
- Copy-to-clipboard functionality

## Architecture

```
Frontend (index.html)
    ↓ HTTP requests
Backend (Flask API)
    ↓ Text generation
Hugging Face Inference API
    ↓ Embeddings
FAISS Vector Database (RAG)
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Hugging Face account and API token ([Get one here](https://huggingface.co/settings/tokens))

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Windows (PowerShell):
   ```powershell
   $env:HF_TOKEN="your_huggingface_token_here"
   ```
   
   Windows (Command Prompt):
   ```cmd
   set HF_TOKEN=your_huggingface_token_here
   ```
   
   Linux/Mac:
   ```bash
   export HF_TOKEN=your_huggingface_token_here
   ```

4. **Run the Flask backend**
   ```bash
   python meeting_minder.py
   ```
   
   The API will start on `http://localhost:5000`

5. **Open the frontend**
   
   Open `index.html` in your web browser, or serve it with:
   ```bash
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

## Usage

### Basic Meeting Analysis

1. Open the web interface
2. Paste your meeting transcript in the text area
3. Click "Analyze Meeting"
4. View the extracted summary, action items, decisions, and questions

### With RAG Context (Optional)

1. Upload company documents using the "Upload Context Documents" section
2. The system will index the documents for semantic search
3. When analyzing meetings, relevant context will be automatically retrieved
4. Enable/disable RAG with the checkbox

### Copy Email Summary

Click the "Copy to Clipboard" button under the email summary to copy the formatted summary for sending to meeting attendees.

## API Documentation

### Endpoints

#### `GET /`
Health check endpoint
```json
{
  "status": "running",
  "service": "Meeting Minder API",
  "endpoints": ["/upload_docs", "/summarize"]
}
```

#### `POST /upload_docs`
Upload documents for RAG context

**Request:**
```json
{
  "docs": ["document text 1", "document text 2"]
}
```

**Response:**
```json
{
  "status": "indexed",
  "chunks": 42,
  "message": "Successfully indexed 42 document chunks"
}
```

#### `POST /summarize`
Analyze meeting transcript

**Request:**
```json
{
  "transcript": "meeting text...",
  "use_docs": true
}
```

**Response:**
```json
{
  "summary": "3-4 sentence summary...",
  "action_items": [
    {
      "task": "Complete API refactoring",
      "assignee": "John",
      "due": "December 31, 2024"
    }
  ],
  "decisions": ["Use React Native for mobile app"],
  "open_questions": ["Do we need additional backend resources?"],
  "email_summary": "Formatted email text..."
}
```

## Deployment

### Option 1: Vercel (Frontend) + Railway (Backend) ⭐ Recommended

**Deploy Backend to Railway:**
1. Create account at [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Add environment variable: `HF_TOKEN`
4. Railway will auto-detect Python and use `Procfile`

**Deploy Frontend to Vercel:**
1. Create account at [vercel.com](https://vercel.com)
2. Import project from GitHub
3. Update `API_BASE` in `index.html` to your Railway URL
4. Deploy

### Option 2: Render (Full-Stack)

1. Create account at [render.com](https://render.com)
2. Create new Blueprint instance
3. Connect your GitHub repository
4. Render will use `render.yaml` to deploy both services
5. Add `HF_TOKEN` environment variable in dashboard

### Option 3: Local with Ngrok (Testing)

1. Run Flask locally: `python meeting_minder.py`
2. In another terminal: `ngrok http 5000`
3. Update `API_BASE` in `index.html` to ngrok URL
4. Open `index.html` in browser

## Testing

### Sample Transcript

A sample meeting transcript is provided in `sample_transcript.txt`. Use it to test the application:

1. Open `sample_transcript.txt`
2. Copy the content
3. Paste into the Meeting Transcript field
4. Click "Analyze Meeting"

### Expected Output

- **Summary**: Overview of Q4 planning discussion
- **Action Items**: API refactoring (John), Dashboard mockups (Lisa), Mobile mockups (Lisa), Backend requirements doc (Mike)
- **Decisions**: Use React Native, Include dark mode in mobile
- **Open Questions**: Need for additional backend resources

## Cost & Performance

### Hugging Face Inference API
- **Free tier**: 30,000 characters/month
- **Pro tier**: $9/month for 3M characters
- Average meeting (1000 words) ≈ 5,000 characters
- Free tier = ~6 meetings/month

### Optimization Tips
1. Use caching for repeated transcripts
2. Limit `max_new_tokens` to reduce costs
3. Monitor usage in HF dashboard
4. Consider self-hosting models for high volume

## Troubleshooting

### "HF_TOKEN not set" error
- Make sure you've set the environment variable before running the app
- Verify token is valid at https://huggingface.co/settings/tokens

### CORS errors
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check that backend URL in `index.html` matches your Flask server

### Slow response times
- First request may be slow (model loading)
- Subsequent requests should be faster
- Consider upgrading to `flan-t5-base` for better quality (slower)

### Empty or malformed results
- Check that transcript has clear structure
- Try with sample transcript first
- Review Flask console logs for errors

## Project Structure

```
flask-app/
├── meeting_minder.py      # Flask backend with FAISS & HF integration
├── index.html             # Frontend UI
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── sample_transcript.txt  # Example meeting transcript
├── Procfile              # Railway/Render deployment config
├── runtime.txt           # Python version specification
├── vercel.json           # Vercel frontend config
├── render.yaml           # Render blueprint
└── README.md             # This file
```

## Technologies Used

- **Backend**: Flask, FAISS, sentence-transformers
- **AI Models**: google/flan-t5-small, all-MiniLM-L6-v2
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Deployment**: Vercel, Railway, Render

## Future Enhancements

- [ ] Multi-language support
- [ ] Speaker diarization
- [ ] Calendar integration for due dates
- [ ] Slack/Teams integration
- [ ] Audio transcription (Whisper API)
- [ ] Meeting templates
- [ ] Analytics dashboard

## License

MIT License - feel free to use for personal or commercial projects

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Flask console logs
3. Open a GitHub issue with error details

---

Built with ❤️ using Hugging Face Inference API
