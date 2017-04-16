# -*- coding: utf-8 -*-
import sys
import os
from lz4 import compressHC, uncompress
import tempfile


"""main file"""

def vernam(inputpath, keypath, outputpath, force=False, mode="raw"):
    """
    This function performs vernam cipher with using an input file and a key,
    result is saved in the output file.

     parameters
    -----------
    inputpath  : path to the file used as input
    keypath    : path to the file used as key
    outputpath : path to the file used as output
    mode       : working mode, Modes are:
        * raw: traditional way
        * lz4e: all input data will be compressed via lz4
        * lz4d: all output data will be decompress via lz4
        * base32: all data will be converted to base32 beforehand
    """

    if not os.path.exists(keypath):
        sys.exit("Could not find key {}".format(keypath))
    if not os.path.exists(inputpath):
        sys.exit("Could not find input file {}".format(inputpath))
    if os.path.exists(outputpath):
        if force is False:
            sys.exit("output file exists, won't overwrite {}".format(
                                                            outputpath))
        else:
            sys.stderr.write("Output file will be overwritten as requested.\n")

    try:
        if mode == "lz4e":
            inputfile=bytearray(compressHC((open(inputpath, 'rb')).read()))
        else:
            inputfile=bytearray(open(inputpath, 'rb').read())
        keyfile=bytearray(open(keypath, 'rb').read())
    except:
        raise
    size=len(inputfile)
    outputfile = bytearray(size)
    for i in range(size):
        outputfile[i] = inputfile[i] ^ keyfile[i]
    if mode == "lz4d":
        outputfile=uncompress(str(outputfile))
    open(outputpath, 'wb').write(outputfile)
