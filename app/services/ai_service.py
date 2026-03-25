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

def generate_response(user_message: str, products: list, business_name: str, history: list = None):
    if history is None:
        history = []
        
    product_list = ""
    for p in products:
        product_list += f"- {p['name']} (Rp{p['price']}): {p['description']}\n"
 
    system_prompt = f"""Kamu adalah admin WhatsApp untuk UMKM bernama "{business_name}".

Tugas kamu:
- Jika ini adalah pesan pertama dari pelanggan (history kosong), awali jawabanmu dengan: "Selamat datang di {business_name}! 😊"
- Jawab pertanyaan customer dengan ramah dan santun.
- Gunakan data produk yang tersedia jika mereka bertanya tentang menu/produk.
- Jawab singkat, jelas, dan natural.

Data produk:
{product_list}
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return "Maaf, sistem sedang sibuk. Silakan coba lagi."


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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Admin Intent Error: {e}")
        return '{"intent": "unknown"}'