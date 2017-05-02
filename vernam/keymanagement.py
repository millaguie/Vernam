import sys
import os
import yaml
import uuid
import hashlib
import ownbase32
from struct import unpack


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

def catalog(keyPath, l2r, force = False):
    """
    This function catalogs a new keyfile by creating a description yaml file

     Parameters
    -----------
    keyPath : path to the file used as key
    l2r     : True if using left to right key reading
    force   : Force yaml file overwrite
    """

    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if os.path.exists(keyPath+".yaml") and force is False:
        sys.exit("A description file already exists, won't create a new one")
    genUUID = uuid.uuid4()
    hashSum = getKeyHashFromKey(keyPath)
    if l2r is False:
        startByte = os.path.getsize(keyPath)
    else:
        startByte = 0
    configFile = open(keyPath+".yaml", "w")
    fileName = os.path.basename(keyPath)
    configFile.write("---\n"+
                    "keyfile: {}\n".format(fileName) +
                    "UUID: {}\n".format(str(genUUID)) +
                    "sha512: {}\n".format(hashSum) +
                    "l2r: {}\n".format(l2r) +
                    "nextByte: {}".format(startByte)
                    )

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

def getKeyBytes(keyPath, size, l2r=None, offset=None, waste=False):
    """
    This function read bytes from key and return them. If reading in l2r mode
    function will return bytes reordered to r2l. If waste is true, will mark all
    readebytes as used into key yaml file, when using waste offset may not be
    set, as we will start in the last byte used.

     Parameters
    -----------
    keyPath : path to the file used as key
    size    : size in bytes to read
    l2r     : True if using left to right key reading
    offset  : where in key start to read
    waste   : Mark read bytes as used and update key config
    """

    keySize= os.path.getsize(keyPath)

    if offset is not None and offset > keySize:
        print("offset: {}, keysize: {}".format(offset, keySize))
        sys.exit("key is smaller than key offset")

    keyConfig = yaml.load(open(keyPath+".yaml",'r'))
    if offset is None and waste is True:
        offset = keyConfig["nextByte"]
        l2r = keyConfig["l2r"]

    elif l2r is None:
        l2r = not keyConfig["l2r"]

    if l2r is True and offset + size >= keySize:
        sys.exit("Do not have enough unused key to complete this action")

    if l2r is False:
        if offset - size <= 0:
            sys.exit("Do not have enough unused key to complete this action")
        else:
            print ("keysize: {}, offset: {}, size: {}".format(keySize,offset,size))
            print("{} of {} bytes will be in use after this action".format(
                keySize - (offset - size), keySize))
    else:
        if offset + size > keySize:
            sys.exit("Do not have enough unused key to complete this action")
        else:
            print("{} of {} bytes will be in use after this action".format(
                offset + size,keySize))
    print ("OFFSET LECTURA: {}".format(offset))
    if l2r is True:
        try:
            inputFile = open(keyPath, 'rb')
            inputFile.seek(offset)
            key=inputFile.read(size)
            print("L2R")
        except:
            raise
    else:
        try:
            inputFile = open(keyPath, 'rb')
            inputFile.seek(offset - size)
            keyR=inputFile.read(size)
            offset = offset - size
            key = keyR[::-1]
            print("R2L")
        except:
            raise
    if waste is True:
        keyConfig["nextByte"] = offset
        with open(keyPath+".yaml", 'w') as keyConfigFile:
            keyConfigFile.write( yaml.dump(keyConfig, default_flow_style=False))
    return key, offset, l2r

def printable2file(keyPath,outputPath,force=False):
    if os.path.exists(outputPath) and force is False:
        sys.exit("Will not overwrite output file without force")
    file = open(outputPath,"w")
    file.write(printable(keyPath))
    file.close()

def printable(keyPath):
    """
    This function returns a string with the printable version of the key
    """
    #ownBase32 = dict.fromkeys(string.ascii_lowercase, 0)
    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if not os.path.exists(keyPath+".yaml"):
        sys.exit("Could not find decriptor for key, please catalog it before")
    s=str()
    try:
        ob32=ownbase32.ownBase32()
        file = open(keyPath, 'rb')
        byte =  unpack(">H",file.read(2))[0]
        while byte:
            usable = ownbase32.getFromByte(byte)
            s+="{}{}{}".format(ob32[usable[0]+1],ob32[usable[1]+1],
                                   ob32[usable[2]+1])
            byte =  unpack(">h",file.read(2))[0]
    except:
        raise
    return s
