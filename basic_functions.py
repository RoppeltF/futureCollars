def save_stuff(data, filename):
    with open(filename, "a") as f:
        f.write(data + "\n")

def load_inventory_from(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]
