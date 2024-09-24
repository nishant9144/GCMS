from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCM
        self.bin_by_id = AVLTree()  # Key: bin_id, Value: Bin object
        self.object_by_id = AVLTree()  # Key: object_id, Value: bin_id
        self.bin_by_capacity = AVLTree()  # Key: capacity, Value: internal AVLTree of bins

    def add_bin(self, bin_id, capacity):
        # Create a new bin and add it to the bin_by_id tree
        new_bin = Bin(bin_id, capacity, capacity)
        self.bin_by_id.insert(bin_id, new_bin)

        if self.bin_by_capacity.root is None:
            inner_tree = AVLTree()
            inner_tree.insert(bin_id, new_bin)
            self.bin_by_capacity.insert(capacity, inner_tree)
            return
        node = self.bin_by_capacity.search(capacity)
        if node:
            node.value.insert(bin_id, new_bin)
        else:
            inner_tree = AVLTree()
            inner_tree.insert(bin_id, new_bin)
            self.bin_by_capacity.insert(capacity, inner_tree)

    def add_object(self, object_id, size, color):
        # Create a new object
        new_object = Object(object_id, size, color)

        # Find the best bin based on color
        if color in {Color.BLUE, Color.YELLOW}:
            best_bin = self._CompactFit(size)
        elif color in {Color.RED, Color.GREEN}:
            best_bin = self._LargestFit(size)
        if best_bin is None:
            raise NoBinFoundException()
        if best_bin.key < size:
            raise NoBinFoundException()

        # Find the specific object to add to the best bin
        best_bin_found = self._find_best_fit_object(best_bin, object_id, color)
        best_bin_found.value.add_object(new_object)
        self.object_by_id.insert(object_id, best_bin_found.key)
        node = self.bin_by_capacity.search(best_bin.key)
        if node.value.size == 1:
            self.bin_by_capacity.delete(best_bin.key)
        else:
            node.value.delete(best_bin_found.key)
        # best_bin_found.value.available_space -= size

        node = self.bin_by_capacity.search(best_bin_found.value.available_space)
        if node:
            node.value.insert(best_bin_found.key, best_bin_found.value)
        else:
            inner_tree = AVLTree()
            inner_tree.insert(best_bin_found.key, best_bin_found.value)
            self.bin_by_capacity.insert(best_bin_found.value.available_space, inner_tree)

    def _find_best_fit_object(self, best_bin, object_id, color):
        # Helper method to find the best fitting object based on color
        if color == Color.BLUE:
            return self._smallestID(best_bin.value.root)
        elif color == Color.YELLOW:
            return self._largestID(best_bin.value.root)
        elif color == Color.RED:
            return self._smallestID(best_bin.value.root)
        elif color == Color.GREEN:
            return self._largestID(best_bin.value.root)

    def delete_object(self, object_id):
        # Find the bin containing the object
        found_bin = self.object_by_id.search(object_id)
        if found_bin:
            found_bin_id = found_bin.value
            bin = self.bin_by_id.search(found_bin_id).value
            object_size = bin.object_tree.search(object_id).value.object_size
            old_key = bin.available_space
            old_bin = self.bin_by_capacity.search(old_key)
            if old_bin.value.size == 1:
                self.bin_by_capacity.delete(old_key)
            else:
                old_bin.value.delete(found_bin_id)
            self.object_by_id.delete(object_id)
            new_key = bin.available_space + object_size
            bin.remove_object(object_id)
            
            if self.bin_by_capacity.search(new_key):
                self.bin_by_capacity.search(new_key).value.insert(found_bin_id, bin)
            else:
                inner_tree = AVLTree()
                inner_tree.insert(found_bin_id, bin)
                self.bin_by_capacity.insert(new_key, inner_tree)
        else:
            return None

    def bin_info(self, bin_id):
        # Returns a tuple with current available space and list of objects in the bin
        found_bin = self.bin_by_id.search(bin_id)
        if found_bin:
            bin_info = found_bin.value.object_tree.inorder()
            return (found_bin.value.available_space, bin_info)
        return None

    def object_info(self, object_id):
        # Returns the bin_id in which the object is stored 
        found_node = self.object_by_id.search(object_id)
        if found_node:
            return found_node.value
    
    def _CompactFit(self, size):
        # Find the bin with the least available space that can fit the object
        current_node = self.bin_by_capacity.root
        best_fit_node = None

        # Traverse to find the best fit bin based on capacity and ID
        while current_node:
            if current_node.key >= size:
                best_fit_node = current_node
                current_node = current_node.left  # Move left for a tighter fit
            else:
                current_node = current_node.right  # Move right for larger bins

        return best_fit_node

    def _LargestFit(self, size):
        # Find the bin with the largest available space that can fit the object
        current_node = self.bin_by_capacity.root
        best_fit_node = None

        # Traverse to find the best fit bin based on capacity and ID
        while current_node:
                best_fit_node = current_node
                current_node = current_node.right  # Move right for larger bins
        return best_fit_node
    
    def _smallestID(self, root):
        # Find the node with the smallest ID
        current_node = root
        while current_node.left:
            current_node = current_node.left
        return current_node
    
    def _largestID(self, root):
        # Find the node with the largest ID
        current_node = root
        while current_node.right:
            current_node = current_node.right
        return current_node
