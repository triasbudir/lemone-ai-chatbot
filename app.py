"""
app.py
======
Aplikasi Streamlit untuk Lemone AI Chatbot.
Jalankan dengan: streamlit run app.py
"""

import streamlit as st
import sys
import os

# Tambahkan folder src ke path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from chatbot import LemoneChatbot

# ── Konfigurasi halaman ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lemone AI Assistant",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── CSS Kustom ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #FAFAFA; }
    .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
    .bot-header {
        background: linear-gradient(135deg, #FF6B35, #FF8C61);
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .source-box {
        background: #F0F4FF;
        border-left: 3px solid #4A90D9;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 12px;
        color: #555;
        margin-top: 4px;
    }
    .badge-online {
        display: inline-block;
        background: #2ECC71;
        color: white;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 99px;
    }
</style>
""", unsafe_allow_html=True)


# ── Inisialisasi chatbot (cached agar tidak reload setiap interaksi) ──────────
@st.cache_resource(show_spinner="Memuat Lemone AI Assistant...")
def get_chatbot():
    return LemoneChatbot()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://via.placeholder.com/200x60/FF6B35/white?text=LEMONE", use_column_width=True)
    st.markdown("### 🤖 Lemone AI Assistant")
    st.markdown("""
    Halo! Saya adalah asisten AI untuk **PT Lemone Surya Indonesia**.

    Saya bisa membantu Anda dengan:
    - 📦 Informasi produk & kategori
    - 💰 Harga grosir & diskon
    - 🚚 Pengiriman & logistik
    - 🔄 Kebijakan retur
    - ✂️ Custom order / private label
    - 📋 Cara menjadi reseller
    """)

    st.divider()

    # Contoh pertanyaan
    st.markdown("#### 💡 Coba tanyakan:")
    sample_questions = [
        "Berapa harga grosir kaos polos?",
        "Bagaimana cara menjadi reseller?",
        "Apakah ada minimum order?",
        "Bisa custom logo merek sendiri?",
        "Kebijakan retur seperti apa?",
        "Berapa diskon untuk order besar?"
    ]

    for q in sample_questions:
        if st.button(q, key=f"sample_{q}", use_container_width=True):
            st.session_state["quick_question"] = q

    st.divider()

    # Tombol reset
    if st.button("🗑️ Reset Percakapan", use_container_width=True, type="secondary"):
        st.session_state["messages"] = []
        st.session_state["quick_question"] = ""
        if "chatbot" in st.session_state:
            st.session_state.chatbot_instance = None
        st.rerun()

    st.markdown("""
    <small>
    📍 Tanah Abang, Jakarta Pusat<br>
    ✉️ cs@lemonesurya.co.id<br>
    🕐 Sen-Jum 08.00–17.00 WIB
    </small>
    """, unsafe_allow_html=True)


# ── Header utama ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="bot-header">
    <h3 style="margin:0">👗 Lemone AI Assistant</h3>
    <p style="margin:4px 0 0 0; opacity:0.9; font-size:14px">
        Asisten resmi PT Lemone Surya Indonesia
        <span class="badge-online">● Online</span>
    </p>
</div>
""", unsafe_allow_html=True)


# ── Inisialisasi state ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = ""

# Pesan selamat datang
if not st.session_state.messages:
    welcome = (
        "Halo! Selamat datang di **Lemone AI Assistant** 👗\n\n"
        "Saya siap membantu Anda dengan informasi seputar produk, harga grosir, "
        "cara order, pengiriman, dan layanan PT Lemone Surya Indonesia.\n\n"
        "Silakan ajukan pertanyaan Anda!"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome})


# ── Load chatbot ──────────────────────────────────────────────────────────────
try:
    chatbot = get_chatbot()
except FileNotFoundError as e:
    st.error(f"⚠️ {e}")
    st.info("Jalankan perintah berikut di terminal untuk membangun vector store:\n\n```bash\npython src/build_vectorstore.py\n```")
    st.stop()


# ── Tampilkan riwayat chat ────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👗" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

        # Tampilkan sumber jika ada
        if msg.get("sources"):
            with st.expander("📄 Lihat sumber informasi", expanded=False):
                for i, src in enumerate(msg["sources"][:2], 1):
                    st.markdown(f'<div class="source-box"><b>Sumber {i}:</b> {src[:300]}...</div>',
                                unsafe_allow_html=True)


# ── Input pengguna ────────────────────────────────────────────────────────────
# Handle quick question dari sidebar
user_input = st.session_state.pop("quick_question", "") or ""

chat_input = st.chat_input("Ketik pertanyaan Anda di sini...")
if chat_input:
    user_input = chat_input

if user_input:
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Dapatkan respons chatbot
    with st.chat_message("assistant", avatar="👗"):
        with st.spinner("Sedang mencari informasi..."):
            response = chatbot.chat(user_input)
            answer = response["answer"]
            sources = response["sources"]

        st.markdown(answer)

        # Tampilkan sumber
        if sources:
            with st.expander("📄 Lihat sumber informasi", expanded=False):
                for i, src in enumerate(sources[:2], 1):
                    st.markdown(
                        f'<div class="source-box"><b>Sumber {i}:</b> {src[:300]}...</div>',
                        unsafe_allow_html=True
                    )

    # Simpan ke riwayat
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
