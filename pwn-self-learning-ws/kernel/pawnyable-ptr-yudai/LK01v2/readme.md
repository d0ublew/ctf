# Kernel Heap

## SLAB

- oldest type
- used in Solaris
- no chunk size metadata
- similar sized chunks are allocated on the same memory page
- uses bitmap to manage free space (stored in the beginning of the page frame)
- has cache

## SLUB

- default allocator
- intended for large systems
- similar sized chunks are allocated on the same page frame
- uses singly linked list to manage free spaces (the pointer to the head is stored in the page frame descriptor)
- has cache for each cpu (uses singly linked list)


## SLOB

- lightweight
- used on embedded devices
- similar allocation mechanism to glibc malloc
- free spaces are managed in a single list (regardless of size)
- a freed chunk has an offset to the next free space of similar size
