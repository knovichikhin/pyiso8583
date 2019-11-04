__all__ = ['decode', 'DecodeError']


class DecodeError(ValueError):
    r"""Subclass of ValueError that describes ISO8583 decoding error.

    Attributes
    ----------
    msg : str
        The unformatted error message
    s : bytes or bytearray
        The ISO8583 byte array being parsed
    doc : dict
        Partially decoded Python represination of ISO8583 byte array
    pos : int
        The start index of ISO8583 byte array where parsing failed
    field : int or str
        The ISO8583 field where parsing failed
    """

    def __init__(self, msg: str, s: bytes or bytearray,
                 doc: dict, pos: int, field: int or str):
        errmsg = f"{msg}: field {field} pos {pos}"
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.s = s
        self.doc = doc
        self.field = field
        self.pos = pos

    def __reduce__(self):
        return self.__class__, (
            self.msg, self.s, self.doc, self.pos, self.field)


def decode(s: bytes or bytearray, spec: dict) -> dict:
    r"""Deserialize a bytes or bytearray instance containing
    ISO8583 data to a Python dict.

    Parameters
    ----------
    s : bytes or bytearray
        Byte array containing encoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    dict
        Decoded ISO8583 data

    Raises
    ------
    DecodeError
        An error decoding ISO8583 bytearray
    TypeError
        `s` must be a bytes or bytearray instance

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default
    >>> s = b'0200\x40\x10\x10\x00\x00\x00\x00\x00161234567890123456123456111'
    >>> d = iso8583.decode(s, spec=default)
    """
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError(f'the ISO8583 data must be bytes or bytearray, '
                        f'not {s.__class__.__name__}')

    d = {
        'bm': set()
    }
    idx = 0

    idx = _decode_header(s, d, idx, spec)
    idx = _decode_type(s, d, idx, spec)
    idx = _decode_bitmaps(s, d, idx, spec)

    # Create the variable in case the bitmap set is empty
    # and there is extra data afterwards.
    # Set field to the last mandatory one: primary bitmap.
    f = 'p'

    for f in sorted(d['bm']):
        # Secondary bitmap is already decoded in _decode_bitmaps
        if f == 1:
            continue
        idx = _decode_field(s, d, idx, f, spec)

    if idx != len(s):
        raise DecodeError(
            "Extra data after last field", s, d, idx, f) from None

    return d

#
# Private interface
#


def _decode_header(s: bytes or bytearray, d: dict,
                   idx: int, spec: dict) -> int:
    r"""Decode ISO8583 header data if present.

    Parameters
    ----------
    s : bytes or bytearray
        Byte array containing encoded ISO8583 data
    d : dict
        Dict containing decoded ISO8583 data
    idx : int
        Current index in ISO8583 byte array
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    int
        Index in ISO8583 byte array where parsing of the header ended

    Raises
    ------
    DecodeError
        An error decoding ISO8583 bytearray.
    """
    flen = spec['h']['max_len']
    if flen == 0:
        return idx

    d['h'] = {
        'e': {
            'len': b'',
            'data': bytes(s[idx:idx + flen])
        },
        'd': ''
    }

    if len(s[idx:idx + flen]) != flen:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + flen])} bytes, " +
            f"expecting {flen}", s, d, idx, 'h') from None

    try:
        if spec['h']['data_encoding'] == 'b':
            d['h']['d'] = s[idx:idx + flen].hex().upper()
        else:
            d['h']['d'] = s[idx:idx + flen].decode(spec['h']['data_encoding'])
    except Exception as e:
        raise DecodeError(f"Failed to decode ({e})", s, d, idx, 'h') from None

    return idx + flen


def _decode_type(s: bytes or bytearray, d: dict, idx: int, spec: dict) -> int:
    r"""Decode ISO8583 message type.

    Parameters
    ----------
    s : bytes or bytearray
        Byte array containing encoded ISO8583 data
    d : dict
        Dict containing decoded ISO8583 data
    idx : int
        Current index in ISO8583 byte array
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    int
        Index in ISO8583 byte array where parsing of message type ended

    Raises
    ------
    DecodeError
        An error decoding ISO8583 bytearray.
    """
    if spec['t']['data_encoding'] == 'b':
        flen = 2
    else:
        flen = 4
    d['t'] = {
        'e': {
            'len': b'',
            'data': bytes(s[idx:idx + flen])
        },
        'd': ''
    }

    if len(s[idx:idx + flen]) != flen:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + flen])} bytes, " +
            f"expecting {flen}", s, d, idx, 't') from None

    try:
        if spec['t']['data_encoding'] == 'b':
            d['t']['d'] = s[idx:idx + flen].hex().upper()
        else:
            d['t']['d'] = s[idx:idx + flen].decode(spec['t']['data_encoding'])
    except Exception as e:
        raise DecodeError(f"Failed to decode ({e})", s, d, idx, 't') from None

    return idx + flen


