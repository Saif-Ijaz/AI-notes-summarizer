# 📘 AI Notes Summarizer & Q&A

An AI-powered study notes assistant that summarizes PDF documents and answers questions using Groq AI and semantic search.

## 🚀 Features

- 📄 Upload PDF study notes
- 🤖 Generate AI-based summaries using Groq LLM
- 💡 Ask questions from your notes using semantic search (ChromaDB)
- 🗄️ Store documents in MongoDB Atlas
- ⚡ Fast and lightweight — runs with a single command

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend + Backend | Streamlit |
| AI Model | Groq API (compound-mini) |
| Vector Search | ChromaDB + Sentence Transformers |
| Database | MongoDB Atlas |
| PDF Parsing | PyPDF |

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Saif-Ijaz/AI-notes-summarizer.git
cd AI-notes-summarizer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=notes_db
```

- Get Groq API key: https://console.groq.com/keys
- Get MongoDB URI: https://cloud.mongodb.com

### 5. Run the app
```bash
streamlit run app/app.py
```

Open browser at: **http://localhost:8501**

## 📂 Project Structure

```
AI-notes-summarizer/
├── app/
│   ├── app.py          ← Main Streamlit app
│   ├── summarizer.py   ← Groq AI summarization
│   ├── qa.py           ← Groq AI Q&A
│   ├── embeddings.py   ← ChromaDB semantic search
│   ├── database.py     ← MongoDB connection
│   ├── config.py       ← Environment variables
│   └── logger.py       ← Logging
├── .env                ← API keys (not pushed)
├── requirements.txt
└── README.md
```

## 🔒 Security

- `.env` file is excluded from Git
- Never share your API keys publicly

## 👤 Author

**Saif Ijaz** — [GitHub](https://github.com/Saif-Ijaz)
