# -*- coding: utf-8 -*-

# Here will be functions

def readconfig(args):
    """
    This function reads configuration file and combine it with parameters from
    console input to generate the configuration list.

      Parameters
    ----------
    sequence : str, Sequence, or 1D np.ndarray (np.uint8 or '\|S1')
        Characters representing the DNA sequence itself.
    metadata : dict, optional
        Arbitrary metadata which applies to the entire sequence.
    positional_metadata : Pandas DataFrame consumable, optional
        Arbitrary per-character metadata. For example, quality data from
        sequencing reads. Must be able to be passed directly to the Pandas
        DataFrame constructor.
    lowercase : bool or str, optional
        If ``True``, lowercase sequence characters will be converted to
        uppercase characters in order to be valid IUPAC DNA characters. If
        ``False``, no characters will be converted. If a str, it will be
        treated as a key into the positional metadata of the object. All
        lowercase characters will be converted to uppercase, and a ``True``
        value will be stored in a boolean array in the positional metadata
        under the key.
    validate : bool, optional
        If ``True``, validation will be performed to ensure that all sequence
        characters are in the IUPAC DNA character set. If ``False``, validation
        will not be performed. Turning off validation will improve runtime
        performance. If invalid characters are present, however, there is
        **no guarantee that operations performed on the resulting object will
        work or behave as expected.** Only turn off validation if you are
        certain that the sequence characters are valid. To store sequence data
        that is not IUPAC-compliant, use ``Sequence``.
    Attributes
    ----------
    values
    metadata
    positional_metadata
    alphabet
    gap_chars
    default_gap_char
    definite_chars
    degenerate_chars
    degenerate_map
    complement_map
    See Also
    --------
    RNA
    GrammaredSequence
    Notes
    -----
    Subclassing is disabled for DNA, because subclassing makes
    it possible to change the alphabet, and certain methods rely on the
    IUPAC alphabet. If a custom sequence alphabet is needed, inherit directly
    from ``GrammaredSequence``.
    References
    ----------
    .. [1] Nomenclature for incompletely specified bases in nucleic acid
       sequences: recommendations 1984.
       Nucleic Acids Res. May 10, 1985; 13(9): 3021-3030.
       A Cornish-Bowden
    Examples
    --------
    >>> from skbio import DNA
    >>> DNA('ACCGAAT')
    DNA
    --------------------------
    Stats:
        length: 7
        has gaps: False
        has degenerates: False
        has definites: True
        GC-content: 42.86%
    --------------------------
    0 ACCGAAT
    Convert lowercase characters to uppercase:
    >>> DNA('AcCGaaT', lowercase=True)
    DNA
    --------------------------
    Stats:
        length: 7
        has gaps: False
        has degenerates: False
        has definites: True
        GC-content: 42.86%
    --------------------------
    0 ACCGAAT

    """

    #TODO
