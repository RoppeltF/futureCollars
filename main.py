
# from inventory import Inventory


op = 99
items = []

balance = 1000

def menu(menu_name,menu_options):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(menu_options,1):
        print( f"{x} - {opt}")
    print("0 - Quit")

def items_menu(menu_name,items):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(items, 1):
        print(f"#{x} - {opt["item_name"]}")
    print("0 - Quit")

def warehouse_balance(balance):
    #The program should prompt for an amount to add or subtract from the account.
    options = ["Add Balance", "Subtract"]
    while True:
        menu("Balance Menu",options)
        op = int( input("\n Chose the operation to perform: "))

        if op == 0:
            break
        elif op == 1:
            a = int(input(f"Enter the amount to add to company Balance: {balance} :"))
            balance = balance + a
            print("New balance: ", balance )
        elif op == 2:
            a = int(input(f"Enter the amount to deduct from company Balance: {balance} :"))
            balance = balance - a
            print("New balance: ", balance )
        else:
            print("Operation invalid Try again")
    return balance


def inventory(item_name,item_quantity,item_price):
    try:
         if item_name != None and item_name != "":
            items_dict = {}
            items_dict["item_name"] = item_name
            items_dict["item_info"] = {"item_price": item_price, "item_quantity": item_quantity}
            items.append(items_dict)
            print("Item added")
            return items
         elif items:
             return items
         else:
            print("Empy inventory please add some. \n")
            add_inventory()
            return 0
    except ValueError:
        print("Something fail")


def add_inventory():
    try:
        n = int(input("How many items will be added:  "))
        for i in range(n):
            item_name = input("Name item to add: ")
            item_price = input(f"Add the price for {item_name}: ")
            item_quantity = input(f"How many {item_name} is available: ")
            inventory(item_name, item_quantity, item_price)
    except ValueError:
        print("\n")
        print("Invalid number please try again \n")
        add_inventory()


def show_inventory():
    for x, opt in enumerate(items,1):
        print(f"{x} - {opt["item_name"]} - Price: {opt["item_info"]["item_price"]} - Quantity: {opt["item_info"]["item_quantity"]}")



def sale():
    #The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly.
    options = ['Add Item', 'Manage price', 'Manage quantity']
    while True:
        menu("Sale Menu", options)

        op = int( input("\n Chose the operation to perform: "))

        if op == 0:
            break
        elif op == 1: #ADD ITEM
            try:
                add_inventory()
            except ValueError:
                 print("Failed to add items")

        elif op == 2:
            items = inventory("","","")
            if items == 0 :
                print("\n")
                sale()
                # items = add_inventory()
            else:
                print("\n")
                items_menu("Price Update Menu", items)
                try:
                    print("\n")
                    op = int(input("Pick item N. to update the price: "))
                except ValueError:
                    print("incorrect Option, please try again")
                    print("\n")
                    op = int(input("Pick item N. to update the price: "))

                if op == 0:
                    break

                op -=1
                print(f"Item selected: {items[op]['item_name']}")
                print(f"Old Item price: {items[op]['item_info']['item_price']}")

                try:
                    new_price = int(input("Enter new price: "))
                except ValueError:
                    print("Value must be greater than 0")
                    new_price = int(input("Enter new price: "))

                items[op]['item_info']['item_price'] = new_price

        elif op == 3:
            items = inventory(None,None,None)
            if items == 0 :
                print("\n")
                sale()
                # items = add_inventory()
            else:
                items_menu("Quantity Update Menu", items)

                try:
                    print("\n")
                    op = int(input("Pick item N. to update the quantity: "))
                except ValueError:
                    print("incorrect Option, please try again")
                    print("\n")
                    op = int(input("Pick item N. to update the quantity: "))

                if items == 0:
                    print("\n")
                    sale()
                if op == 0:
                    break
                op -= 1
                print(f"Item selected: {items[op]['item_name']}")
                print(f"Old Item quantity: {items[op]['item_info']['item_quantity']}")

                try:
                    new_quantity = int(input("Enter new quantity: "))
                except ValueError:
                    print("Value must be greater than 0")
                    new_quantity = int(input("Enter new quantity: "))

                items[op]['item_info']['item_quantity'] = new_quantity

                print("!!!! Information updated !!!!")
                print(f"Item: {items[op]["item_name"]}")
                print(f"Quantity:{items[op]["item_info"]["item_quantity"]}")
                print(f"Item Value:{items[op]["item_info"]["item_price"]}")


def purchase(balance):
    # The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly. Ensure that the account balance is not negative after a purchase operation.
    total = 0
    while True:
        items_menu("Select Item to Sell", items)
        print("")
        if items:
            op = int(input("Select item to sell: "))
            if op == 0:
                print(f"Total: {total}")
                break
            op -= 1
            print(f"Selected Item: {items[op]["item_name"]}")
            print(f"Item Price: {items[op]["item_info"]["item_price"]}")
            quantity = int(input("How many will be bought: "))
            items[op]["item_info"]["item_quantity"] = int(items[op]["item_info"]["item_quantity"]) - quantity
            total = total + int(items[op]["item_info"]["item_price"]) * quantity

        else:
            print("Inventory is empty please add some")
            add_inventory()
            purchase(balance)

    print(f"Total: {total}")
    balance = balance - total
    return balance


def list():
    #Display the total inventory in the warehouse along with product prices and quantities.
    if items:
        while True:
            items_menu("Inventory",items)

            op = int(input("\n Chose item to display its information: "))

            if op == 0:
                break
            else:
                op -= 1
                print("")
                print(f"Item: {items[op]["item_name"]}")
                print(f"Quantity:{items[op]["item_info"]["item_quantity"]}")
                print(f"Item Value:{items[op]["item_info"]["item_price"]}")
                print("")
    else:
        inventory("", "", "")
        list()

# def review():
    #Prompt for two indices 'from' and 'to', and display all recorded operations within that range. If ‘from’ and ‘to’ are empty, display all recorder operations. Handle cases where 'from' and 'to' values are out of range.


options = ['Update Balance', 'Manage Inventory', 'Sell', 'Account Balance', 'List', 'Warehouse', 'Review']

while True:
    menu("Warehouse Menu",options)

    op = int(input("\n Chose the operation to perform: "))

    if op == 0:
        break
    elif op == 1:
        balance = warehouse_balance(balance)
    elif op == 2:
        sale()
    elif op == 3:
        balance = purchase(balance)
    elif op == 4:
        print("::: Account Balance :::")
        print("")
        print(balance)
    elif op == 5:
        print("::: Warehouse Status :::")
        show_inventory()
    elif op == 6:
        print("::: Warehouse Status :::")
        list()
    elif op == 7:
        print("Review not available yet")
        # review()
    else:
        print("Invalid Option")
