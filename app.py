import streamlit as st
from langdetect import detect
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import faiss
import numpy as np

# Initialize model and FAISS index
model = SentenceTransformer("sentence-transformers/LaBSE")
index = faiss.IndexFlatL2(768)  # 768 = LaBSE embedding dimension
chunk_store = []

st.title("🌍 Multi-Language RAG System")

uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=["txt", "pdf"])
preferred_lang = st.selectbox("Select your preferred language", ["en", "hi", "te", "fr", "es", "de"])

if uploaded_file:
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    else:
        text = uploaded_file.read().decode()

    if not text.strip():
        st.error("Could not extract text from the document.")
    else:
        doc_lang = detect(text)
        st.write(f"Detected document language: `{doc_lang}`")

        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        embeddings = model.encode(chunks)

        for chunk, emb in zip(chunks, embeddings):
            index.add(np.array([emb], dtype='float32'))
            chunk_store.append(chunk)

        st.success("Document embedded and stored!")

        query = st.text_input("Ask a question based on the uploaded document")
        if query:
            translated_query = GoogleTranslator(source='auto', target=doc_lang).translate(query)
            query_embedding = model.encode([translated_query])[0]

            D, I = index.search(np.array([query_embedding], dtype='float32'), 3)
            context = "\n".join([chunk_store[i] for i in I[0]])

            st.markdown("### 📘 Retrieved Context")
            st.write(context)

            translated_context = GoogleTranslator(source=doc_lang, target=preferred_lang).translate(context)
            st.markdown("### 🌐 Translated Answer")
            st.write(translated_context)
