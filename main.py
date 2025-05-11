import os
import sys
import struct
import csv

BLOCK_SIZE = 512
MAGIC_NUMBER = b"4348PRJ3"
MINIMAL_DEGREE = 10  # t value in B-tree terminology
MAX_KEYS = 19
MAX_CHILDREN = 20

#initialze the b-tree
class BTreeNode:
    def __init__(self, block_id, parent_id=0, is_leaf=True):
        self.block_id = block_id
        self.parent_id = parent_id
        self.is_leaf = is_leaf
        self.num_keys = 0
        self.keys = [0] * MAX_KEYS  # 19 keys
        self.values = [0] * MAX_KEYS  # 19 values
        self.children = [0] * MAX_CHILDREN  # 20 children, 0 indicates no child

    #check if it's full
    def is_full(self):
        return self.num_keys == MAX_KEYS

#manage the operations on the index file
class IndexFile:
    def __init__(self, filename):
        self.filename = filename
        self.root_block_id = 0
        self.next_block_id = 1
        self.nodes_in_memory = {} #this is a cache for nodes and it has a limit of 3

    #create an index file
    def create(self):
        if os.path.exists(self.filename):
            raise FileExistsError(f"File {self.filename} already exists")

        with open(self.filename, 'wb') as f:
            # writes the header according to instructions
            header = struct.pack('>8sQQ', MAGIC_NUMBER, self.root_block_id, self.next_block_id)
            header += b'\0' * (BLOCK_SIZE - len(header))
            f.write(header)
#manages the b-tree operations
class BTree:

    def __init__(self, index_file):
        self.index_file = index_file
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
