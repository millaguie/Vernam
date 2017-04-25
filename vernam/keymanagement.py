import sys
import os
import yaml
import uuid
import hashlib

def getKeyHashFromKey(keyPath):
    """
    This function get the hashcode for the key, it returns a hash.

     parameters
    -----------
    keyPath : path to the file used as key
    """
    print("Generating hash of key, this might take some time")
    BLOCKSIZE = 65536
    hasher = hashlib.sha512()
    with open(keyPath, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()

def catalog(keyPath):
    """
    This function catalogs a new keyfile by creating a description yaml file

     Parameters
    -----------
    keyPath : path to the file used as key
    """

    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if os.path.exists(keyPath+".yaml"):
        sys.exit("A description file already exists, won't create a new one")
    genUUID = uuid.uuid4()
    hashSum = getKeyHashFromKey(keyPath)
    configFile = open(keyPath+".yaml", "w")
    fileName = os.path.basename(keyPath)
    configFile.write("---\n"+
                    "keyfile: {}\n".format(fileName) +
                    "UUID: {}\n".format(str(genUUID)) +
                    "sha512: {}".format(hashSum))

def checkCatalogUUID(keyPath, binaryUUID=None, asciiUUID=None):
    """
    Function to check key UUID and UUID used in message, returns True or False

     Parameters
    -----------
    keyPath     : path to the file used as key
    binaryUUID  : optional, message UUID in binary format
    asciiUUID   : optional, message UUID in string format
    """
    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if not os.path.exists(keyPath+".yaml"):
        sys.exit("Could not find decriptor for key, please catalog it before")

    keyConfig = {}
    keyConfig = yaml.load(open(keyPath+".yaml",'r'))
    confUUID = uuid.UUID("urn:uuid:"+keyConfig["UUID"])
    if asciiUUID is not None:
        messageUUID = uuid.UUID(asciiUUID)
    elif binaryUUID is not None:
        messageUUID = uuid.UUID(binaryUUID)
    else:
        return False
    if messageUUID.int == confUUID.int:
        return True
    else:
        return False

def getCatalogUUID(keyPath):
    """
    Function to get UUID from key config file, returns an UUID object.

     Parameters
    -----------
    keyPath     : path to the file used as key

    """

    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if not os.path.exists(keyPath+".yaml"):
        sys.exit("Could not find decriptor for key, please catalog it before")

    keyConfig = {}
    keyConfig = yaml.load(open(keyPath+".yaml",'r'))
    return uuid.UUID("urn:uuid:"+keyConfig["UUID"])
