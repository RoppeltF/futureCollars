import functools
from datetime import datetime



def menu(menu_name,menu_options):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(menu_options,1):
        print( f"{x} - {opt.capitalize()}")
    print("0 - Quit")


def items_menu(menu_name,items):
    if not items:
        print("No inventory Available, Try adding some!")
        return 1
    else:
        print(f":::: {menu_name}  ::::")
        for x, item in enumerate(items, 1):
            print(f"#{x} - {item.name}")
        print("#0 - Quit")
        return 0


def op_check(message):
    try:
        op = int(input(f"{message} "))
    except ValueError:
        print("Invalid option please try again !")
        return op_check(message)
    return op


def save_stuff(item,file_name,type="a+"):
    item = str(item)
    file_name = str(file_name)
    with open(file_name,type) as file:
        file.write(item+"\n")


def LOG(log_entry,file_name="LOG.txt"):
    log_entry = f"[{datetime.now()}] {log_entry}"
    save_stuff(log_entry,file_name)


#Rel. Manager class
def load_balance(filename):
    try:
        with open(filename,"r") as balance:
            balance = balance.read()
            balance.strip()
            current_balance = int(balance)
    except FileNotFoundError:
        print("File with Balance does not exists, creating new file with 0 balance")
        print("Please update your balance")
        current_balance = 0
    return current_balance


#Log decorator
def action(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            save_stuff(f"[{datetime.now()}] Action: {name} started", "LOG.txt")
            result = func(self, *args, **kwargs)
            save_stuff(f"[{datetime.now()}] Action: {name} completed", "LOG.txt")
            return result
        return wrapper
    return decorator


def print_receipt(items):
    print("")
    print("")
    print(items)
    print("")
    print("")
    if items:

        item_width = max(len(x[0][0]) for x in items) + 2
        price_width = 10
        qty_width = 10
        total_width = 10

        total_line = item_width + price_width + qty_width + total_width + 6
        total_purchased = 0

        print("#" * total_line)
        print(
            f"{'Item:':<{item_width}} {'Price:':>{price_width}} {'Quantity:':>{qty_width}} {'Total:':>{total_width}}")

        for its in items:
            for name, price, qty, total in its:
                print(f"{name:<{item_width}} {price:>{price_width}} {qty:>{qty_width}} {total:>{total_width}}")
                total_purchased += total

        print("")
        print(f"Total purchased: #{total_purchased}")
        print("")
        print("#" * total_line)
        print("")