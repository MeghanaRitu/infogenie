import streamlit as st
import os
import requests
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Streamlit setup
st.set_page_config(page_title="InfoGenie", layout="wide")
st.title("InfoGenie - Ask Your Questions About Valtech")

VECTOR_STORE_DIR = "faiss_index"
embedding = OllamaEmbeddings(model="llama3")

# Load FAISS vector store
@st.cache_resource(show_spinner="Loading document index...")
def get_vectorstore():
    return FAISS.load_local(VECTOR_STORE_DIR, embeddings=embedding, allow_dangerous_deserialization=True)

# Ask Ollama (non-streaming)
def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2
    }
    try:
        res = requests.post(url, json=payload)
        return res.json().get("response", "").strip()
    except Exception as e:
        return f" Failed to connect to Ollama: {e}"

# Load vectorstore
db = get_vectorstore()

# Session state chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("### 💬 Chat")
for q, a in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        st.markdown(a)

# Input from user
user_input = st.chat_input("Type your question here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        relevant_docs = db.similarity_search(user_input, k=4)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        sources = set(doc.metadata.get("source", "Unknown") for doc in relevant_docs)

        prompt = (
            "You are an AI assistant helping to summarize and answer questions "
            "based on employee policy and user guide documents.\n"
            "Each section includes its source name in the format [SOURCE: filename]. "
            "Use only the relevant information from these to answer the user's question.\n\n"
            f"{context}\n\n"
            f"User: {user_input}"
        )

        answer = ask_ollama(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)
        st.caption(f"📎 Source(s): {', '.join(sources)}")

    st.session_state.history.append((user_input, answer))