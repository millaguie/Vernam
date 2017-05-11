import unittest

import keymanagement
import tempfile
import os
from uuid import UUID

def createFakeKey():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write("just a test")
    f.close
    return f

def clearFakeKey(f):
    os.unlink(f.name)
    os.unlink(f.name+".yaml")


class SimplisticTest(unittest.TestCase):


    def test_getKeyHashFromKey(self):
        f = createFakeKey()
        assert keymanagement.getKeyHashFromKey(f.name) == "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
        os.unlink(f.name)


    def test_catalog(self):
        f = createFakeKey()
        keymanagement.catalog(f.name, True, force = True)
        assert os.path.exists(f.name+".yaml")
        clearFakeKey(f)

    def test_getCatalogUUID(self):
        f = createFakeKey()
        keymanagement.catalog(f.name, True, force = True)
        assert UUID(keymanagement.getCatalogUUID(f.name).urn[9:], version=4)
        clearFakeKey(f)


    def test_getKeyBytes(self):
        f = createFakeKey()
        f.write("0"*10000)
        keymanagement.catalog(f.name, True, force = True)
        k = keymanagement.getKeyBytes(f.name, 1, l2r=True, waste=True)
        assert 'j' == k[0]
        clearFakeKey(f)

    def test_printable(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        b = bytearray([150,150,150,150,150,0,0,0,0])
        f.write(b)
        f.close()
        keymanagement.catalog(f.name, True, force = True)
        assert "gvx6ml6rb" == keymanagement.printable(f.name)
        clearFakeKey(f)




if __name__ == '__main__':
    unittest.main()
