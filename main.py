import argparse
import csv
import pickle
import textwrap
import os
import json


# from pydoc import describe


def parse_arguments():
    pwd = os.getcwd()

    parser = argparse.ArgumentParser(
        prog='main.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
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

    parser.add_argument("-s", "--source", default="in.csv",
                        help="Path/filename of the CSV to be modified")

    parser.add_argument("-o", "--output", default="out.csv",
                        help="Output file -Default: out.csv")

    parser.add_argument("-c", "--changes", nargs='+',
                        help="Change is matrix based line,column,new_value")

    parser.add_argument("params", nargs='*',
                        help="Takes positional arguments in 1 csv is input 2nd cvs as output 3rd field is path/folder 4th changes to perform")

    args = parser.parse_args()

    # extensions
    ext = (".csv", ".txt", ".json", ".pickle", ".pkl")

    if not args.changes:
        parser.print_help()
        parser.exit()

    if len(args.params) >= 3:
        args.source = args.params[0] if args.params[0].endswith(ext) else args.source
        args.output = args.params[1] if args.params[1].endswith(ext) else args.output
        args.changes = args.params[2:]
    elif len(args.params) == 2:
        args.source = args.params[0] if args.params[0].endswith(ext) else args.source
        args.output = args.params[1] if args.params[1].endswith(ext) else args.output
        args.changes = args.changes

    elif len(args.params) < 2 and args.source and args.output:
        try:
            args.changes = args.changes if args.params[0].endswith(ext) else args.params[:] or args.changes
            args.source = args.params[0] if args.params[0].endswith(ext) else args.source or args.source
        except:
            args.changes = args.changes
            args.source = args.source
    else:
        parser.error("You must provide at least one change.")

    return args


# Base class for reading and writing files
class FileHandler:
    def __init__(self, filename):
        self.filename = filename  # store the file name/path
        self.data = []  # will hold file content as list of lists

    def load(self):
        pass  # to be implemented in subclasses

    def save(self, output_filename):
        pass  # to be implemented in subclasses

    def apply_change(self, col, row, value):
        # Try to update the specified cell in the data matrix
        try:
            old_value = self.data[row][col]  # get current value
            self.data[row][col] = value  # replace with new value
            print(f"Changed (col {col}, row {row}): '{old_value}' -> '{value}'")
        except IndexError:
            print(f"Invalid position: col {col}, row {row} - skipping.")


# Handler for CSV files
class CSVHandler(FileHandler):
    def load(self):
        with open(self.filename, 'r') as f:
            self.data = [line.strip().split(',') for line in f]  # split each line by comma

    def save(self, output_filename):
        with open(output_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)  # write list of lists to CSV


# Handler for JSON files
class JSONHandler(FileHandler):
    def load(self):
        with open(self.filename, 'r') as f:
            self.data = json.load(f)  # load JSON as Python list of lists

    def save(self, output_filename):
        with open(output_filename, 'w') as f:
            json.dump(self.data, f)  # dump Python list back to JSON


# Handler for Pickle files
class PickleHandler(FileHandler):
    def load(self):
        with open(self.filename, 'rb') as f:
            self.data = pickle.load(f)  # load Pickle as Python list of lists

    def save(self, output_filename):
        with open(output_filename, 'wb') as f:
            pickle.dump(self.data, f)  # dump Python list back to Pickle


# Detect and return the right handler based on file extension
def get_handler(filename):
    if filename.endswith('.csv') or filename.endswith('.txt'):
        return CSVHandler(filename)
    elif filename.endswith('.json'):
        return JSONHandler(filename)
    elif filename.endswith(('.pickle', '.pkl')):
        return PickleHandler(filename)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


# Ensure source file exists; otherwise list files in same directory
def validate_source_file(filepath):
    if not os.path.isfile(filepath):
        print(f"Error: Source file '{filepath}' not found.")
        print("")

        current_dir = os.path.dirname(os.getcwd())
        print(f"-- {current_dir} --")
        for file in os.listdir():
            print(f"L {file}")
        exit(1)


def main():
    args = parse_arguments()
    validate_source_file(args.source)

    handler = get_handler(args.source)
    handler.load()

    for change in args.changes:
        try:
            col, row, value = change.split(',')
            handler.apply_change(int(col), int(row), value)
        except ValueError:
            print(f"Invalid change format: {change}. Use col,row,value")

    dst_handler = get_handler(args.destination)
    dst_handler.data = handler.data
    dst_handler.save(args.destination)

    print(f"Modified file saved to '{args.destination}'")


if __name__ == '__main__':
    main()