def _decode_bitmaps(s: bytes or bytearray, d: dict,
                    idx: int, spec: dict) -> int:
    r"""Decode ISO8583 primary and secondary bitmaps.

    Parameters
    ----------
    s : bytes or bytearray
        Byte array containing encoded ISO8583 data
    d : dict
        Dict containing decoded ISO8583 data
    idx : int
        Current index in ISO8583 byte array
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    int
        Index in ISO8583 byte array where parsing of bitmaps ended

    Raises
    ------
    DecodeError
        An error decoding ISO8583 bytearray.
    """
    # Parse primary bitmap
    if spec['p']['data_encoding'] == 'b':
        flen = 8
    else:
        flen = 16
    d['p'] = {
        'e': {
            'len': b'',
            'data': bytes(s[idx:idx + flen])
        },
        'd': ''
    }

    if len(s[idx:idx + flen]) != flen:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + flen])} bytes, " +
            f"expecting {flen}", s, d, idx, 'p') from None

    try:
        if spec['p']['data_encoding'] == 'b':
            d['p']['d'] = s[idx:idx + flen].hex().upper()
            bm = s[idx:idx + flen]
        else:
            d['p']['d'] = s[idx:idx + flen].decode(spec['p']['data_encoding'])
            bm = bytes.fromhex(d['p']['d'])
    except Exception as e:
        raise DecodeError(f"Failed to decode ({e})", s, d, idx, 'p') from None

    for i, byte in enumerate(bm):
        for bit in range(1, 9):
            if byte >> (8 - bit) & 1:
                d['bm'].add(i * 8 + bit)

    idx += flen

    # Check if secondary bitmap is not required
    if 1 not in d['bm']:
        return idx

    # Parse secondary bitmap
    if spec[1]['data_encoding'] == 'b':
        flen = 8
    else:
        flen = 16
    d[1] = {
        'e': {
            'len': b'',
            'data': bytes(s[idx:idx + flen])
        },
        'd': ''
    }

    if len(s[idx:idx + flen]) != flen:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + flen])} bytes, " +
            f"expecting {flen}", s, d, idx, 1) from None

    try:
        if spec[1]['data_encoding'] == 'b':
            d[1]['d'] = s[idx:idx + flen].hex().upper()
            bm = s[idx:idx + flen]
        else:
            d[1]['d'] = s[idx:idx + flen].decode(spec[1]['data_encoding'])
            bm = bytes.fromhex(d[1]['d'])
    except Exception as e:
        raise DecodeError(f"Failed to decode ({e})", s, d, idx, 1) from None

    for i, byte in enumerate(bm):
        for bit in range(1, 9):
            if byte >> (8 - bit) & 1:
                d['bm'].add(64 + i * 8 + bit)

    return idx + flen


def _decode_field(s: bytes or bytearray, d: dict,
                  idx: int, f: int, spec: dict) -> int:
    r"""Decode ISO8583 individual fields.

    Parameters
    ----------
    s : bytes or bytearray
        Byte array containing encoded ISO8583 data
    d : dict
        Dict containing decoded ISO8583 data
    idx : int
        Current index in ISO8583 byte array
    f : int
        Field number to be decoded
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    int
        Index in ISO8583 byte array where parsing of the field ended

    Raises
    ------
    DecodeError
        An error decoding ISO8583 bytearray.
    """
    len_type = spec[f]['len_type']
    d[f] = {
        'e': {
            'len': bytes(s[idx:idx + len_type]),
            'data': b''
        },
        'd': ''
    }

    if len(s[idx:idx + len_type]) != len_type:
        raise DecodeError(
            f"Field length is {len(s[idx:idx + len_type])} bytes wide, " +
            f"expecting {len_type}", s, d, idx, f) from None

    # Parse field length if present.
    # For fixed-length fields max_len is the length.
    if len_type == 0:
        flen = spec[f]['max_len']
    else:
        try:
            if spec[f]['len_encoding'] == 'b':
                flen = int(s[idx:idx + len_type].hex(), 10)
            else:
                flen = int(s[idx:idx + len_type].decode(
                                                spec[f]['len_encoding']), 10)
        except Exception as e:
            raise DecodeError(
                f"Failed to decode length ({e})", s, d, idx, f) from None

    if flen > spec[f]['max_len']:
        raise DecodeError(
            f"Field data is {flen} bytes, " +
            f"larger than maximum {spec[f]['max_len']}",
            s, d, idx, f) from None

    idx += len_type

    # Do not parse zero-length field
    if flen == 0:
        return idx

    # Parse field data
    d[f]['e']['data'] = bytes(s[idx:idx + flen])

    if len(d[f]['e']['data']) != flen:
        raise DecodeError(
            f"Field data is {len(d[f]['e']['data'])} bytes, expecting {flen}",
            s, d, idx, f) from None

    try:
        if spec[f]['data_encoding'] == 'b':
            d[f]['d'] = d[f]['e']['data'].hex().upper()
        else:
            d[f]['d'] = d[f]['e']['data'].decode(spec[f]['data_encoding'])
    except Exception as e:
        raise DecodeError(f"Failed to decode ({e})", s, d, idx, f) from None

    return idx + flen
