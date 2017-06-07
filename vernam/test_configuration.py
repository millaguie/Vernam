import unittest
import tempfile
import os
import configuration

class SimplisticTest(unittest.TestCase):

    def test_readConfig(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        configuration.readConfig(f.name+"11")
        assert os.path.exists(f.name+"11")
        c = configuration.readConfig(f.name+"11")
        assert c["keyfile"] == "defaultrawfile.rnd"
        f.close
        os.unlink(f.name)
        os.unlink(f.name+"11")




if __name__ == '__main__':
    unittest.main()
