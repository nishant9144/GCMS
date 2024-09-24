# Galactic Cargo Management System (GCMS)

This repository contains the solution for Galactic Cargo Management System (GCMS).

## Contents

[TOC]

## Background
In the vast expanse of the galaxy, interstellar shipping companies face the challenge of efficiently packing cargo into space cargo bins. This system assigns unique integer IDs to bins and objects and efficiently handles the cargo based on its color.

## Cargo Color rules
- **Blue Cargo (Compact Fit, Least ID)**: Assign to the bin with the smallest remaining capacity. If multiple bins have the same remaining capacity, the one with the least ID is chosen.
- **Yellow Cargo (Compact Fit, Greatest ID)**: Same as Blue Cargo, but the bin with the greatest ID is chosen.
- **Red Cargo (Largest Fit, Least ID)**: Assign to the bin with the largest remaining capacity. If multiple bins have the same remaining capacity, the one with the least ID is chosen.
- **Green Cargo (Largest Fit, Greatest ID)**: Same as Red Cargo, but the bin with the greatest ID is chosen.


## Project Structure
- **gcms.py**: Main GCMS class to manage bins and objects.
- **bin.py**: Implementation of the `Bin` class that stores the bin information.
- **object.py**: Implementation of the `Object` class, storing the object details including color, ID, and size.
- **avl.py**: AVL Tree implementation to manage bins and objects efficiently.
- **node.py**: AVL Tree node implementation.
- **exceptions.py**: Contains exceptions.
- **main.py**: A script for testing and debugging purposes.

## Solution
I have made use of AVL tree. For AVL tree, we will use different comparators for performing the task assigned to it so that we do not have to write the code again.

- **avl.py**: I have created a basic comparator which compares the key of its nodes.
In the class AVLTree, I have created basic methoda like insert, delete, search and traversal.
For the attributes, I went for the size of the tree, and its root.

- **bin.py**: For the bin class,I have created attributes like the capacity of the bin, the bin_id, the tree in which the objects are stored, and the available_space in the bin.
For the methods, I went for add_object which adds object to the tree and updates the available_space adn delete_object which deletes the object from the tree and do the same as before.

- **object.py**: I have created this class for creating object which has ID, size and color as its attributes.

- **node.py**: This class creates a Node which has key and value attributes.
The key is the main feature according to which the comparator works.

- **exception.py**: This is for raising NoBinFoundException.

- **gcms.py**: This class hold 3 trees. It goes by object_by_ID, bin_by_id and bin_by_capacity.
The object_by_id tree has nodes which holds key as object_id and value as bin_id in which it is stored.
The bin_by_id has key as its ID and value as the bin.
The bin_by_capacity has nodes which has key as the capacity of the bin 	and value as a inner tree which has key as the Id of the bin with the same 	available_space and value as the bin.

##Time and Space Complexity Analysis
n represents the number of objects and m represents the number of bins.

- The program has space complexity as O(n + m)
- The whole program has time complexity in order of log for every operation.

