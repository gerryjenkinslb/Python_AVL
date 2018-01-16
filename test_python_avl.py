from avl_tree import AVLTree, AVLNode
from avl_tree_utils import *

import random

def assert_true( exp, msg):
    if not exp:
        print(f'*** Test failed: {msg}')

def dict_to_sorted_pairs(d): return [ (k,d[k]) for k in sorted(d.keys())]

def test_balance1(): # test setitem, balance, iteration of tree
    # print('test inserting letters a to z')
    d = {k: i for i, k in enumerate('abcdefghijklmnopqrstuvwxyz')}
    tree = tree_from_dict(d)
    assert_true(is_balanced(tree), "tree is not balanced after inserting a-z,0-25")
    assert_true(dict_to_sorted_pairs(d) == list(tree), f"a-z,0-25 tree did not match, was {list(tree)}")

    d = {k: i for i, k in enumerate(range(100, 0, -1))}
    tree = tree_from_dict(d)
    assert_true(is_balanced(tree), "tree is not balanced after inserting a-z,0-25")
    assert_true(dict_to_sorted_pairs(d) == list(tree), f"a-z,0-25 tree did not match, was {list(tree)}")

def test_insert_remove(size): # test tree from random, delete, and rebalance, setitem with existing key
    lbase = list(range(0,size))
    random.shuffle(lbase) # randomize

    dref = {}
    tree = AVLTree()
    for key in lbase:
        v = random.choice(lbase)
        tree[key] = v
        dref[key] = v
        assert_true(dict_to_sorted_pairs(dref) == list(tree), f"random tree did not match reference")
        assert_true(is_balanced(tree), f"1 tree is not balanced after inserting {size} random keys/values")
    assert_true(dict_to_sorted_pairs(dref) == list(tree), f"random tree did not match reference")
    deleted_keys = random.sample(lbase,size//2)
    for key in deleted_keys: # delete half of original
        del tree[key]
        del dref[key]
        assert_true(is_balanced(tree), f"tree is not balanced after deleting key:{key} ")
        assert_true(dict_to_sorted_pairs(dref) == list(tree), f"random tree did not match reference")
        
def test_tree():
    test_balance1()
    test_insert_remove(500)

if __name__ == '__main__':
    test_tree()
