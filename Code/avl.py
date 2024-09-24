from node import Node

def comp_1(node1, node2): # compare id
    return node1.key - node2.key

class AVLTree:
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def insert(self, key, value):
        new_node = Node(key, value)
        self.root = self._insert(self.root,new_node)
        self.size += 1

    def _insert(self, node, new_node):
        if node is None:
            return new_node
        
        if self.comparator(new_node, node) < 0:
            node.left = self._insert(node.left, new_node)
        elif self.comparator(new_node, node) > 0:
            node.right = self._insert(node.right, new_node)
        else:
            return node   
             
        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))
        
        return self._balance(node)
    
    def _balance(self, node):
        balance = self._get_balance(node)

        # Left-heavy case
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._leftRotate(node.left)  # Left-Right case
            return self._rightRotate(node)  # Left-Left case
        
        # Right-heavy case
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rightRotate(node.right)  # Right-Left case
            return self._leftRotate(node)  # Right-Right case

        return node

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._getHeight(node.left) - self._getHeight(node.right)

    def _getHeight(self, root):
        if not root:
            return 0
        return root.height
    
    def _leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._getHeight(z.left), self._getHeight(z.right))
        y.height = 1 + max(self._getHeight(y.left), self._getHeight(y.right))

        return y

    def _rightRotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self._getHeight(z.left), self._getHeight(z.right))
        y.height = 1 + max(self._getHeight(y.left), self._getHeight(y.right))

        return y
    
    def delete(self, key):
        dummy_node = Node(key)
        self.root = self._delete(self.root, dummy_node)
        self.size -= 1

    def _delete(self, node, dummy_node):
        if node is None:
            return node

        if self.comparator(dummy_node, node) < 0:
            node.left = self._delete(node.left, dummy_node)
        elif self.comparator(dummy_node, node) > 0:
            node.right = self._delete(node.right, dummy_node)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp)
        
        node.height = 1 + max(self._getHeight(node.left), self._getHeight(node.right))
        
        return self._balance(node)
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def search(self, key):
        dummy_node = Node(key)
        return self._search(self.root, dummy_node)
    
    def _search(self, node, dummy_node):
        if node is None:
            return node
        
        if self.comparator(dummy_node, node) < 0:
            return self._search(node.left, dummy_node)
        elif self.comparator(dummy_node, node) > 0:
            return self._search(node.right, dummy_node)
        else:
            return node
    
    def inorder(self):
        return self._inorder(self.root)
    
    def _inorder(self, node):
        if node is None:
            return []
        return self._inorder(node.left) + [node.value.id] + self._inorder(node.right)