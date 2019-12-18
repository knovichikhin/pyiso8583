from typing import Tuple

__all__ = ["decode", "DecodeError"]


class DecodeError(ValueError):
    r"""Subclass of ValueError that describes ISO8583 decoding error.

    Attributes
    ----------
    msg : str
        The unformatted error message
    s : bytes or bytearray
        The ISO8583 bytes instance being parsed
    doc_dec : dict
        Dict containing partially decoded ISO8583 data
    doc_enc : dict
        Dict containing partially encoded ISO8583 data
    pos : int
        The start index where ISO8583 bytes data failed parsing
    field : str
        The ISO8583 field where parsing failed
    """

    def __init__(
        self,
        msg: str,
        s: bytes or bytearray,
        doc_dec: dict,
        doc_enc: dict,
        pos: int,
        field: str,
    ):
        errmsg = f"{msg}: field {field} pos {pos}"
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.s = s
        self.doc_dec = doc_dec
        self.doc_enc = doc_enc
        self.field = field
        self.pos = pos

    def __reduce__(self):
        return (
            self.__class__,
            (self.msg, self.s, self.doc_dec, self.doc_enc, self.pos, self.field),
        )


def decode(s: bytes or bytearray, spec: dict) -> Tuple[dict, dict]:
    r"""Deserialize a bytes or bytearray instance containing
    ISO8583 data to a Python dict.

    Parameters
    ----------
    s : bytes or bytearray
        Encoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data

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
    >>> s = b"0200\x40\x10\x10\x00\x00\x00\x00\x00161234567890123456123456111"
    >>> doc_dec, doc_enc = iso8583.decode(s, spec=default)
    """
    if not isinstance(s, (bytes, bytearray)):
        raise TypeError(
            f"the ISO8583 data must be bytes or bytearray, not {s.__class__.__name__}"
        )

    doc_dec = {"bm": set()}
    doc_enc = {"bm": set()}
    idx = 0

    idx = _decode_header(s, doc_dec, doc_enc, idx, spec)
    idx = _decode_type(s, doc_dec, doc_enc, idx, spec)
    idx = _decode_bitmaps(s, doc_dec, doc_enc, idx, spec)

    # Create the variable in case the bitmap set is empty
    # and there is extra data afterwards.
    # Set field to the last mandatory one: primary bitmap.
    f_id = "p"

    for f_id in [str(i) for i in sorted(doc_dec["bm"])]:
        # Secondary bitmap is already decoded in _decode_bitmaps
        if f_id == "1":
            continue
        idx = _decode_field(s, doc_dec, doc_enc, idx, f_id, spec)

    if idx != len(s):
        raise DecodeError(
            "Extra data after last field", s, doc_dec, doc_enc, idx, f_id
        ) from None

    return doc_dec, doc_enc


#
# Private interface
#


def _decode_header(
    s: bytes or bytearray, doc_dec: dict, doc_enc: dict, idx: int, spec: dict
) -> int:
    r"""Decode ISO8583 header data if present.

    Parameters
    ----------
    s : bytes or bytearray
        Encoded ISO8583 data
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
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
    f_len = spec["h"]["max_len"]

    # Header is not expected according to specifications
    if f_len <= 0:
        return idx

    doc_dec["h"] = ""
    doc_enc["h"] = {"len": b"", "data": bytes(s[idx : idx + f_len])}

    if len(s[idx : idx + f_len]) != f_len:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + f_len])} bytes, expecting {f_len}",
            s,
            doc_dec,
            doc_enc,
            idx,
            "h",
        ) from None

    try:
        if spec["h"]["data_enc"] == "b":
            doc_dec["h"] = s[idx : idx + f_len].hex().upper()
        else:
            doc_dec["h"] = s[idx : idx + f_len].decode(spec["h"]["data_enc"])
    except Exception as e:
        raise DecodeError(
            f"Failed to decode ({e})", s, doc_dec, doc_enc, idx, "h"
        ) from None

    return idx + f_len


def _decode_type(
    s: bytes or bytearray, doc_dec: dict, doc_enc: dict, idx: int, spec: dict
) -> int:
    r"""Decode ISO8583 message type.

    Parameters
    ----------
    s : bytes or bytearray
        Encoded ISO8583 data
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
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

    # Message type is a set length in ISO8583
    if spec["t"]["data_enc"] == "b":
        f_len = 2
    else:
        f_len = 4

    doc_dec["t"] = ""
    doc_enc["t"] = {"len": b"", "data": bytes(s[idx : idx + f_len])}

    if len(s[idx : idx + f_len]) != f_len:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + f_len])} bytes, expecting {f_len}",
            s,
            doc_dec,
            doc_enc,
            idx,
            "t",
        ) from None

    try:
        if spec["t"]["data_enc"] == "b":
            doc_dec["t"] = s[idx : idx + f_len].hex().upper()
        else:
            doc_dec["t"] = s[idx : idx + f_len].decode(spec["t"]["data_enc"])
    except Exception as e:
        raise DecodeError(
            f"Failed to decode ({e})", s, doc_dec, doc_enc, idx, "t"
        ) from None

    return idx + f_len


