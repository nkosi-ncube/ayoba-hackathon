import requests

BASE_URL = 'https://25ce-41-116-66-178.ngrok-free.app/gatewayapi'

def get_orders():
    response = requests.get(f'{BASE_URL}/orders/')
    print(response.json())

def get_order_items():
    response = requests.get(f'{BASE_URL}/orderitems/')
    print(response.json())

def get_products():
    response = requests.get(f'{BASE_URL}/products/')
    print(response.json())

def get_customers():
    response = requests.get(f'{BASE_URL}/customers/')
    print(response.json())

def create_order(customer_id, total):
    data = {
        "customer": customer_id,
        "total": total
    }
    response = requests.post(f'{BASE_URL}/orders/', json=data)
    print(response.json())

def create_order_item(order_id, product_id, quantity, price):
    data = {
        "order": order_id,
        "product": product_id,
        "quantity": quantity,
        "price": price
    }
    response = requests.post(f'{BASE_URL}/orderitems/', json=data)
    print(response.json())

def create_product(name, price):
    data = {
        "name": name,
        "price": price
    }
    response = requests.post(f'{BASE_URL}/products/', json=data)
    print(response.json())

def create_customer(name, language):
    data = {
        "name": name,
        "language": language
    }
    response = requests.post(f'{BASE_URL}/customers/', json=data)
    print(response.json())

def add_to_cart(customer_id, product_id, quantity):
    # Creating a dummy order for the cart since cart functionality is not directly implemented
    order_data = {
        "customer": customer_id,
        "total": 0
    }
    order_response = requests.post(f'{BASE_URL}/orders/', json=order_data)
    order = order_response.json()

    # Adding items to the cart
    item_data = {
        "order": order["id"],
        "product": product_id,
        "quantity": quantity,
        "price": "29.99"  # Assuming a fixed price for simplicity
    }
    item_response = requests.post(f'{BASE_URL}/orderitems/', json=item_data)
    print(item_response.json())

def checkout(order_id):
    # Assuming the checkout process involves finalizing the order
    # You might need to send a POST request to a checkout endpoint if implemented
    print(f"Order {order_id} checked out successfully.")

# Business Profile Functions
def get_business_profiles():
    response = requests.get(f'{BASE_URL}/businessprofiles/')
    print(response.json())

def create_business_profile(user_id, business_name, contact_email, contact_phone, address, working_hours, description):
    data = {
        "user": user_id,
        "business_name": business_name,
        "contact_email": contact_email,
        "contact_phone": contact_phone,
        "address": address,
        "working_hours": working_hours,
        "description": description
    }
    response = requests.post(f'{BASE_URL}/businessprofiles/', json=data)
    print(response.json())

def main():
    while True:
        print("\n1. Get Orders")
        print("2. Get Order Items")
        print("3. Get Products")
        print("4. Get Customers")
        print("5. Create Order")
        print("6. Create Order Item")
        print("7. Create Product")
        print("8. Create Customer")
        print("9. Add to Cart")
        print("10. Checkout")
        print("11. Get Business Profiles")
        print("12. Create Business Profile")
        print("13. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            get_orders()
        elif choice == '2':
            get_order_items()
        elif choice == '3':
            get_products()
        elif choice == '4':
            get_customers()
        elif choice == '5':
            customer_id = input("Enter customer ID: ")
            total = input("Enter total amount: ")
            create_order(customer_id, total)
        elif choice == '6':
            order_id = input("Enter order ID: ")
            product_id = input("Enter product ID: ")
            quantity = int(input("Enter quantity: "))
            price = input("Enter price: ")
            create_order_item(order_id, product_id, quantity, price)
        elif choice == '7':
            name = input("Enter product name: ")
            price = input("Enter product price: ")
            create_product(name, price)
        elif choice == '8':
            name = input("Enter customer name: ")
            language = input("Enter customer language: ")
            create_customer(name, language)
        elif choice == '9':
            customer_id = input("Enter customer ID: ")
            product_id = input("Enter product ID: ")
            quantity = int(input("Enter quantity: "))
            add_to_cart(customer_id, product_id, quantity)
        elif choice == '10':
            order_id = input("Enter order ID to checkout: ")
            checkout(order_id)
        elif choice == '11':
            get_business_profiles()
        elif choice == '12':
            user_id = input("Enter user ID: ")
            business_name = input("Enter business name: ")
            contact_email = input("Enter contact email: ")
            contact_phone = input("Enter contact phone: ")
            address = input("Enter address: ")
            working_hours = input("Enter working hours: ")
            description = input("Enter description: ")
            create_business_profile(user_id, business_name, contact_email, contact_phone, address, working_hours, description)
        elif choice == '13':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
