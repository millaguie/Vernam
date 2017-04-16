# -*- coding: utf-8 -*-
import sys
import os


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
    if not os.path.exists(keypath):
        sys.exit("Could not find key {}".format(keypath))
    if not os.path.exists(inputpath):
        sys.exit("Could not find input file {}".format(inputpath))
    if os.path.exists(outputpath):
        sys.exit("output file exists, won't overwrite {}".format(outputpath))
    try:
        keyfile=bytearray(open(keypath, 'rb').read())
        inputfile=bytearray(open(inputpath, 'rb').read())
    except:
        raise
    size=len(inputfile)
    outputfile = bytearray(size)
    for i in range(size):
        outputfile[i] = inputfile[i] ^ keyfile[i]

    open(outputpath, 'wb').write(outputfile)
