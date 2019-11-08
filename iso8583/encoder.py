__all__ = ['encode', 'EncodeError']


class EncodeError(ValueError):
    r"""Subclass of ValueError that describes ISO8583 encoding error.

    Attributes
    ----------
    msg : str
        The unformatted error message
    doc : dict
        Partially encoded Python represination of ISO8583 byte array
    field : int or str
        The ISO8583 field where parsing failed
    """

    def __init__(self, msg: str, doc: dict, field: int or str):
        errmsg = f"{msg}: field {field}"
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc = doc
        self.field = field

    def __reduce__(self):
        return self.__class__, (self.msg, self.doc, self.field)


def encode(d: dict, spec: dict) -> bytearray:
    r"""Serialize Python dict containing ISO8583 data to a bytearray.

    Parameters
    ----------
    d : dict
        Dict containing decoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytearray
        Encoded ISO8583 data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray
    TypeError
        `d` must be a dict instance

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default
    >>> d = {}
    >>> iso8583.add_field(d, 't', '0210')
    >>> iso8583.add_field(d, 39, '00')
    >>> iso8583.encode(d, spec=default)
    bytearray(b'0210\x00\x00\x00\x00\x02\x00\x00\x0000')
    """
    if not isinstance(d, dict):
        raise TypeError(f'the ISO8583 data must be dict, '
                        f'not {d.__class__.__name__}')

    s = bytearray()
    s += _encode_header(d, spec)
    s += _encode_type(d, spec)
    s += _encode_bitmaps(d, spec)

    for f in sorted(d['bm']):
        # Secondary bitmap is already encoded in _encode_bitmaps
        if f == 1:
            continue
        s += _encode_field(d, f, spec)

    return s

#
# Private interface
#


