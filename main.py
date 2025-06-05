# """
#     1.Even or Odd
#     Ask the user to enter a number and print whether it's even or odd.
#
#     2.Guess the Number
#     The computer chooses a random number between 1 and 10. The user keeps guessing until they get it right. After each guess, inform if it was too high, too low, or correct.
#
#     3.Numbers from 1 to 20 – Skip 13
#     Print numbers from 1 to 20, but skip the number 13 using continue.
#
#     4.Numbers Divisible by 3 up to 50
#     Print all numbers from 1 to 50 that are divisible by 3.
#
#     5.Password Entry
#     Ask the user to enter a password. If it matches "python123", print "Access granted". After 3 wrong attempts, terminate the program.
#
#     6.Sum of Positive Numbers
#     Keep asking the user for numbers. Add only the positive numbers. Stop if the user enters 0. Ignore negative numbers using continue.
#
#     7.Simple Calculator Menu
#     Display a menu with 3 options:
#
# 1. Add
# 2. Subtract
# 3. Quit
#
# Perform the selected operation on two numbers.
#
#     8.Multiplication Table
#     Print a multiplication table from 1 to 10 in the format a x b = result.
#
#     9.Prime Numbers up to 100
#     Print all prime numbers between 2 and 100.
#
#     10.Guess the Letter
#     The computer randomly picks a lowercase letter. The user must guess the letter until they get it right.
#
# """
import random
import string

print("\n" * 2)
#
# #1. Even or Odd

number = int(input("Enter a number to check if its even or odd:"))

if number%2 == 0:
    print("number is even")
else:
    print("number is odd")

print("\n"*3)


# # 2.Guess the Number
# # The computer chooses a random number between 1 and 10. The user keeps guessing until they get it right. After each guess, inform if it was too high, too low, or correct.

user_number = 12

number =  random.randint(1, 10)

while user_number != number:
    user_number = int(input("Guess the secret number:"))
    if user_number == number:
        print("Correct Urray !!! you guessed the number")
        print("\n" * 2)
        break
    else:
        print(" Nope, please try again")
        print("\n"*2)

#    3.Numbers from 1 to 20 – Skip 13
#    Print numbers from 1 to 20, but skip the number 13 using continue.

for i in range(1,21):
    if i == 13:
        continue
    else:
        print(i)


#  # 4.Numbers Divisible by 3 up to 50
#  # Print all numbers from 1 to 50 that are divisible by 3.


for i in range(1,51):
    if i % 3 == 0:
        print(i)


# #    5.Password Entry
# #    Ask the user to enter a password. If it matches "python123", print "Access granted". After 3 wrong attempts, terminate the program.

secret = "python123"

attempt = 1

while attempt <= 3:
    passwd = input("Enter the secret password:")
    if passwd != secret:
        attempt += 1
        continue
    print(" Access granted ")
    break


# #    6.Sum of Positive Numbers
# #    Keep asking the user for numbers. Add only the positive numbers. Stop if the user enters 0. Ignore negative numbers using continue.

sum = 0
number = 0
print("type 0 to exit")
while True:
    number = int(input("Enter a number to be added:: "))
    if number == 0:
        break
    if number < 0:
        print("Enter a positive number!")
        continue
    sum += number

print("\n"*2)

print("total: ",sum)


# # 7.Simple Calculator Menu
# # Display a menu with 3 options:
# #
# # 1. Add
# # 2. Subtract
# # 3. Multiply
# # 4. Devide
# # 0. Quit


while True:
    print("::: Calculator Menu :::")
    print("::: 1. Add :::")
    print("::: 2. Subtract :::")
    print("::: 0. Quit :::")

    print("\n")
    op = int(input("Enter the desired Option::"))

    if op == 0:
        break
    elif op == 1:
        a = int(input("Select 1st number to add:"))
        b = int(input("Select 1st number to add:"))
        print("Result: ",a+b)
    elif op == 2:
        a = int(input("Select 1st number to subtract:"))
        b = int(input("Select 1st number to subtract:"))
        print("Result: ", a - b)
    elif op == 3:
        a = int(input("Select 1st number to multiply:"))
        b = int(input("Select 1st number to multiply:"))
        print("Result: ", a * b)
    elif op == 4:
        a = int(input("Select 1st number to divide:"))
        b = int(input("Select 1st number to divide:"))
        print("Result: ", a//b)
    else:
        print("Invalid Option")


# #   8.Multiplication Table
# #   Print a multiplication table from 1 to 10 in the format a x b = result.

print("::: Multiplication table :::")
a = int(input("Please select a number: "))
b = int(input(f"Please select a number to multiply {a} up to: "))
for i in range(1,b+1):
    print(f"{i} x {a} = ", i*a )


#   9.Prime Numbers up to 100
#   Print all prime numbers between 2 and 100.

num = 7

prime = False

if num > 0 and num <= 3:
    print(num, "is a prime number")
elif num > 1:
    for i in range(2, num):
        if (num % i) == 0:
            prime = True

    if prime:
        print(num, "is not a prime number")
    else:
        print(num, "is a prime number")




#   10.Guess the Letter
#   The computer randomly picks a lowercase letter. The user must guess the letter until they get it right.

user_letter = "A"

secret_letter =  random.choice(string.ascii_lowercase)

print(secret_letter)
while user_letter != secret_letter:
    user_letter = str(input("Guess the secret letter:"))
    if user_letter == secret_letter:
        print("Correct")
        print("\n" )
        break
    print(" Nope, please try again")
    print("\n"*2)