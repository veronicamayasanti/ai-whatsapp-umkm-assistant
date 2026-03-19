import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.services.ai_service import generate_response

products = []
message = "apakah ada air putih"
response = generate_response(message, products)
print(f"AI Response for '{message}':")
print(response)
