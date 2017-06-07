import unittest
import util

class SimplisticTest(unittest.TestCase):

    def test_getKeyHashFromKey(self):
        assert  util.hashSum("AAA") ==  "8d708d18b54df3962d696f069ad42dad7762b5d4d3c97ee5fa2dae0673ed46545164c078b8db3d59c4b96020e4316f17bb3d91bf1f6bc0896bbe75416eb8c385"

if __name__ == '__main__':
    unittest.main()
