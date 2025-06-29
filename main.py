items = [{"item_name":"popcorn","item_info":{"price":"7","quantity":"99"}},
        {"item_name":"pans","item_info":{"price":"1","quantity":"999"}},
        {"item_name":"TV","item_info":{"price":"700","quantity":"9"}}
        ]

balance = 1000

LOG=[]

def menu(menu_name,menu_options):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(menu_options,1):
        print( f"{x} - {opt}")
    print("0 - Quit")

def items_menu(menu_name,items):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(items, 1):
        print(f"#{x} - {opt["item_name"]}")
    print("#0 - Quit")


def op_check(message):
    try:
        op = int(input(f"{message}: "))
    except ValueError:
        print("Invalid option please try again !")
        op_check(message)
    return op


def purchase(balance):
    # The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly. Ensure that the account balance is not negative after a purchase operation.
    total = 0
    while True:
        items_menu("Select Item to Sell", items)
        print("")
        if items:
            op = int(input("Select item to sell: "))
            if op == 0:
                break
            op -= 1
            if op < len(items):
                print(f"Selected Item: {items[op]["item_name"]}")
                print(f"Item Price: {items[op]["item_info"]["price"]}")
                quantity = int(input("How many will be bought: "))
                items[op]["item_info"]["quantity"] = int(items[op]["item_info"]["quantity"]) - quantity
                total = total + int(items[op]["item_info"]["price"]) * quantity
                check_balance =  balance - total
                if  check_balance < 0 :
                    print("Operation denied no change available! please try again")
                    LOG.append(f"Operation denied !! -- Items purchased- {items[op]["item_name"]} - Item quantity - {items[op]["item_info"]["quantity"]} - total value: {total}")
                    total=0
                    break
                LOG.append(f" Items purchased- {items[op]["item_name"]} - Item quantity - {items[op]["item_info"]["quantity"]} - total value: {total}")
            else:
                print("option not available. Try again")
                purchase(balance)
        else:
            print("Inventory is empty please add some")
            break

    print(f"Total purchased: {total}")
    balance = balance - total
    print(f"Warehouse balance: {balance}")
    LOG.append(f"New warehouse balance: {balance}")
    return balance

while True:
    options = ["balance", "sale", "purchase", "account", "list", "warehouse", "review"]
    menu("Warehouse Menu",options)

    op = op_check("Chose the operation to perform:")

    if op == 0:
        break
    elif op == 1:
        options=["Add","Subtract"]
        while True:
            menu("Balance Menu",options)
            op = op_check("chose an operation:")
            if op ==0:
                break
            if op == 1:
                new_balance = int(input(f"Enter value to add to balance- {balance} - :"))
                balance += new_balance

                LOG.append(f" Value added on account- {new_balance} - total new balance {balance} ")

            if op == 2:
                new_balance = int(input(f"Enter value to subtract to balance- {balance} - :"))
                LOG.append(f" Value removed from account- {new_balance} - total new balance {balance} ")
                balance -= new_balance


        print(f"\nNew balance is {balance}:")
        print("")

    elif op == 2:

        print(":::: Sale Menu ::::")
        print("")
        item_name = input("Enter new item Name:")
        item_price = int(input(f"Enter {item_name} price:"))
        item_quantity = int(input(f"Enter {item_name} quantity:"))

        new_item = {}
        new_item = {"item_name":item_name,"item_info":{"price":item_price,"quantity":item_price}}

        try:
            items.append(new_item)
            print(f"{item_name} added !")
            LOG.append(f" New item added:{ item_name} - Price: {item_price} - Quantity: {item_quantity}")
        except:
            print(f"An error happened {item_name} not added! ")
            LOG.append(f"ERROR ADDING ITEM {item_name}")

    elif op == 3:
        balance = purchase(balance)
    elif op == 4:
        print("::: Account Balance :::")
        print("")
        print(f" Current Balance: {balance}")
        print("")
        LOG.append(f"Balance requested - {balance}")
    elif op == 5:
        print("")
        print(f":::: Warehouse Stock  ::::")
        print(f"Total items: {len(items)}")
        for x, item in enumerate(items, 1):
            print(f"#{x} - {item["item_name"]}")

        LOG.append(f" Full Warehouse stock Visualized")
        print("")
    elif op == 6:
        while True:
            items_menu("Item Stock", items)
            op = op_check("Enter item number to show its status:")
            if op == 0:
                break
            op -= 1

            print(f"# Name:   {items[op]["item_name"]} ")
            print(f"##L Item Price:  {items[op]["item_info"]["price"]} ")
            print(f"##L Item quantity: {items[op]["item_info"]["quantity"]} ")
            print("")
            LOG.append(f"Item Visualized: {items[op]["item_name"]} - Item Price:  {items[op]["item_info"]["price"]} -  Item quantity: {items[op]["item_info"]["quantity"]} ")

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
                LOG.append("LOG FILE FULLY VISUALIZED")
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

                LOG.append("LOG Visualized from line {x} to {y}")
    else:
        print("Invalid Option")
