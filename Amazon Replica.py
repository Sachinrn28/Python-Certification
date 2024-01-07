#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json

# Constants for JSON file names
ADMINS_FILE = "admins.json"
MEMBERS_FILE = "members.json"
PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

# Load data from JSON files (or create empty data structures)
def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Save data to JSON files
def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Registration function for both admins and members
def register(full_name, address, email, password, user_type):
    if user_type == "admin":
        admins = load_data(ADMINS_FILE)
        admin = {
            "Full Name": full_name,
            "Address": address,
            "Email": email,
            "Password": password
        }
        admins.append(admin)
        save_data(ADMINS_FILE, admins)
    elif user_type == "member":
        members = load_data(MEMBERS_FILE)
        member = {
            "Full Name": full_name,
            "Address": address,
            "Email": email,
            "Password": password
        }
        members.append(member)
        save_data(MEMBERS_FILE, members)
    else:
        print("Invalid user type. Please enter 'admin' or 'member'.")

# Login function for both admins and members
def login(email, password, user_type):
    if user_type == "admin":
        admins = load_data(ADMINS_FILE)
        for admin in admins:
            if admin["Email"] == email and admin["Password"] == password:
                return admin
    elif user_type == "member":
        members = load_data(MEMBERS_FILE)
        for member in members:
            if member["Email"] == email and member["Password"] == password:
                return member
    return None

# Function to create/update a product
def create_update_product(admin, product_id, product_name, manufacturer_name, price, discount, total_stock):
    if admin:
        products = load_data(PRODUCTS_FILE)
        # Check if product exists and update or create a new one
        product_exists = False
        for product in products:
            if product["Product ID"] == product_id:
                product_exists = True
                product.update({
                    "Product Name": product_name,
                    "Manufacturer Name": manufacturer_name,
                    "Price": price,
                    "Discount": discount,
                    "Total Stock Available": total_stock
                })
                break
        if not product_exists:
            new_product = {
                "Created By": admin["Email"],
                "Product ID": product_id,
                "Product Name": product_name,
                "Manufacturer Name": manufacturer_name,
                "Price": price,
                "Discount": discount,
                "Total Stock Available": total_stock
            }
            products.append(new_product)
        save_data(PRODUCTS_FILE, products)

# Function to list products
def list_products(admin):
    if admin:
        products = load_data(PRODUCTS_FILE)
        admin_products = [product for product in products if product.get("Created By") == admin["Email"]]
        return admin_products
    return None

# Function to create an order
def create_order(member, product_id, quantity):
    if member:
        products = load_data(PRODUCTS_FILE)
        orders = load_data(ORDERS_FILE)

        # Find the product
        product = next((prod for prod in products if prod["Product ID"] == product_id), None)
        if product:
            # Check if quantity is available
            if int(quantity) <= product["Total Stock Available"]:
                order = {
                    "Order ID": "ORD" + str(len(orders) + 1),
                    "Product Name": product["Product Name"],
                    "Price": product["Price"],
                    "Discount": product["Discount"],
                    "Price after Discount": product["Price"] * (1 - float(product["Discount"].strip('%')) / 100),
                    "Quantity": int(quantity),
                    "Total Cost": product["Price"] * (1 - float(product["Discount"].strip('%')) / 100) * int(quantity),
                    "Ordered By": member["Email"],
                    "Delivering to": member["Address"],
                }
                orders.append(order)
                # Update total stock available
                product["Total Stock Available"] -= int(quantity)
                save_data(PRODUCTS_FILE, products)
                save_data(ORDERS_FILE, orders)
            else:
                print("Quantity not available.")
        else:
            print("Product not found.")

