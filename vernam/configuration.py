# -*- coding: utf-8 -*-

# Here will be functions


def readconfig(args):
    """
    This function reads configuration file and combine it with parameters from
    console input to generate the configuration list.

     Parameters
    ----------
    keyfile (-k) : str, path to a file containing the random data used as key
        for the cipher.
    optimization (-o) :  You can choose one of the following methods:
        lz4 : Will compress input or decompres output with lz4, this has a great
            performance with all file types.
        base32 : Old style. key will be read as 4 bits blocks, input and output
            will use  RFC 4648 Base 32 encoding. This is useful when one of
            the sides is doing the maths by hand.
        raw  : default operation mode, will use 1KB pages for ciphering
    """
    #TODO
