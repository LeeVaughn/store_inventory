import datetime
import csv
from typing import OrderedDict

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


def menu_loop():
    """Show the menu."""
    choice = None

    print("Enter 'q' to quit.")

    for key, value in menu.items():
        print("{}) {}".format(key, value.__doc__))

    choice = input("Selection: ").lower().strip()

    if choice in menu:
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
    product = Product.get(Product.product_id)
    print(product.product_name)


def add_product():
    """Add a new product to the database."""


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
