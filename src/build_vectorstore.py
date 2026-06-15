import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

KNOWLEDGE_BASE_PATH = "data/knowledge_base.txt"
VECTORSTORE_DIR     = "data/faiss_db"

def build_vectorstore():
    print("=" * 55)
    print("  LEMONE AI – Membangun Vector Store")
    print("=" * 55)

    print("\n[1/4] Membaca knowledge base...")
    loader = TextLoader(KNOWLEDGE_BASE_PATH, encoding="utf-8")
    documents = loader.load()
    print(f"      ✔ {len(documents)} dokumen dimuat")

    print("[2/4] Memecah teks menjadi chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(documents)
    print(f"      ✔ {len(chunks)} chunks dibuat")

    print("[3/4] Membuat embeddings (HuggingFace - GRATIS)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print(f"[4/4] Menyimpan ke FAISS di '{VECTORSTORE_DIR}'...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)

    print("\n" + "=" * 55)
    print(f"  ✅ Vector store berhasil dibuat!")
    print(f"     Total chunks: {len(chunks)}")
    print("=" * 55)

if __name__ == "__main__":
    build_vectorstore()