def _encode_header(d: dict, spec: dict) -> bytes:
    r"""Encode ISO8583 header data if present from `d['h']['d']`.

    Parameters
    ----------
    d : dict
        Dict containing decoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 data containing header

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """
    if spec['h']['max_len'] == 0:
        return b''

    # Header data is a required field.
    try:
        d['h']['d']
    except KeyError:
        raise EncodeError(f"Define d['h']['d']", d, 'h') from None

    # Initialize the dictionary.
    # d['h']['d'] is provided.
    d['h']['e'] = {
        'len': b'',
        'data': b''
    }

    try:
        if spec['h']['data_encoding'] == 'b':
            d['h']['e']['data'] = bytes.fromhex(d['h']['d'])
        else:
            d['h']['e']['data'] = d['h']['d'].encode(
                                                spec['h']['data_encoding'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", d, 'h') from None

    if len(d['h']['e']['data']) != spec['h']['max_len']:
        raise EncodeError(
            f"Field data is {len(d['h']['e']['data'])} bytes, " +
            f"expecting {spec['h']['max_len']}",
            d, 'h') from None

    return d['h']['e']['data']


def _encode_type(d: dict, spec: dict) -> bytes:
    r"""Encode ISO8583 message type from `d['t']['d']`.

    Parameters
    ----------
    d : dict
        Dict containing decoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 data containing message type

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """
    # Message type is a required field.
    try:
        d['t']['d']
    except KeyError:
        raise EncodeError(f"Define d['t']['d']", d, 't') from None

    # Initialize the dictionary.
    # d['t']['d'] is provided.
    d['t']['e'] = {
        'len': b'',
        'data': b''
    }

    if spec['t']['data_encoding'] == 'b':
        flen = 2
    else:
        flen = 4

    try:
        if spec['t']['data_encoding'] == 'b':
            d['t']['e']['data'] = bytes.fromhex(d['t']['d'])
        else:
            d['t']['e']['data'] = d['t']['d'].encode(
                                                spec['t']['data_encoding'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", d, 't') from None

    if len(d['t']['e']['data']) != flen:
        raise EncodeError(
            f"Field data is {len(d['t']['e']['data'])} " +
            f"bytes, expecting {flen}",
            d, 't') from None

    return d['t']['e']['data']


def _encode_bitmaps(d: dict, spec: dict) -> bytes:
    r"""Encode ISO8583 primary and secondary bitmap from `d['bm']`.

    Parameters
    ----------
    d : dict
        Dict containing decoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 data containing primary and/or secondary bitmaps

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """
    # BM list is a required field. Primary and secondary bitmaps
    # will be created out of it.
    try:
        d['bm']
    except KeyError:
        raise EncodeError(f"Define d['bm']", d, 'p') from None

    # Initialize the dictionary.
    d['p'] = {
        'e': {
            'len': b'',
            'data': b''
        },
        'd': ''
    }

    # Provided bitmap must consist of 1-128 field range
    if not d['bm'].issubset(range(1, 129)):
        raise EncodeError(
            "Bitmap contains fields outside 1-128 range", d, 'bm') from None

    # Disable secondary bitmap if no 65-128 fields are present
    if d['bm'].isdisjoint(range(65, 129)):
        d['bm'].discard(1)
    else:
        d['bm'].add(1)

    # Turn bitmap bits of associated field on.
    # There is no need to sort this set because the code below will
    # figure out appropriate byte/bit for each field.
    s = bytearray(
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    for f in d['bm']:
        # Fields start at 1. Make them zero-bound for easier conversion.
        f -= 1

        # Place this particular field in a byte where it belongs.
        # E.g. field 8 belongs to byte 0, field 121 belongs to byte 15.
        byte = int(f / 8)

        # Determine bit to enable. ISO8583 bitmaps are left-aligned.
        # E.g. fields 1, 9, 17, etc. enable bit 7 in bytes 0, 1, 2, etc.
        bit = 7 - (f - byte * 8)
        s[byte] |= 1 << bit

    # Encode primary bitmap
    d['p']['d'] = s[0:8].hex()

    try:
        if spec['p']['data_encoding'] == 'b':
            d['p']['e']['data'] = bytes(s[0:8])
        else:
            d['p']['e']['data'] = d['p']['d'].encode(
                                                spec['p']['data_encoding'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", d, 'p') from None

    # Encode secondary bitmap if enabled.
    if 1 not in d['bm']:
        return d['p']['e']['data']

    # Initialize the dictionary.
    # Secondary bitmap is created from d['bm'] every time.
    d[1] = {
        'e': {
            'len': b'',
            'data': b''
        },
        'd': s[8:16].hex()
    }

    try:
        if spec[1]['data_encoding'] == 'b':
            d[1]['e']['data'] = s[8:16]
        else:
            d[1]['e']['data'] = d[1]['d'].encode(spec[1]['data_encoding'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", d, 1) from None

    return d['p']['e']['data'] + d[1]['e']['data']


def _encode_field(d: dict, f: int, spec: dict) -> bytes:
    r"""Encode ISO8583 individual field from `d[field]['d']`.

    Parameters
    ----------
    d : dict
        Dict containing decoded ISO8583 data
    f : int
        Field number to be encoded
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 data containing field data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """
    # Field data is required when enabled in the bitmap.
    try:
        d[f]['d']
    except KeyError:
        raise EncodeError(f"Define d[{f}]['d']", d, f) from None

    # Initialize the dictionary.
    # d[f]['d'] is provided.
    d[f]['e'] = {
        'len': b'',
        'data': b''
    }

    # Encode field data
    try:
        if spec[f]['data_encoding'] == 'b':
            d[f]['e']['data'] = bytes.fromhex(d[f]['d'])
        else:
            d[f]['e']['data'] = d[f]['d'].encode(spec[f]['data_encoding'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", d, f) from None

    len_type = spec[f]['len_type']
    flen = len(d[f]['e']['data'])

    # Fixed length field.
    if len_type == 0:
        if flen != spec[f]['max_len']:
            raise EncodeError(
                f"Field data is {flen} bytes, expecting {spec[f]['max_len']}",
                d, f) from None

        d[f]['e']['len'] = b''
        return d[f]['e']['data']

    # Continue with variable length field.

    if flen > spec[f]['max_len']:
        raise EncodeError(
            f"Field data is {flen} bytes, " +
            f"larger than maximum {spec[f]['max_len']}",
            d, f) from None

    # Encode field length
    try:
        if spec[f]['len_encoding'] == 'b':
            # Odd field length type is not allowed for purpose of string
            # to BCD translation. Double it, e.g.:
            # BCD LVAR length \x09 must be string '09'
            # BCD LLVAR length \x99 must be string '99'
            # BCD LLLVAR length \x09\x99 must be string '0999'
            # BCD LLLLVAR length \x99\x99 must be string '9999'
            d[f]['e']['len'] = bytes.fromhex('{:0{len_type}d}'.format(
                flen, len_type=len_type * 2))
        else:
            d[f]['e']['len'] = bytes('{:0{len_type}d}'.format(
                flen, len_type=len_type), spec[f]['len_encoding'])
    except Exception as e:
        raise EncodeError(f"Failed to encode length ({e})", d, f) from None

    return d[f]['e']['len'] + d[f]['e']['data']
