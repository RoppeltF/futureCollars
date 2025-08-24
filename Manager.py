import datetime
from itertools import product
from basic_functions import action,save_stuff, load_balance,LOG,print_receipt
from Item import *
from datetime import datetime



class Manager:
    def __init__(self, inventory_file="inventory.txt", balance_file="balance.txt"):
        self.inventory_file = inventory_file
        self.balance_file = balance_file
        self.items = load_inventory_from(inventory_file)
        self.balance = load_balance(balance_file)

    def assign(self, action_name, *args, **kwargs):
        method = getattr(self, action_name, None)
        if not method:
            raise ValueError(f"No such action: {action_name}")
        return method(*args, **kwargs)

    @action("balance")
    def balance_action(self, add: int = 0, subtract: int = 0):
        if add:
            self.balance += add
        elif subtract:
            if self.balance - subtract < 0:
                LOG(f" Operation denied ! Balance not available for removal -#{subtract}#-")
                raise ValueError("Insufficient balance. Operation denied!")

            self.balance -= subtract
        save_stuff(self.balance, self.balance_file, type="w")
        return self.balance


    @action("addInventory")
    def addInventory(self, name: str, price: int, quantity: int):
        new_item = f"{name},{price},{quantity}"
        try:
            self.items.append(Item(name, price, quantity))
            save_stuff(new_item, self.inventory_file)
            LOG(f"AddInventory: Added item {name} - price {price} - quantity {quantity})")
            print(f"{name} Added successfully")
            return True
        except Exception as e:
            LOG(f"AddInventory: Failed to add item {name}: {e}")
            return False

    @action("purchase")
    def purchase(self, item_index: int, quantity: int):
        items_list=[]
        total=0

        if item_index < 0 or item_index >= len(self.items):
            print("option not available. Try again")

        item = self.items[item_index]
        item_total_cost = int(item.price) * quantity

        if self.balance - item_total_cost < 0:
            LOG(f"[{datetime.now()}] Purchase denied: Insufficient balance, total cost {item_total_cost}, balance {self.balance}")
            raise ValueError("Insufficient balance to proceed with sell")

        item.quantity = int(item.quantity) - int(quantity)
        self.balance -= int(item_total_cost)

        item.quantity = int(item.quantity) - quantity

        if int(item.quantity) < 0:
            print(f"Can't sell quantity: {quantity} as there's not that many units")
            LOG(f"Operation denied: Not enough stock for {item.name} - Item quantity requested - {quantity} - total available: {item.quantity}")
            return None

        else:
            total_cost = total + int(item.price) * quantity

            items_list.append([item.name, int(item.price), int(quantity), total_cost])

            print("Current total: ",total_cost)

            if  self.balance - total_cost < 0 :
                print("Operation denied no change available! please try again")
                LOG(f"Operation denied: Items purchased- {item.name} - Item quantity - {item.quantity} - total value: {item_total_cost} - Total value above balance")
                total=0
                return None

            LOG(f"Items purchased- {item.name} - Item quantity - {item.quantity} - total value: {total}")

        save_stuff(self.balance, self.balance_file, type="w")

        #Save inventory
        with open(self.inventory_file, "w") as f:
            for its in self.items:
                f.write(f"{its.name},{its.price},{its.quantity}\n")


        LOG(f"Purchased {quantity} of {item.name}, cost {item_total_cost}")
        LOG(f"Purchased {quantity} of {item.name}; new balance {self.balance}")

        return items_list

    @action("balance_report")
    def balance_report(self):
        LOG(f"Balance report requested: {self.balance}")
        return self.balance


