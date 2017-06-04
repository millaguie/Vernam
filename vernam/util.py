# -*- coding: utf-8 -*-
"""
Util class handles all unspecific utilities
"""

import hashlib


def hashSum(data):
    """
    This function helps to create hash resumes for many parts of the code. It
    uses sha512 as hashing algorithm

     parameters
    -----------

    data : data to be hashsed
    """
    hasher = hashlib.sha512()
    for b in data:
        hasher.update(b)
    return hasher.hexdigest()
