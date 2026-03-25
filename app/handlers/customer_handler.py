from app.services.product_service import get_products_by_owner
from app.services.ai_service import generate_response
from app.utils.session_store import customer_sessions

def handle_customer_message(owner, from_number: str, message: str):
    products = get_products_by_owner(owner["id"])

    if not products:
        return "Maaf, saat ini belum ada produk tersedia."

    # Inisialisasi history untuk nomor ini jika belum ada
    if from_number not in customer_sessions:
        customer_sessions[from_number] = []
        
    history = customer_sessions[from_number]

    response_text = generate_response(message, products, owner["business_name"], history)

    # Simpan percakapan ke history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response_text})
    
    # Batasi history maksimal 10 pesan terakhir agar konteks tidak terlalu panjang dan token hemat
    if len(history) > 10:
        customer_sessions[from_number] = history[-10:]

    return response_text