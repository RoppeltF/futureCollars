
LOG=[]

class Item():
    def __init__(self,name, price, quantity):
        self.name     = name
        self.price    = price
        self.quantity = quantity

    def __str__(self):
        return f"Product: {self.name} - Price: {self.price} - Quantity: {self.quantity}"

    def convert_to_csv(self):
        return f"{self.name},{self.price},{self.quantity}"


def menu(menu_name,menu_options):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(menu_options,1):
        print( f"{x} - {opt}")
    print("0 - Quit")


def items_menu(menu_name,items):
    if not items:
        print("No inventory Available, Try adding some!")
    else:
        print(f":::: {menu_name}  ::::")
        for x, item in enumerate(items, 1):
            print(f"#{x} - {item.name}")
        print("#0 - Quit")


def op_check(message):
    try:
        op = int(input(f"{message}: "))
    except ValueError:
        print("Invalid option please try again !")
        op_check(message)
    return op


def save_stuff(item,file_name,type="a+"):
    item = str(item)
    file_name = str(file_name)
    with open(f"{file_name}.txt",type) as file:
        file.write(item+"\n")


def load_csv_to_obj(items):  # Map text line to object
    name, price, quantity = items.strip().split(',')
    return Item(name, price, quantity)


def load_inventory_from(filename):
    items = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                items.append(load_csv_to_obj(line))
    except FileNotFoundError:
        print("File with inventory not exists, creating new file")
    return items


def load_balance():
    with open("balance.txt") as balance:
        balance = balance.read()
        balance.strip()
        current_balance = int(balance)

    return current_balance

def print_receipt(items):
    item_width = max(len(x[0]) for x in items) + 2
    price_width = 10
    qty_width = 10
    total_width = 10

    total_line = item_width + price_width + qty_width + total_width + 6
    total_purchased = 0


    print("#" * total_line)
    print(f"{'Item:':<{item_width}} {'Price:':>{price_width}} {'Quantity:':>{qty_width}} {'Total:':>{total_width}}")

    for name, price, qty, total in items:
        print(f"{name:<{item_width}} {price:>{price_width}} {qty:>{qty_width}} {total:>{total_width}}")
        total_purchased +=total
    print("")
    print(f"Total purchased: #{total_purchased}")
    print("")
    print("#" * total_line)
    print("")

def purchase(balance,items):
    # The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly. Ensure that the account balance is not negative after a purchase operation.
    total = 0
    items_list = []
    while True:
        items_menu("Select Item to Sell", items)
        print("")
        if items:
            op = op_check("Select item to sell: ")

            if op == 0:
                break
            op -= 1
            if op < len(items):

                print(f"Selected Item: {items[op].name}")
                print(f"Item Price: {items[op].price}")
                quantity = int(input("How many will be bought: "))
                items[op].quantity = int(items[op].quantity) - quantity
                total = total + int(items[op].price) * quantity

                item = items[op].name,items[op].price,quantity,total
                items_list.append(item)

                print("Current total: ",total)

                check_balance =  balance - total
                if  check_balance < 0 :
                    print("Operation denied no change available! please try again")
                    save_stuff(f"Operation denied !! -- Items purchased- {items[op].name} - Item quantity - {items[op].quantity} - total value: {total}","LOG")
                    total=0
                    break
                save_stuff(f" Items purchased- {items[op].name} - Item quantity - {items[op].quantity} - total value: {total}","LOG")
            else:
                print("option not available. Try again")
                purchase(balance,items)
        else:
            print("Inventory is empty please add some")
            break

    print_receipt(items_list)

    # print(f"Total purchased: {total}")
    balance = balance - total
    save_stuff(balance,"balance","w")
    print(f"Warehouse balance: {balance}")
    save_stuff(f"New warehouse balance: {balance}","LOG")
    return balance


