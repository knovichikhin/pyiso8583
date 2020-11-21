from typing import Any, Dict, Mapping, MutableMapping, Set, Tuple, Type

__all__ = ["encode", "EncodeError"]

DecodedDict = MutableMapping[str, str]
EncodedDict = Dict[str, Dict[str, bytes]]
SpecDict = Mapping[str, Mapping[str, Any]]


class EncodeError(ValueError):
    r"""Subclass of ValueError that describes ISO8583 encoding error.

    Attributes
    ----------
    msg : str
        The unformatted error message
    doc_dec : dict
        Dict containing decoded ISO8583 data being encoded
    doc_enc : dict
        Dict containing partially encoded ISO8583 data
    field : str
        The ISO8583 field where parsing failed
    """

    def __init__(
        self, msg: str, doc_dec: DecodedDict, doc_enc: EncodedDict, field: str
    ):
        errmsg = f"{msg}: field {field}"
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc_dec = doc_dec
        self.doc_enc = doc_enc
        self.field = field

    def __reduce__(
        self,
    ) -> Tuple[Type["EncodeError"], Tuple[str, DecodedDict, EncodedDict, str]]:
        return self.__class__, (self.msg, self.doc_dec, self.doc_enc, self.field)


def encode(doc_dec: DecodedDict, spec: SpecDict) -> Tuple[bytearray, EncodedDict]:
    r"""Serialize Python dict containing ISO8583 data to a bytearray.

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
        Dict containing encoded ISO8583 data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray
    TypeError
        `doc_dec` must be a dict instance

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> doc_dec = {
    ...     't': '0210',
    ...     '3': '111111',
    ...     '39': '05'}
    >>> s, doc_enc = iso8583.encode(doc_dec, spec)
    >>> s
    bytearray(b'0210200000000200000011111105')
    """

    if not isinstance(doc_dec, dict):
        raise TypeError(
            f"Decoded ISO8583 data must be dict, not {doc_dec.__class__.__name__}"
        )

    s = bytearray()
    doc_enc: EncodedDict = {}
    fields: Set[int] = set()
    s += _encode_header(doc_dec, doc_enc, spec)
    s += _encode_type(doc_dec, doc_enc, spec)
    s += _encode_bitmaps(doc_dec, doc_enc, spec, fields)

    for field_key in [str(i) for i in sorted(fields)]:
        # Secondary bitmap is already encoded in _encode_bitmaps
        if field_key == "1":
            continue
        s += _encode_field(doc_dec, doc_enc, field_key, spec)

    return s, doc_enc


#
# Private interface
#


def _encode_header(doc_dec: DecodedDict, doc_enc: EncodedDict, spec: SpecDict) -> bytes:
    r"""Encode ISO8583 header data if present from `d["h"]`.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 header data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """

    # Header is not expected according to specifications
    if spec["h"]["max_len"] <= 0:
        return b""

    # Header data is a required field.
    try:
        doc_dec["h"]
    except KeyError:
        raise EncodeError(
            "Field data is required according to specifications", doc_dec, doc_enc, "h"
        ) from None

    return _encode_field(doc_dec, doc_enc, "h", spec)


def _encode_type(doc_dec: DecodedDict, doc_enc: EncodedDict, spec: SpecDict) -> bytes:
    r"""Encode ISO8583 message type from `d["t"]`.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 message type data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """

    # Message type is a required field.
    try:
        doc_dec["t"]
    except KeyError:
        raise EncodeError("Field data is required", doc_dec, doc_enc, "t") from None

    # Message type is a set length in ISO8583
    if spec["t"]["data_enc"] == "b":
        f_len = 2
    else:
        f_len = 4

    doc_enc["t"] = {"len": b"", "data": b""}

    try:
        if spec["t"]["data_enc"] == "b":
            doc_enc["t"]["data"] = bytes.fromhex(doc_dec["t"])
        else:
            doc_enc["t"]["data"] = doc_dec["t"].encode(spec["t"]["data_enc"])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", doc_dec, doc_enc, "t") from None

    if len(doc_enc["t"]["data"]) != f_len:
        raise EncodeError(
            f"Field data is {len(doc_enc['t']['data'])} bytes, expecting {f_len}",
            doc_dec,
            doc_enc,
            "t",
        ) from None

    return doc_enc["t"]["data"]


