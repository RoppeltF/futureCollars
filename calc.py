from math import floor

products = {
    "product_floor_tiles_white": {"price": 120, "size": 15},  # product with a price calculated according to packages
    "product_floor_tiles_black": {"price": 140, "size": 20},  # product with a price calculated according to packages
    "paint_can": {"price": 60},  # product with art price
    "paint_brush": {"price": 60},  # product with art price
    "planks": {"price": 80, "loss": 0.1, "unit": "meters"},  # product with price per quantity with loss
    "concrete": {"price": 60, "loss": 0.05, "unit": "kilograms"}  # product with price per quantity with loss
}

products_piece = {"paint_can", "paint_brush"}
products_pack = {"product_floor_tiles_white", "product_floor_tiles_black"}
products_amount = {"planks", "concrete"}


def piece_or_pack_ask():
    print("Enter number of pieces")
    return int(input())


def amount_ask(unit_name):
    print("Enter quantity ({})".format(unit_name))
    return floor(int(input()))


def piece_print(quantity):
    print("ordered {} quantity".format(quantity))


def pack_print(quantity, pack_size):
    packs = int((quantity + pack_size - 1) / pack_size)
    print("ordered {} the number of packages".format(packs))


def amount_print(quantity, unit):
    print("ordered {} ({})".format(quantity, unit))


def price_piece(price, quatity):
    return price * quantity

# def price_pack(price, pack_size, pieces)

# def price_amount(price, loss, quantity)


total_price = 0
while True:
    print("Enter a product name or a blank line if you want to end")
    product = input()
    if not product:
        break
    if product not in products:
        print("Wrong product name")
        continue
    # Asking about order of quantity
    if product in products_piece or product in products_pack:
        quantity = piece_or_pack_ask()
    if product in products_amount:
        quantity = amount_ask(products[product]["unit"])
    # Print the confirmation
    if product in products_piece:
        piece_print(quantity)
    if product in products_pack:
        pack_print(quantity, products[product]["size"])
    if product in products_amount:
        amount_print(quantity, products[product]["unit"])
    # Caclulate and add the price
    if product in products_piece:

        if product in products_pack:

            if product in products_amount: