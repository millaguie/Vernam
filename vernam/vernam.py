# -*- coding: utf-8 -*-
"""
This is the core module form verna encryption. It manages all
Vernam encryption/decription stuff
"""
from __future__ import print_function
import sys
import os
import math
from lz4 import compressHC, uncompress
import tempfile
import keymanagement
import message
import ownbase32


def encrypt(inputPath, keyPath, outputPath, force=False, mode="raw"):
    """
    This function performs vernam encryption using an input file and a key,
    result is stored in output file.

    Args:
        * inputPath  : path to the file used as input
        * keyPath    : path to the file used as key
        * outputPath : path to the file used as output
        * mode       : working mode, Modes are:
            * raw: traditional way
            * lz4: all input data will be compressed via lz4
            * human: all data will be converted to ownBase32 beforehand
    Returns:
        None
    """
    if not os.path.exists(inputPath):
        print("Could not find input file {}".format(inputPath),file=sys.stderr)
        sys.exit(10)
    if os.path.exists(outputPath):
        if force is False:
            print("output file exists, won't overwrite {}".format(
                outputPath),file=sys.stderr)
            sys.exit(11)
        else:
            sys.stderr.write("Output file will be overwritten as requested.\n")
    if not os.path.exists(keyPath):
        print("Could not find key {}".format(keyPath),file=sys.stderr)
        sys.exit(103)
    try:
        if mode == "lz4":
            inputfile = bytearray(compressHC((open(inputPath, 'rb')).read()))
        elif mode == "human":
            inputfile = ownbase32.string2ownBase32(open(inputPath, 'rb').read())
        else:
            inputfile = bytearray(open(inputPath, 'rb').read())
    except:
        raise
    if mode == "human":
        # An even number of bytes is needed for tranformation.
        size = int(math.ceil(((len(inputfile)+1 / 3)/2.)) * 2)
    else:
        size = len(inputfile)

    key, offset, l2r = keymanagement.getKeyBytes(keyPath, size, waste=True)
    key = bytearray(key)
    if mode == "human":
        key = keymanagement.ba2humankeyba(key)
        if len(key) != len(inputfile):
            key = key[:len(inputfile)-len(key)]
        inputfile = ownbase32.string2ob32ba(inputfile)
        ciphered = vernam(inputfile, key)
        message.writeHumanMessage(outputPath, ciphered, offset * 3)
    else:
        message.writeMessage(keyPath, outputPath, vernam(inputfile, key), offset,
                             l2r=l2r)

def decrypt(inputPath, keyPath, outputPath, force=False, mode="raw"):
    """
    This function performs vernam decryption using an input file and a key,
    result is stored in output file.

    Args:
        * inputPath  : path to the file used as input
        * keyPath    : path to the file used as key
        * outputPath : path to the file used as output
        * mode       : working mode, Modes are:
            * raw: traditional way
            * lz4: all input data will be decompressed via lz4
            * human: all data will be converted to ownBase32 beforehand
    Returns:
        None
    """
    if not os.path.exists(inputPath):
        print("Could not find input file {}".format(inputPath),file=sys.stderr)
        sys.exit(10)
    if os.path.exists(outputPath):
        if force is False:
            print("output file exists, won't overwrite {}".format(
                outputPath),file=sys.stderr)
            sys.exit(11)
        else:
            sys.stderr.write("Output file will be overwritten as requested.\n")
    if mode == "human":
        seek, inputCryp = message.readHumanMessage(inputPath)
        offset = seek / 3
        size = int(math.ceil(((len(inputCryp)+1 / 3)/2.)) * 2)
        l2r = True
    else:
        offset, l2r, inputCryp = message.readMessage(keyPath, inputPath)
        offset = offset[0]
        size = len(inputCryp)
    print("offset: {} - {}, l2r: {}".format(offset, type(offset), l2r))
    key = keymanagement.getKeyBytes(keyPath, size, offset=offset, l2r=l2r)
    key = bytearray(key[0])
    if mode == "human":
        key = keymanagement.ba2humankeyba(key)
        if len(key) != len(inputCryp):
            key = key[:len(inputCryp)-len(key)]
        inputCryp = ownbase32.string2ob32ba(inputCryp)
        clear = ownbase32.ba2ob32string(vernam(inputCryp, key))
        print(clear)
    else:
        clear = vernam(bytearray(inputCryp), key)
    if mode == "lz4":
        clear = uncompress(str(clear))
    open(outputPath, 'wb').write(clear)


def vernam(one, two):
    """
    This function performs vernam (de)ciphering with two bytearrays, order
    doesn't matter as it is a pure xor fuction. function will return xored
    bytearray

    Args:
        * one, two : Two arraybytes to perform vernam cipher.
    Returns:
        A bytearray with Vernam results
    """
    if len(one) != len(two):
        print("arraybytes length differs, can not vernam with them",file=sys.stderr)
        sys.exit(5)
    size = len(one)
    outputfile = bytearray(size)
    for i in range(size):
        outputfile[i] = one[i] ^ two[i]
    return outputfile
