from typing import Tuple

__all__ = ['encode', 'EncodeError']


class EncodeError(ValueError):
    r'''Subclass of ValueError that describes ISO8583 encoding error.

    Attributes
    ----------
    msg : str
        The unformatted error message
    doc_dec : dict
        Partially decoded Python representation of ISO8583 bytes instance
    doc_enc : dict
        Partially encoded Python representation of ISO8583 bytes instance
    field : int or str
        The ISO8583 field where parsing failed
    '''

    def __init__(self, msg: str, doc_dec: dict,
                 doc_enc: dict, field: int or str):
        errmsg = f"{msg}: field {field}"
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc_dec = doc_dec
        self.doc_enc = doc_enc
        self.field = field

    def __reduce__(self):
        return self.__class__, (
            self.msg, self.doc_dec, self.doc_enc, self.field)


def encode(doc_dec: dict, spec: dict) -> Tuple[bytearray, dict]:
    r'''Serialize Python dict containing ISO8583 data to a bytearray.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    s : bytearray
        Encoded ISO8583 data
    doc_enc : dict
        Encoded Python representation of ISO8583 bytes instance

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray
    TypeError
        `doc_dec` must be a dict instance

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default
    >>> doc_dec = {}
    >>> iso8583.add_field(doc_dec, 't', '0210')
    >>> iso8583.add_field(doc_dec, '39', '00')
    >>> s, doc_enc = iso8583.encode(doc_dec, spec=default)
    >>> s
    bytearray(b'0210\x00\x00\x00\x00\x02\x00\x00\x0000')
    '''
    if not isinstance(doc_dec, dict):
        raise TypeError(f'Decoded ISO8583 data must be dict, '
                        f'not {doc_dec.__class__.__name__}')

    s = bytearray()
    doc_enc = {}
    s += _encode_header(doc_dec, doc_enc, spec)
    s += _encode_type(doc_dec, doc_enc, spec)
    s += _encode_bitmaps(doc_dec, doc_enc, spec)

    for f_id in [str(i) for i in sorted(doc_dec['bm'])]:
        # Secondary bitmap is already encoded in _encode_bitmaps
        if f_id == '1':
            continue
        s += _encode_field(doc_dec, doc_enc, f_id, spec)

    return s, doc_enc

#
# Private interface
#


def _encode_header(doc_dec: dict, doc_enc: dict, spec: dict) -> bytes:
    r'''Encode ISO8583 header data if present from `d['h']`.

    Parameters
    ----------
    doc_dec : dict
        Decoded Python representation of ISO8583 bytes instance
    doc_enc : dict
        Encoded Python representation of ISO8583 bytes instance
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
    '''

    # Header is not expected according to specifications
    if spec['h']['max_len'] <= 0:
        return b''

    # Header data is a required field.
    try:
        doc_dec['h']
    except KeyError:
        raise EncodeError(
            f"Field data is required according to specifications",
            doc_dec, doc_enc, 'h') from None

    doc_enc['h'] = {
        'len': b'',
        'data': b''
    }

    try:
        if spec['h']['data_enc'] == 'b':
            doc_enc['h']['data'] = bytes.fromhex(doc_dec['h'])
        else:
            doc_enc['h']['data'] = doc_dec['h'].encode(spec['h']['data_enc'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})",
                          doc_dec, doc_enc, 'h') from None

    if len(doc_enc['h']['data']) != spec['h']['max_len']:
        raise EncodeError(
            f"Field data is {len(doc_enc['h']['data'])} bytes, " +
            f"expecting {spec['h']['max_len']}",
            doc_dec, doc_enc, 'h') from None

    return doc_enc['h']['data']


def _encode_type(doc_dec: dict, doc_enc: dict, spec: dict) -> bytes:
    r'''Encode ISO8583 message type from `d['t']`.

    Parameters
    ----------
    doc_dec : dict
        Decoded Python representation of ISO8583 bytes instance
    doc_enc : dict
        Encoded Python representation of ISO8583 bytes instance
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
    '''

    # Message type is a required field.
    try:
        doc_dec['t']
    except KeyError:
        raise EncodeError(f"Field data is required",
                          doc_dec, doc_enc, 't') from None

    # Message type is a set length in ISO8583
    if spec['t']['data_enc'] == 'b':
        f_len = 2
    else:
        f_len = 4

    doc_enc['t'] = {
        'len': b'',
        'data': b''
    }

    try:
        if spec['t']['data_enc'] == 'b':
            doc_enc['t']['data'] = bytes.fromhex(doc_dec['t'])
        else:
            doc_enc['t']['data'] = doc_dec['t'].encode(spec['t']['data_enc'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})",
                          doc_dec, doc_enc, 't') from None

    if len(doc_enc['t']['data']) != f_len:
        raise EncodeError(
            f"Field data is {len(doc_enc['t']['data'])} " +
            f"bytes, expecting {f_len}",
            doc_dec, doc_enc, 't') from None

    return doc_enc['t']['data']


