from app.services.product_service import get_products_by_owner
from app.services.ai_service import generate_response


def handle_customer_message(owner, message: str):
    products = get_products_by_owner(owner["id"])

    if not products:
        return "Maaf, saat ini belum ada produk tersedia."

    return generate_response(message, products)