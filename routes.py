# routes.py
import os
from flask import render_template, request, Blueprint, flash, session, redirect,url_for
from flask_login import login_user, logout_user, login_required, current_user


from sqlalchemy import exc
from extensions import db

from dbClasses import Balance, ItemDB, LOG, UserDB
from basic_functions import save_stuff, load_inventory_from


bp = Blueprint("app", __name__)

# -----------------------------
# Aux Func.
# -----------------------------
def check_balance():
    try:
        current_balance = db.session.query(Balance).order_by(Balance.id.desc()).first()
        if current_balance is None:
            return 0  # default balance
        return current_balance.balance
    except Exception as e:
        db.session.add(LOG(f"Could not load balance: {e}", "ERROR"))
        db.session.commit()
        return 0


def load_inventory():
    try:
        inventory = db.session.query(ItemDB).all()
    except exc.SQLAlchemyError as sqlError:
        print("########################")
        print(sqlError)
        inventory = []
    if not inventory:
        inventory = []
    return inventory


# -----------------------------
# Routes
# -----------------------------
@bp.route('/', methods=['GET', 'POST'])
def index():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("app.dashboard"))

    # Handle any POST requests to the index (though there probably shouldn't be any)
    if request.method == 'POST':
        # Log this for debugging
        print(f"Unexpected POST request to index route with form data: {request.form}")
        # Redirect to avoid the Method Not Allowed error
        return redirect(url_for("app.index"))

    return render_template("index.html", page_title="Welcome")


