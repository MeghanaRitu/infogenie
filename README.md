# infogenie
AI First Hackathon
Idea: InfoGenie – A Conversational AI for Internal Knowledge Access

Objective
The objective of InfoGenie is to streamline employee access to internal organizational knowledge using a conversational AI assistant. Instead of navigating multiple portals, internal wikis, or interrupting colleagues for routine queries, employees can simply interact with InfoGenie to retrieve accurate, real-time information regarding company policies, processes, or documentation. The goal is to reduce information retrieval time, standardize responses, and improve productivity across departments.

Implementation
InfoGenie is built using Ollama, a framework for running lightweight local LLMs. We use LangChain to orchestrate a Retrieval-Augmented Generation (RAG) pipeline, enabling InfoGenie to respond to user questions with accurate, document-grounded answers.

Tech Stack
Ollama + LLaMA 3 → Lightweight local LLM inference
LangChain → RAG pipeline orchestration
FAISS → Fast vector-based document similarity search
Streamlit → Chat UI frontend
Pytesseract + PyMuPDF → OCR for scanned PDFs
Python → Backend logic

Applications
InfoGenie is designed to assist employees across all departments, including HR, IT, Finance, Operations, and Delivery to fetch details like HR policies, forms, security measures etc. It acts as a single point of interaction for routine internal queries, reducing dependency on Teams threads and documentation browsing.

InfoGenie has the potential to evolve into a fully self-hosted, enterprise-ready internal knowledge assistant that boosts employee productivity and enables instant access to organizational intelligence.
