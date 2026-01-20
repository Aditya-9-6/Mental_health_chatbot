import json
import streamlit as st
import os  # Added import
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from constants import CRISIS_KEYWORDS

# Load Knowledge Base
@st.cache_resource
def load_knowledge_base():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__)) # Added path logic
        kb_path = os.path.join(current_dir, "knowledge_base.json")
        with open(kb_path, "r") as f:
            data = json.load(f)
        documents = []
        for item in data:
            page_content = f"Question: {item['question']}\nAnswer: {item['answer']}"
            metadata = {"question": item['question']}
            documents.append(Document(page_content=page_content, metadata=metadata))
        return documents
    except FileNotFoundError:
        st.error("knowledge_base.json not found. Please create it first.")
        return []

# Initialize Vector Store
@st.cache_resource
def get_vector_store(_documents, _api_key):
    if not _documents:
        return None
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=_api_key)
        vectorstore = FAISS.from_documents(_documents, embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {e}")
        return None

def check_safety(user_input):
    for keyword in CRISIS_KEYWORDS:
        if keyword in user_input.lower():
            return False
    return True
