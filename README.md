
# 🧠 RAG Chatbot 

---

## 🛠️ Tech Stack

- Python 3.11+
- FastAPI (`uvicorn`)
- Streamlit
- FAISS
- Sambanova cloud (for LLM)
- Hugging Face Embeddings

---

## 📁 Project Structure

```
.
├── backend/
│   └── app.py                  # FastAPI backend
├── frontend/
│   └── streamlit_app.py        # Streamlit UI
├── data/
│   └── pdfs/                   # PDF and JSON data files
├── embeddings/
│   └── faiss_index/            # FAISS vector store
├── requirements.txt
├── .env                        # API keys (ignored in git)
```

---

## ✅ Prerequisites

- Python 3.11+
- pip

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/mdhuzaifapatel/rag-chatbot-alltius.git 
cd rag-chatbot-alltius
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On Linux/macOS
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Setup API Keys

Create a `.env` file in the root directory:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
SAMBANOVA_API_KEY=your_sambanova_api_key_here
```

> ⚠️ Never share or commit your `.env` file.

---

## ▶️ Running the Application

### 1. Start the FastAPI backend

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: [http://localhost:8000](http://localhost:8000)

---

### 2. In a new terminal, start the Streamlit frontend

```bash
streamlit run frontend/streamlit_app.py
```

Frontend will open on: [http://localhost:8501](http://localhost:8501)

---
