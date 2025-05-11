import os
import sys
import struct
import csv

BLOCK_SIZE = 512
MAGIC_NUMBER = b"4348PRJ3"
MINIMAL_DEGREE = 10  # t value in B-tree terminology
MAX_KEYS = 19
MAX_CHILDREN = 20

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

#create the index file
def create_index_file(filename):
    if os.path.exists(filename):
        print(f"Error: File '{filename}' already exists.")
        sys.exit(1)

    try:
        with open(filename, 'wb') as f:
            # magics number, then root block, and then next block and gotta pad to 512 byres
            f.write(MAGIC_NUMBER)
            f.write(struct.pack('>Q', 0))
            f.write(struct.pack('>Q', 1))
            f.write(b'\x00' * (BLOCK_SIZE - 24))
        print(f"Index file '{filename}' created successfully.")
    #error out if it doesn't work
    except IOError as e:
        print(f"Error creating file '{filename}': {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python project3.py <command> <index_file> [args...]")
        sys.exit(1)

    command = sys.argv[1].lower()
    index_file = sys.argv[2]

    if command == 'create':
        create_index_file(index_file)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()