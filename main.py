import ast
from hashlib import file_digest

from User_class import *

def menu(menu_name,menu_options):
    print(f":::: {menu_name}  ::::")
    for x, opt in enumerate(menu_options,1):
        print( f"{x} - {opt}")
    print("0 - Quit")

def op_check(message):
    try:
        op = int(input(f"{message}: "))
        return op
    except ValueError:
        print("Invalid option please try again !")
        op_check(message)


def list_per_Class(file,class_name):
    for line in file:
        line = line .strip() # remove leading/trailing whitespace
        if line:
            data_dict = ast.literal_eval(line)
            for c_name in data_dict["Class_Name"]:
                if c_name == class_name:
                    print(f"Name: {data_dict["Name"]} {data_dict["Surname"]}  - Class Name: {data_dict["Class_Name"][0]}")



# list all the classes the student attends and the teachers of these classes.
def list_per_name(file,student_name,):
    for line in file:
        line = line.strip() # remove leading/trailing whitespace
        if line:
            stu_dict = ast.literal_eval(line)
            if (student_name[0].strip() == stu_dict["Name"].strip() and student_name[1].strip() == stu_dict["Surname"].strip()):
                teacher_file = open("teacher.db")
                teacher_dict =[]

                for line in teacher_file:
                    data_dict = ast.literal_eval(line)
                    teacher_dict.append(data_dict)

                print(f"\n {stu_dict['Name']} {stu_dict['Surname']} is enrolled in:")

                for class_name in stu_dict['Class_Name']:
                    print(f" - {class_name}")
                    class_teachers = [t for t in teacher_dict if class_name in t['Class_Name']]
                    if class_teachers:
                        for teacher in class_teachers:
                            full_name = f"{teacher['Name'].strip()} {teacher['Surname'].strip()}"
                            print(f"   >> Taught by: {full_name} ({teacher['Subject']})")
                    else:
                        print("   >> No teacher found for this class.")
            else:
                print("Student not found.")



while True:
    options = ["Create","Manage"]
    menu("School Menu",options)

    op = op_check("Chose the operation to perform")

    if op == 0:
        break
    # Create User
    if op == 1:
        while True:
            options = ["Student", "Teacher","Homeroom Teacher"]
            menu("Create User", options)
            op = op_check("Choose the type of User to Create")

            if op == 0:
                break

            if op == 1:
                name = input("Enter Student Name: ")
                surname = input(f"Enter {name} Last name: ")
                class_name = []

                while True:
                    c_name = input(f"Enter {name} Class Name ( empty to exit ): ")
                    if c_name == "":
                        break
                    elif c_name != "":
                        class_name.append(c_name.upper())


                student = User(name,surname,class_name)
                student.create_student()

            elif op == 2:
                class_name = []

                name = input("Enter Teacher Name: ")
                surname = input(f"Enter {name} Last name: ")

                while True:
                    c_name = input(f"Enter {name} Classroom ( empty to exit ): ")

                    if c_name == "":
                        break
                    elif c_name != "":
                        class_name.append(c_name.upper())

                subject = input(f"Enter {name} Class Subject: ")

                teacher = User(name, surname, class_name)
                teacher.create_teacher(subject)

            elif op == 3:

                name = input("Enter Homeroom teacher Name: ")
                surname = input(f"Enter {name} Last name: ")
                class_name = []

                while True:
                    c_name = input(f"Enter {name} Class Name ( empty to exit ): ")
                    if c_name == "":
                        break
                    elif c_name != "":
                        class_name.append(c_name.upper())

                hr_teacher = User(name, surname, class_name)
                hr_teacher.homeroom_teacher()

            else:
                print("Invalid Option, please try  again")

    if op == 2:
        options =["Class", "Student", "Teacher", "Homeroom Teacher"]
        while True:
            menu("User Management", options)
            op = op_check("Choose operation to perform: ")

            if op == 0:
                break

     #  - 'class': Prompt for a class to display (e.g., "3C"), the program should list all students in the class and the homeroom teacher.
            if op == 1:
                class_name = input("Enter the class name: ")
                student_file = open(f"{pwd}/student.db")
                hr_teacher_file = open(f"{pwd}/homeroom_teacher.db")


                list_per_Class(student_file,class_name)
                list_per_Class(hr_teacher_file,class_name)

    #   - 'student': Prompt for a student's first and last name, the program should list all the classes the student attends and the teachers of these classes.
            elif op == 2:
                name = input("Enter Student Name: ")
                surname = input(f"Enter {name} Surname: ")
                student_name = [name,surname]
                student_file = open("student.db")
                list_per_name(student_file, student_name)

    #   - 'teacher': Prompt for a teacher's first and last name, the program should list all the classes the teacher teaches.
            elif op == 3:
                teacher = []
                name = input("Enter Student Name: ").strip()
                surname = input(f"Enter {name} Surname: ").strip()

                teacher_file = open("teacher.db")

                for line in teacher_file:
                    data_dict = ast.literal_eval(line)
                    teacher.append(data_dict)

                    if name == teacher[-1]["Name"].strip() and surname == teacher[-1]["Surname"].strip():
                        print(f"\n {teacher[-1]['Name']} {teacher[-1]['Surname']} teaches in: ")
                        for c_name in teacher[-1]['Class_Name']:
                            print(" " + c_name)


    #   - 'homeroom teacher': Prompt for a homeroom teacher's first and last name, the program should list all students the homeroom teacher leads.
            elif op == 4:

                name = input("Enter Homeroom Teacher Name: ").strip()
                surname = input(f"Enter {name} Surname: ").strip()

                homeroom_file = open("homeroom_teacher.db")
                student_file = open("student.db")

                stu_dict = []
                for line in homeroom_file:
                    line = line.strip()
                    if line:
                        hrt_dict = ast.literal_eval(line)
                        if name == hrt_dict["Name"].strip() and surname == hrt_dict["Surname"].strip():
                            data_dict = ast.literal_eval(line)

                            print(f"\n {name} {surname} is the Homeroom teacher of:")

                            for hr_class_name in data_dict['Class_Name']:
                                print(hr_class_name,":")
                                for student in student_file:
                                    student = student.strip()
                                    if student:
                                        stu_data = ast.literal_eval(student)
                                        stu_dict.append(stu_data)
                                        for stu_class_name in stu_data["Class_Name"]:
                                            if stu_class_name == hr_class_name:
                                                print(f"Name: {stu_data['Name']} {stu_data['Surname']}")

                    else:
                        print("Homeroom Teacher not found.")


            else:
                print("Invalid Option, please try  again")


    else:
        print("Invalid Option, please try  again")