@bp.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("app.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please, add your Username and Password!", "danger")
            return render_template("login.html")

        user = UserDB.get_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            flash("sucessfully logged in", "success")
            return redirect(url_for("app.dashboard"))
        else:
            flash("Username or Password invalid!", "danger")
            return render_template("login.html",page_title="Login")  # Added explicit return here

    # For GET requests, show the login form
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("app.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        mobile = request.form.get("mobile")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Validate required fields
        if not all([username, email, first_name, last_name, mobile, password, confirm]):
            flash("Please fillup all the information!", "danger")
            return render_template("register.html")

        # Normalize data
        username = username.lower()
        email = email.lower()
        first_name = first_name.lower().capitalize()
        last_name = last_name.lower().capitalize()
        mobile = mobile.strip()
        user_type = "user"  # default

        if password != confirm:
            flash("As senhas não coincidem!", "danger")
            return render_template("register.html")

        if UserDB.get_by_username(username):
            flash("User already exists!", "danger")
            return render_template("register.html")

        try:
            # IF is first USER Create the user as ADMIN
            is_first_user = db.session.query(UserDB).all()
            if not is_first_user:
                user_type="admin"
                user = UserDB.create_user(username, email, first_name, last_name, mobile, user_type, password)
            else:
                # Create the user as default type
                user = UserDB.create_user(username, email, first_name, last_name, mobile, user_type, password)

            flash("Account created sucessfully.", "success")
            return redirect(url_for("app.login"))
        except Exception as e:
            flash("Error creating account try again later", "danger")
            db.session.rollback()
            return render_template("register.html")

    return render_template("register.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logout sucessfully!", "success")
    return redirect(url_for("app.index"))


# Make sure your dashboard route is properly defined
@login_required
@bp.route('/dashboard', methods=['GET'])  # Explicitly specify GET method
def dashboard():
    balance = check_balance()
    inventory = load_inventory()
    stock_level = sum(item.item_quantity for item in inventory)
    total_inventory_value = sum(item.item_price * item.item_quantity for item in inventory)

    return render_template("dashboard.html", page_title="Home", balance=balance, inventory=stock_level,total_inventory_value=total_inventory_value,)


@login_required
@bp.route('/add_inventory')
def add_inventory():
    items = load_inventory()
    items_list = [item for item in items]
    current_balance = check_balance()  # Add current balance to show on the form

    return render_template("add_inventory.html", page_title="Add Inventory",
                           items=items_list, current_balance=current_balance)


@login_required
@bp.route('/add_item_form', methods=["POST", "GET"])
def add_item_form():
    db.session.add(LOG("Action Started: Adding item to Inventory", "INFO"))
    current_balance = check_balance()

    name = request.form["item_name"].lower().capitalize()
    price = request.form["item_price"]
    quantity = request.form["item_quantity"]

    total_cost = request.form["total_cost"]
    print(total_cost)
    db.session.add(LOG(f"Adding item: {name}, Price: {price}, Quantity: {quantity}", "INFO"))

    item = ItemDB(name, price, quantity)
    db.session.add(item)

    try:
        db.session.commit()
        response = f"{name} successfully added to inventory."
    except exc.SQLAlchemyError:
        db.session.rollback()
        db.session.add(LOG(f"Updating item instead: {name}", "INFO"))
        item_update = db.session.query(ItemDB).filter(ItemDB.item_name == f"{name}").first()
        if item_update:
            item_update.item_quantity = quantity
            item_update.item_price = price
            db.session.commit()
            response = f"{name} updated successfully"
        else:
            response = f"Error updating {name}"

    db.session.add(LOG("Action Completed: Adding item to Inventory", "INFO"))
    db.session.commit()

    return render_template("response_page.html", response=response), {"Refresh": "3; url=add_inventory"}


@bp.route('/delete_item', methods=['POST'])
@login_required
def delete_item():
    db.session.add(LOG("Action Started: Deleting item from Inventory", "INFO"))
    item_id = request.form.get('item_id')
    if item_id:
        item = db.session.query(ItemDB).filter(ItemDB.id == item_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            flash(f"Item {item.item_name} deleted successfully", "success")  # Added success category
            db.session.add(LOG(f"Action: Item {item.item_name} deleted from inventory", "INFO"))
            db.session.commit()  # Commit the log entry
        else:
            flash("Item not found.", "danger")
    else:
        flash("Item not found.", "danger")

    return redirect(url_for('app.add_inventory'))



@bp.route('/sell')
@login_required
def sell():
    inventory = load_inventory()
    item_list = [item.item_name for item in inventory if item.item_quantity > 0]
    items_with_no_stock = []

    for item in  inventory:
        if item.item_quantity == 0:
            items_with_no_stock.append( item.item_name )

    return render_template("sell.html", page_title="Sell", item_list=item_list, items_with_no_stock=items_with_no_stock)


@login_required
@bp.route('/cart', methods=["POST", "GET"])
def cart():
    db.session.add(LOG("Action Started: Adding item to cart", "INFO"))

    item_name = request.form["item_name"]
    amount_requested = request.form["amount"]

    inventory = load_inventory()
    for item in inventory:
        if item_name == item.item_name:
            cart_item = f"{item.item_name},{item.item_price},{amount_requested}"
            save_stuff(cart_item, "cart.txt")

            db.session.add(LOG(
                f"Added to cart: {item.item_name}, Price: {item.item_price}, Quantity: {amount_requested}", "INFO"
            ))

    db.session.add(LOG("Action Completed: Adding item to cart", "INFO"))
    db.session.commit()

    response = f"{amount_requested} of {item_name} added successfully to cart"
    return render_template("response_page.html", page_title="Cart", response=response), {"Refresh": "3; url=sell"}


def get_cart_count():
    """Get the number of items in the cart"""
    try:
        cart = load_inventory_from("cart.txt")
        return len(cart) if cart else 0
    except:
        return 0

# Add this context processor to make cart_count available in all templates
@bp.app_context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        try:
            cart = load_inventory_from("cart.txt")
            cart_count = len(cart) if cart else 0
        except:
            cart_count = 0
        return {'cart_count': cart_count}
    return {'cart_count': 0}




@login_required
@bp.route('/shopping_cart', methods=["POST", "GET"])
def shopping_cart():
    inventory = load_inventory()
    current_balance = check_balance()

    try:
        cart = load_inventory_from("cart.txt")
    except:
        cart = ""

    cart_info, total = [], 0

    if cart:
        for item_id, entry in enumerate(cart, 1):
            row = [item_id] + entry.split(",") + [int(entry.split(",")[1]) * int(entry.split(",")[2])]
            cart_info.append(row)
            total += row[4]
    else:
        if os.path.exists("cart.txt"):
            os.remove("cart.txt")

    # CONFIRM PURCHASE
    if "Confirm" in request.form:
        total_cost = 0  # Track total cost for balance deduction

        # Process each cart item
        for c_info in cart_info:
            cart_item, cart_price, cart_amount = c_info[1:4]
            item_total_cost = int(cart_price) * int(cart_amount)

            for item in inventory:
                if item.item_name == cart_item:
                    new_item_stock = int(item.item_quantity) - int(cart_amount)
                    if new_item_stock >= 0:
                        # Update stock
                        update_stock = db.session.query(ItemDB).filter(ItemDB.item_name == cart_item).first()
                        update_stock.item_quantity = new_item_stock

                        # Add to total cost
                        total_cost += item_total_cost

                        # Log the sale
                        db.session.add(LOG(f"Sold {cart_amount} x {cart_item} for €{item_total_cost}", "INFO"))
                    else:
                        flash(f"Insufficient stock for {cart_item}. Available: {item.item_quantity}", "danger")
                        return render_template("shopping_cart.html", page_title="Shopping Cart",
                                               cart_info=cart_info, total=total)

        # Update balance once with total cost
        new_balance = current_balance + total_cost  # Add because it's income from sales

        # Update or create balance record
        balance_row = db.session.query(Balance).order_by(Balance.id.desc()).first()
        if balance_row:
            # Create new balance record (since you're tracking balance history)
            db.session.add(Balance(new_balance))
        else:
            # Create first balance record
            db.session.add(Balance(new_balance))

        # Log the transaction
        db.session.add(LOG(f"Sale completed. Total: €{total_cost}. New balance: €{new_balance}", "INFO"))

        # Clear cart
        db.session.add(LOG("Clearing Cart", "INFO"))
        if os.path.exists("cart.txt"):
            os.remove("cart.txt")

        db.session.commit()
        flash(f"Purchase confirmed! Total: €{total_cost}", "success")
        return render_template("shopping_cart.html", page_title="Shopping Cart",
                               cart_info="", total="0")

    # CANCEL PURCHASE
    elif "Cancel" in request.form:
        db.session.add(LOG("Clearing Cart", "INFO"))
        if os.path.exists("cart.txt"):
            os.remove("cart.txt")
        db.session.commit()
        return render_template("shopping_cart.html", page_title="Shopping Cart", cart_info="", total=0)

    return render_template("shopping_cart.html", page_title="Shopping Cart", cart_info=cart_info, total=total)



@login_required
@bp.route('/balance')
def balance():
    current_balance = check_balance()
    return render_template("update_balance.html", page_title="Balance", balance=current_balance)


@login_required
@bp.route('/balance_update_form', methods=["POST", "GET"])
def balance_update_form():
    db.session.add(LOG("Action Started: Updating Balance", "INFO"))
    current_balance = check_balance()

    operation = request.form["operation"]
    amount = int(request.form["amount"])

    if operation == "add":
        current_balance += amount
        response = f"Value of: € {amount} Added to Balance"
        db.session.add(LOG(f"Amount Added: € {amount}", "INFO"))

    elif operation == "subtract":
        current_balance -= amount
        if current_balance >= 0:
            response = f"Value of: € {amount} Subtracted successfully from Balance"
            db.session.add(LOG(f"Amount Subtracted: € {amount}", "INFO"))
        else:
            response = f"Operation cancelled: Insufficient balance"
            db.session.add(LOG("Operation cancelled: Negative balance", "ERROR"))
            current_balance += amount  # rollback

    db.session.add(Balance(current_balance))
    db.session.commit()

    db.session.add(LOG(f"New Balance: {current_balance}", "INFO"))
    db.session.add(LOG("Action Completed: Updating Balance", "INFO"))
    db.session.commit()

    return render_template("response_page.html", page_title="Balance", response=response), {"Refresh": "3; url=dashboard"}


@login_required
@bp.route('/history')
@bp.route('/history/')
@bp.route('/history/<int:line_from>')
@bp.route('/history/<int:line_from>/')
@bp.route('/history/<int:line_from>/<int:line_to>')
@bp.route('/history/<int:line_from>/<int:line_to>/')
def logs(line_from=None, line_to=None):
    logs = db.session.query(LOG).order_by(LOG.id.desc())
    log_info = [[log_id, entry.date, entry.message] for log_id, entry in enumerate(logs, 1)]

    if line_from is not None and line_to is not None:
        return render_template("history.html", page_title="History", log_info=log_info[line_from-1:line_to])
    if line_from is not None and line_to is None:
        return render_template("history.html", page_title="History", log_info=log_info[line_from-1:])
    return render_template("history.html", page_title="History", log_info=log_info)


# -----------------------------
# ERRORS
# -----------------------------


@bp.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), {"Refresh": "5; url=/dashboard"}


@bp.errorhandler(400)
def internal_error(err):
    return render_template("404.html"), {"Refresh": "5; url=/dashboard"}


@bp.errorhandler(500)
def internal_error(err):
    return render_template("500.html"), {"Refresh": "5; url=/dashboard"}
