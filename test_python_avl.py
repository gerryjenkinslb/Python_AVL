from python_avl import AVLTree
import unittest
import random

class AVLTreeTests(unittest.TestCase):
    def setUp(self):
        self.avl = AVLTree()

    kv_set1 = ((50, 'a'), (10, 'b'), (70, 'c'), (30, 'd'), (85, 'd'), (15, 'e'), (45, 'f'))

    def assert_key_values(self, kvs):
        for k, v in kvs:
            self.avl.put(k, v)
            d[k] = v
        for k, v in kvs:
            assert self.avl.get(k) == v

    def test_put(self):
        self.avl[25] = 'g'
        assert self.avl[25] == 'g'

    def testSize(self):
        for k, v in self.kv_set1:
            self.avl.put(k, v)
        assert self.avl.length() == 7

    def testLarge(self):
        print('.testing a large random tree')
        i = 0
        randList = []
        while i < 1000:
            nrand = random.randrange(1, 10000000)
            if nrand not in randList:
                randList.append(nrand)
                i += 1
        # print(randList)

        for n in randList:  # build tree
            self.avl.put(n, n)

        sortList = randList[:]
        sortList.sort()
        random.shuffle(randList)
        for n in randList:  # original list randomized
            # delete n from sortList and Tree and check matches
            sortList.remove(n)
            self.avl.delete(n)
            if len(sortList) > 1:
                assert list(self.avl) == sortList
        assert self.avl.root == None

    def testManyTrees(self):
        print('** testing many trees of sizes 10 to 75')
        for _ in range(100):
            n = random.randrange(1, 75)
            ordered = list(range(1, n + 1))
            shuffled = ordered[:]
            random.shuffle(shuffled)
            for e in shuffled: self.avl.put(e, e)
            shuffled2 = ordered[:]
            random.shuffle(shuffled2)
            for e in shuffled2:
                self.avl.delete(e)
                ordered.remove(e)
                if len(self.avl) > 0:
                    if list(self.avl) != ordered:
                        print(f'tree   : {list(self.avl)}')
                        print(f'ordered: {ordered}')
                        assert (list(self.avl) == ordered)
            assert self.avl.root == None and len(self.avl) == 0

    def testIter(self):
        print('** testing iteration')
        import random
        i = 0
        randList = []
        while i < 300:
            nrand = random.randrange(1, 10000)
            if nrand not in randList:
                randList.append(nrand)
                i += 1
        for n in randList:
            self.avl.put(n, n)
        sortList = randList[:]
        sortList.sort()

        i = 0
        for j in self.avl:
            assert j == sortList[i]
            i += 1

    def testBadDelete(self):
        self.avl.put(10, 10)
        with self.assertRaises(KeyError):
            self.avl.delete(5)
        self.avl.delete(10)
        with self.assertRaises(KeyError):
            self.avl.delete(5)


if __name__ == '__main__':
    import platform

    print(platform.python_version())
    unittest.main()
