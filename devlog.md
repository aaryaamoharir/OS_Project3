# Project 3 Development Log

## **05-10-2025 7:01PM Session**
Due to finals I didn't have time to work on this project before hand but I think 
I have a pretty good understanding of how the project needs to work. 

These are the requirements that I think I understand from the pdf and external research that I did 
to understand what I'm supposed to do. 
1. B-Tree implementation with minimal degree of 10 
(19 key/value pairs, 20 child pointers per node)
2. Index files divided into 512-byte blocks
3. Never have more than 3 nodes in memory at any time
4. 8-byte integers stored in big-endian byte order
5. First block contains file header with magic number, root block ID, and next block ID
6. Node blocks contain block ID, parent ID, number of keys, arrays of keys, values, and child pointers
7. Commands include create, insert, search, load, print, extract

## 11:31 PM 
I did some more research and have a strong outline of how I'll be implementing this. I'll get started on 
actually implementing it tomorrow and should hopefully be ready to submit by tomorrow night.

## **05-11-2025 9:38AM Session**
Today I'll be implementing all aspects of the project. I think I'll start with creating the b-tree structure. 
It makes more sense to have multiple classes so I'll create BTreeNode class for the actual 
BTree structure and a BTree class to manage all the operations. Lastly, since the file operations 
are a little different I'll create a seperate class to handle file operations as well. 

Additionally, in my previous projects my code has been incredibly messy to read so I'm going to try to make it 
more modular using multiple methods, classes, and variables for constants instead of 
just putting in the variable values. 

I'm currently having trouble with it reading in the number of arguments for some reason so I'm ending this session and will come
back in a while to continue working on the project 

## **05-11-2025 2:41PM Session**
Currently I'm working on creating a basic implementation of the program. I realized 
the issue from the morning was because I wasn't using the last line (name == main) and 
therefore, it was never going to the main function 

I was having some issues with creating the file because I forgot to consider if the file already 
exists but that was a quick fix. 

## **05-11-2025 4:55PM Session**
Working on implementing a b-tree with a 512 block so I watched a quick youtube video 
to better understand what it was asking. I didn't really understand how to serialize the block so I ended 
up watching a video and realized struct.unpack could be helpful. 

Now I plan to work on the b-tree insert method. 


