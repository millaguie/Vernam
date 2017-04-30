# -*- coding: utf-8 -*-
import sys
import os
from lz4 import compressHC, uncompress
import tempfile
import keymanagement
import message


def encrypt(inputPath,keyPath,outputPath, force=False, mode="raw"):
    """
    This function performs vernam encryption using an input file and a key,
    result is stored in output file.

     parameters
    -----------
    inputPath  : path to the file used as input
    keyPath    : path to the file used as key
    outputPath : path to the file used as output
    mode       : working mode, Modes are:
        * raw: traditional way
        * lz4e: all input data will be compressed via lz4
        * lz4d: all output data will be decompress via lz4
        * base32: all data will be converted to base32 beforehand
    """
    if not os.path.exists(inputPath):
        sys.exit("Could not find input file {}".format(inputPath))
    if os.path.exists(outputPath):
        if force is False:
            sys.exit("output file exists, won't overwrite {}".format(
                                                            outputPath))
        else:
            sys.stderr.write("Output file will be overwritten as requested.\n")
    if not os.path.exists(keyPath):
        sys.exit("key file not found\n")
    try:
        if mode == "lz4":
            inputfile=bytearray(compressHC((open(inputPath, 'rb')).read()))
        else:
            inputfile=bytearray(open(inputPath, 'rb').read())
    except:
        raise
    size=len(inputfile)
    key, offset, l2r = keymanagement.getKeyBytes(keyPath, size, waste=True)
    key = bytearray(key)
    message.writeMessage(keyPath,outputPath,vernam(inputfile, key), offset,
                        l2r=l2r)

def decrypt(inputPath,keyPath,outputPath, force=False, mode="raw"):
    """
    This function performs vernam decryption using an input file and a key,
    result is stored in output file.

     parameters
    -----------
    inputPath  : path to the file used as input
    keyPath    : path to the file used as key
    outputPath : path to the file used as output
    mode       : working mode, Modes are:
        * raw: traditional way
        * lz4e: all input data will be compressed via lz4
        * lz4d: all output data will be decompress via lz4
        * base32: all data will be converted to base32 beforehand
    """
    if not os.path.exists(inputPath):
        sys.exit("Could not find input file {}".format(inputPath))
    if os.path.exists(outputPath):
        if force is False:
            sys.exit("output file exists, won't overwrite {}".format(
                                                            outputPath))
        else:
            sys.stderr.write("Output file will be overwritten as requested.\n")
    offset, l2r, inputCryp = message.readMessage(keyPath,inputPath)
    size=len(inputCryp)
    offset=offset[0]
    print("offset: {} - {}, l2r: {}".format(offset,type(offset), l2r))
    key = keymanagement.getKeyBytes(keyPath, size, offset=offset, l2r=l2r)
    key=bytearray(key[0])
    clear = vernam(bytearray(inputCryp),key)
    if mode == "lz4":
        clear=uncompress(str(clear))
    open(outputPath, 'wb').write(clear)


def vernam(one, two):
    """
    This function performs vernam (de)ciphering with two bytearrays, order
    doesn't matter as it is a pure xor fuction. function will return xored
    bytearray

    parameters
    ----------
    one, two : Two arraybytes to perform vernam cipher.
    """
    if len(one) is not len(two):
        sys.exit("arraybytes length differs, can not vernam with them")
    size=len(one)
    outputfile = bytearray(size)
    for i in range(size):
        outputfile[i] = one[i] ^ two[i]
    return outputfile


#### Pasar lo de abajo a arriba con las dos opciones cifrar y descifrar
def vernamold(inputPath, keyPath, outputPath, action, force=False, mode="raw"):
    """
    This function performs vernam cipher with using an input file and a key,
    result is saved in the output file.

     parameters
    -----------
    inputPath  : path to the file used as input
    keyPath    : path to the file used as key
    outputPath : path to the file used as output
    mode       : working mode, Modes are:
        * raw: traditional way
        * lz4e: all input data will be compressed via lz4
        * lz4d: all output data will be decompress via lz4
        * base32: all data will be converted to base32 beforehand
    """

    if not os.path.exists(keyPath):
        sys.exit("Could not find key {}".format(keyPath))
    if not os.path.exists(inputPath):
        sys.exit("Could not find input file {}".format(inputPath))
    if os.path.exists(outputPath):
        if force is False:
            sys.exit("output file exists, won't overwrite {}".format(
                                                            outputPath))
        else:
            sys.stderr.write("Output file will be overwritten as requested.\n")

    try:
        if mode == "lz4" and action is "encrypt":
            inputfile=bytearray(compressHC((open(inputPath, 'rb')).read()))
        else:
            inputfile=bytearray(open(inputPath, 'rb').read())
    except:
        raise

    if action is "encrypt":
        size=len(inputfile)
        key=bytearray(getKeyBytes(keyPath, size, waste=True))
    else:
        offset, l2r, message = readMessage(keyPath, inputfile)
        size=len(message)
        key = bytearray(getKeyBytes(keyPath, size, l2r=l2r, offset=offset))

    outputfile = bytearray(size)
    for i in range(size):
        outputfile[i] = inputfile[i] ^ key[i]
    if mode == "lz4d":
        outputfile=uncompress(str(outputfile))
    open(outputPath, 'wb').write(outputfile)