def _encode_bitmaps(doc_dec: dict, doc_enc: dict, spec: dict) -> bytes:
    r'''Encode ISO8583 primary and secondary bitmap from `d['bm']`.

    Parameters
    ----------
    doc_dec : dict
        Decoded Python representation of ISO8583 bytes instance
    doc_enc : dict
        Encoded Python representation of ISO8583 bytes instance
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
    '''

    # BM list is a required field.
    # Primary and secondary bitmaps will be created from it.
    try:
        doc_dec['bm']
    except KeyError:
        raise EncodeError(f"Field data is required",
                          doc_dec, doc_enc, 'bm') from None

    # Bitmap must consist of 1-128 field range
    if not doc_dec['bm'].issubset(range(1, 129)):
        raise EncodeError(
            "Bitmap contains fields outside 1-128 range",
            doc_dec, doc_enc, 'bm') from None

    # Eanble or disable secondary bitmap based on presence of 65-128 fields
    if doc_dec['bm'].isdisjoint(range(65, 129)):
        doc_dec['bm'].discard(1)
    else:
        doc_dec['bm'].add(1)

    doc_enc['bm'] = doc_dec['bm']

    # Turn on bitmap bits of associated fields.
    # There is no need to sort this set because the code below will
    # figure out appropriate byte/bit for each field.
    s = bytearray(
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    for f in doc_dec['bm']:
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
    doc_dec['p'] = s[0:8].hex().upper()
    doc_enc['p'] = {
        'len': b'',
        'data': b''
    }

    try:
        if spec['p']['data_enc'] == 'b':
            doc_enc['p']['data'] = bytes(s[0:8])
        else:
            doc_enc['p']['data'] = doc_dec['p'].encode(spec['p']['data_enc'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})",
                          doc_dec, doc_enc, 'p') from None

    # No need to produce secondary bitmap if it's not required
    if 1 not in doc_dec['bm']:
        return doc_enc['p']['data']

    # Encode secondary bitmap
    doc_dec['1'] = s[8:16].hex()
    doc_enc['1'] = {
        'len': b'',
        'data': b''
    }

    try:
        if spec['1']['data_enc'] == 'b':
            doc_enc['1']['data'] = s[8:16]
        else:
            doc_enc['1']['data'] = doc_dec['1'].encode(spec['1']['data_enc'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})",
                          doc_dec, doc_enc, '1') from None

    return doc_enc['p']['data'] + doc_enc['1']['data']


def _encode_field(doc_dec: dict, doc_enc: dict,
                  f_id: str, spec: dict) -> bytes:
    r'''Encode ISO8583 individual field from `d[field]`.

    Parameters
    ----------
    doc_dec : dict
        Decoded Python representation of ISO8583 bytes instance
    doc_enc : dict
        Encoded Python representation of ISO8583 bytes instance
    f_id : str
        Field ID to be encoded
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
    '''

    # Field data is required when enabled in the bitmap.
    try:
        doc_dec[f_id]
    except KeyError:
        raise EncodeError(f"Field data is required according to bitmap",
                          doc_dec, doc_enc, f_id) from None

    # Encode field data
    doc_enc[f_id] = {
        'len': b'',
        'data': b''
    }

    try:
        if spec[f_id]['data_enc'] == 'b':
            doc_enc[f_id]['data'] = bytes.fromhex(doc_dec[f_id])
        else:
            doc_enc[f_id]['data'] = doc_dec[f_id].encode(
                                                spec[f_id]['data_enc'])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})",
                          doc_dec, doc_enc, f_id) from None

    len_type = spec[f_id]['len_type']
    f_len = len(doc_enc[f_id]['data'])

    # Handle fixed length field. No need to calculate length.
    if len_type == 0:
        if f_len != spec[f_id]['max_len']:
            raise EncodeError(
                f"Field data is {f_len} bytes, " +
                f"expecting {spec[f_id]['max_len']}",
                doc_dec, doc_enc, f_id) from None

        doc_enc[f_id]['len'] = b''
        return doc_enc[f_id]['data']

    # Continue with variable length field.

    if f_len > spec[f_id]['max_len']:
        raise EncodeError(
            f"Field data is {f_len} bytes, " +
            f"larger than maximum {spec[f_id]['max_len']}",
            doc_dec, doc_enc, f_id) from None

    # Encode field length
    try:
        if spec[f_id]['len_enc'] == 'b':
            # Odd field length type is not allowed for purpose of string
            # to BCD translation. Double it, e.g.:
            # BCD LVAR length \x09 must be string '09'
            # BCD LLVAR length \x99 must be string '99'
            # BCD LLLVAR length \x09\x99 must be string '0999'
            # BCD LLLLVAR length \x99\x99 must be string '9999'
            doc_enc[f_id]['len'] = bytes.fromhex('{:0{len_type}d}'.format(
                                                 f_len, len_type=len_type * 2))
        else:
            doc_enc[f_id]['len'] = bytes('{:0{len_type}d}'.format(
                                         f_len, len_type=len_type),
                                         spec[f_id]['len_enc'])
    except Exception as e:
        raise EncodeError(f"Failed to encode length ({e})",
                          doc_dec, doc_enc, f_id) from None

    return doc_enc[f_id]['len'] + doc_enc[f_id]['data']