while True:

    items = load_inventory_from("inventory.txt")
    current_balance = load_balance()


    options = ["balance", "sale", "purchase", "account", "list", "warehouse", "review"]
    menu("Warehouse Menu",options)

    op = op_check("Chose the operation to perform:")

    if op == 0:
        break

    elif op == 1:
        options=["Add","Subtract"]

        while True:
            current_balance = load_balance()
            menu("Balance Menu",options)
            op = op_check("chose an operation: ")

            if op ==0:
                break

            if op == 1:
                new_balance = int(input( f"Value to add to balance -#{current_balance}#- : " ) )
                current_balance = current_balance + new_balance

                save_stuff(current_balance,"balance","w")
                save_stuff(f"Value added on account -#{new_balance}#-  total new balance -#{current_balance}#-","LOG")

            if op == 2:
                # current_balance = load_balance()
                new_balance = int(input(f"Value to subtract from balance -#{current_balance}#- :"))


                if  current_balance - new_balance < 0 :
                    print("Operation denied Balance can't be Negative! ")
                    save_stuff(f"Operation denied ! Balance not available for removal -#{current_balance}#-","LOG")
                    break

                current_balance = current_balance - new_balance

                save_stuff(f"Value removed from account -#{new_balance}#- total new balance -#{current_balance}#-","LOG")

                save_stuff(current_balance, "balance","w")

        print(f"\nBalance is {current_balance}:")
        print("")

    elif op == 2:

        print(":::: Sale Menu ::::")
        print("")
        item_name = input("Enter new item Name:")
        item_price = int(input(f"Enter {item_name} price:"))
        item_quantity = int(input(f"Enter {item_name} quantity:"))

        new_item = f"{item_name},{str(item_price)},{str(item_quantity)}"

        try:
            items.append(new_item)
            print(f"{item_name} added !")

            save_stuff(new_item, "inventory")
            save_stuff(f" New item added:{ item_name} - Price: {item_price} - Quantity: {item_quantity}","LOG")

        except:
            print(f"An error happened {item_name} not added! ")
            save_stuff(f"ERROR ADDING ITEM {item_name}","LOG")
    elif op == 3:
        current_balance = purchase(current_balance,items)
    elif op == 4:
        print("::: Account Balance :::")
        print("")

        print(f" Current Balance: {current_balance}")
        print("")
        save_stuff(f"Balance requested - {current_balance}","LOG")
    elif op == 5:
        print("")
        print(f":::: Warehouse Stock  ::::")
        print(f"Total items: {len(items)}")
        for x, item in enumerate(items, 1):
            print(f"#{x} - {item.name}")

        save_stuff(f"Full Warehouse stock Visualized","LOG")
        print("")
    elif op == 6:
        while True:
            items_menu("Item Stock", items)
            op = op_check("Enter item number to show its status:")
            if op == 0:
                break
            op -= 1

            print(f"# Name:   {items[op].name} ")
            print(f"## Item Price:  {items[op].price} ")
            print(f"## Item quantity: {items[op].quantity} ")
            print("")
            save_stuff(f"Item Visualized: {items[op].name} - Item Price:  {items[op].price} -  Item quantity: {items[op].quantity}","LOG")

    elif op == 7:
        while True:
            options=["All","Range"]
            menu("Logs Review",options)
            op = op_check("Choose option to review logs: ")

            if op == 0:
                break
            if op == 1:
                for x, log in enumerate(LOG,1):
                    print(f"#{x} - {log}")
                save_stuff("LOG FILE FULLY VISUALIZED","LOG")
            if op == 2:
                x = op_check(f"Enter 1st value to check Logs from 0 to {len(LOG)}: ")
                y = op_check(f"Enter 2st value to check Logs from 0 to {len(LOG)}: ")

                if y >= x:
                    for z, log in enumerate(LOG[x:y], 1):
                        print(f"#{z} - {log}")
                else:
                    print(f"Please try again 2 value must be bigger than 1st value {x}: ")
                    y = op_check(f"Enter 2st value to check Logs from 0 to {len(LOG)}: ")
                    for z, log in enumerate(LOG[x:y], 1):
                        print(f"#{z} - {log}")

                save_stuff("LOG Visualized from line {x} to {y}","LOG")
    else:
        print("Invalid Option")