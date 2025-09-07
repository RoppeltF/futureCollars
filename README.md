FLASK - HTML & CSS & SQL
Final project

To RUN:

flask --app main db revision init_DB  
flask --app main db upgrade
flask --app main run 
  

Inventory Management System
A Flask-based web application for managing inventory, sales, and balance tracking with user authentication.
Features

User Authentication: Register, login, and logout functionality
Inventory Management: Add, update, and delete inventory items
Sales System: Shopping cart functionality with stock management
Balance Tracking: Monitor and update account balance
Activity Logging: Comprehensive logging system for all operations
Dashboard: Overview of key metrics (balance, inventory levels, total value)

Features: Paginated log viewing, most recent first

Technical Details
Dependencies

Flask
Flask-Login (user session management)
SQLAlchemy (database ORM)
Custom modules: extensions, dbClasses, basic_functions

Database Models

UserDB: User accounts and authentication
ItemDB: Inventory items (name, price, quantity)
Balance: Balance history tracking
LOG: Activity logging

Security Features

Login required decorators on protected routes
Password hashing (via UserDB.check_password)
User session management
Input validation and sanitization


File Operations

cart.txt: Temporary storage for shopping cart items, using through cart.txt file
Automatic file cleanup after purchase/cancel completion

Error Handling

Custom error pages (404, 400, 500)
Auto-redirect to dashboard on errors
Comprehensive logging of all operations
Transaction rollbacks on database errors

Usage Flow

Registration/Login: Create account or log in
Dashboard: View system overview
Add Inventory: Manage product stock
Sales: Add items to cart and process sales
Balance: Monitor and adjust account balance
History: Review all system activities

Features
Automatic Features

Stock Validation: Prevents overselling
Balance Protection: Prevents negative balances
Activity Logging: All operations are logged
Data Normalization: Consistent data formatting
Cart Count: Real-time cart item count in navigation

Installation & Setup

Install required dependencies
Configure database connection in extensions.py
Set up database models from dbClasses.py
Run the Flask application
Register your first user account

Notes

First User creates is Admin, all other users registered are default type.
Default user type is "user"
Balance increases with sales (income)
All monetary values appear to be in Euros (€)
Cart data is temporarily stored in text files
System maintains comprehensive audit trail through logging
