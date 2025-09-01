from datetime import datetime

def save_stuff(item,file_name,type="a+"):
    item = str(item)
    file_name = str(file_name)
    try:
        with open(file_name,type) as file:
            file.write(item+"\n")
        print(f"Saving/updating: {item}")
    except:
        print(f"Error while adding information: {item}")
        print(f"Error while adding information to file: {file_name}")


def load_inventory_from(filename):
    items = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                items.append(line.strip())
    except FileNotFoundError:
        print(f"File {filename} does not exists, creating it")
        save_stuff("",filename)
    return items

