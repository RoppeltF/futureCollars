import argparse
import textwrap
import os
from pydoc import describe


def parse_arguments():
    pwd = os.getcwd()

    parser = argparse.ArgumentParser(
        prog='main.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = textwrap.dedent('''\
        - CSV file modifier matrix based -
        
        
        ** all arguments are optional except the changes if using default values **
        ** you can ran the script with or without the parameter notation **
        
        Example:
      
        python main.py in.csv out.csv 0,0,piano 3,1,mug 1,2,17 3,3,0
        and
        python main.py -s in.csv -o out.csv -c 0,0,piano 3,1,mug 1,2,17 3,3,0
        
        And the 'in.csv' file content is: 
        
        door,3,7,0
        sand,12,5,1
        brush,22,34,5
        poster,red,8,stick
        
        The following 'out.csv' file should be generated:
        
        piano,3,7,0
        sand,12,5,mug
        brush,17,34,5
        poster,red,8,0'''),
        epilog='If in doubt about positioning use argument declaration: -s -o -c \n')

    parser.add_argument("-s","--source",default="in.csv",
                        help="Path/filename of the CSV to be modified")

    parser.add_argument("-o","--output",default="out.csv",
                        help="Output file -Default: out.csv")

    parser.add_argument("-c","--changes",nargs='+',
                        help="Change is matrix based line,column,new_value")

    #argument used as placement arguments instead of parametized ones
    parser.add_argument("params",nargs='*',
                        help="Takes positional arguments in 1 csv is input 2nd cvs as output 3rd field is path/folder 4th changes to perform")

    args = parser.parse_args()


    if not args.changes:
        parser.print_help()
        parser.exit()

    if len(args.params) >= 3:
        args.source = args.params[0] if args.params[0].endswith(".csv") else args.source
        args.output = args.params[1] if args.params[1].endswith(".csv") else args.output
        args.changes = args.params[2:]
    elif len(args.params) == 2:
        args.source = args.params[0] if args.params[0].endswith(".csv") else args.source
        args.output = args.params[1] if args.params[1].endswith(".csv") else args.output
        args.changes = args.changes

    elif len(args.params) < 2 and args.source and args.output:
        try:
            args.changes = args.changes if args.params[0].endswith(".csv") else args.params[:] or args.changes
            args.source = args.params[0] if args.params[0].endswith(".csv") else args.source or args.source
        except:
            args.changes = args.changes
            args.source = args.source

    else:
        parser.error("You must provide at least one change.")

    return args


def load_file(csv_file):
    try:
        with open(csv_file) as file:
            return file.read().splitlines()
    except:
        print(f"File {csv_file} doesn't exist!")


# def save_file(item,file_name,type="a+"):
#     file_name = str(file_name)
#     with open(f"{file_name}",type) as file:
#
#             file.write(item+"\n")


def save_file(items, filename):
    print("===============================================")
    print(f"Output File: {args.output}")
    print("===============================================")
    with open(filename, 'a+') as file:
        for item in items:
            if isinstance(item, list):
                line = ",".join(map(str, item))
            else:
                line = str(item)
            print(line)
            file.write(line + '\n')
    print("\n"*2)

def main(args):

    source_file = load_file(args.source)

    for change in args.changes:
        if len(change.split(',')) == 3:

            try:
                x,y,value = change.split(',')
                new_line = source_file[ int(x) ].split(',')
                print("===============================================")
                print(f"X: {x}   Y:{y}   Value:{value} ")
                print("===============================================")
                print("Line to edit: ",new_line)
                print(f"Item to edit: {new_line[int(y)]}")
                print(f"New value: {value}")
                new_line[ int(y) ] = str(value)
                print("New line:",new_line[0])
                print("===============================================")

                source_file[int(x)] = new_line

            except IndexError:
                print(f"\nX: {x} or Y: {y} coordinate cannot be fount please correct argument {change}\n")
        else:
            print(f"\nArgument is incorrect {args.changes[0]}. \nUse main.py -h for help.\n")
    print("\n")

    save_file(source_file,args.output)








if __name__ == '__main__':
## python reader.py in.csv out.csv 0,0,piano 3,1,mug 1,2,17 3,3,0
    args = parse_arguments()
    main(args)