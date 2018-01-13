class AVLNode:  # node class hidden from client

    def __init__(self, key, value = 0):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 # bottom starts at height of 1

    def __iter__(self):  # this is a generator functions due to the yields
        """The standard inorder traversal of a binary tree for self that returns nodes"""
        if self.left:
            for node in self.left:  yield node  # generate left node
        yield self  # generate center node
        if self.right:
            for node in self.right: yield node  # generate right node

    def __repr__(self): return f"Node( k={self.key}, v={self.value}, h={self.height})"

# AVLTree implement a binary search AVL Tree with the following interface functions:
#         __contains__(y)     y in t
#         __getitem__(y)      t[y]
#         __setitem__(k, v)   t[k] = v
#         __delitem__(k)      del t[k]
#         __len__()           len(t)
#         __iter__()          for k,v in t: - in-order traversal

class AVLTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self): return self.size
    
    def __setitem__(self, key, value): self.root = self._put(self.root, key, value)

    def _put(self, node, key, value):  # recursive _put follow tree down till place found for new node
        if not node: # place found, return new node
            self.size += 1
            return AVLNode(key, value)

        elif key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else: # equal
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
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else: # equal, it is found
            if node.left is None: # case of only right child
                return node.right # replace node with child

            elif node.right is None: # case of only left child
                return node.left # replace node with child

            # case of two children
            succ = self._get_min_node(node.right) # successor of node
            node.key = succ.key # copy
            node.value = succ.value
            node.right = self._delete(node.right, succ.key)  # delete succ succ key
            return node

        # If the tree has only one node, simply return it
        if node is None: return node

        return self._adjust_node(node, key)

    def _find_node(self, node, key):
        if not node:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find_node(node.left, key)
        return self._find_node(node.right, key)

    def __getitem__(self, key):
        node = self._find_node(self.root, key)
        return node.value if node else None

    def __contains__(self, key): return self[key] is not None
    
    def _height(self,node): return node.height if node else 0
    
    def _balance(self, node): return self._height(node.left) - self._height(node.right)

    def _leftRotate(self, a): #                                  a                    b
        b = a.right  #                                            \    Left         // \    < update link //
        x = b.left  #                                              b   Rotate(a)   a   c
        b.left = a   # update b left link point to a             /  \   - - ->     \\       < update link \\
        a.right = x  # replace a.right link to now point to     x    c              x
        a.height = 1 + max(self._height(a.left), self._height(a.right))
        b.height = 1 + max(self._height(b.left), self._height(b.right))
        return b

    def _rightRotate(self, a):  #                                     a                b
        b = a.left  #                                                /    Right       / \\  < update link \\
        x = b.right  #                                              b     Rotate(a)  c   a
        b.right = a  # update b right link point to a             /  \   - - ->     //      < update link //
        a.left = x  # replace c left link to now point to x      c    x            x
        a.height = 1 + max(self._height(a.left), self._height(a.right))
        b.height = 1 + max(self._height(b.left), self._height(b.right))
        return b

    def _get_min_node(self, node):
        return self._get_min_node(node.left) if node.left else node

    def __iter__(self): # client iterate in order key/values
        if not self.root: return
        for n in self.root: yield (n.key, n.value)

## end AVLTree

#### TEST it ###

def is_balanced(tree): # used to check balance of tree
    for node in tree.root:
        if tree._balance(node) not in (1, 0, -1): return False
    return True

def print_tree(tree):
    blank = AVLNode("  ")
    space_geometry = ((0, 2), (2, 6), (6, 14), (14, 30), (30, 62))  # floor ->  (pre-spaces, join space)
    th = tree.root.height
    nextQ = [ tree.root]
    i = 0
    while True:
        if i > 5: # too big
            print("... to many levels to list")
            break
        floor = th - i - 1
        if floor < 0: return
        print(" "*(space_geometry[floor][0]), end='')
        line = (" "*(space_geometry[floor][1])).join([ "%2s"%(x.key)for x in nextQ])
        print(line)
        i += 1
        fromQ = nextQ
        nextQ = []
        for node in fromQ:
            if node.left is not None:
                nextQ.append(node.left)
            else:
                nextQ.append(blank)
            if node.right is not None:
                nextQ.append(node.right)
            else:
                nextQ.append(blank)



def main(): # run tests on AVLTree for contains, getitem, setitem, delitem, len, and iter operators

    tree = AVLTree()
    tree[10] = 1 # build a tree
    tree[20] = 2
    tree[30] = 3
    tree[40] = 4
    tree[5] = 5
    tree[6] = 6
    print_tree(tree)
    assert is_balanced(tree)
    assert [(5,5),(6,6),(10,1),(20,2),(30,3),(40,4)] == [ n for n in tree ]
    assert len(tree) == 6
    l = [ 10,20,30,40,5,6]
    for k in l:
        print('delete', k)
        print_tree(tree)
        del tree[k]
        #tree[k] = 'replaced'


if __name__ == "__main__":
    # execute only if run as a script
    main()
