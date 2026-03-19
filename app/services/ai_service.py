from openai import OpenAI
from app.config.settings import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)


def safe_parse_json(text):
    try:
        # bersihkan markdown code block jika ada
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except:
        return None

def generate_response(user_message: str, products: list):
    product_list = ""
    for p in products:
        product_list += f"- {p['name']} (Rp{p['price']}): {p['description']}\n"
 
    prompt = f"""
Kamu adalah admin WhatsApp untuk sebuah UMKM.

Tugas kamu:
- jawab pertanyaan customer dengan ramah
- gunakan data produk yang tersedia
- jawab singkat, jelas, dan natural

Data produk:
    {product_list}

Pertanyaan customer:
    {user_message}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah admin UMKM yang ramah."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content



def parse_admin_intent(message: str):

    prompt = f"""
Kamu adalah AI yang mengekstrak perintah admin UMKM.

Tugas:
- pahami maksud user
- output HARUS JSON valid

Format:
{{
  "intent": "add_product | delete_product | update_product | list_product | unknown",
  "name": "...",
  "price": number,
  "description": "...",
  "target_name": "..."
}}

Contoh:

Input: tambahin latte 25000
Output:
{{"intent":"add_product","name":"latte","price":25000}}

Input: hapus latte
Output:
{{"intent":"delete_product","target_name":"latte"}}

Input: update kopi hitam 2000
Output:
{{"intent":"update_product","target_name":"kopi hitam", "price":2000}}

Input: lihat produk
Output:
{{"intent":"list_product"}}


Input:
{message}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content