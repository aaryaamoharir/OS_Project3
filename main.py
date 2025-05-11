import os
import sys
import struct
import csv

# these are the constants
BLOCK_SIZE = 512
MAGIC_NUMBER = b"4348PRJ3"
MINIMAL_DEGREE = 10  # t-value basically
MAX_KEYS = 19
MAX_CHILDREN = 20

#class BTreeNode:
#class IndexFile:
#class BTree:

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

    command = sys.argv[1].lower()  #turn it all lowercase for comparsion

    if command == "create" and len(sys.argv) == 3:
        create_index_file(sys.argv[2])
    elif command == "insert" and len(sys.argv) == 5:
        insert_key_value(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "search" and len(sys.argv) == 4:
        search_key(sys.argv[2], sys.argv[3])
    elif command == "load" and len(sys.argv) == 4:
        load_from_csv(sys.argv[2], sys.argv[3])
    elif command == "print" and len(sys.argv) == 3:
        print_all(sys.argv[2])
    elif command == "extract" and len(sys.argv) == 4:
        extract_to_csv(sys.argv[2], sys.argv[3])
    else:
        print("Invalid command or wrong number of arguments")
        sys.exit(1)
