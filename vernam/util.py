# -*- coding: utf-8 -*-
"""
Util module handles all unspecific utilities
"""

import hashlib


def hashSum(data):
    """
    This function helps to create hash resumes for many parts of the code. It
    uses sha512 as hashing algorithm

    Args:
        * data : data to be hashsed

    Returns:
        Hash in hexdigest format
    """
    hasher = hashlib.sha512()
    for b in data:
        hasher.update(b)
    return hasher.hexdigest()
