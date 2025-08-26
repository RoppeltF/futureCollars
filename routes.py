from flask import Flask, render_template, request, session

from basic_functions import *

app = Flask(__name__)

@app.route('/')
@app.route('/dashboard')
@app.route('/home')
@app.route('/index')
def dashboard():
    balance = load_balance("balance.txt")
    inventory = load_inventory_from("inventory.txt")
    inventory_qty = 0

    for item in inventory:
        inventory_qty += int( item.split(",")[-1].strip("/") )
    return render_template("dashboard.html", page_title="Home", balance=balance, inventory=inventory_qty)


@app.route('/add_inventory')
def add_inventory():
    return render_template("add_inventory.html",page_title="Add Inventory")


@app.route('/add_item_form', methods=["POST","GET"])
def get_data():
    LOG("Action Started: Adding item to Inventory")

    name = request.form["item_name"]
    price = request.form["item_price"]
    quantity = request.form["item_quantity"]

    LOG(f"Adding item to Inventory: Name: {name} Price: {price} Quantity: {quantity}")
    save_stuff(f"{name},{price},{quantity}","inventory.txt")
    LOG("Action Stopped: Adding item to Inventory")
    return render_template("add_inventory_response.html",item_name=name),{"Refresh": "3; url=dashboard"}


@app.route('/sell')
def sell():
    inventory = load_inventory_from("inventory.txt")
    item_list = []

    for item in inventory:
        item_list.append( item.split(",")[0] )


    return render_template("sell.html",page_title="Sell",item_list=item_list)

@app.route('/cart',methods=["POST","GET"])
def cart():
    LOG("Action Started: Adding item to cart")
    item_name = request.form["item_name"]

    amount_requested = request.form["amount"]

    inventory = load_inventory_from("inventory.txt")

    inv_item_name = []
    for item in inventory:
        inv_item_name.append(item.split(",")[0])

    item_id = inv_item_name.index(item_name)

    item_name,item_price,item_quantity = inventory[item_id].split(",")

    save_stuff(f"{item_name},{amount_requested},{item_price}","cart.txt")

    #updating stock amount
    new_item_stock = int(item_quantity) - int(amount_requested)
    print("New Item STOCK:: ",new_item_stock)
    if new_item_stock >= 0:
        inventory[item_id] = f"{item_name},{item_price},{new_item_stock}"

    LOG(f"Adding item to cart: Name: {item_name} Price: {item_price} Quantity: {amount_requested}")
    response = f"added successfully to cart"

    try:

        with open("inventory.txt", "w") as file:
            for item in inventory:
                file.write(item + "\n")
        LOG(f"updating {item_name} inventory")
    except:
        print("error updating inventory")

    LOG("Action Stopped: Adding item to cart")
    return render_template("cart.html", page_title="Balance",item_name=item_name,response=response),{"Refresh": "3; url=sell"}


@app.route('/shopping_cart')
def shopping_cart():
    cart = load_inventory_from("cart.txt")
    cart_info = []

    for item_id, entry in enumerate(cart, 1):
        row = [item_id] + entry.split(",") + [int(entry.split(",")[1]) * int(entry.split(",")[2])]
        cart_info.extend( [row] )

    total = 0
    for sum in cart_info:
        total = total+ int(sum[4])

    return render_template("shopping_cart.html", page_title="Shopping Cart", cart_info=cart_info,total=total)


@app.route('/balance')
def balance():
    current_balance = load_balance("balance.txt")
    return render_template("update_balance.html",page_title="Balance",balance=current_balance)


@app.route('/balance_update_form', methods=["POST","GET"])
def balance_update():
    LOG("Action Started: Updating Balance")

    current_balance = load_balance("balance.txt")
    LOG(f"Previous Balance: {current_balance}")

    operation = request.form["operation"]
    amount = request.form["amount"]

    if operation == "add":
        response = f"added successfully to Balance"
        current_balance += int(amount)
        LOG(f"Amount Added:{ amount } Added to Balance")
    elif operation == "subtract":
        response = f"subtracted successfully from Balance"
        current_balance -= int(amount)
        LOG(f"Amount Subtracted: { amount } from Balance")


    save_stuff(current_balance,"balance.txt","w")
    LOG(f"New Balance: {current_balance}")
    LOG("Action Stopped: Updating Balance")

    return render_template("update_balance_response.html", page_title="Balance",amount=amount,response=response),{"Refresh": "3; url=dashboard"}


@app.route('/history')
@app.route('/history/')
@app.route('/history/<int:line_from>/<int:line_to>')
def logs(line_from=None, line_to=None):
    logs = load_inventory_from("LOG.txt")
    log_info = []

    for log_id,entry in enumerate(logs,1):
        log_info.append([ log_id,entry.split(";")[0],entry.split(";")[1] ] )
    print(log_info)

    if line_from is not None and line_to is not None:
        return render_template("history.html",page_title="History", log_info=log_info[line_from-1:line_to])
    else:
        return render_template("history.html",page_title="History",log_info=log_info)




@app.errorhandler(404)
def page_not_found(error):
    return "Page not found, redirecting to the dashboard shortly",404,{"Refresh": "3; url=dashboard"}

@app.errorhandler(500)
def page_not_found(error):
    return "Internal Error, redirecting to the dashboard shortly",500,{"Refresh": "3; url=dashboard"}

