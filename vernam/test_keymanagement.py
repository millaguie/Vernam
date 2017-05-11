import unittest

import keymanagement
import tempfile
import os

class SimplisticTest(unittest.TestCase):

    def test_getKeyHashFromKey(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write("just a test")
        f.close
        assert keymanagement.getKeyHashFromKey(f.name) == "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
        os.unlink(f.name)



if __name__ == '__main__':
    unittest.main()
