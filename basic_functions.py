from datetime import datetime

def LOG(log_entry,file_name="LOG.txt"):
    log_entry = f"[{datetime.now()}] ; {log_entry}"
    save_stuff(log_entry,file_name)

def save_stuff(item,file_name,type="a+"):
    item = str(item)
    file_name = str(file_name)
    try:
        with open(file_name,type) as file:
            file.write(item+"\n")
        print(f"Saving/updating: {item}")
    except:
        print(f"Error while adding information: {item}")
        print(f"Error while adding information to file: {file_name}")


def load_inventory_from(filename):
    items = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                items.append(line.strip())
    except FileNotFoundError:
        print(f"File {filename} does not exists, creating it")
        save_stuff("",filename)
    return items


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


def load_balance(filename):
    try:
        with open(filename,"r") as balance:
            balance = balance.read()
            balance.strip()
            current_balance = int(balance)
    except FileNotFoundError:
        LOG("File with Balance does not exists, creating new file with 0 balance")
        current_balance = "0"
        with open(filename,"w") as balance:
            balance.write(current_balance)
    return current_balance