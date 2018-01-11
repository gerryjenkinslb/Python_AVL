import unittest

''' Description:  Implement a binary search AVLTree with the following interface functions:
        __contains__(y)     y in t
        __getitem__(y)      t[y]
        __setitem__(k, v)   t[k] = v
        __delitem__(k)      del t[k]
        __len__()           len(t)
        __iter__()          for k in t:
        put(k, v)
        get(k)
'''

class AVLTree:

    class _Node:  # node hidden from client

        def __init__(self, key, value = 0):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.height = 1 # bottom starts at height of 1

        def __iter__(self):  # this is a generator functions due to the yields
            """The standard inorder traversal of a binary tree for self that returns nodes"""
            if self:
                if self.left:
                    for node in self.left:  # call inter
                        yield node  # generate left node
                yield self  # generate center node
                if self.right:
                    for node in self.right:
                        yield node  # generate right node

        def __repr__(self): return f"Node( k={self.key}, v={self.value}, h={self.height})"

    # new AVLTree
    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        self.put(key, value)

    def put(self, key, value = None): # allow only keys in tree
        self.root = self._put(self.root, key, value)



    def _put(self, node, key, value):  # recursive _put follow tree down till place found for new node
        if not node: # place found, return new node
            self.size = self.size + 1
            return self._Node(key, value)

        elif key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            node.value = value  # key already in tree, change value
            return node # return existing node

        return self.adjustNode(key, node)

    def adjustNode(self, key, node):
        node.height = 1 + max(self.getHeight(node.right), self.getHeight(node.left))
        balance = self.getBalance(node)

        # check for imbalance and rotate to correct
        if balance > 1: # left heavy
            if key > node.left.key:
                node.left = self.leftRotate(node.left) # Left Right
            return self.rightRotate(node) # catch either Left Right or Right Right
        elif balance < -1:
            if key < node.right.key:
                node.right = self.rightRotate(node.right) # Right Left
            return self.leftRotate(node) # catch either Right Left or Left Left

        return node

    # Recursive function to delete a node with
    # given key from subtree with given node.
    # It returns node of the modified subtree.
    def delete(self, node, key):

        if not node: return node # not found

        # find node with key
        elif key < node.value:
            node.left = self.delete(node.left, key)
        elif key > node.value:
            node.right = self.delete(node.right, key)
        else: # equal, it is found
            if node.left is None: # case of only right child
                return node.right # replace node with child

            elif node.right is None: # case of only left child
                return node.left # replace node with child

            # case of two children
            succ = self.getMinValueNode(node.right) # successor of node
            node.key = succ.key # copy
            node value = succ.value
            node.right = self.delete(node.right, succ.value)

        # If the tree has only one node,
        # simply return it
        if node is None:
            return node

        # Step 2 - Update the height of the
        # ancestor node
        node.height = 1 + max(self.getHeight(node.left),
                              self.getHeight(node.right))

        # Step 3 - Get the balance factor
        balance = self.getBalance(node)

        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(node.left) >= 0:
            return self.rightRotate(node)

        # Case 2 - Right Right
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.leftRotate(node)

        # Case 3 - Left Right
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        # Case 4 - Right Left
        if balance < -1 and self.getBalance(node.right) > 0:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return root


    def getHeight(self, node): return node.height if node else 0

    def getBalance(self, node): return self.getHeight(node.left) - self.getHeight(node.right)

    #     a                             b
    #      \                          // \      < update link //
    #       b     Left Rotate(a)      a   c
    #     /  \   - - - - - - - ->     \\        < update link \\
    #    x    c                        x

    def leftRotate(self, a):
        b = a.right
        x = b.left   # get x
        b.left = a   # update b left link point to a
        a.right = x  # replace a.right link to now point to x

        # Update heights
        a.height = 1 + max(self.getHeight(a.left), self.getHeight(a.right))
        b.height = 1 + max(self.getHeight(b.left), self.getHeight(b.right))

        # Return the new root node
        return b


    #         a                          b
    #        /                          / \\      < update link \\
    #       b     Right Rotate(a)      c   a
    #     /  \   - - - - - - - ->         //      < update link //
    #    c    x                          x

    def rightRotate(self, a):
        b = a.left
        x = b.right  # get x d
        b.right = a  # update b right link point to a
        a.left = x  # replace c left link to now point to x

        # Update heights
        a.height = 1 + max(self.getHeight(a.left), self.getHeight(a.right))
        b.height = 1 + max(self.getHeight(b.left), self.getHeight(b.right))

        # Return the new root node
        return b

    def getMinNode(self, node):
        if node is None or node.left is None:
            return node
        return self.getMinNode(node.left)

    def iterate(self):
        node = self.root
        if not node: return None
        for n in node:
            yield n

    def isBalanced(self):
        for n in self.iterate():
            bal = self.getBalance(n)
            if bal not in (1,0,-1): return False
        return True

    def __iter__(self): # client iterate in order key/values
        for n in self.iterate():
            yield n.key,n.value


def main(): # run tests on this class
    print("tests")
    tree = AVLTree()
    tree.put(10)
    tree.put(20)
    tree.put(30)
    tree.put(40)
    tree.put(5)
    tree.put(6)
    assert tree.isBalanced()
    assert [5,6,10,20,30,40] == [ n[0] for n in tree ]


if __name__ == "__main__":
    # execute only if run as a script
    main()