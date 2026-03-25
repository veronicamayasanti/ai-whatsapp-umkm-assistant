from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from app.database.models import create_tables
from app.services.owner_service import get_owner_by_phone
from app.handlers.admin_handler import handle_admin_message
from app.handlers.customer_handler import handle_customer_message
import uvicorn

app = FastAPI()

# Inisialisasi Database
@app.on_event("startup")
def startup_event():
    create_tables()

@app.post("/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    To: str = Form(...)
):
    # Twilio format: 'whatsapp:+628123456789'
    # Kita hanya butuh nomornya, tanpa 'whatsapp:' dan tanpa tanda '+'
    from_number = From.replace("whatsapp:", "").replace("+", "")
    to_number = To.replace("whatsapp:", "").replace("+", "")

    # Di mode sandbox Twilio, 'to_number' adalah nomor Twilio (+14155238886)
    # Karena ini project portofolio single-user, kita ambil langsung owner yang kita daftarkan
    owner = get_owner_by_phone("6283117459361")

    if owner:
        owner = dict(owner)
        
        # Logika: Jika pengirim adalah owner, maka itu perintah admin
        if from_number == owner["phone_number"]:
            response_text = handle_admin_message(owner, Body)
        else:
            response_text = handle_customer_message(owner, from_number, Body)
    else:
        response_text = "Maaf, nomor ini belum terdaftar sebagai asisten UMKM."

    # Buat respon format TwiML (XML) untuk Twilio
    twiml_resp = MessagingResponse()
    twiml_resp.message(response_text)

    return Response(content=str(twiml_resp), media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
