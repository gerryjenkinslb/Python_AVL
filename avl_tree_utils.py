from avl_tree import AVLTree, AVLNode

def tree_height(node):
    return 1 + max( 0 if node.left is None else tree_height(node.left),
                    0 if node.right is None else tree_height(node.right))

def print_tree(root):
    # spacing[i] -> ( prespace, join space ), i is distance from bottom level 0 is bottom
    spacing = ((0, 1), (3, 6), (9, 16), (19, 37), (39, 77), (79, 157))

    def nstr(node): return f'{node.key:2d},{node.height}' if node else '  _ '

    height = tree_height(root)
    max = (2 ** height) -1
    btree = [None]*(max+1)
    btree[1] = root # root

    def left(i): return btree[i * 2]
    def right(i): return btree[i * 2 + 1]
    def parent(i): return btree[i//2]

    for i in range(2,max+1):
        if parent(i):
            if i % 2 == 0: btree[i] = parent(i).left
            else: btree[i] = parent(i).right

    stree = [nstr(node) for node in btree ]
    print(stree[1:])
    seg = 1
    from_bottom = height-1
    while from_bottom >= 0:
        row = stree[seg:seg*2] # row to print
        srow = (" " * spacing[from_bottom][1]).join(row)
        srow = " " * spacing[from_bottom][0] + srow
        print(srow)
        from_bottom -= 1
        seg = seg*2

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
