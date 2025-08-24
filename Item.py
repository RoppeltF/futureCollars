
def load_inventory_from(filename):
    items = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                items.append(load_csv_to_obj(line))
    except FileNotFoundError:
        print("File with inventory not exists, add some inventory")
    return items


def load_csv_to_obj(items):  # Map text line to object
    name, price, quantity = items.strip().split(',')
    return Item(name, price, quantity)


class Item():
    def __init__(self,name, price, quantity):
        self.name     = name
        self.price    = price
        self.quantity = quantity

    def __str__(self):
        return f"Product: {self.name} - Price: {self.price} - Quantity: {self.quantity}"

    def convert_to_csv(self):
        return f"{self.name},{self.price},{self.quantity}"