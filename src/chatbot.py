import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
VECTORSTORE_DIR = "data/faiss_db"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)

class LemoneChatbot:
    def __init__(self):
        self.vectorstore = load_vectorstore()
        self.history = []

    def chat(self, user_message):
        docs = self.vectorstore.similarity_search(user_message, k=4)
        context = chr(10).join([d.page_content for d in docs])
        system = "Kamu adalah Lemone AI Assistant untuk PT Lemone Surya Indonesia, fashion grosir B2B. Jawab dalam Bahasa Indonesia yang ramah dan profesional. Gunakan informasi berikut sebagai referensi: " + context
        messages = [{"role": "system", "content": system}]
        messages += self.history
        messages.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(model="llama3-8b-8192", messages=messages, temperature=0.3)
        answer = response.choices[0].message.content
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": answer})
        if len(self.history) > 10:
            self.history = self.history[-10:]
        return {"answer": answer, "sources": [d.page_content for d in docs]}

    def reset_memory(self):
        self.history = []
