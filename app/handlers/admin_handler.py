from app.utils.parser import (
    parse_add_product,
    parse_delete_product,
    parse_update_product
)
from app.services.product_service import add_product
from app.utils.validator import validate_product_data
from app.services.product_service import get_products_by_owner, format_products
from app.services.product_service import delete_product, update_product
from app.utils.session_store import sessions
from app.services.ai_service import parse_admin_intent, safe_parse_json, generate_response

def handle_admin_message(owner, message: str):
    owner_id = owner["id"]
    # ambil session atau buat baru
    if owner_id not in sessions:
        sessions[owner_id] = {"history": []}
    session = sessions[owner_id]
    
    if "history" not in session:
        session["history"] = []
    
    history = session["history"]

    # 🔥 HANDLE KONFIRMASI DELETE
    if "pending_delete" in session:
        print(f"Pending delete found for session {owner_id}: {session['pending_delete']}")
        if message.lower() == "yes":
            product_id = session.pop("pending_delete")
            print(f"Deleting product {product_id} for owner {owner_id}")
            return delete_product(product_id, owner["id"])

        elif message.lower() == "no":
            session.pop("pending_delete")
            print(f"Delete action canceled for {owner_id}")
            return "Penghapusan dibatalkan ✅"

        else:
            print("Received invalid confirmation message")
            return "Ketik 'yes' untuk konfirmasi atau 'no' untuk batal ❌"

    if message.startswith("/add_product"):
        data = parse_add_product(message)

        is_valid, msg = validate_product_data(data)

        if not is_valid:
            return msg

        return add_product(
            owner_id=owner["id"],
            name=data.get("name"),
            price=int(data.get("price")),
            description=data.get("description", "")
        )

    if message.startswith("/list_product"):
        products = get_products_by_owner(owner["id"])
        text, mapping = format_products(products)

        # simpan mapping ke owner
        session["product_map"] = mapping

        return text

    if message.startswith("/delete_product"):

        number = parse_delete_product(message)

        if not number:
            return "Format salah. Contoh: /delete_product 1 ❌"

        mapping = session.get("product_map")

        # ❌ kalau tidak ada mapping → STOP
        if not mapping:
            return "Silakan ketik /list_product dulu ❌"

        product_id = mapping.get(number)

        if not product_id:
            return "Nomor tidak valid ❌"

        # 🔍 ambil nama produk (biar user yakin)
        products = get_products_by_owner(owner["id"])
        product_name = None

        for p in products:
            if p["id"] == product_id:
                product_name = p["name"]
                break

        if not product_name:
            return "Produk tidak ditemukan ❌"

        # 🧠 simpan pending action
        session["pending_delete"] = product_id

        return f'Yakin ingin menghapus "{product_name}"? (yes/no)'

### Update product ###
    if message.startswith("/update_product"):
        number, data = parse_update_product(message)

        if not number:
            return "Format salah. Contoh: /update_product 1 ❌"

        mapping = session.get("product_map")

        if not mapping:
            return "Silakan ketik /list_product dulu ❌"

        product_id = mapping.get(number)

        if not product_id:
            return "Nomor tidak valid ❌"

        return update_product(product_id, owner["id"], data)

    # 🔥 AI PARSING (fallback)
    ai_result = parse_admin_intent(message)
    data = safe_parse_json(ai_result)
    print("AI RESULT:", data)

    # 🤖 FALLBACK KE AI CUSTOMER JIKA PESAN BUKAN PERINTAH ADMIN
    intent = data.get("intent") if data else "unknown"

    if not data or intent == "unknown":
        products = get_products_by_owner(owner["id"])
        response_text = generate_response(message, products, owner["business_name"], history)
        
        # Simpan ke history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response_text})
        
        if len(history) > 10:
            session["history"] = history[-10:]
            
        return response_text

    if intent == "add_product":
        name = data.get("name")
        price = data.get("price")

        if not name or not price:
            return "Nama dan harga wajib diisi ❌"



        try:
            price = int(price)
        except:
            return "Harga harus angka ❌"

        return add_product(
            owner_id=owner["id"],
            name=name,
            price=price,
            description=data.get("description", "")
        )

    if intent == "delete_product":
        target_name = data.get("target_name")

        # 🔥 VALIDASI
        if not target_name:
            return "Sebutkan nama produk yang ingin dihapus ❌"

        products = get_products_by_owner(owner["id"])

        for p in products:
            if target_name.lower() in p["name"].lower():
                return delete_product(p["id"], owner["id"])

        return "Produk tidak ditemukan ❌"

    if intent == "update_product":
        target_name = data.get("target_name")

        if not target_name:
            return "Sebutkan nama produk yang ingin diupdate ❌"

        products = get_products_by_owner(owner["id"])

        for p in products:
            if target_name.lower() in p["name"].lower():

                update_data = {}

                if data.get("name"):
                    update_data["name"] = data.get("name")

                if data.get("price"):
                    try:
                        update_data["price"] = int(data.get("price"))
                    except:
                        return "Harga harus angka ❌"

                if data.get("description"):
                    update_data["description"] = data.get("description")

                if not update_data:
                    return "Tidak ada data yang diupdate ❌"

                return update_product(
                    p["id"],
                    owner["id"],
                    update_data
                )

        return "Produk tidak ditemukan ❌"

    if intent == "list_product":
        products = get_products_by_owner(owner["id"])

        if not products:
            return "Belum ada produk ❌"

        text = "📋 Daftar Produk:\n"

        for p in products:
            text += f"- {p['name']} (Rp{p['price']})\n"
        return text



