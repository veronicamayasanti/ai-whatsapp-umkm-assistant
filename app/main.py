from app.database.models import create_tables
from app.services.owner_service import register_owner, get_owner_by_phone
from app.handlers.admin_handler import handle_admin_message
from app.handlers.customer_handler import handle_customer_message

def main():
    create_tables()

    # daftar owner (sekali saja)
    # result = register_owner("Kopi Kenangan AI", "628123456789")
   # print(result)

    # simulasi pesan masuk
    from_number = "62812879856789"  # customer
    to_number = "628123456789"



    #message = """/update_product 1
    #Nama: Cappuccino
    #Harga: 30000
    #Deskripsi: kopi foam enak"""

    #message = "/list_product"
    #message = "/delete_product 2"
    #message = """/add_product
    #Nama: Mocha  Latte
    #Harga: 28000
    #Deskripsi:
    # """

    message = "mau pesan susu apakah ada"

    # logic
    owner = get_owner_by_phone(to_number)

    if owner:
        owner = dict(owner)

        if from_number == owner["phone_number"]:
            response = handle_admin_message(owner, message)
        else:
            response = handle_customer_message(owner, message)

        print("\nmessage: ")
        print(message)
        print("\nResponse:")
        print(response)
    else:
        print("Owner tidak ditemukan")


if __name__ == "__main__":
    main()