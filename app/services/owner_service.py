from app.database.db import get_connection


def register_owner(business_name: str, phone_number: str):
    conn = get_connection()
    cursor = conn.cursor()

    # cek dulu apakah sudah ada
    cursor.execute("""
    SELECT * FROM owners WHERE phone_number = ?
    """, (phone_number,))

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "Owner sudah terdaftar ⚠️"

    cursor.execute("""
    INSERT INTO owners (business_name, phone_number)
    VALUES (?, ?)
    """, (business_name, phone_number))

    conn.commit()
    conn.close()

    return "Owner berhasil didaftarkan ✅"

def get_owner_by_phone(phone_number: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM owners WHERE phone_number = ?
    """, (phone_number,))

    owner = cursor.fetchone()
    conn.close()

    return owner