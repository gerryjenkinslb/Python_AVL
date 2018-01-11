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

        return self._adjust_node(node, key)

    def _adjust_node(self, node, key):
        node.height = 1 + max(self._height(node.right), self._height(node.left))
        balance = self._balance(node)

        # check for imbalance and rotate to correct
        if balance > 1: # left heavy
            if key > node.left.key:
                node.left = self._leftRotate(node.left) # Left Right
            return self._rightRotate(node) # catch either Left Right or Right Right
        elif balance < -1:
            if key < node.right.key:
                node.right = self._rightRotate(node.right) # Right Left
            return self._leftRotate(node) # catch either Right Left or Left Left

        return node

    def __delitem__(self, key):
        self.root = self._delete(self.root, key)

    # Recursive function to delete a node with
    # given key from subtree with given node.
    # It returns node of the modified subtree.
    def _delete(self, node, key):

        if not node: return node # not found

        # find node with key
        elif key < node.value:
            node.left = self._delete(node.left, key)
        elif key > node.value:
            node.right = self._delete(node.right, key)
        else: # equal, it is found
            if node.left is None: # case of only right child
                return node.right # replace node with child

            elif node.right is None: # case of only left child
                return node.left # replace node with child

            # case of two children
            succ = self.getMinValueNode(node.right) # successor of node
            node.key = succ.key # copy
            node.value = succ.value
            node.right = self._delete(node.right, succ.key)  # promote succ key

        # If the tree has only one node,
        # simply return it
        if node is None:
            return node

        return self._adjust_node(node, key)

    def _find_node(self, node, key):
        if not node:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find_node(node.left, key)
        return self._find_node(node.right, key)

    def __getItem__(self, key):
        node = self._find_node(self.root, key)
        return node.value if node else None

    def get(self,key): return self[key]

    def __contains__(self, key):
        return self[key] is not None

    @staticmethod
    def _height(node): return node.height if node else 0

    def _balance(self, node): return self._height(node.left) - self._height(node.right)

    #     a                             b
    #      \                          // \      < update link //
    #       b     Left Rotate(a)      a   c
    #     /  \   - - - - - - - ->     \\        < update link \\
    #    x    c                        x

    def _leftRotate(self, a):
        b = a.right
        x = b.left   # get x
        b.left = a   # update b left link point to a
        a.right = x  # replace a.right link to now point to x

        # Update heights
        a.height = 1 + max(self._height(a.left), self._height(a.right))
        b.height = 1 + max(self._height(b.left), self._height(b.right))

        # Return the new root node
        return b


    #         a                          b
    #        /                          / \\      < update link \\
    #       b     Right Rotate(a)      c   a
    #     /  \   - - - - - - - ->         //      < update link //
    #    c    x                          x

    def _rightRotate(self, a):
        b = a.left
        x = b.right  # get x d
        b.right = a  # update b right link point to a
        a.left = x  # replace c left link to now point to x

        # Update heights
        a.height = 1 + max(self._height(a.left), self._height(a.right))
        b.height = 1 + max(self._height(b.left), self._height(b.right))

        # Return the new root node
        return b

    def _get_min_node(self, node):
        if node is None or node.left is None:
            return node
        return self._get_min_node(node.left)

    def _iterate_nodes(self):
        node = self.root
        if not node: return None
        for n in node:
            yield n

    def _is_balanced(self):
        for n in self._iterate_nodes():
            bal = self._balance(n)
            if bal not in (1,0,-1): return False
        return True

    def __iter__(self): # client iterate in order key/values
        for n in self._iterate_nodes():
            yield n.key, n.value


def main(): # run tests on this class
    print("tests")
    tree = AVLTree()
    tree.put(10)
    tree.put(20)
    tree.put(30)
    tree.put(40)
    tree.put(5)
    tree.put(6)
    assert tree._is_balanced()
    assert [5,6,10,20,30,40] == [ n[0] for n in tree ]


if __name__ == "__main__":
    # execute only if run as a script
    main()