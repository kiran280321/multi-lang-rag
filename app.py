import streamlit as st
from langdetect import detect
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
import chromadb
from PyPDF2 import PdfReader
model = SentenceTransformer("sentence-transformers/LaBSE")
client = chromadb.Client()
collection = client.get_or_create_collection("rag-docs")
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
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            collection.add(documents=[chunk], embeddings=[emb.tolist()], ids=[f"doc_{i}"])
        st.success("Document embedded and stored!")
        query = st.text_input("Ask a question based on the uploaded document")
        if query:
            translated_query = GoogleTranslator(source='auto', target=doc_lang).translate(query)
            query_embedding = model.encode([translated_query])[0]
            results = collection.query(query_embeddings=[query_embedding.tolist()], n_results=3)
            context = "\n".join(results["documents"][0])
            st.markdown("### 📘 Retrieved Context")
            st.write(context)
            translated_context = GoogleTranslator(source=doc_lang, target=preferred_lang).translate(context)
            st.markdown("### 🌐 Translated Answer")
            st.write(translated_context)
