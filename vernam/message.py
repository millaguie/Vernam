import sys
import os
import uuid
import hashlib
import keymanagement
import array
from struct import pack
from struct import unpack
from util import hashSum

global L2RHEADER
L2RHEADER = bytearray([222, 210, 7, 163, 100]);
global R2LHEADER
R2LHEADER = bytearray([222, 210, 7, 163, 101]);
global max_int64
max_int64 = 0xFFFFFFFFFFFFFFFF



def readMessage(keyPath, messagePath):
        """
        This function reads a message (envelope) in the defined format, and
        returns the data inside the file, offset in key file and the raw data.
        It checks that message key UUID matchs defined key UUID, also checks
        consistency of message via sha512

         Parameters
        -----------
        keyPath     : path to the file used as key
        messagePath : path to the file used to read the message
        """
    keyUUID = keymanagement.getCatalogUUID(keyPath)

    with open(messagePath, "rb") as file:
        header = unpack(">iiiii", file.read(5*4))
        print(header)
        msgSize = unpack(">Q",file.read(8))[0]
        print(msgSize)
        offsetInKey = unpack(">Q",file.read(8))
        #Hay que convertir los dos enteros de 64 bits en uno de 128
        msgKeyUUID1, msgKeyUUID2 = unpack(">QQ",file.read(16))
        print(type(msgKeyUUID1))
        msgKeyUUID = (msgKeyUUID1 << 64) | msgKeyUUID2
        if keyUUID.int != msgKeyUUID:
            raise ValueError("Bad Key UUID")
        message = unpack(">{}s".format(msgSize), file.read(msgSize))[0]
        print(message)
        msgFileHash = file.read()
        if hashSum(message) != msgFileHash.encode("hex"):
            raise ValueError("Failed to hash message ")
        return offsetInKey, message




def writeMessage(keyPath, messagePath, ciphered, offsetInKey, leftToRigth=True):
    """
    This function Writes a message in the defined format.
    Format of the message is as follows
    * Header 20 bytes, as defined, two options, one for R2L and another for L2R
      it's on the todo.
    * Message size in 8 bytes (64 bits) integer
    * Key UUID used in message 16 bytes
    * Message it's self, it's size is defined in the second field
    * Hash of the message, 32 bytes a sha512

     Parameters
    -----------
    keyPath     : path to the file used as key
    messagePath : path to the file used to store the message
    ciphered    : ciphered data to write in the file (envelope)
    offsetInKey : need to jump to this byte in key to decrypt
    leftToRigth : Indicates if the key will need to be readed R2L or L2R (true)
    """

    keyUUID = keymanagement.getCatalogUUID(keyPath)
    msgSize = len(ciphered)
    print(msgSize)
    print(ciphered)
    with open(messagePath, "wb") as file:
        # Write file header right to left or left to right
        file.write(pack(">iiiii", *R2LHEADER))
        # Write menssage size in bytes
        file.write(pack(">Q",msgSize))
        # Write offset in key to decrypt message
        file.write(pack(">Q",offsetInKey))
        # Write Key UUID for easy key management
        file.write(pack('>QQ', (keyUUID.int >> 64) & max_int64,
                        keyUUID.int & max_int64))
        #write message it's self
        file.write(pack(">{}s".format(msgSize), ciphered))
        # Get hash for the message
        msgHash = hashSum(ciphered)
        msgHashint = msgHash.decode("hex")
        msgHashArray = bytearray(msgHashint)
        hashSize = msgHashArray.count(msgHashArray)
        file.write(msgHashArray)
