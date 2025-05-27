
"""

Write a program that prompts the user for the following pieces of information:
  - Recipient's name
  - Year of birth
  - Personalized message
  - Sender's name


[Recipient's Name], let's celebrate your [Age] years of awesomeness!
Wishing you a day filled with joy and laughter as you turn [Age]!

[Short Personalized Message]

With love and best wishes,
[Sender's Name]

"""

print("Welcome to the Birthday Card Generator!")
print("")

recipient_name = input("Enter the recipient's name: ")
year_of_birth = int(input("Enter the recipient's year of birth: "))
message = input("Enter a short personalized message: ")
sender_name = input("Enter your name: ")
current_year = 2025
age = current_year - year_of_birth

print(f"""{recipient_name}, let's celebrate your {age} years of awesomeness!
Wishing you a day filled with joy and laughter as you turn {age}!

{message}

With love and best wishes,
{sender_name} """)