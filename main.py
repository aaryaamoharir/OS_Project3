import os
import sys
import struct
import csv



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def main():
    print(len(sys.argv))
    if len(sys.argv) < 2:
        print("Usage: python project3.py <command> [arguments]")
        print("Commands:")
        print("  create <index_file>")
        print("  insert <index_file> <key> <value>")
        print("  search <index_file> <key>")
        print("  load <index_file> <csv_file>")
        print("  print <index_file>")
        print("  extract <index_file> <csv_file>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "create" and len(sys.argv) == 3:
        #function to create index
    elif command == "insert" and len(sys.argv) == 5:
        #function to insert index
    elif command == "search" and len(sys.argv) == 4:
        #functio nto searhc
    elif command == "load" and len(sys.argv) == 4:
        #function to load
    elif command == "print" and len(sys.argv) == 3:
        #function to print
    elif command == "extract" and len(sys.argv) == 4:
        #function to extract
    else:
        print("Invalid command or wrong number of arguments")
        sys.exit(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
