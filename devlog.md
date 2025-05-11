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

