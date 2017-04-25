import sys
import os
import uuid
import hashlib
import keymanagement
import array
from struct import pack

global L2RHEADER
L2RHEADER = bytearray([222, 210, 7, 163, 100]);
global R2LHEADER
R2LHEADER = bytearray([222, 210, 7, 163, 101]);
global max_int64
max_int64 = 0xFFFFFFFFFFFFFFFF



def readMessage(keyPath, messagePath):



    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
        # a, b     = struct.unpack('>QQ', packed)
        # unpacked = (a << 64) | b


def writeMessage(keyPath, messagePath, ciphered, offsetInKey, leftToRigth=True):

    print(keyPath)
    keyUUID = keymanagement.getCatalogUUID(keyPath)
    msgSize = ciphered.count(ciphered)
    with open(messagePath, "wb") as file:
        # Write file header right to left or left to right
        file.write(pack(">IIIII", *R2LHEADER))
        # Write menssage size in bytes
        file.write(pack(">Q",msgSize))
        # Write offset in key to decrypt message
        file.write(pack(">Q",offsetInKey))
        # Write Key UUID for easy key management
        file.write(pack('>QQ', (keyUUID.int >> 64) & max_int64,
                        keyUUID.int & max_int64))
        #write message it's self
        file.write(pack(">I%ds" % (msgSize,), msgSize, ciphered))
        # Prpeare hash for the message
        hasher = hashlib.sha512()
        for b in ciphered:
            hasher.update(b)
        msgHash = hasher.hexdigest()

        #Write message hash
        print(msgHash)
        msgHashint = msgHash.decode("hex")
        msgHashArray = bytearray(msgHashint)
        hashSize = msgHashArray.count(msgHashArray)
        file.write(msgHashArray)