def _decode_bitmaps(
    s: bytes or bytearray, doc_dec: dict, doc_enc: dict, idx: int, spec: dict
) -> int:
    r"""Decode ISO8583 primary and secondary bitmaps.

    Parameters
    ----------
    s : bytes or bytearray
        Encoded ISO8583 data
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
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

    # Primary bitmap is a set length in ISO8583
    if spec["p"]["data_enc"] == "b":
        f_len = 8
    else:
        f_len = 16

    doc_dec["p"] = ""
    doc_enc["p"] = {"len": b"", "data": bytes(s[idx : idx + f_len])}

    if len(s[idx : idx + f_len]) != f_len:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + f_len])} bytes, expecting {f_len}",
            s,
            doc_dec,
            doc_enc,
            idx,
            "p",
        ) from None

    try:
        if spec["p"]["data_enc"] == "b":
            doc_dec["p"] = s[idx : idx + f_len].hex().upper()
            bm = s[idx : idx + f_len]
        else:
            doc_dec["p"] = s[idx : idx + f_len].decode(spec["p"]["data_enc"])
            bm = bytes.fromhex(doc_dec["p"])
    except Exception as e:
        raise DecodeError(
            f"Failed to decode ({e})", s, doc_dec, doc_enc, idx, "p"
        ) from None

    doc_dec["bm"] = set(
        [
            byte_idx * 8 + bit
            for bit in range(1, 9)
            for byte_idx, byte in enumerate(bm)
            if byte >> (8 - bit) & 1
        ]
    )
    doc_enc["bm"] = doc_dec["bm"].copy()

    idx += f_len

    # No need to produce secondary bitmap if it's not required
    if 1 not in doc_dec["bm"]:
        return idx

    # Decode secondary bitmap
    # Secondary bitmap is a set length in ISO8583
    if spec["1"]["data_enc"] == "b":
        f_len = 8
    else:
        f_len = 16

    doc_dec["1"] = ""
    doc_enc["1"] = {"len": b"", "data": bytes(s[idx : idx + f_len])}

    if len(s[idx : idx + f_len]) != f_len:
        raise DecodeError(
            f"Field data is {len(s[idx:idx + f_len])} bytes, expecting {f_len}",
            s,
            doc_dec,
            doc_enc,
            idx,
            "1",
        ) from None

    try:
        if spec["1"]["data_enc"] == "b":
            doc_dec["1"] = s[idx : idx + f_len].hex().upper()
            bm = s[idx : idx + f_len]
        else:
            doc_dec["1"] = s[idx : idx + f_len].decode(spec["1"]["data_enc"])
            bm = bytes.fromhex(doc_dec["1"])
    except Exception as e:
        raise DecodeError(
            f"Failed to decode ({e})", s, doc_dec, doc_enc, idx, "1"
        ) from None

    doc_dec["bm"].update(
        [
            64 + byte_idx * 8 + bit
            for bit in range(1, 9)
            for byte_idx, byte in enumerate(bm)
            if byte >> (8 - bit) & 1
        ]
    )
    doc_enc["bm"] = doc_dec["bm"].copy()

    return idx + f_len


def _decode_field(
    s: bytes or bytearray, doc_dec: dict, doc_enc: dict, idx: int, f_id: str, spec: dict
) -> int:
    r"""Decode ISO8583 individual fields.

    Parameters
    ----------
    s : bytes or bytearray
        Encoded ISO8583 data
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    idx : int
        Current index in ISO8583 byte array
    f_id : str
        Field ID to be decoded
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
    len_type = spec[f_id]["len_type"]

    doc_dec[f_id] = ""
    doc_enc[f_id] = {"len": bytes(s[idx : idx + len_type]), "data": b""}

    if len(s[idx : idx + len_type]) != len_type:
        raise DecodeError(
            f"Field length is {len(s[idx:idx + len_type])} bytes wide, expecting {len_type}",
            s,
            doc_dec,
            doc_enc,
            idx,
            f_id,
        ) from None

    # Parse field length if present.
    # For fixed-length fields max_len is the length.
    if len_type == 0:
        f_len = spec[f_id]["max_len"]
    else:
        try:
            if spec[f_id]["len_enc"] == "b":
                f_len = int(s[idx : idx + len_type].hex(), 10)
            else:
                f_len = int(s[idx : idx + len_type].decode(spec[f_id]["len_enc"]), 10)
        except Exception as e:
            raise DecodeError(
                f"Failed to decode length ({e})", s, doc_dec, doc_enc, idx, f_id
            ) from None

    if f_len > spec[f_id]["max_len"]:
        raise DecodeError(
            f"Field data is {f_len} bytes, larger than maximum {spec[f_id]['max_len']}",
            s,
            doc_dec,
            doc_enc,
            idx,
            f_id,
        ) from None

    idx += len_type

    # Do not parse zero-length field
    if f_len == 0:
        return idx

    # Parse field data
    doc_enc[f_id]["data"] = bytes(s[idx : idx + f_len])

    if len(doc_enc[f_id]["data"]) != f_len:
        raise DecodeError(
            f"Field data is {len(doc_enc[f_id]['data'])} bytes, expecting {f_len}",
            s,
            doc_dec,
            doc_enc,
            idx,
            f_id,
        ) from None

    try:
        if spec[f_id]["data_enc"] == "b":
            doc_dec[f_id] = doc_enc[f_id]["data"].hex().upper()
        else:
            doc_dec[f_id] = doc_enc[f_id]["data"].decode(spec[f_id]["data_enc"])
    except Exception as e:
        raise DecodeError(
            f"Failed to decode ({e})", s, doc_dec, doc_enc, idx, f_id
        ) from None

    return idx + f_len
