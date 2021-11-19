from peewee import *
import csv
import pprint

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField()
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta():
        database = db

def add_inventory():
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

if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    add_inventory()
