from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class Bin:
    def __init__(self, bin_id, capacity, available_space):
        self.id = bin_id
        self.capacity = capacity
        self.available_space = available_space
        self.object_tree = AVLTree()

    def add_object(self, object):
        # Implement logic to add an object to this bin
        if object.object_size > self.available_space:
            raise NoBinFoundException
        self.object_tree.insert(object.id, object)
        self.available_space -= object.object_size
        
    def remove_object(self, object_id):
        # Implement logic to remove an object from this bin
        object_node = self.object_tree.search(object_id).value
        if object_node is None:
            # print(f"Object with ID {object_id} not found.")
            return
        self.object_tree.delete(object_id)
        self.available_space += object_node.object_size
