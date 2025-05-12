import os
import sys
import struct
import csv

BLOCK_SIZE = 512
MAGIC_NUMBER = b"4348PRJ3"
MINIMAL_DEGREE = 10  # t value in B-tree terminology
MAX_KEYS = 19
MAX_CHILDREN = 20

#class for each node of the BTree
class BTreeNode:
    def __init__(self, block_id=0, parent_id=0, key_count=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.key_count = key_count
        self.keys = [0] * MAX_KEYS
        self.values = [0] * MAX_KEYS
        self.children = [0] * MAX_CHILDREN

    #convert to a 512 byte block
    def to_bytes(self):
        data = bytearray()
        data.extend(struct.pack('>Q', self.block_id))
        data.extend(struct.pack('>Q', self.parent_id))
        data.extend(struct.pack('>Q', self.key_count))
        for key in self.keys:
            data.extend(struct.pack('>Q', key))
        for value in self.values:
            data.extend(struct.pack('>Q', value))
        for child in self.children:
            data.extend(struct.pack('>Q', child))
        data.extend(b'\x00' * (BLOCK_SIZE - len(data)))  # Pad to 512 bytes
        return bytes(data)

    #create a node from the block
    #creates and return an instance of a class
    @classmethod
    def from_bytes(cls, data, block_id):
        node = cls(block_id=block_id)
        node.parent_id = struct.unpack('>Q', data[8:16])[0]
        node.key_count = struct.unpack('>Q', data[16:24])[0]
        for i in range(MAX_KEYS):
            node.keys[i] = struct.unpack('>Q', data[24 + i * 8:32 + i * 8])[0]
            node.values[i] = struct.unpack('>Q', data[176 + i * 8:184 + i * 8])[0]
        for i in range(MAX_CHILDREN):
            node.children[i] = struct.unpack('>Q', data[328 + i * 8:336 + i * 8])[0]
        return node

#class for the BTree
class BTree:
    def __init__(self, filename):
        self.filename = filename
        self.root_id, self.next_id = read_header(filename)

    def insert(self, key, value):
        """Insert a key/value pair into the B-Tree."""
        if self.root_id == 0:
            # Create new root node
            root = BTreeNode(block_id=self.next_id, key_count=1)
            root.keys[0] = key
            root.values[0] = value
            write_node(self.filename, root)
            self.next_id += 1
            self.root_id = root.block_id
            write_header(self.filename, self.root_id, self.next_id)
        else:
            # Load root node
            root = read_node(self.filename, self.root_id)
            if root.key_count == MAX_KEYS:
                # Split root
                new_root = BTreeNode(block_id=self.next_id)
                self.next_id += 1
                new_root.children[0] = root.block_id
                root.parent_id = new_root.block_id
                self._split_child(new_root, 0)
                write_node(self.filename, root)
                self._insert_non_full(new_root, key, value)
                write_node(self.filename, new_root)
                self.root_id = new_root.block_id
                write_header(self.filename, self.root_id, self.next_id)
            else:
                self._insert_non_full(root, key, value)
                write_node(self.filename, root)

    #splits a full child node
    def _split_child(self, parent, child_index):
        child = read_node(self.filename, parent.children[child_index])
        new_node = BTreeNode(block_id=self.next_id, parent_id=parent.block_id)
        self.next_id += 1

        # Move middle key/value to parent
        middle_index = MINIMAL_DEGREE - 1
        parent.keys[parent.key_count] = child.keys[middle_index]
        parent.values[parent.key_count] = child.values[middle_index]
        parent.key_count += 1

        # seocnd half
        new_node.key_count = MINIMAL_DEGREE - 1
        for i in range(new_node.key_count):
            new_node.keys[i] = child.keys[middle_index + 1 + i]
            new_node.values[i] = child.values[middle_index + 1 + i]
            new_node.children[i] = child.children[middle_index + 1 + i]
        new_node.children[new_node.key_count] = child.children[middle_index + 1 + new_node.key_count]

        # child pointers
        parent.children[child_index + 1] = new_node.block_id
        for i in range(parent.key_count):
            if parent.children[i] != 0:
                child_node = read_node(self.filename, parent.children[i])
                child_node.parent_id = parent.block_id
                write_node(self.filename, child_node)

        # truncate the child
        child.key_count = MINIMAL_DEGREE - 1
        for i in range(child.key_count, MAX_KEYS):
            child.keys[i] = 0
            child.values[i] = 0
        for i in range(child.key_count + 1, MAX_CHILDREN):
            child.children[i] = 0

        write_node(self.filename, child)
        write_node(self.filename, new_node)

    #insert into a non full node (doesn't need to be split or anything)
    def _insert_non_full(self, node, key, value):
        i = node.key_count - 1
        if node.children[0] == 0:  # Leaf node
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
            node.key_count += 1
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            child = read_node(self.filename, node.children[i])
            if child.key_count == MAX_KEYS:
                self._split_child(node, i)
                write_node(self.filename, node)
                if key > node.keys[i]:
                    i += 1
                child = read_node(self.filename, node.children[i])
            self._insert_non_full(child, key, value)
            write_node(self.filename, child)

#searches for a key
    def search(self, key):
        if self.root_id == 0:
            return None
        return self._search_node(self.root_id, key)

#goes through and tries to search the node for a key recursively
    def _search_node(self, block_id, key):
        node = read_node(self.filename, block_id)
        i = 0
        while i < node.key_count and key > node.keys[i]:
            i += 1
        if i < node.key_count and key == node.keys[i]:
            return node.values[i]
        if node.children[0] == 0:  # Leaf node
            return None
        return self._search_node(node.children[i], key)

    #this will print all the key value in order (using recursion since it's been a minute since I've used it so I wanted to try it)
    def print_all(self):
        if self.root_id == 0:
            print("Index is empty.")
            return
        self._print_node(self.root_id)

    #recursively prints out all the pairs in key value format
    def _print_node(self, block_id):
        node = read_node(self.filename, block_id)
        for i in range(node.key_count):
            if node.children[i] != 0:
                self._print_node(node.children[i])
            print(f"key {node.keys[i]}, value {node.values[i]}")
        if node.children[node.key_count] != 0:
            self._print_node(node.children[node.key_count])

    #extracts them all into the csv file as long as it doesn't already exist
    def extract(self, csv_file):
        if os.path.exists(csv_file):
            print(f"Error: Output file '{csv_file}' already exists.")
            return False
        pairs = []
        self._collect_pairs(self.root_id, pairs)
        try:
            with open(csv_file, 'w') as f:
                for key, value in pairs:
                    f.write(f"{key},{value}\n")
            return True
        except IOError as e:
            print(f"Error writing to '{csv_file}': {e}")
            return False

    #collects the key value pairs in order
    def _collect_pairs(self, block_id, pairs):
        if block_id == 0:
            return
        node = read_node(self.filename, block_id)
        for i in range(node.key_count):
            if node.children[i] != 0:
                self._collect_pairs(node.children[i], pairs)
            pairs.append((node.keys[i], node.values[i]))
        if node.children[node.key_count] != 0:
            self._collect_pairs(node.children[node.key_count], pairs)


#create the index file
def create_index_file(filename):
    if os.path.exists(filename):
        print(f"Error: File '{filename}' already exists.")
        sys.exit(1)

    try:
        with open(filename, 'wb') as f:
            # magics number, then root block, and then next block and gotta pad to 512 byres
            f.write(MAGIC_NUMBER)
            f.write((0).to_bytes(8, byteorder='big'))
            f.write((1).to_bytes(8, byteorder='big'))
            f.write(b'\x00' * (BLOCK_SIZE - 24))
        print(f"Index file '{filename}' created successfully.")
    #error out if it doesn't work
    except IOError as e:
        print(f"Error creating file '{filename}': {e}")
        sys.exit(1)

#read the header and it must match the magic number
def read_header(filename):
    with open(filename, 'rb') as f:
        f.seek(0)
        magic = f.read(8)
        if magic != MAGIC_NUMBER:
            raise ValueError("Invalid index file")
        root_id = struct.unpack('>Q', f.read(8))[0]
        next_id = struct.unpack('>Q', f.read(8))[0]
    return root_id, next_id

#whenever you write the header it has to have the magic number, root, next_id, and then fill it with zeros
def write_header(filename, root_id, next_id):
    with open(filename, 'r+b') as f:
        f.seek(0)
        f.write(MAGIC_NUMBER)
        f.write(struct.pack('>Q', root_id))
        f.write(struct.pack('>Q', next_id))
        f.write(b'\x00' * (BLOCK_SIZE - 24))

def read_node(filename, block_id):
    with open(filename, 'rb') as f:
        f.seek(block_id * BLOCK_SIZE)
        data = f.read(BLOCK_SIZE)
    return BTreeNode.from_bytes(data, block_id)

def write_node(filename, node):
    with open(filename, 'r+b') as f:
        f.seek(node.block_id * BLOCK_SIZE)
        f.write(node.to_bytes())


def is_valid_index_file(filename):
    """Check if the file is a valid index file by verifying the magic number."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        return False

    try:
        with open(filename, 'rb') as f:
            magic = f.read(8)
            if magic != MAGIC_NUMBER:
                print(f"Error: File '{filename}' is not a valid index file.")
                return False
        return True
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return False

def insert_command(filename, key, value):
    """Handle the insert command."""
    if not is_valid_index_file(filename):
        sys.exit(1)
    try:
        key = int(key)
        value = int(value)
        if key < 0 or value < 0:
            raise ValueError("Key and value must be non-negative")
        tree = BTree(filename)
        existing_value = tree.search(key)
        if existing_value is not None:
            print(f"Error: Key {key} already exists in '{filename}'.")
            sys.exit(1)

        tree.insert(key, value)
        print(f"Inserted key {key} with value {value} into '{filename}'.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error accessing file '{filename}': {e}")
        sys.exit(1)

#searches through the b-tree to find the key basically
def search_command(filename, key):
    if not is_valid_index_file(filename):
        sys.exit(1)
    try:
        key = int(key)
        if key < 0:
            raise ValueError("Key must be non-negative")
        tree = BTree(filename)
        value = tree.search(key)
        if value is not None:
            print(f"Found: key {key}, value {value}")
        else:
            print(f"Key {key} not found in '{filename}'.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error accessing file '{filename}': {e}")
        sys.exit(1)

#handles the load file
def load_command(index_file, csv_file):
    if not is_valid_index_file(index_file):
        sys.exit(1)
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' does not exist.")
        sys.exit(1)
    try:
        tree = BTree(index_file)
        with open(csv_file, 'r') as f:
            for line in f:
                key, value = map(int, line.strip().split(','))
                if key < 0 or value < 0:
                    raise ValueError("Keys and values must be non-negative")
                    # Check for duplicate key
                existing_value = tree.search(key)
                if existing_value is not None:
                    print(f"Error: Key {key} already exists in '{index_file}'.")
                    sys.exit(1)
                tree.insert(key, value)
        print(f"Loaded key/value pairs from '{csv_file}' into '{index_file}'.")
    except ValueError as e:
        print(f"Error in CSV file: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error accessing files: {e}")
        sys.exit(1)

#handles the print_command
def print_command(filename):
    if not is_valid_index_file(filename):
        sys.exit(1)
    try:
        tree = BTree(filename)
        tree.print_all()
    except IOError as e:
        print(f"Error accessing file '{filename}': {e}")
        sys.exit(1)

#handles the extract command by sending it to the extract method
def extract_command(index_file, csv_file):
    if not is_valid_index_file(index_file):
        sys.exit(1)
    try:
        tree = BTree(index_file)
        if tree.extract(csv_file):
            print(f"Extracted key/value pairs to '{csv_file}'.")
    except IOError as e:
        print(f"Error accessing files: {e}")
        sys.exit(1)

def main():
    #if len(sys.argv) < 3:
    #    print("Usage: python project3.py <command> <index_file> [args...]")
    #    sys.exit(1)

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
    index_file = sys.argv[2]

    if command == 'create':
        create_index_file(index_file)
    elif command == 'insert':
        if len(sys.argv) != 5:
            print("Usage: python project3.py insert <index_file> <key> <value>")
            sys.exit(1)
        insert_command(index_file, sys.argv[3], sys.argv[4])
    elif command == 'search':
        if len(sys.argv) != 4:
            print("Usage: python project3.py search <index_file> <key>")
            sys.exit(1)
        search_command(index_file, sys.argv[3])
    elif command == 'load':
        if len(sys.argv) != 4:
            print("Usage: python project3.py insert <index_file> <csv_file>")
            sys.exit(1)
        load_command(index_file, sys.argv[3])
    elif command == 'print':
        if len(sys.argv) != 3:
            print("Usage: python project3.py print <index_file>")
            sys.exit(1)
        print_command(index_file)
    elif command == 'extract':
        if len(sys.argv) != 4:
            print("Usage: python project3.py extract <index_file> <csv_file>")
            sys.exit(1)
        extract_command(index_file, sys.argv[3])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()