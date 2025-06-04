"""
In this exercise, you are tasked to create a Python program that simulates a package loading system. Each package can carry
 a maximum of 20 kg of goods. Items are added to the package with weights ranging from 1 to 10 kg. If adding an item
 to the package would exceed the 20 kg limit, the package should be sent, and the current item should start a new package.
 If an item with a weight of 0 is given, the program should terminate.

1. Write a program that prompts the user for the maximum number of items to be shipped.
2. The program should allow the user to enter the weight of each item, one by one.
3. If adding an item would increase the total weight of the current package above 20 kg, mark the current package as sent
and start a new package with the current item.
4. If an item with a weight of 0 kg is given, the program should terminate as if the maximum number of items has been reached.
5. At the end of the program, display the following information:

  Number of packages sent
  Total weight of packages sent
  Total 'unused' capacity (non-optimal packaging). This is calculated as the number of packages sent multiplied by 20 kg, minus the total weight of packages sent.
  The package number that had the most 'unused' capacity and the amount of 'unused' capacity in that package.

Hints:

- Use a loop to continuously prompt the user for item weights until the maximum number of items has been reached or an item with a weight of 0 kg is given.
- Keep track of the current package's total weight and the number of packages sent.
- Remember to handle cases where the weight of an item is outside the acceptable range (1 to 10 kg, unless it's 0).
- Handle user inputs that are not as expected (for example, if the user enters a string instead of a number for the item's weight).
   The program should not crash in these cases, but instead, it should display an appropriate error message.

"""
import os

MAX_WEIGHT = 20

i = 0
shipping_total_weight = 0
shipping_package_count = 1

# Print the size of terminal
fill_terminal = os.get_terminal_size()


print(":" * fill_terminal[0])
print(":" * fill_terminal[0])

print("\n" * 2)

print(":::::::: package loading system ::::::::")
print("::::::::")
print("::::::::    Type 0 to exit")


try:
    n_items_to_ship = int(input("how many items will be shipped ? "))
    print("")
    if n_items_to_ship < 0:
        print("Maximum number of items must be 1 or higher")
    elif n_items_to_ship == 0:
        print("Exiting...")

except ValueError:
    print("Invalid input. Please enter a valid number of items.")

i = 0
while i < n_items_to_ship:
    try:
        item_weight = int(input(f"Please enter item {i+1} of {n_items_to_ship} weight: "))
        if item_weight == 0:
            print("Exiting...")
        elif item_weight < 1 or item_weight > 10:
            print("Item weight must be between 1 and 10 kg.")
            continue
        elif shipping_total_weight + item_weight > 20:
            print(f"\n item {i+1} sent separately as it exceeds max shipping weight of 20kg")
            shipping_package_count += 1
            shipping_total_weight += item_weight
        else:
            shipping_total_weight += item_weight

    except ValueError:
        print("Invalid input. Please enter a valid weight for the item.")
    i += 1

print("\n"*2)

print(f"Number of package sent: {shipping_package_count}" )
print(f"total shipping weight: {shipping_total_weight}" )

unused_capacity = (shipping_package_count * 20) - shipping_total_weight
print(f"Unused capacity: {unused_capacity}")

print("\n"*3)
