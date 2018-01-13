from avl_tree import AVLTree, AVLNode

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


def tree_from_keys(l): # return new tree from iter of keys
    tree = AVLTree()
    for key in l: tree[key] = None
    return tree


def tree_from_dict(d): # create tree from dict key/values
    tree = AVLTree()
    for key in d.keys():
        tree[key] = d[key]
    return tree


def is_balanced(tree): # used to check balance of tree
    for node in tree.root:
        if tree._balance(node) not in (1, 0, -1): return False
    return True


def tree_to_dict(tree): # convert tree to dict
    d = {}
    for k,v in tree:
        d[k] = v
    return d