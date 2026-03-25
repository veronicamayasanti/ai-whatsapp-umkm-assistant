# AI WhatsApp UMKM Assistant 🥘🚀

Asisten WhatsApp berbasis AI (GPT-4o) untuk membantu UMKM mengelola stok produk dan melayani pelanggan secara otomatis. 

Proyek ini dirancang sebagai solusi efisiensi bagi pemilik usaha makanan/minuman agar dapat melakukan pengelolaan produk (CRUD) langsung melalui chat WhatsApp, serta memberikan pelayanan pelanggan yang ramah dan cerdas 24/7.

## ✨ Fitur Utama
- **AI-Powered Customer Service**: Menjawab pertanyaan pelanggan tentang menu, harga, dan deskripsi produk secara natural menggunakan OpenAI GPT-4o.
- **WhatsApp Admin CRUD**: Pemilik dapat menambah, melihat, mengupdate, dan menghapus produk hanya dengan mengirimkan perintah chat atau bahasa natural ke Bot.
- **Conversational Memory**: Bot memiliki "ingatan" sehingga dapat memahami konteks percakapan sebelumnya dalam satu sesi chat.
- **Welcome Message Dinamis**: Salam pembuka otomatis yang menyebutkan nama bisnis yang diambil langsung dari database.
- **WhatsApp Integration**: Menggunakan Twilio API untuk menghubungkan logika Python ke aplikasi WhatsApp secara real-time.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Framework**: FastAPI (untuk Webhook)
- **AI Model**: OpenAI GPT-4o-mini
- **Database**: SQLite (Ringan dan portabel)
- **API Provider**: Twilio WhatsApp API
- **Tunneling**: ngrok (untuk pengujian lokal)

## 📁 Struktur Project
```text
ai-whatsapp-umkm-assistant/
├── app/
│   ├── api.py            # Entry point FastAPI Webhook
│   ├── main.py           # Script simulasi lokal
│   ├── handlers/         # Logika pesan Admin & Customer
│   ├── services/         # Integrasi AI & Database
│   ├── database/         # Konfigurasi SQLite
│   └── utils/            # Parser & Validator
├── data/                 # Folder Database
├── .env.example          # Template API Key
├── .gitignore            # File pengecualian git
├── requirements.txt      # Daftar dependensi
└── README.md
```

## 🚀 Cara Menjalankan

### 1. Persiapan Environment
```bash
# Clone repository
git clone https://github.com/username/ai-whatsapp-umkm-assistant.git
cd ai-whatsapp-umkm-assistant

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate untuk Windows

# Install dependensi
pip install -r requirements.txt
```

### 2. Konfigurasi API
Buat file baru bernama `.env` (copy dari `.env.example`) dan masukkan API Key Anda:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Menjalankan Server
```bash
# Jalankan server FastAPI
python -m uvicorn app.api:app --host 0.0.0.0 --port 8008 --reload
```

### 4. Menghubungkan ke WhatsApp (ngrok)
Gunakan ngrok untuk membuat server lokal Anda dapat diakses oleh Twilio:
```bash
ngrok http 8008
```
Salin URL publik dari ngrok (misal: `https://abcd.ngrok-free.dev`) dan masukkan ke **Twilio Sandbox Settings** sebagai Webhook URL: `https://abcd.ngrok-free.dev/whatsapp`.

## 📝 Catatan Portofolio
Proyek ini dibuat untuk mendemonstrasikan kemampuan integrasi LLM (Large Language Model) dengan aplikasi komunikasi dunia nyata (WhatsApp). Fokus utamanya adalah pada **Logika Handler**, **Context Management**, dan **Prompt Engineering**.

---
*Dibuat oleh [Nama Anda] sebagai bagian dari portofolio AI Engineering.*
