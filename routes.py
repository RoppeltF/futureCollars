import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_alembic import Alembic
from basic_functions import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

alembic = Alembic()
alembic.init_app(app)

from datetime import datetime

class Balance(db.Model):
    def __init__(self, balance):
        self.balance = balance

    id =  db.Column( db.Integer(),primary_key=True )
    balance = db.Column( db.Integer(),nullable=False )


def check_balance():
    try:
        current_balance = db.session.query( Balance ).order_by( Balance.id.desc() ).first()

        if current_balance is None:
            current_balance =  0  # default balance when no record exists
        return current_balance.balance

    except Exception as e:
        LOG(f"Could not load loading balance: {e}","ERROR")
        return 0


def load_inventory():
    try:
        inventory = db.session.query( ItemDB ).all()

    except exc.SQLAlchemyError as sqlError:
        print("########################")
        print(sqlError)

    finally:
        if inventory == None:
            inventory = ["Inventory not Found",0,0]

    return inventory


class ItemDB(db.Model):
    def __init__(self, item_name,item_price,item_quantity):
        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), unique=True, nullable=False)
    item_price = db.Column(db.Integer(), unique=False, nullable=False)
    item_quantity = db.Column(db.Integer(), unique=False, nullable=False)


class LOG(db.Model):
    def __init__(self, message, type):
        self.date = datetime.now()
        self.message = message
        self.type = type

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column( db.DateTime(),default=datetime)
    message = db.Column(db.String(120), unique=False, nullable=False)
    type = db.Column(db.String(120), unique=False, nullable=False)


@app.route('/')
@app.route('/dashboard')
@app.route('/home')
@app.route('/index')
def dashboard():
    balance = check_balance()
    inventory = load_inventory()
    stock_level = 0

    for item in inventory:
        stock_level += item.item_quantity

    return render_template("dashboard.html", page_title="Home", balance=balance, inventory=stock_level)


@app.route('/add_inventory')
def add_inventory():

    items = load_inventory()
    items_list = []

    for item in items:
        items_list.append(item.item_name)

    return render_template("add_inventory.html",page_title="Add Inventory",items=items_list)


@app.route('/add_item_form', methods=["POST","GET"])
def get_data():
    db.session.add( LOG("Action Started: Adding item to Inventory","INFO") )

    items = load_inventory()
    items_list = []

    for item in items:
        items_list.append(item.item_name)

    name = request.form["item_name"].lower().capitalize()
    price = request.form["item_price"]
    quantity = request.form["item_quantity"]

    db.session.add( LOG(f"Adding item to Inventory: Name: {name} Price: {price} Quantity: {quantity}","INFO") )

    item = ItemDB(name,price,quantity)
    db.session.add(item)
    try:
        db.session.commit()
        response = f"{name} successfully added in inventory."
    except exc.SQLAlchemyError as sqlError:
        db.session.rollback()
        db.session.add(LOG(f"Updating item to Inventory: Name: {name} Price: {price} Quantity: {quantity}", "INFO"))
        item_update = db.session.query(ItemDB).filter(ItemDB.item_name==f"{name}").first()
        item_update.item_quantity = quantity
        item_update.item_price = price
        db.session.add(item_update)
        db.session.commit()
        response = f"{name} updated successfully"

    db.session.add( LOG("Action Stopped: Adding item to Inventory","INFO") )
    db.session.commit()

    return render_template("response_page.html",response=response),{"Refresh": "3; url=dashboard"}


@app.route('/sell')
def sell():
    inventory = load_inventory()
    item_list = []

    for item in inventory:
        item_list.append( item.item_name )

    return render_template("sell.html",page_title="Sell",item_list=item_list)


@app.route('/cart',methods=["POST","GET"])
def cart():

    db.session.add( LOG("Action Started: Adding item to cart","INFO") )
    item_name = request.form["item_name"]
    amount_requested = request.form["amount"]

    inventory = load_inventory()

    inv_item_name = []
    for item in inventory:
        if item_name == item.item_name:
            cart_item = f"{item.item_name},{item.item_price},{amount_requested}"
            save_stuff(cart_item, "cart.txt")

            ########################################
            ########################################
            ########################################
            ########## CHECK AMOUNT IN STOCK TO ADD TO CART


    db.session.add( LOG(f"Adding item to cart: Name: {item_name} Price: {item.item_price} Quantity: {amount_requested}","INFO") )
    response = f"{amount_requested} of {item_name} added successfully to cart"

    db.session.add( LOG("Action Stopped: Adding item to cart","INFO") )
    return render_template("response_page.html", page_title="Balance",response=response),{"Refresh": "3; url=sell"}


