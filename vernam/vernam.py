# -*- coding: utf-8 -*-
import sys


"""main file"""

def vernam(inputpath, keypath, outputpath):
    """
    This function performs vernam cipher with using an input file and a key,
    result is saved in the output file.

     parameters
    -----------
    inputpath  : path to the file used as input
    keypath    : path to the file used as key
    outputpath : path to the file used as output
    """
    keyfile=bytearray(open(keypath, 'rb').read())
    inputfile=bytearray(open(inputpath, 'rb').read())
    size=len(inputfile)
    outputfile = bytearray(size)
    for i in range(size):
        outputfile[i] = inputfile[i] ^ keyfile[i]

    open(outputpath, 'wb').write(outputfile)
