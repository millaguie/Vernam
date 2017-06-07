# -*- coding: utf-8 -*-
"""
Message class holds all methods to work with message files
"""
import sys
import os
import array
from struct import pack
from struct import unpack
import uuid
import hashlib
import keymanagement
import yaml
import ownbase32
from util import hashSum

L2RHEADER = bytearray([222, 210, 7, 163, 100])
R2LHEADER = bytearray([222, 210, 7, 163, 101])



def readMessage(keyPath, messagePath):
    """
    This function reads a message (envelope) in the defined format, and
    returns the data inside the file, offset in key file and the reading mode
    for the key.
    It checks that message key UUID matchs defined key UUID, also checks
    consistency of message via sha512

    Args:
        * keyPath: path to the file used as key
        * messagePath: path to the file used to read the message

    Returns:
        Data inside the envelope
    """
    keyUUID = keymanagement.getCatalogUUID(keyPath)
    with open(messagePath, "rb") as file:
        header = bytearray(unpack(">iiiii", file.read(5*4)))
        if header == L2RHEADER:
            L2R = True
        elif header == R2LHEADER:
            L2R = False
            print("AQUI")
        else:
            raise ValueError("File format unknown")
        msgSize = unpack(">Q", file.read(8))[0]
        offsetInKey = unpack(">Q", file.read(8))
        msgKeyUUID1, msgKeyUUID2 = unpack(">QQ", file.read(16))
        msgKeyUUID = (msgKeyUUID1 << 64) | msgKeyUUID2
        if keyUUID.int != msgKeyUUID:
            raise ValueError("Bad Key UUID")
        message = unpack(">{}s".format(msgSize), file.read(msgSize))[0]
        msgFileHash = file.read()
        if hashSum(message) != msgFileHash.encode("hex"):
            raise ValueError("Failed to hash message ")
        print("LECTURA -> offset: {}, L2R: {}".format(offsetInKey, L2R))
        return offsetInKey, L2R, message

def writeHumanMessage(outputPath, message, seek):
    """
    This function writes a message in the human friendly format.
    Format of the message is as follows:

    offset#message

    Args:
        * outputPath: path to the new message file
        * message: message to write in the file
        * seek: offset in key to decrypt message

    Returns:
        None
    """
    with open(outputPath, "w") as f:
        f.write("{}#{}".format(seek, ownbase32.ba2ob32string(message)))

def readHumanMessage(inputPath):
    """
    This function reads a message in the human friendly format.
    Function will return two elements, key offset and the
    encrypted message.

    Args:
        * inputPath: path to the message file to read

    Returns:
        An array:
            * Offset in the key
            * Encrypted message
    """
    with open(inputPath, "r") as f:
        s = f.read()
    s = s.split("#")
    return int(s[0]), s[1]



def writeMessage(keyPath, messagePath, ciphered, offsetInKey, l2r=True):
    """
    This function Writes a message in the defined format. Format of the message is as follows:
        * Header 20 bytes, as defined, two options, one for R2L and another for L2R it's on the todo.
        * Message size in 8 bytes (64 bits) integer
        * Key UUID used in message 16 bytes
        * Message it's self, it's size is defined in the second field
        * Hash of the message, 32 bytes a sha512

    Args:
        * keyPath: path to the file used as key
        * messagePath: path to the file used to store the message
        * ciphered: ciphered data to write in the file (envelope)
        * offsetInKey: need to jump to this byte in key to decrypt
        * l2r: Indicates if the key will need to be readed R2L or L2R (True)
    Returns:
        None
    """

    keyUUID = keymanagement.getCatalogUUID(keyPath)
    msgSize = len(ciphered)

    with open(messagePath, "wb") as file:
        max_int64 = 0xFFFFFFFFFFFFFFFF
        # Write file header right to left or left to right
        if l2r is True:
            file.write(pack(">iiiii", *L2RHEADER))
        else:
            file.write(pack(">iiiii", *R2LHEADER))
            offsetInKey = offsetInKey + msgSize
        # Write menssage size in bytes
        file.write(pack(">Q", msgSize))
        # Write offset in key to decrypt message
        file.write(pack(">Q", offsetInKey))
        # Write Key UUID for easy key management
        file.write(pack('>QQ', (keyUUID.int >> 64) & max_int64,
                        keyUUID.int & max_int64))
        #write message it's self
        ciphered = str(ciphered)
        file.write(pack(">{}s".format(msgSize), ciphered))
        # Get hash for the message
        msgHash = hashSum(ciphered)
        msgHashint = msgHash.decode("hex")
        msgHashArray = bytearray(msgHashint)
        hashSize = msgHashArray.count(msgHashArray)
        print("ESCRITURA -> offset: {}, L2R: {}".format(offsetInKey, l2r) )
        file.write(msgHashArray)