def _encode_bitmaps(
    doc_dec: DecodedDict, doc_enc: EncodedDict, spec: SpecDict, fields: Set[int]
) -> bytes:
    r"""Encode ISO8583 primary and secondary bitmap from dictionary keys.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.
    fields: set
        Will be populated with enabled field numbers

    Returns
    -------
    bytes
        Encoded ISO8583 primary and/or secondary bitmaps data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """

    # Secondary bitmap will be calculated as needed
    doc_dec.pop("1", None)

    # Primary and secondary bitmaps will be created from the keys
    try:
        fields.update([int(k) for k in doc_dec.keys() if k.isnumeric()])
    except AttributeError:
        raise EncodeError(
            f"Dictionary contains invalid fields {[k for k in doc_dec.keys() if not isinstance(k, str)]}",
            doc_dec,
            doc_enc,
            "p",
        ) from None

    # Bitmap must consist of 1-128 field range
    if not fields.issubset(range(1, 129)):
        raise EncodeError(
            f"Dictionary contains fields outside of 1-128 range {sorted(fields.difference(range(1, 129)))}",
            doc_dec,
            doc_enc,
            "p",
        ) from None

    # Add secondary bitmap if any 65-128 fields are present
    if not fields.isdisjoint(range(65, 129)):
        fields.add(1)

    # Turn on bitmap bits of associated fields.
    # There is no need to sort this set because the code below will
    # figure out appropriate byte/bit for each field.
    s = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    for f in fields:
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
    doc_dec["p"] = s[0:8].hex().upper()
    doc_enc["p"] = {"len": b"", "data": b""}

    try:
        if spec["p"]["data_enc"] == "b":
            doc_enc["p"]["data"] = bytes(s[0:8])
        else:
            doc_enc["p"]["data"] = doc_dec["p"].encode(spec["p"]["data_enc"])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", doc_dec, doc_enc, "p") from None

    # No need to produce secondary bitmap if it's not required
    if 1 not in fields:
        return doc_enc["p"]["data"]

    # Encode secondary bitmap
    doc_dec["1"] = s[8:16].hex().upper()
    doc_enc["1"] = {"len": b"", "data": b""}

    try:
        if spec["1"]["data_enc"] == "b":
            doc_enc["1"]["data"] = bytes(s[8:16])
        else:
            doc_enc["1"]["data"] = doc_dec["1"].encode(spec["1"]["data_enc"])
    except Exception as e:
        raise EncodeError(f"Failed to encode ({e})", doc_dec, doc_enc, "1") from None

    return doc_enc["p"]["data"] + doc_enc["1"]["data"]


def _encode_field(
    doc_dec: DecodedDict, doc_enc: EncodedDict, field_key: str, spec: SpecDict
) -> bytes:
    r"""Encode ISO8583 individual field from `d[field]`.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    field_key : str
        Field ID to be encoded
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    bytes
        Encoded ISO8583 field data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """

    # Encode field data
    doc_enc[field_key] = {"len": b"", "data": b""}

    try:
        if spec[field_key]["data_enc"] == "b":
            doc_enc[field_key]["data"] = bytes.fromhex(doc_dec[field_key])
        else:
            doc_enc[field_key]["data"] = doc_dec[field_key].encode(
                spec[field_key]["data_enc"]
            )
    except Exception as e:
        raise EncodeError(
            f"Failed to encode ({e})", doc_dec, doc_enc, field_key
        ) from None

    len_type = spec[field_key]["len_type"]
    f_len = len(doc_enc[field_key]["data"])

    # Handle fixed length field. No need to calculate length.
    if len_type == 0:
        if f_len != spec[field_key]["max_len"]:
            raise EncodeError(
                f"Field data is {f_len} bytes, expecting {spec[field_key]['max_len']}",
                doc_dec,
                doc_enc,
                field_key,
            ) from None

        doc_enc[field_key]["len"] = b""
        return doc_enc[field_key]["data"]

    # Continue with variable length field.

    if f_len > spec[field_key]["max_len"]:
        raise EncodeError(
            f"Field data is {f_len} bytes, larger than maximum {spec[field_key]['max_len']}",
            doc_dec,
            doc_enc,
            field_key,
        ) from None

    # Encode field length
    try:
        if spec[field_key]["len_enc"] == "b":
            # Odd field length type is not allowed for purpose of string
            # to BCD translation. Double it, e.g.:
            # BCD LVAR length \x09 must be string "09"
            # BCD LLVAR length \x99 must be string "99"
            # BCD LLLVAR length \x09\x99 must be string "0999"
            # BCD LLLLVAR length \x99\x99 must be string "9999"
            doc_enc[field_key]["len"] = bytes.fromhex(
                "{:0{len_type}d}".format(f_len, len_type=len_type * 2)
            )
        else:
            doc_enc[field_key]["len"] = bytes(
                "{:0{len_type}d}".format(f_len, len_type=len_type),
                spec[field_key]["len_enc"],
            )
    except Exception as e:
        raise EncodeError(
            f"Failed to encode length ({e})", doc_dec, doc_enc, field_key
        ) from None

    return doc_enc[field_key]["len"] + doc_enc[field_key]["data"]
