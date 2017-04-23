import sys
import os
import yaml
import uuid
import hashlib


def catalog(keyPath):
    """
    This function catalogs a new keyfile by creating a description yaml file

     parameters
    -----------
    keyPath : path to the file used as key
    """

    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if os.path.exists(keyPath+".yaml"):
        sys.exit("A description finle already exists, won't create a new one")
    genUUID=uuid.uuid4()
    print("Generating hash of key, this might take some time")
    BLOCKSIZE = 65536
    hasher = hashlib.sha512()
    with open(keyPath, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    hashSum=hasher.hexdigest()
    configFile = open(keyPath+".yaml", "w")
    fileName=os.path.basename(keyPath)
    configFile.write("---\n"+
                    "keyfile: {}\n".format(fileName) +
                    "UUID: {}\n".format(str(genUUID)) +
                    "sha512: {}".format(hashSum))
