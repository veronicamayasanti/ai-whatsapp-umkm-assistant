import textwrap
from app.database.models import create_tables
from app.services.owner_service import register_owner, get_owner_by_phone
from app.handlers.admin_handler import handle_admin_message
from app.handlers.customer_handler import handle_customer_message

def main():
    """
    Script simulasi untuk mencoba logika bot secara lokal tanpa WhatsApp/Twilio.
    Ubah variabel 'message' untuk mengetes berbagai skenario.
    """
    create_tables()

    # 1. Pastikan Owner sudah terdaftar (Hanya perlu sekali)
    # register_owner("Rumah Makan 3 Putri", "6283117459361")

    # 2. Konfigurasi Simulasi
    from_number = "62812879856789"  # Nomor simulasi customer
    to_number = "6283117459361"    # Nomor simulasi owner
    
    # Masukkan pesan simulasi di sini:
    message = "Halo, saya mau lihat menu makanannya dong"

    # 3. Eksekusi Logika
    owner = get_owner_by_phone(to_number)

    if owner:
        owner = dict(owner)
        if from_number == owner["phone_number"]:
            response = handle_admin_message(owner, message)
        else:
            response = handle_customer_message(owner, from_number, message)

        print("-" * 30)
        print(f"USER SAYS: {message}")
        print("-" * 30)
        print("BOT RESPONDS:")
        print(textwrap.fill(response, width=60))
        print("-" * 30)
    else:
        print(f"Owner dengan nomor {to_number} tidak ditemukan di database.")

if __name__ == "__main__":
    main()