
"""

1.Swap Values
Create two variables a and b, assign them any numbers, and then swap their values.

2.Rectangle Area and Perimeter
Define variables width and height, and calculate the area and perimeter of a rectangle.

3.Calculate Average
Create three variables with grades (grade1, grade2, grade3) and calculate the arithmetic average.

4.Temperature Conversion
Given a temperature in Celsius (c), convert it to Fahrenheit using the formula:
f = (c * 9/5) + 32

5.Simple Calculator
Declare two numbers (x, y) and print the result of basic operations: addition, subtraction, multiplication, and division.

6.String Concatenation
Create variables first_name and last_name, then combine them into one full name variable full_name.

7.Compare Values
Create two variables and compare them using comparison operators (>, <, ==, !=). Print the results.

8.Boolean Variable and not Operator
Create a boolean variable like is_logged_in = False, then use the not operator to take action if the condition is not met.

9.Logical Operators: and, or
Use boolean variables (e.g. is_password_correct, is_username_correct) and combine them with logical operators to simulate login access logic.

10.Check If Number Is Within a Range
Create a variable number and use logical operators to check if it's between 10 and 20 (inclusive).

"""

### 1
aux = 0
a = 123
b = 456

a=aux
a=b
b=aux

#############

### 2


width = 15
height = 35

area=  width * height
perimeter = 2 * (height+ width)

print(f"the area of {height} * {width} is:: {area}")
print(f"the perimeter of {height} * {width} is:: {perimeter}")

print("\n\n")
##############

### 3

grade1 = 10
grade2 = 6
grade3 = 8

average = ( grade1 + grade2 + grade3 ) / 3

print(f"Grades: \n{grade1} \n{grade2} \n{grade3}")
print(f"The Average of grades is: {average}")

print("\n\n")
###############

### 4
C_temp = int(input("Enter the temperature to convert (C -> F): "))
f = (C_temp * 9/5) + 32
print(f"\n\n {f}")

###############

### 5

x = int(input("Enter a number for X: " ))
y = int(input("Enter a number for Y: " ))

print(f"Add X and Y:  {x+y}")
print(f"Sub X and Y:  {x-y}")
print(f"Mult X and Y: {x*y}")
print(f"Div X and Y:  {x/y}")

print("\n\n")
###############


### 6


first_name = input("Enter your First Name:: ")
last_name = input("Enter your Last Name:: ")

full_name = first_name +" "+ last_name

print(f" Hi {full_name} !!!")
print("\n\n")

###############

### 7

a = 12
b = 27

print(a == b)
print(a != b)
print(a < b)
print(a > b)
print("\n\n")
###############
### 8
#Create a boolean variable like is_logged_in = False, then use the not operator to take action if the condition is not met.

logged_in = False

if logged_in is not False:
    print("User logged in")
else:
    print("User not logged in")
print("\n\n")
###############

### 9
#Use boolean variables (e.g. is_password_correct, is_username_correct) and combine them with logical operators to simulate login access logic.

correct_passwd = False

if logged_in == True and correct_passwd == True:
    print("You're logged in")
else:
    print("Access denied")

print("\n\n")
###############
### 10


number = int(input("Enter a number"))
if 10 <= number <= 20:
    print(f"Number: {number} is between 10 and 20.")
else:
    print(f"Number:  {number} is NOT between 10 and 20.")
print("\n\n")
###############