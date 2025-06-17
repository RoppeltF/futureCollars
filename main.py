"""
# Hints:
#
# - Use a loop to continuously prompt for commands until the 'end' command is entered.
# - Keep track of the account balance and warehouse inventory.
# - Remember to handle edge cases, like invalid command inputs, negative amounts during a 'purchase' operation, or out-of-range indices during a 'review' operation.
# - The balance, sale, and purchase commands are remembered by the program.
# - Handle user inputs that are not as expected. The program should not crash in these cases, but instead, it should display an appropriate error message.
# """


op = 99
items = []
balance = 0

def menu(menu_name,menu_options):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(menu_options[::-1],0):
        print(x, " - " + opt)

def inventory(item_name,item_quantity,item_price):

    items_dict ={}
    items_dict["item_name"] = item_name
    items_dict["item_info"] = {"item_price": item_price,"item_quantity": item_quantity}
    items.append(items_dict)

def balance():
    #The program should prompt for an amount to add or subtract from the account.
    options = ["add","sub"]

    op = int( input("\n Chose the operation to perform: "))

    while True:
        if op == 0:
            break
        elif op == 1:
            a = int(input("Select 1st number to add:"))
            b = int(input("Select 1st number to add:"))
            print("Result: ", a + b)
        elif op == 2:
            a = int(input("Select 1st number to subtract:"))
            b = int(input("Select 1st number to subtract:"))
            print("Result: ", a - b)
        else:
            print("Operation invalid Try again")

def sale():
    #The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly.
    options = ["Manage quantity", "Manage price","Add Item","Quit"]
    while True:
        menu("Sale", options)

        op = int( input("\n Chose the operation to perform: "))

        if op == 0:
            break
        elif op == 1: #ADD ITEM
            try:
                n = int(input("How many items will be added:  "))
            except ValueError:
                print("Invalid number please try again \n")
                n = int(input("How many items will be added:  "))

            for i in range(n):
                item_name = input("Name item to add: ")
                item_price = input(f"Add the price for {item_name}: ")
                item_quantity = input(f"How many {item_name} is available: ")

                inventory(item_name,item_quantity,item_price)

        elif op == 2:
            print("Operation invalid Try again")
        elif op == 3:
            print("Operation invalid Try again")
        elif op == 4:
            print("Operation invalid Try again")
        else:
            print("Operation invalid Try again")


def purchase():
    # The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly. Ensure that the account balance is not negative after a purchase operation.
    options = ["add","sub"]
    print("::: Balance Menu :::")
    for x, opt in enumerate(options, 1):
        print(x, " - " + opt)
    op = int( input("\n Chose the operation to perform: "))

def account():
    #Display the current account balance.
    options = ["add","sub"]
    print("::: Account Balance Menu :::")
    for x, opt in enumerate(options, 1):
        print(x, " - " + opt)
    op = int( input("\n Chose the operation to perform: "))

def list():
    #Display the total inventory in the warehouse along with product prices and quantities.
    options = ["quantity","price"]
    print("::: Item Menu :::")
    for x, opt in enumerate(options, 1):
        print(x, " - " + opt)
    op = int( input("\n Chose the operation to perform: "))

def warehouse():
    #Prompt for a product name and display its status in the warehouse.
    options = ["add","sub"]
    print("::: Warehouse Status :::")
    for x, opt in enumerate(options, 1):
        print(x, " - " + opt)
    op = int( input("\n Chose the operation to perform: "))

def review():
    #Prompt for two indices 'from' and 'to', and display all recorded operations within that range. If ‘from’ and ‘to’ are empty, display all recorder operations. Handle cases where 'from' and 'to' values are out of range.
    options = ["add","sub"]
    print("::: Balance Menu :::")
    for x, opt in enumerate(options, 1):
        print(x, " - " + opt)
    op = int( input("\n Chose the operation to perform: "))


# options = ['Review', 'Warehouse', 'List', 'Account', 'Purchase', 'Sale', 'Balance', "Quit"]
print("####### options var #############")


while True:
    menu("Warehouse Menu",['Review', 'Warehouse', 'List', 'Account', 'Purchase', 'Sale', 'Balance', "Quit"])

    print("\n")
    op = int(input("Enter the desired Option:: "))

    if op == 0:
        break
    elif op == 1:
        balance()
    elif op == 2:
        sale()
    elif op == 3:
        a = int(input("Select 1st number to multiply:"))
        b = int(input("Select 1st number to multiply:"))
        print("Result: ", a * b)
    elif op == 4:
        a = int(input("Select 1st number to divide:"))
        b = int(input("Select 1st number to divide:"))
    elif op == 5:
        a = int(input("Select 1st number to add:"))
        b = int(input("Select 1st number to add:"))
        print("Result: ", a + b)
    elif op == 6:
        a = int(input("Select 1st number to subtract:"))
        b = int(input("Select 1st number to subtract:"))
        print("Result: ", a - b)
    elif op == 7:
        a = int(input("Select 1st number to multiply:"))
        b = int(input("Select 1st number to multiply:"))
        print("Result: ", a * b)
    else:
        print("Invalid Option")
