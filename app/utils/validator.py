def validate_product_data(data: dict):
    if not data.get("name"):
        return False, "Nama produk wajib diisi ❌"

    if not data.get("price"):
        return False, "Harga wajib diisi ❌"

    try:
        int(data.get("price"))
    except:
        return False, "Harga harus angka ❌"

    return True, "Valid ✅"

