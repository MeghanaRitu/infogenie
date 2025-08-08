import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_ollama import OllamaEmbeddings
from file_reader import extract_text_from_file, get_supported_files

FOLDER_PATH = r"C:\Users\Meghana.R\Downloads\infogenie\documents"  #change as per your file structure
VECTOR_STORE_DIR = "faiss_index"

embedding = OllamaEmbeddings(model="llama3")

def load_documents():
    file_paths = get_supported_files(FOLDER_PATH)
    docs = []
    for path in file_paths:
        content = extract_text_from_file(path)
        doc = Document(page_content=content, metadata={"source": os.path.basename(path)})
        docs.append(doc)
    return docs

def create_vectorstore():
    raw_docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = []
    for doc in raw_docs:
        for chunk in splitter.split_text(doc.page_content):
            chunks.append(Document(page_content=chunk, metadata=doc.metadata))
    db = FAISS.from_documents(chunks, embedding)
    db.save_local(VECTOR_STORE_DIR)
    print("FAISS index created and saved.")

if __name__ == "__main__":
    create_vectorstore()