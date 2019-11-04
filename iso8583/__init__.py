r"""`ISO8583 <https://en.wikipedia.org/wiki/ISO_8583>`_
is an international standard for financial transaction card originated
interchange messaging. It is the ISO standard for systems that exchange
electronic transactions initiated by cardholders using payment cards.

:mod:`iso8583` serializes and deserializes ISO8583 data between a ``bytes`` or
``bytearray`` instance containing ISO8583 data and a Python ``dict``.
"""

__version__ = '1.0.0'
__all__ = [
    'add_field', 'del_field', 'pp',
    'decode', 'DecodeError',
    'encode', 'EncodeError',
]
__author__ = 'Konstantin Novichikhin <konstantin.novichikhin@gmail.com>'

from iso8583.decoder import decode, DecodeError
from iso8583.encoder import encode, EncodeError


def add_field(d: dict, field: int or str, val: str) -> None:
    r"""Add or override field and its value to ISO8583 dictionary.

    Parameters
    ----------
    d : dict
        Dict containing ISO8583 data
    field : int or str
        Key of a field to be added
    val : str
        Value of a field to be added

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default
    >>> s = b'0200\x40\x10\x10\x10\x00\x00\x00\x00161234567890123456123456111D00000000'
    >>> d = iso8583.decode(s, spec=default)
    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20, 28]
    t   Message Type                        : [0200]
    p   Bitmap, Primary                     : [4010101000000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    28  Amount, Transaction Fee             : [D00000000]
    >>> iso8583.add_field(d, 't', '0210')
    >>> iso8583.add_field(d, 39, '00')
    >>> iso8583.encode(d, spec=default)
    bytearray(b'0210@\x10\x10\x10\x02\x00\x00\x00161234567890123456123456111D0000000000')
    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20, 28, 39]
    t   Message Type                        : [0210]
    p   Bitmap, Primary                     : [4010101002000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    28  Amount, Transaction Fee             : [D00000000]
    39  Response Code                       : [00]
    """
    if 'bm' not in d:
        d['bm'] = set()

    if isinstance(field, int):
        d['bm'].add(field)

    d[field] = {
        'e': {
            'len': b'',
            'data': b''
        },
        'd': val
    }


def del_field(d: dict, field: int or str) -> dict:
    r"""Delete field from ISO8583 dictionary.

    Parameters
    ----------
    d : dict
        Dict containing ISO8583 data
    field : int or str
        Key of a field to be added

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default
    >>> s = b'0200\x40\x10\x10\x10\x00\x00\x00\x00161234567890123456123456111D00000000'
    >>> d = iso8583.decode(s, spec=default)
    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20, 28]
    t   Message Type                        : [0200]
    p   Bitmap, Primary                     : [4010101000000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    28  Amount, Transaction Fee             : [D00000000]
    >>> iso8583.del_field(d, 28)
    {'e': {'len': b'', 'data': b'D00000000'}, 'd': 'D00000000'}
    >>> iso8583.encode(d, spec=default)
    bytearray(b'0200@\x10\x10\x00\x00\x00\x00\x00161234567890123456123456111')
    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20]
    t   Message Type                        : [0200]
    p   Bitmap, Primary                     : [4010100000000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    """
    try:
        d['bm'].discard(field)
    except KeyError:
        pass
    return d.pop(field, None)


def pp(d: dict, spec: dict, desc_width: int = 36) -> None:
    r"""Pretty Print Python dict containing ISO8583 data.

    Parameters
    ----------
    d : dict
        Dict containing ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See iso8583.specs module for examples.
    desc_width : int, optional
        Width of field description that's printed (default 36).
        Specify 0 to print no descriptions.

    Notes
    -----
    To display correct data :func:`iso8583.pp` should be used after
    :func:`iso8583.encode` or :func:`iso8583.decode`.

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default
    >>> s = b'0200\x40\x10\x10\x10\x00\x00\x00\x00161234567890123456123456111D00000000'
    >>> d = iso8583.decode(s, spec=default)
    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20, 28]
    t   Message Type                        : [0200]
    p   Bitmap, Primary                     : [4010101000000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    28  Amount, Transaction Fee             : [D00000000]
    """
    print("bm  {desc: <{desc_width}}: {val}".format(
        desc="Enabled Fields"[:desc_width], desc_width=desc_width,
        val=sorted(d['bm'])))

    # Message header is optional
    if spec['h']['max_len'] > 0:
        print("h   {desc: <{desc_width}}: [{val}]".format(
            desc=spec['h']['desc'][:desc_width], desc_width=desc_width,
            val=d['h']['d']))

    print("t   {desc: <{desc_width}}: [{val}]".format(
        desc=spec['t']['desc'][:desc_width], desc_width=desc_width,
        val=d['t']['d']))
    print("p   {desc: <{desc_width}}: [{val}]".format(
        desc=spec['p']['desc'][:desc_width], desc_width=desc_width,
        val=d['p']['d']))

    for f in sorted(d['bm']):
        if spec[f]['len_type'] == 0:
            print("{index:<3d} {desc: <{desc_width}}: [{val}]".format(
                index=f, desc=spec[f]['desc'][:desc_width],
                desc_width=desc_width, val=d[f]['d']))
        else:
            print("{index:<3d} {desc: <{desc_width}}: {length:0{length_type}d} [{val}]".format(
                index=f, desc=spec[f]['desc'][:desc_width],
                desc_width=desc_width, length=len(d[f]['d']),
                length_type=spec[f]['len_type'], val=d[f]['d']))