@app.route('/shopping_cart', methods=["POST","GET"])
def shopping_cart():
    inventory = load_inventory()
    current_balance = check_balance()
    try:
        cart = load_inventory_from("cart.txt")
    except:
        cart=""

    cart_info = []
    total = 0

    if cart != "":
        for item_id,entry in enumerate(cart, 1):
            row = [item_id] + entry.split(",") + [int(entry.split(",")[1]) * int(entry.split(",")[2])]
            cart_info.extend( [row] )

        for item in cart_info:
            total = total+ int(item[4])
    else:
        os.remove("cart.txt")

    #Update stock amount
    if "Confirm" in request.form:
        for c_info in cart_info:
            cart_item,cart_amount,cart_price = c_info[1:4]
            print(cart_item,cart_amount,cart_price)

            try:
                for item in inventory:
                    if item.item_name == cart_item:
                        new_item_stock = int(item.item_quantity) - int(cart_amount)
                        if new_item_stock >= 0:

                            # DB item info
                            update_stock = db.session.query(ItemDB).filter(ItemDB.item_name == cart_item).first()

                            print("# Item item.stock: ", item.item_quantity)

                            db.session.add(LOG(f"Updating item stock {item} to {new_item_stock}", "INFO"))

                            # Update Item quantity
                            update_stock.item_quantity = new_item_stock

                            print("# Item Stock: ", update_stock.item_quantity)
                            print("# New Item Stock: ", new_item_stock)

                            # balance = ... (if Balance is a DB model, update its row)
                            balance_value = current_balance - (int(item.item_price) * int(cart_amount))
                            print("# Balance: ", balance_value)

                            db.session.add(LOG(f"Updating Balance to: {balance_value}", "INFO"))

                            # If you have a Balance table, update it here instead of adding raw int
                            balance_row = db.session.query(Balance).first()  # or filter by user
                            if balance_row:
                                balance_row.balance = balance_value  # assuming column name is `value`

                            db.session.add(LOG("Clearing Cart", "INFO"))
                            os.remove("cart.txt")

                            # finally commit
                            db.session.commit()

                            return render_template("shopping_cart.html", page_title="Shopping Cart",
                                                   cart_info="", total="0")

            except exc.SQLAlchemyError as sqlError:
                print("########################")
                print("########################")
                print(sqlError)
                print("########################")
                print("########################")

    elif "Cancel" in request.form:
        db.session.add( LOG("Clearing Cart","INFO") )
        os.remove("cart.txt")
        return render_template("shopping_cart.html", page_title="Shopping Cart", cart_info="", total=0)

    db.session.commit()

    return render_template("shopping_cart.html", page_title="Shopping Cart", cart_info=cart_info,total=total)



























@app.route('/balance')
def balance():
    current_balance = check_balance()
    return render_template("update_balance.html",page_title="Balance",balance=current_balance)


@app.route('/balance_update_form', methods=["POST","GET"])
def balance_update():

    db.session.add( LOG("Action Started: Updating Balance","INFO") )
    current_balance = check_balance()

    db.session.add( LOG(f"Previous Balance: {current_balance}","INFO") )

    operation = request.form["operation"]
    amount = request.form["amount"]

    if operation == "add":
        response = f"Value of: € { amount } Added to Balance"
        current_balance += int(amount)
        db.session.add( LOG(f"Amount Added: € { amount } Added to Balance","INFO") )

    elif operation == "subtract":
        current_balance -= int(amount)
        if current_balance >= 0:
            response = f"Value of: € {amount} Subtracted successfully from Balance"
            db.session.add( LOG(f"Amount Subtracted: € {amount} from Balance","INFO") )

        else:
            response = f"Operation cancelled: Subtraction of {amount} from Balance"
            db.session.add( LOG(f"Operation cancelled: Subtraction of {amount} from Balance","ERROR") )

            current_balance += int(amount)

    # balance = Balance(current_balance)
    db.session.add( Balance(current_balance) )
    db.session.commit()

    LOG(f"New Balance: {current_balance}","INFO")
    LOG("Action Stopped: Updating Balance","INFO")

    return render_template("response_page.html", page_title="Balance",response=response),{"Refresh": "3; url=dashboard"}


@app.route('/history')
@app.route('/history/')
@app.route('/history/<int:line_from>')
@app.route('/history/<int:line_from>/')
@app.route('/history/<int:line_from>/<int:line_to>')
@app.route('/history/<int:line_from>/<int:line_to>/')
def logs(line_from=None, line_to=None):
    logs = db.session.query( LOG ).order_by( LOG.id.desc() )
    # logs = load_inventory_from("LOG.txt")

    log_info = []

    for log_id,entry in enumerate(logs,1):
        log_info.append([ log_id,entry.date, entry.message ] )

    if line_from is not None and line_to is not None:
        return render_template("history.html",page_title="History", log_info=log_info[line_from-1:line_to])
    if line_from is not None and line_to is None:
        return render_template("history.html",page_title="History", log_info=log_info[line_from-1:])
    else:
        return render_template("history.html",page_title="History",log_info=log_info)


@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"),{"Refresh": "5; url=/dashboard"}


@app.errorhandler(500)
def page_not_found(err):
    return render_template("500.html"),{"Refresh": "5; url=/dashboard"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
