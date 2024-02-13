from dataclasses import dataclass
from typing import List
from getpass import getpass

staff = {
    "cloma": {"password": "123", "position": ["Manager"]},
    "maturan": {"password": "123", "position": ["asst.Manager"]},
    "yanson": {"password": "123", "position": ["Sale staff"]},
    "gemino": {"password": "123", "position": ["Sale staff"]},
    "gault": {"password": "123", "position": ["Sale staff"]},
    "lasconia": {"password": "123", "position": ["Owner"]}
}


@dataclass
class Staff:
    id: str
    name: str
    position: str


@dataclass
class Menu:
    name: str
    price: float
    category: str = "Restaurant"


@dataclass
class CartItem:
    menu_item: Menu
    quantity: int


@dataclass
class Transaction:
    id: str
    items: List[CartItem]  # Here, List is used to specify that items is a list of CartItem objects
    total: float
    paid_amount: float
    change: float
    user_id: str


class Restaurant:
    def __init__(self):
        self.menu = [
            Menu("Burger", 50.55),
            Menu("Salad", 45.55),
            Menu("Mango float", 65.55)
        ]
        self.staff = []
        self.transactions = []
        self.cart = []

    def login_staff(self):
        while True:
            username = input("Enter username: ")
            if username in staff:
                password = input("Enter password: ")
                if password == staff[username]["password"]:
                    print(f"Welcome back master {username}!")
                    return username
            print("Incorrect username or password. Please try again.")

    def display_menu(self):
        print("Menu:")
        for index, item in enumerate(self.menu):
            print(f"{index + 1}. {item.name}: ₱{item.price}")

    def add_to_cart(self, item_index, quantity):
        if 1 <= item_index <= len(self.menu):
            menu_item = self.menu[item_index - 1]
            # Check if the item is already in the cart, if so, update the quantity
            for cart_item in self.cart:
                if cart_item.menu_item == menu_item:
                    cart_item.quantity += quantity
                    break
            else:
                cart_item = CartItem(menu_item, quantity)
                self.cart.append(cart_item)
            print(f"{quantity} {menu_item.name}(s) added to cart.")
        else:
            print("Invalid menu item index.")

    def show_cart(self):
        total_price = 0
        print("Cart:")
        for index, cart_item in enumerate(self.cart):
            print(
                f"{index + 1}. {cart_item.quantity} {cart_item.menu_item.name}(s) - ₱{cart_item.menu_item.price * cart_item.quantity}")
            total_price += cart_item.menu_item.price * cart_item.quantity
        print(f"Total: ₱{total_price}")

    def remove_from_cart(self, index):
        if 1 <= index <= len(self.cart):
            removed_item = self.cart.pop(index - 1)
            print(f"{removed_item.quantity} {removed_item.menu_item.name}(s) removed from cart.")
        else:
            print("Invalid cart item index.")

    def edit_cart_item(self, index, new_quantity):
        if 1 <= index <= len(self.cart):
            cart_item = self.cart[index - 1]
            cart_item.quantity = new_quantity
            print(f"Quantity of {cart_item.menu_item.name}(s) updated to {new_quantity}.")
            self.show_cart()  # Show cart after editing quantity
        else:
            print("Invalid cart item index.")

    def create_transaction(self, username):
        total_amount = sum(item.menu_item.price * item.quantity for item in self.cart)
        print(f"Total amount: ₱{total_amount}")
        try:
            paid_amount = float(input("Enter the amount paid by the customer: ₱"))
        except ValueError:
            print("Invalid input. Please enter a valid amount.")
            return

        if self.staff:
            user_id = self.staff[0].id
        else:
            user_id = "unknown"

        change = paid_amount - total_amount
        transaction = Transaction("some_id", self.cart, total_amount, paid_amount, change, username)
        self.transactions.append(transaction)
        self.cart = []
        print("Transaction created.")
        print(f"Username: {transaction.user_id}")
        print(f"Change: ₱{change}")
        return total_amount

    def display_receipt(self, transaction):
        username = transaction.user_id
        position = ", ".join(staff.get(username, {}).get("position", []))

        print("Receipt:")
        print(f"Username: {username} ({position})")
        for item in transaction.items:
            print(f"{item.quantity} {item.menu_item.name}(s) - ₱{item.menu_item.price * item.quantity}")
        print(f"Total: ₱{transaction.total}")
        print(f"Paid: ₱{transaction.paid_amount}")
        print(f"Change: ₱{transaction.change}")

    def display_transactions(self):
        print("Transactions:")
        for index, transaction in enumerate(self.transactions):
            username = transaction.user_id
            position = ", ".join(staff.get(username, {}).get("position", []))
            print(f"Transaction {index + 1}:")
            print(f"Username: {username} ({position})")
            self.display_receipt(transaction)
            print()
    def order_menu(self):
        while True:
            self.display_menu()
            item_index = int(input("Enter the item number to add to cart (0 to finish ordering): "))
            if item_index == 0:
                self.show_cart()  # Show cart automatically after finishing ordering
                break
            if 1 <= item_index <= len(self.menu):
                quantity = int(input("Enter the quantity: "))
                self.add_to_cart(item_index, quantity)
            else:
                print("Invalid menu item index.")

    def start_ordering(self):
        username = self.login_staff()
        if username:
            while True:
                print("\n1. Order Menu")
                print("2. Show Cart")
                print("3. Remove from Cart")
                print("4. Edit Cart Item Quantity")
                print("5. Create Transaction")
                print("6. Show Transactions")
                print("7. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    self.order_menu()
                elif choice == '2':
                    self.show_cart()
                elif choice == '3':
                    index = int(input("Enter the index of the item to remove: "))
                    self.remove_from_cart(index)
                elif choice == '4':
                    index = int(input("Enter the index of the item to edit: "))
                    new_quantity = int(input("Enter the new quantity: "))
                    self.edit_cart_item(index, new_quantity)
                elif choice == '5':
                    total_amount = self.create_transaction(username)
                    if total_amount is not None:
                        print(f"Transaction total: ₱{total_amount}")
                elif choice == '6':
                    self.display_transactions()
                elif choice == '7':
                    break
                else:
                    print("Invalid choice. Please try again.")

restaurant = Restaurant()
restaurant.start_ordering()
