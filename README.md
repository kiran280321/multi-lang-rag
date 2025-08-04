🌍 Multi-Language RAG System

This is a multilingual Retrieval-Augmented Generation (RAG) system built for the Nervesparks India Pvt Ltd Software Developer assignment. It allows users to upload documents in various languages and ask questions in any language, with the response provided in their preferred language.

---

🔗 Live Demo
https://multi-lang-raggit-wncdrmeq9y6tn5ef62sxp5.streamlit.app/

🔗 GitHub Repository
https://github.com/kiran280321/multi-lang-rag

---

🚀 Features

- Upload `.txt` or `.pdf` documents in any supported language
- Automatically detects document language
- Cross-lingual search: Ask in any language, get answers from documents in another
- Translates response to user's preferred language
- Vector search powered by FAISS
- Embeddings via multilingual SentenceTransformer: `LaBSE`

---

🛠️ Setup Instructions

1. Clone the repo:
   git clone https://github.com/kiran280321/multi-lang-rag.git
   cd multi-lang-rag

2. Create and activate virtual environment:
   python -m venv venv
   venv\\Scripts\\activate   # On Windows
   source venv/bin/activate  # On Mac/Linux

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Streamlit app:
   streamlit run app.py

---

📁 Folder Structure

multi-lang-rag/
├── app.py               # Streamlit app with FAISS vector store
├── requirements.txt     # All dependencies
├── README.txt           # This file
└── data/
    └── example.txt      # Sample Hindi input for testing

---

🧪 Test Case

- Upload: `data/example.txt` (Hindi)
- Query: `"भारत में शिक्षा प्रणाली के बारे में बताएं"` (in Hindi)
- Preferred Language: English
- Expected: Context retrieved from document, translated answer in English

---

📄 Assumptions

- Each document is in a single language
- Basic character-level chunking (500 characters)
- Google Translate used for multilingual handling
- FAISS used for compatibility with Streamlit Cloud

---

🧠 Summary of Approach

1. User uploads `.txt` or `.pdf` → text is extracted & language detected
2. Document is split into chunks → embedded using `LaBSE`
3. Chunks are indexed in FAISS
4. User query is translated to document's language, embedded, and searched in FAISS
5. Top matches are translated to preferred language and shown to the user

---

🤖 Optional Improvements

- Add GPT-4 / HuggingFace generation on top of context
- Replace Google Translate with high-quality transformers like `opus-mt`
- Cultural context scoring or region-specific translation tuning
"""

