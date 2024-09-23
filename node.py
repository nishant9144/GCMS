from object import *

class Node:
    def __init__(self,key, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value 
        self.height = 1