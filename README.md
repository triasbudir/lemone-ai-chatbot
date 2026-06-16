# 👗 Lemone AI Chatbot

🔗 **Live Demo:** [https://lemone-ai-chatbot.streamlit.app](https://lemone-ai-chatbot.streamlit.app) — Customer Service Berbasis RAG

> **Portfolio Project** — AI Engineer Application  
> Demonstrasi implementasi RAG (Retrieval-Augmented Generation) untuk
> customer service fashion grosir B2B menggunakan LangChain, ChromaDB, dan OpenAI API.

---

## 🏗️ Arsitektur Sistem

```
User (Streamlit UI)
      │
      ▼
  [Query masuk]
      │
      ▼
  LangChain ConversationalRetrievalChain
      │
      ├──► ChromaDB Vector Store ──► similarity search ──► top-K chunks
      │                                                          │
      └──────────────────────────────────────────────────────────┘
                                                                 │
                                                                 ▼
                                                         OpenAI GPT-3.5
                                                    (generate jawaban dari konteks)
                                                                 │
                                                                 ▼
                                                    Jawaban + sumber ditampilkan
```

### Komponen Utama

| Komponen | Teknologi | Fungsi |
|---|---|---|
| LLM | OpenAI GPT-3.5-turbo | Generate respons natural |
| Embedding | OpenAI text-embedding-3-small | Konversi teks ke vektor |
| Vector Store | ChromaDB | Simpan & cari chunk knowledge base |
| RAG Chain | LangChain | Orkestrasi retrieval + generation |
| Memory | ConversationBufferWindowMemory | Ingat 5 pesan terakhir |
| UI | Streamlit | Interface chat web |

---

## 📁 Struktur Project

```
lemone-chatbot/
├── app.py                      # Aplikasi Streamlit (UI)
├── requirements.txt            # Dependencies Python
├── .env.example                # Template environment variables
├── README.md                   # Dokumentasi ini
│
├── src/
│   ├── chatbot.py              # Core RAG engine (LangChain chain)
│   └── build_vectorstore.py    # Script build ChromaDB
│
└── data/
    ├── knowledge_base.txt      # Knowledge base FAQ Lemone
    └── chroma_db/              # Vector store (auto-generated)
```

---

## ⚙️ Cara Setup & Menjalankan

### 1. Clone dan install dependencies

```bash
git clone https://github.com/username/lemone-chatbot.git
cd lemone-chatbot

# Buat virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# atau
venv\Scripts\activate           # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Konfigurasi API Key

```bash
# Salin template env
cp .env.example .env

# Edit .env dan isi OPENAI_API_KEY kamu
# OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

Dapatkan API key di: https://platform.openai.com/api-keys

### 3. Build Vector Store (sekali saja)

```bash
python src/build_vectorstore.py
```

Output yang diharapkan:
```
=======================================================
  LEMONE AI – Membangun Vector Store
=======================================================
[1/4] Membaca knowledge base...
      ✔ 1 dokumen dimuat
[2/4] Memecah teks menjadi chunks...
      ✔ 47 chunks dibuat
[3/4] Membuat embeddings (OpenAI)...
[4/4] Menyimpan ke ChromaDB di 'data/chroma_db'...

=======================================================
  ✅ Vector store berhasil dibuat!
     Total chunks tersimpan: 47
     Lokasi: data/chroma_db
=======================================================
```

### 4. Jalankan Aplikasi

```bash
streamlit run app.py
```

Buka browser di: http://localhost:8501

---

## 🚀 Deploy ke Streamlit Cloud (Gratis)

1. **Push project ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "feat: initial lemone ai chatbot"
   git remote add origin https://github.com/username/lemone-chatbot.git
   git push -u origin main
   ```

2. **Buka** https://share.streamlit.io dan login dengan GitHub

3. **Klik "New app"** → pilih repository dan branch

4. **Tambahkan Secret** di Streamlit Cloud:
   - Settings → Secrets
   - Tambahkan:
     ```toml
     OPENAI_API_KEY = "sk-xxxxxxxxxx"
     OPENAI_MODEL = "gpt-3.5-turbo"
     BOT_NAME = "Lemone AI Assistant"
     ```

5. **Tambahkan startup command** di `packages.txt` (buat file baru):
   ```
   # packages.txt — kosongkan atau tambahkan jika perlu apt packages
   ```

6. **Deploy!** Streamlit Cloud akan otomatis menjalankan build.

> ⚠️ Catatan: Karena ChromaDB tersimpan lokal, perlu modifikasi untuk
> production scale. Solusinya: gunakan Pinecone (cloud vector store)
> atau simpan DB ke persistent storage.

---

## 💡 Fitur & Kemampuan

- ✅ **RAG Pipeline** — Jawaban berdasarkan knowledge base, bukan halusinasi
- ✅ **Conversation Memory** — Ingat konteks percakapan sebelumnya
- ✅ **Source Transparency** — Tampilkan sumber informasi yang digunakan
- ✅ **Quick Questions** — Tombol pertanyaan cepat di sidebar
- ✅ **Custom System Prompt** — Karakter dan persona bot yang konsisten
- ✅ **Reset Conversation** — Mulai percakapan baru kapan saja
- ✅ **Graceful Error Handling** — Pesan error yang informatif

---

## 🔧 Kustomisasi

### Menambah knowledge base
Edit file `data/knowledge_base.txt`, lalu jalankan ulang:
```bash
python src/build_vectorstore.py
```

### Mengganti model
Di file `.env`:
```env
OPENAI_MODEL=gpt-4o   # Lebih canggih tapi lebih mahal
```

### Mengganti karakter bot
Di `src/chatbot.py`, edit bagian `SYSTEM_TEMPLATE`.

---

## 📊 Estimasi Biaya API

Menggunakan GPT-3.5-turbo + text-embedding-3-small:
- Embedding (build sekali): ~$0.001 untuk 50 chunks
- Per percakapan (10 pesan): ~$0.01 - $0.05
- Sangat ekonomis untuk demo dan portofolio

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** — RAG orchestration
- **OpenAI API** — LLM + Embeddings
- **ChromaDB** — Local vector store
- **Streamlit** — Web UI
- **python-dotenv** — Environment management

---

## 👨‍💻 Author

Dibuat sebagai portfolio project untuk posisi **AI Engineer**  
PT Lemone Surya Indonesia — 2024

---

*Proyek ini mendemonstrasikan kemampuan dalam: LangChain, RAG Pipeline,
OpenAI API, ChromaDB, Prompt Engineering, dan deployment aplikasi AI.*
