from avl_tree import AVLTree, AVLNode
import random

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

def assert_true( exp, msg):
    if not exp:
        print(f'*** Test failed: {msg}')

def dict_to_sorted_pairs(d): return [ (k,d[k]) for k in sorted(d.keys())]

def test_balance1(): # test setitem, balance, iteration of tree
    print('test inserting letters a to z')
    d = {k: i for i, k in enumerate('abcdefghijklmnopqrstuvwxyz')}
    tree = tree_from_dict(d)
    assert_true(is_balanced(tree), "tree is not balanced after inserting a-z,0-25")
    assert_true(dict_to_sorted_pairs(d) == list(tree), f"a-z,0-25 tree did not match, was {list(tree)}")

    d = {k: i for i, k in enumerate(range(100, 0, -1))}
    tree = tree_from_dict(d)
    assert_true(is_balanced(tree), "tree is not balanced after inserting a-z,0-25")
    assert_true(dict_to_sorted_pairs(d) == list(tree), f"a-z,0-25 tree did not match, was {list(tree)}")

def test_remove(size): # test tree from random, delete, and rebalance, setitem with existing key
    print(f"test inserting {size} random sequence from 0 to {size-1} inclusive, and then deleting half of them")
    lbase = list(range(0,size))
    random.shuffle(lbase[:]) # randomize

    dref = {}
    tree = AVLTree()
    for key in lbase:
        v = random.choice(lbase)
        tree[key] = v
        dref[key] = v
    assert_true(is_balanced(tree), f"tree is not balanced after inserting {size} random keys/values")
    assert_true(dict_to_sorted_pairs(dref) == list(tree), f"random tree did not match reference")

    deleted_keys = random.sample(lbase,size//2)
    for key in deleted_keys: # delete half of original
        del tree[key]
        del dref[key]
    assert_true(is_balanced(tree), f"tree is not balanced after inserting {size} random keys/values")
    assert_true(dict_to_sorted_pairs(dref) == list(tree), f"random tree did not match reference")






if __name__ == '__main__':
    test_balance1()
    test_remove(10000)