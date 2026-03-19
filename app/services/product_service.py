from app.database.db import get_connection


def add_product(owner_id: int, name: str, price: int, description: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products (owner_id, name, price, description)
    VALUES (?, ?, ?, ?)
    """, (owner_id, name, price, description))

    conn.commit()
    conn.close()

    return "Produk berhasil ditambahkan ✅"

def get_products_by_owner(owner_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products WHERE owner_id = ?
    """, (owner_id,))

    products = cursor.fetchall()
    conn.close()

    return products

def format_products(products):
    if not products:
        return "Belum ada produk ❌", {}

    text = "📋 Daftar Produk:\n"
    mapping = {}

    for i, p in enumerate(products, start=1):
        text += f"{i}. {p['name']} (Rp{p['price']})\n"
        mapping[i] = p["id"]

    text += "\nKetik: /delete_product <nomor>"

    return text, mapping

def delete_product(product_id: int, owner_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM products 
    WHERE id = ? AND owner_id = ?
    """, (product_id, owner_id))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return "Produk tidak ditemukan ❌"

    conn.close()
    return "Produk berhasil dihapus 🗑️"

def update_product(product_id: int, owner_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products WHERE id = ? AND owner_id = ?
    """, (product_id, owner_id))

    product = cursor.fetchone()

    if not product:
        conn.close()
        return "Produk tidak ditemukan ❌"

    name = data.get("name", product["name"])
    price = data.get("price", product["price"])
    description = data.get("description", product["description"])

    cursor.execute("""
    UPDATE products
    SET name = ?, price = ?, description = ?
    WHERE id = ?
    """, (name, price, description, product_id))

    conn.commit()
    conn.close()

    return "Produk berhasil diupdate ✏️"