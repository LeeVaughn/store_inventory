from collections import OrderedDict
import datetime
import os
import csv

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField()
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now)


    class Meta():
        database = db


def initialize_db():
    """Create the DB and table if they don't exist."""
    db.connect()
    db.create_tables([Product], safe=True)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu_loop():
    """Show the menu."""
    choice = None

    while choice != "q":
        clear_screen()

        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))

        print("q) Quit.")
        print("\n")

        choice = input("Selection: ").lower().strip()

        if choice in menu:
            clear_screen()
            menu[choice]()


def add_inventory():
    '''Read CSV and add products to DB.'''
    with open("inventory.csv", newline="") as csvfile:
        inventory = csv.DictReader(csvfile, delimiter=",")
        
        for product in inventory:
            # converts string excluding $ to equivalent of cents
            price_in_cents = int(float(product["product_price"][1:]) * 100)

            try:
                Product.create(
                    product_name=product["product_name"],
                    product_quantity=product["product_quantity"],
                    product_price=price_in_cents,
                    date_updated=product["date_updated"]
                )
            except IntegrityError:
                product_record = Product.get(product_name=product["product_name"])
                product_record.points = product["points"]
                product_record.save()


def view_product():
    """View single product's inventory."""
    entered_id = input("Enter the product id number of the product you would like to view: ")
    product = Product.get(Product.product_id == entered_id)

    clear_screen()

    print("Product Details")
    print("-" * 15)
    print("ID: ", product.product_id)
    print("Name: ", product.product_name)
    # https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
    print("Price: ", "${:,.2f}".format(product.product_price * 0.01))
    print("Quantity: ", product.product_quantity)
    print("Last Updated: ", product.date_updated)
    print("\n")

    next_action = input("Enter 'v' to view another item or 'r' to return to main menu: ").lower().strip()

    print("\n")

    if next_action == "v":
        view_product()


def add_product():
    """Add a new product to the database."""
    entered_name = input("Enter a name for the new product: ")
    entered_quantity = input("Enter a quantity for the new product: ")
    entered_price = input("Enter a price for the new product: ")

    if entered_price:
        entered_price = int(float(entered_price) * 100)

    if entered_name and entered_quantity and entered_price:
        Product.create(product_name=entered_name, product_quantity=entered_quantity, product_price=entered_price)
        print("Product successfully added!")
    else:
        print("\nInvalid Input!\n")

    next_action = input("Enter 'a' to enter a product or 'r' to return to main menu: ").lower().strip()

    if next_action == "a":
        add_product()


def backup_db():
    """Make a backup of the entire inventory."""


menu = OrderedDict([
    ("v", view_product),
    ("a", add_product),
    ("b", backup_db),
])

if __name__ == "__main__":
    initialize_db()
    add_inventory()
    menu_loop()
