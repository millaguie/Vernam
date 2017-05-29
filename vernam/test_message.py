import unittest
import tempfile
import os
import message
import keymanagement
import configuration

def createFakeKey():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write("just a test")
    f.close
    return f

def clearFakeKey(f):
    os.unlink(f.name)
    os.unlink(f.name+".yaml")

class SimplisticTest(unittest.TestCase):

    def test_writeMessage(self):
        f = createFakeKey()
        m = tempfile.NamedTemporaryFile(delete=False)
        keymanagement.catalog(f.name, True, force = True)
        m.close()

        configuration.readConfig(f.name+"11")
        assert os.path.exists(f.name+"11")
        c = configuration.readConfig(f.name+"11")
        assert c["keyfile"] == "defaultrawfile.rnd"
        f.close
        message.writeMessage(f.name, m.name, "hello", 0, True)
        assert os.path.exists(m.name)
        os.unlink(f.name)
        os.unlink(f.name+"11")
        os.unlink(m.name)

    def test_readMessage(self):
        f = createFakeKey()
        m = tempfile.NamedTemporaryFile(delete=False)
        keymanagement.catalog(f.name, True, force = True)
        m.close()

        configuration.readConfig(f.name+"11")
        assert os.path.exists(f.name+"11")
        c = configuration.readConfig(f.name+"11")
        assert c["keyfile"] == "defaultrawfile.rnd"
        f.close
        message.writeMessage(f.name, m.name, "hello", 0, True)
        assert os.path.exists(m.name)
        resp = message.readMessage(f.name,m.name)
        assert resp[0][0]==0
        assert resp[1]==True
        assert resp[2]=="hello"
        os.unlink(f.name)
        os.unlink(f.name+"11")
        os.unlink(m.name)




if __name__ == '__main__':
    unittest.main()
