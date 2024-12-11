import csv
import os
import locale
from time import sleep


def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(        #list
                {                    #dictionary
                    "id": id,       
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

#gör en funktion som hämtar en produkt

    
def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break  # Avsluta loopen så snart produkten hittas

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"


def view_product(products, id):
    # Go through each product in the list
    for product in products:
        # Check if the product's id matches the given id
        if product["id"] == id:
            # If it matches, return the product's name and description
            return f"Visar produkt: {product['name']} {product['desc']} {product['price']} kr {product['quantity']} st"
    
    # If no matching product is found, return this message
    return "Produkten hittas inte"


def truncate(word, max_length): #
    if len(word) > max_length:
        return word[:max_length - 3] + "..."
    else:
        return word
    


def view_products(products):
    header = f"{'Nr':<3} {'Id':<3} {'Name':<40} {'Description':<79} {'Price':<15} {'Quantity'}"
    line = "-" * len(header)
    
    product_list = [header, line]

    for index, product in enumerate(products, 1):
        name = truncate(product['name'], 25)
        desc = truncate(product['desc'], 60)
            
        product_info = f"{index}) (#{product['id']}) {name:<35} \t {desc:<70} \t {locale.currency(product['price'], grouping=True)} \t {product['quantity']}"
        product_list.append(product_info)

    
    return "\n".join(product_list)

def add_product(products, name, desc, price, quantity):
    max_id = max(products,key=lambda x: x['id'])
    value_id = max_id['id']
    new_id = value_id + 1
    products.append({
        "id" : new_id,
        "name" : name ,
        "desc" : desc,
        "price" : price,
        "quantity" : quantity
    })
    return f"Lyckades lägga till{name}"

def edit_product(products):
    while True:
        try:
            num = int(input("Vilken produkt vill du ändra? (Number): "))
            break
        except:
            print("skriv ett nummer")
            continue
    name = input("Namn på produkten: ")
    desc = input("Beskrivning på produkten: ")
    while True:
        try:
            price = float(input("Pris på produkten: "))
            break
        except:
            print("skriv ett nummer")
            continue
    while True:
        try:
            quantity = int(input("Antal produkter: "))
            break
        except:
            print("skriv ett nummer")
            continue

    for product in products:
        if 1 <= num <= len(products):  # Ensure the index is within the valid range
            selected_product = products[num - 1]  # Get the product using the list index
            num = selected_product['id']  # Extract the actual ID of the product
            product["name"] = name
            product["desc"] = desc
            product["price"] = price
            product["quantity"] = quantity
        
def save_products(products):
    csv_file_path = "db_products.csv"
    with open(csv_file_path, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()  # Write the header row
        writer.writerows(products)  # Write the product data

    print(f"Data successfully saved to {csv_file_path}")

#TODO: gör om så du slipper använda global-keyword (flytta inte "product = []")
#TODO: skriv en funktion som returnerar en specifik produkt med hjälp av id


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('db_products.csv')
while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Show ordered list of products

        choice = input("Vill du (V)isa, (T)a bort, (L)ägga till eller (Ä)ndra en produkt? ").strip().upper()

        if choice == "L": #lägga till
            name = input("Namn: ")
            desc = input("Beskrivning: ")
            while True:
                try:
                    price = float(input("Pris: "))
                    break
                except:
                    print("Priset måste vara ett nummer")
            while True:
                try:
                    quantity = int(input("Kvantitet: "))
                    break
                except:
                    print("Kvantitet måste vara ett nummer")
            
            print(add_product(products, name, desc, price, quantity))
            save_products(products)
            

        if choice == "Ä": #Ändra
            edit_product(products)
            save_products(products)

            
            
            
        elif choice in ["V", "T"]:
            try:
                index = int(input("Enter product Number: "))

                    
            except ValueError:
                print("Välj en produkt med siffor")
                sleep(0.5)

            if choice == "V":   #visa
                try:
                    if 1 <= index <= len(products):  # Ensure the index is within the valid range
                        selected_product = products[index - 1]  # Get the product using the list index
                        id = selected_product['id']  # Extract the actual ID of the product
                    print(view_product(products, id))  # Remove product using the actual ID
                    done = input()
                    save_products(products)
                except:
                    print("Ogiltig produkt")
                    sleep(0.3)

            elif choice == "T": #ta bort
                try:
                    if 1 <= index <= len(products):  # Ensure the index is within the valid range
                        selected_product = products[index - 1]  # Get the product using the list index
                        id = selected_product['id']  # Extract the actual ID of the product

                        print(remove_product(products, id))  # Remove product using the actual ID
                        sleep(0.5)
                        save_products(products)     
                except:
                    print("Ogiltig produkt")
                    sleep(1)
