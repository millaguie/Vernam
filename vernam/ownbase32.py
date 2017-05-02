# -*- coding: utf-8 -*-

import string
def ownBase32():
    """
    This function just return the ownBase32 alphabet
    """
    oB32 =  {i:x for i, x in enumerate(string.ascii_lowercase, 1)}
    # Like in old typewriters, l will work as 1 and o will work as 0
    # because of little name space z will work as 2
    oB32[27] = "3"
    # because of little name space, a will work as 4 and s will work as 5
    oB32[28] = "6"
    oB32[29] = "7"
    oB32[30] = "8"
    oB32[31] = "9"
    oB32[32] = " "
    return oB32

def string2ownBase32(characters):
    """
    This function convert a string to ownBase32. Just give a string as parameter
    and it will retun a string converted by best effor to ownBase32

     Parameters
    -----------
    characters  : String to convert
    """
    # bla bla bla
    oB32 = ownBase32();
    print(type(inBase32))
    for c in characters.lower():
        if c is "1":
            c = "l"
        elif c is "2":
            c = "z"
        elif c is "0":
            c = "o"
        elif c is "4":
            c = "a"
        elif c is "5":
            c = "s"
        if c in oB32.values():
            c = oB32.values().index(c)+1
        else:
            print("{} is not an ob32 printable, using space as {}".format(c,c))
            c = 32
        inBase32 = inBase32 + oB32[c]
    return inBase32

def getFromByte(twobytes):
    """
    This function convert a (un)signed 16 bits integer to three ob32 characters.
    It will be used to convert key to ob32, in order to waste as little key as
    possible all reads will be in done in 16 bits and 15 bits will be
    used (3 groups of 5)

    This fuction will return an array of three ob32 characters.

     Parameters
    -----------
    data  : binary raw data
    """
    one = int('{:016b}'.format(twobytes)[1:6],2)
    two = int('{:016b}'.format(twobytes)[6:11],2)
    three = int('{:016b}'.format(twobytes)[11:16],2)
    return one,two,three
