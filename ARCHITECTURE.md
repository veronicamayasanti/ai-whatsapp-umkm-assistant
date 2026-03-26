# Arsitektur Proyek - AI WhatsApp UMKM Assistant 🏗️

Dokumen ini menjelaskan bagaimana komponen-komponen dalam aplikasi ini saling berinteraksi.

## Aliran Data (Data Flow)

Aplikasi ini menggunakan model **Webhook-driven Architecture**:

1.  **WhatsApp User**: Mengirim pesan ke nomor WhatsApp Business (via Twilio Sandbox).
2.  **Twilio**: Menerima pesan dan mengirimkan `HTTP POST` request ke URL Webhook yang dikonfigurasi (ngrok).
3.  **FastAPI (app/api.py)**: Menerima request dari Twilio, mengekstrak nomor pengirim dan isi pesan.
4.  **Handler Selection**:
    *   Jika nomor pengirim = Nomor Owner → Gunakan `admin_handler.py`.
    *   Jika nomor pengirim != Nomor Owner → Gunakan `customer_handler.py`.
5.  **Logic Processing**:
    *   **Admin**: Bisa berupa perintah manual (`/add_product`) atau bahasa natural (AI-powered intent recognition).
    *   **Customer**: AI meninjau daftar produk dari database dan membalas pertanyaan pelanggan.
6.  **OpenAI GPT-4o**: Digunakan oleh handler untuk memahami konteks atau menghasilkan respon yang ramah.
7.  **Database (SQLite)**: Menyimpan data owner dan produk.
8.  **Twilio Response**: FastAPI mengirimkan balik format TwiML ke Twilio untuk ditampilkan sebagai pesan balasan di WhatsApp.

## Struktur Komponen

*   **`app/api.py`**: Entry point untuk webhook.
*   **`app/handlers/`**: Berisi logika pemisahan peran antara Admin dan Customer.
*   **`app/services/`**:
    *   `ai_service.py`: Logika integrasi dengan OpenAI SDK.
    *   `product_service.py`: CRUD produk ke database.
    *   `owner_service.py`: Manajemen data UMKM (Owner).
*   **`app/utils/`**: Helper untuk parsing pesan dan validasi data.
*   **`data/`**: Lokasi file database SQLite (`umkm.db`).

## Keamanan & Sesi

*   **Session Management**: Menggunakan dictionary sederhana di memori untuk menyimpan histori percakapan dalam satu sesi.
*   **Environment Variables**: Semua API Key disimpan di file `.env` yang tidak di-commit ke Git.
