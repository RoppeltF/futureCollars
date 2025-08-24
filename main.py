from basic_functions import *
from Item import *
from Manager import *

def main():
    manage = Manager()

    while True:

        items = load_inventory_from("inventory.txt")
        current_balance = load_balance("balance.txt")

        options = ["balance", "add Inventory", "purchase", "account", "list Inventory", "warehouse", "review"]
        menu("Warehouse Menu", options)

        op = op_check("Chose the operation to perform:")

        if op == 0:
            break

        # Balance
        elif op == 1:
            options = ["Add", "Subtract"]

            while True:
                current_balance = load_balance("balance.txt")
                menu("Balance Menu", options)
                op = op_check("chose an operation: ")

                if op == 0:
                    break

                if op == 1: #Aadd / Subtract Balance
                    current_balance = manage.assign("balance_action")
                    new_balance = int(input(f"Value to add to current balance #{current_balance} : "))
                    manage.assign("balance_action", add=new_balance)

                    print(f"NEW BALANCE: {manage.assign("balance_action")}")

                    save_stuff(f"Value added on account #{new_balance} total new balance #{current_balance}#","LOG.txt")
                if op == 2:
                    new_balance = int(input(f"Value to subtract from balance #{current_balance} :"))

                    if current_balance - new_balance < 0:
                        manage.assign("balance_action", subtract=new_balance)

                    print(f"NEW BALANCE: {manage.assign("balance_action")}")
                    save_stuff(f"Value removed from account #{new_balance}# total new balance #{current_balance}#-","LOG.txt")

            print(f"\nNew Balance is {manage.assign("balance_action")}:")
            print("")

        # Add Inventory
        elif op == 2:

            print(":::: Add Inventory Menu ::::")
            print("")
            item_name = input("Enter new item Name:")
            item_price = int(input(f"Enter {item_name} price:"))
            item_quantity = int(input(f"Enter {item_name} quantity:"))

            # new_item = f"{item_name},{str(item_price)},{str(item_quantity)}"
            manage.assign("addInventory",item_name,item_price,item_quantity)
            # manage.addInventory(item_name,item_price,item_quantity)

        # Sell items
        elif op == 3:
            purchase_list = []
            while True:
                items_menu("Select Item to Sell", items)
                print("")
                if items:
                    op = op_check("Select item:")

                    if op == 0:
                        print_receipt(purchase_list)
                        break

                    else:

                        op -= 1

                        print(f"Selected Item: {items[op].name}")
                        print(f"Item Price: {items[op].price}")
                        print(f"Item Stock: {items[op].quantity}")

                        print("")
                        quantity = int(input("How many will be bought: "))

                        purchase_list.append(manage.assign("purchase",op,quantity))

        # Show Balance
        elif op == 4:
            print("::: Account Balance :::")
            print("")

            print(f" Current Balance: {manage.balance_report()}")
            print("")
            save_stuff(f"Balance requested - {current_balance}", "LOG.txt")

        # List Items in inventory.txt
        elif op == 5:
            print("")
            print(f":::: Warehouse Stock  ::::")
            print(f"Total items: {len(items)}")
            for x, item in enumerate(items, 1):
                print(f"#{x} - {item.name}")

            save_stuff(f"Full Warehouse stock Visualized", "LOG.txt")
            print("")

        # Stock info
        elif op == 6:
            while True:

                if items_menu("Item Stock", items) == 0:
                    op = op_check("Enter item number to show its status or 0 to quit")
                    if op == 0:
                        break
                    else:
                        op -= 1

                    print(f"# Name:   {items[op].name} ")
                    print(f"## Item Price:  {items[op].price} ")
                    print(f"## Item quantity: {items[op].quantity} ")
                    print("")
                    LOG(f"Item Visualized: {items[op].name} - Item Price:  {items[op].price} -  Item quantity: {items[op].quantity}")
                else:
                    break

        # LOG Review
        elif op == 7:
            while True:
                options = ["all", "range"]
                menu("LOG's Review", options)
                op = op_check("Choose option to review LOG: ")

                if op == 0:
                    break
                if op == 1:
                    for x, LOG.txt in enumerate(LOG.txt, 1):
                        print(f"#{x} - {LOG.txt}")
                    save_stuff("LOG.txt FILE FULLY VISUALIZED", "LOG.txt")
                if op == 2:
                    x = op_check(f"Enter 1st value to check LOG.txts from 0 to {len(LOG.txt)}: ")
                    y = op_check(f"Enter 2st value to check LOG.txts from 0 to {len(LOG.txt)}: ")

                    if y >= x:
                        for z, LOG.txt in enumerate(LOG.txt[x:y], 1):
                            print(f"#{z} - {LOG.txt}")
                    else:
                        print(f"Please try again 2 value must be bigger than 1st value {x}: ")
                        y = op_check(f"Enter 2st value to check LOG.txts from 0 to {len(LOG.txt)}: ")
                        for z, LOG.txt in enumerate(LOG.txt[x:y], 1):
                            print(f"#{z} - {LOG.txt}")

                    save_stuff("LOG.txt Visualized from line {x} to {y}", "LOG.txt")
        else:
            print("Invalid Option")


if __name__ == '__main__':
    main()