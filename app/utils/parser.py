def parse_add_product(message: str):
    lines = message.split("\n")

    data = {}

    for line in lines:
        if "Nama:" in line:
            data["name"] = line.split("Nama:")[1].strip()
        elif "Harga:" in line:
            data["price"] = int(line.split("Harga:")[1].strip())
        elif "Deskripsi:" in line:
            data["description"] = line.split("Deskripsi:")[1].strip()

    return data

def parse_delete_product(message: str):
    try:
        return int(message.split(" ")[1])
    except:
        return None



def parse_update_product(message: str):
    lines = message.split("\n")

    try:
        product_id = int(lines[0].split(" ")[1])
    except:
        return None, {}

    data = {}

    for line in lines[1:]:
        if "Nama:" in line:
            data["name"] = line.split("Nama:")[1].strip()
        elif "Harga:" in line:
            data["price"] = int(line.split("Harga:")[1].strip())
        elif "Deskripsi:" in line:
            data["description"] = line.split("Deskripsi:")[1].strip()

    return product_id, data