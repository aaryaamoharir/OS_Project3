# 
# README_AaryaaMoharir_Acm220004

# Overall 
This Python program implements a command-line index file management system using a B-Tree data structure, as specified for a CS4348 Operating Systems Concepts project (Spring 2025).
The program manages index files stored as binary files, where each file contains a B-Tree with a minimum degree of 10 (allowing up to 19 key/value pairs per node). The index file 
is divided into 512-byte blocks, with the first block serving as the header and subsequent blocks representing B-Tree nodes. The program supports six commands: 
create, insert, search, load, print, and extract, which allow users to create index files, insert key/value pairs, search for keys, load pairs from a CSV file, print all pairs, 
and extract pairs to a CSV file, respectively. The implementation ensures that no more than three nodes are in memory at any time, handles big-endian 8-byte integer storage, and 
includes robust error checking for invalid inputs and file operations.

# Main.py 

This is the main program that implements the B-Tree index file manager. It processes command-line arguments to execute one of the supported commands, 
interacting with binary index files and CSV files as needed. The program is structured around two main classes: BTreeNode and BTree, along with several 
utility functions for file operations and command handling.

# BTreeNode Class 

The BTreeNode class represents a single node in the B-Tree, stored in a 512-byte block. Each node contains:

Block ID: 8 bytes, identifying the node’s position in the file.
Parent Block ID: 8 bytes, referencing the parent node (0 for the root).
Key Count: 8 bytes, indicating the number of key/value pairs (max 19).
Keys: 152 bytes (19 × 8-byte integers), storing keys in sorted order.
Values: 152 bytes (19 × 8-byte integers), storing values corresponding to keys.
Children: 160 bytes (20 × 8-byte block IDs), pointing to child nodes (0 for leaf nodes).
Unused: 24 bytes, padding to fill the 512-byte block.

The class provides methods to:

to_bytes(): Serialize the node into a 512-byte block.
from_bytes(): Deserialize a 512-byte block into a node object.


# External functions 

create_index_file(filename): Creates a new index file with a header block.
read_header(filename): Reads the root and next block IDs from the header.
write_header(filename, root_id, next_id): Updates the header.
read_node(filename, block_id): Reads a node from the file.
write_node(filename, node): Writes a node to the file.
is_valid_index_file(filename): Verifies the file’s magic number (4348PRJ3).
Command handlers: insert_command, search_command, load_command, print_command, and extract_command process respective commands.


# Devlog.md 
The devlog is structured in a diary format that contains my thoughts before starting a programming session and after finishing it. It includes what I did during 
that session, how I felt about it, and what I plan to do in the future. 

# How to run the program 

The program can be run through the terminal using _python3 main.py <command> <index_file> [args...]_
It needs to be run using python3 

# Supported Commands  
1. create <index_file>
Creates a new index file with a header block.

2. insert <index_file> <key> <value>
Inserts a key/value pair into the B-Tree.

3. dex_file> <key>
Searches for a key and prints its value if found.

4. load <index_file> <csv_file>
Loads key/value pairs from a CSV file into the B-Tree.

5. print <index_file>
Prints all key/value pairs in-order.

6. extract <index_file> <csv_file>
Saves all key/value pairs to a CSV file.

# Error Handling 
The program handles various error conditions:

File Errors: Checks for file existence and validity (magic number 4348PRJ3).
Input Validation: Ensures keys and values are non-negative integers.
Duplicate Keys: Rejects duplicate keys in insert and load commands.
I/O Errors: Catches and reports file access issues.
Command Syntax: Validates the number and format of command-line arguments.

The program outputs logs for every action performed by threads in this format:
THREAD_TYPE ID [THREAD_TYPE ID]: MSG

# Overall Notes 

Memory Constraint: The program adheres to the requirement of keeping at most three nodes in memory, achieved by loading and writing nodes on-demand.
Big-Endian: All integers are stored in big-endian format, ensuring compatibility across platforms.
B-Tree Properties: Maintains a minimum degree of 10, with nodes supporting up to 19 keys and 20 children, ensuring balanced trees.
Duplicate Keys: Enforces unique keys, consistent with typical B-Tree index usage.
