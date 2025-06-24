import main

items = [{"item_name": "Pipoca","item_info":{"item_price":7,"item_quantity":87}}]

class Inventory():

    def __init__(self,item_name, item_quantity,item_price):
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.item_price = item_price
        pass
    # def inventory(self, item_name, item_quantity,item_price):
    def inventory(self):
        try:
            if items:
                return items
            else:
                 if self.item_name != None and self.item_name != "":
                    items_dict = {}
                    items_dict["item_name"] = self.item_name
                    items_dict["item_info"] = {"item_price": self.item_price, "item_quantity": self.item_quantity}
                    items.append(items_dict)
                    return items
                 else:
                    print("Empy inventory please add some. \n")
                    Inventory.add_inventory()
                    return 0
        except ValueError:
            print("Something fail")

    def show_inventory():
        main.menu("Inventory",items)