# Main function
if __name__ == "__main__":
    while True:
        print("\nMain Menu")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_type = input("Enter user type (admin/member): ")
            full_name = input("Enter your full name: ")
            address = input("Enter your full address: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            register(full_name, address, email, password, user_type)
            print(f"{user_type.capitalize()} registered successfully.")
        elif choice == "2":
            user_type = input("Enter user type (admin/member): ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user = login(email, password, user_type)
            if user:
                print(f"Welcome, {user['Full Name']}!")
                if user_type == "admin":
                    while True:
                        print("\nAdmin Menu")
                        print("1. Create/Update Product")
                        print("2. List Admin Products")
                        print("3. Logout")
                        admin_choice = input("Enter your choice: ")
                        if admin_choice == "1":
                            product_id = input("Enter Product ID: ")
                            product_name = input("Enter Product Name: ")
                            manufacturer_name = input("Enter Manufacturer Name: ")
                            price = float(input("Enter Price: "))
                            discount = input("Enter Discount (e.g., 10%): ")
                            total_stock = int(input("Enter Total Stock Available: "))
                            create_update_product(user, product_id, product_name, manufacturer_name, price, discount, total_stock)
                            print("Product created/updated successfully.")
                        elif admin_choice == "2":
                            admin_products = list_products(user)
                            if admin_products:
                                for product in admin_products:
                                    print(f"Product ID: {product['Product ID']}")
                                    print(f"Product Name: {product['Product Name']}")
                                    print(f"Manufacturer Name: {product['Manufacturer Name']}")
                                    print(f"Price: {product['Price']}")
                                    print(f"Discount: {product['Discount']}")
                                    print(f"Total Stock Available: {product['Total Stock Available']}")
                                    print("-" * 30)
                            else:
                                print("No products found.")
                        elif admin_choice == "3":
                            break
                        else:
                            print("Invalid choice. Please try again.")
                elif user_type == "member":
                    while True:
                        print("\nMember Menu")
                        print("1. Create Order")
                        print("2. Logout")
                        member_choice = input("Enter your choice: ")
                        if member_choice == "1":
                            product_id = input("Enter Product ID to order: ")
                            quantity = input("Enter the quantity: ")
                            create_order(user, product_id, quantity)
                        elif member_choice == "2":
                            break
                        else:
                            print("Invalid choice. Please try again.")
            else:
                print("Login failed. Please check your credentials.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


# In[7]:


import json

# Function to read data from a JSON file
def read_json_data(filename):
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []  # Initialize as an empty list if the file doesn't exist
    return data

# Function to write data to a JSON file
def write_json_data(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# -------------- Member Management --------------

# Function to add a new member
def add_member(full_name, address, email, password):
    members = read_json_data('members.json')
    new_member = {
        "Full Name": full_name,
        "Address": address,
        "Email": email,
        "Password": password
    }
    members.append(new_member)
    write_json_data('members.json', members)

# Example usage to add a new member
add_member("Viru Sahastrabudhhe", "Villa 25, Imperial College, New Delhi India", "Virus@gmail.com", "SilencerIsTheBest")

# -------------- Product Management --------------

# Function to add a new product
def add_product(created_by, product_id, product_name, manufacturer_name, price, discount, total_stock):
    products = read_json_data('products.json')
    new_product = {
        "Created By": created_by,
        "Product ID": product_id,
        "Product Name": product_name,
        "Manufacturer Name": manufacturer_name,
        "Price": price,
        "Discount": discount,
        "Total Stock Available": total_stock
    }
    products.append(new_product)
    write_json_data('products.json', products)

# Example usage to add a new product
add_product("Test Admin 1", "GTRX1", "GEFORCE RTX 3070", "Nvidia", 70000, "30%", 10)

# -------------- Order Management --------------

# Function to add a new order
def add_order(order_id, product_name, price, discount, price_after_discount, quantity, total_cost, ordered_by, delivering_to):
    orders = read_json_data('orders.json')
    new_order = {
        "Order ID": order_id,
        "Product Name": product_name,
        "Price": price,
        "Discount": discount,
        "Price after Discount": price_after_discount,
        "Quantity": quantity,
        "Total Cost": total_cost,
        "Ordered By": ordered_by,
        "Delivering to": delivering_to
    }
    orders.append(new_order)
    write_json_data('orders.json', orders)

# Example usage to add a new order
add_order("ORD1", "Steelseries Rival 600", 5000, "10%", 4500.0, 2, 9000, "Viru Sahastrabudhhe", "Villa 26, Imperial College, New Delhi India")


# In[6]:


import json

# Constants for JSON file names
ADMINS_FILE = "admins.json"
MEMBERS_FILE = "members.json"
PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

# Load data from JSON files (or create empty data structures)
def load_data():
    try:
        with open(ADMINS_FILE, "r") as file:
            admins = json.load(file)
    except FileNotFoundError:
        admins = []

    try:
        with open(MEMBERS_FILE, "r") as file:
            members = json.load(file)
    except FileNotFoundError:
        members = []

    try:
        with open(PRODUCTS_FILE, "r") as file:
            products = json.load(file)
    except FileNotFoundError:
        products = []

    try:
        with open(ORDERS_FILE, "r") as file:
            orders = json.load(file)
    except FileNotFoundError:
        orders = []

    return admins, members, products, orders

# Save data to JSON files
def save_data(admins, members, products, orders):
    with open(ADMINS_FILE, "w") as file:
        json.dump(admins, file, indent=4)

    with open(MEMBERS_FILE, "w") as file:
        json.dump(members, file, indent=4)

    with open(PRODUCTS_FILE, "w") as file:
        json.dump(products, file, indent=4)

    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)


# Registration function for both admins and members
def register(full_name, address, email, password, user_type):
    if user_type == "admin":
        admins, members, products, orders = load_data()
        admin = {
            "Full Name": full_name,
            "Address": address,
            "Email": email,
            "Password": password
        }
        admins.append(admin)
        save_data(admins, members, products, orders)
    elif user_type == "member":
        admins, members, products, orders = load_data()
        member = {
            "Full Name": full_name,
            "Address": address,
            "Email": email,
            "Password": password
        }
        members.append(member)
        save_data(admins, members, products, orders)
    else:
        print("Invalid user type. Please enter 'admin' or 'member'.")

# Login function for both admins and members
def login(email, password, user_type):
    if user_type == "admin":
        admins, _, _, _ = load_data()
        for admin in admins:
            if admin["Email"] == email and admin["Password"] == password:
                return admin
    elif user_type == "member":
        _, members, _, _ = load_data()
        for member in members:
            if member["Email"] == email and member["Password"] == password:
                return member
    return None

# Function to create/update a product
def create_update_product(admin, product_id, product_name, manufacturer_name, price, discount, total_stock):
    if admin:
        _, _, products, _ = load_data()
        # Check if product exists and update or create a new one
        product_exists = False
        for product in products:
            if product["Product ID"] == product_id:
                product_exists = True
                product.update({
                    "Product Name": product_name,
                    "Manufacturer Name": manufacturer_name,
                    "Price": price,
                    "Discount": discount,
                    "Total Stock Available": total_stock
                })
                break
        if not product_exists:
            new_product = {
                "Created By": admin["Email"],
                "Product ID": product_id,
                "Product Name": product_name,
                "Manufacturer Name": manufacturer_name,
                "Price": price,
                "Discount": discount,
                "Total Stock Available": total_stock
            }
            products.append(new_product)
            save_data(*load_data())

# Function to list products
def list_products():
    _, _, products, _ = load_data()
    return products

# Function to create an order
def create_order(member, product_id, quantity):
    if member:
        admins, members, products, orders = load_data()
        # Find the product
        product = None
        for prod in products:
            if prod["Product ID"] == product_id:
                product = prod
                break
        if product:
            # Check if quantity is available
            if int(quantity) <= product["Total Stock Available"]:
                order = {
                    "Order ID": "ORD" + str(len(orders) + 1),
                    "Product Name": product["Product Name"],
                    "Price": product["Price"],
                    "Discount": product["Discount"],
                    "Price after Discount": product["Price"] * (1 - float(product["Discount"].strip('%')) / 100),
                    "Quantity": int(quantity),
                    "Total Cost": product["Price"] * (1 - float(product["Discount"].strip('%')) / 100) * int(quantity),
                    "Ordered By": member["Email"],
                    "Delivering to": member["Address"],
                }
                orders.append(order)
                # Update total stock available
                product["Total Stock Available"] -= int(quantity)
                save_data(admins, members, products, orders)
            else:
                print("Quantity not available.")
        else:
            print("Product not found.")



# Main function (for testing)
if __name__ == "__main__":
    # Test the functions here
    pass

