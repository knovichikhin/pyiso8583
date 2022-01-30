from typing import Any, Dict, Mapping, Set, Tuple, Type, Union

__all__ = ["decode", "DecodeError"]

DecodedDict = Dict[str, str]
EncodedDict = Dict[str, Dict[str, bytes]]
SpecDict = Mapping[str, Mapping[str, Any]]


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
        s: Union[bytes, bytearray],
        doc_dec: DecodedDict,
        doc_enc: EncodedDict,
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

    def __reduce__(
        self,
    ) -> Tuple[
        Type["DecodeError"],
        Tuple[str, Union[bytes, bytearray], DecodedDict, EncodedDict, int, str],
    ]:
        return (
            self.__class__,
            (self.msg, self.s, self.doc_dec, self.doc_enc, self.pos, self.field),
        )


def decode(
    s: Union[bytes, bytearray], spec: SpecDict
) -> Tuple[DecodedDict, EncodedDict]:
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
    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b"02004010100000000000161234567890123456123456111"
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> pprint.pprint(doc_dec)
    {'12': '123456',
     '2': '1234567890123456',
     '20': '111',
     'p': '4010100000000000',
     't': '0200'}
    """

    if not isinstance(s, (bytes, bytearray)):
        raise TypeError(
            f"Encoded ISO8583 data must be bytes or bytearray, not {s.__class__.__name__}"
        )

    doc_dec: DecodedDict = {}
    doc_enc: EncodedDict = {}
    fields: Set[int] = set()
    idx = 0

    idx = _decode_header(s, doc_dec, doc_enc, idx, spec)
    idx = _decode_type(s, doc_dec, doc_enc, idx, spec)
    idx = _decode_bitmaps(s, doc_dec, doc_enc, idx, spec, fields)

    # `field_key` can be used to throw an exception after the loop.
    # So, create it here in case the `fields` set is empty
    # and never enters the loop to create the variable.
    # Set `field_key` to the last mandatory one: primary bitmap.
    field_key = "p"

    for field_key in [str(i) for i in sorted(fields)]:
        # Secondary bitmap is already decoded in _decode_bitmaps
        if field_key == "1":
            continue
        idx = _decode_field(s, doc_dec, doc_enc, idx, field_key, spec)

    if idx != len(s):
        raise DecodeError(
            "Extra data after last field", s, doc_dec, doc_enc, idx, field_key
        )

    return doc_dec, doc_enc


#
# Private interface
#


def _decode_header(
    s: Union[bytes, bytearray],
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    idx: int,
    spec: SpecDict,
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

    # Header is not expected according to specifications
    if spec["h"]["max_len"] <= 0:
        return idx

    return _decode_field(s, doc_dec, doc_enc, idx, "h", spec)


def _decode_type(
    s: Union[bytes, bytearray],
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    idx: int,
    spec: SpecDict,
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
        )

    if spec["t"]["data_enc"] == "b":
        doc_dec["t"] = s[idx : idx + f_len].hex().upper()
    else:
        try:
            doc_dec["t"] = s[idx : idx + f_len].decode(spec["t"]["data_enc"])
        except LookupError:
            raise DecodeError(
                "Failed to decode field, unknown encoding specified",
                s,
                doc_dec,
                doc_enc,
                idx,
                "t",
            ) from None
        except Exception:
            raise DecodeError(
                "Failed to decode field, invalid data",
                s,
                doc_dec,
                doc_enc,
                idx,
                "t",
            ) from None

    return idx + f_len


def _decode_bitmaps(
    s: Union[bytes, bytearray],
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    idx: int,
    spec: SpecDict,
    fields: Set[int],
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
    fields: set
        Will be populated with enabled field numbers

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
        )

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

    fields.update(
        [
            byte_idx * 8 + bit
            for bit in range(1, 9)
            for byte_idx, byte in enumerate(bm)
            if byte >> (8 - bit) & 1
        ]
    )

    idx += f_len

    # No need to produce secondary bitmap if it's not required
    if 1 not in fields:
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
        )

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

    fields.update(
        [
            64 + byte_idx * 8 + bit
            for bit in range(1, 9)
            for byte_idx, byte in enumerate(bm)
            if byte >> (8 - bit) & 1
        ]
    )

    return idx + f_len


def _decode_field(
    s: Union[bytes, bytearray],
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    idx: int,
    field_key: str,
    spec: SpecDict,
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
    field_key : str
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
    len_type = spec[field_key]["len_type"]

    # Optional field added in v2.1. Prior specs do not have it.
    len_count = spec[field_key].get("len_count", "bytes")

    doc_dec[field_key] = ""
    doc_enc[field_key] = {"len": bytes(s[idx : idx + len_type]), "data": b""}

    if len(s[idx : idx + len_type]) != len_type:
        raise DecodeError(
            f"Field length is {len(s[idx:idx + len_type])} bytes wide, expecting {len_type}",
            s,
            doc_dec,
            doc_enc,
            idx,
            field_key,
        )

    # Parse field length if present.
    # For fixed-length fields max_len is the length.
    if len_type == 0:
        enc_field_len: int = spec[field_key]["max_len"]
    # Variable field length
    else:
        # BCD length
        if spec[field_key]["len_enc"] == "b":
            try:
                enc_field_len = int(s[idx : idx + len_type].hex(), 10)
            except Exception:
                raise DecodeError(
                    "Failed to decode field length, invalid BCD data",
                    s,
                    doc_dec,
                    doc_enc,
                    idx,
                    field_key,
                ) from None
        # Text length
        else:
            try:
                decoded_length = s[idx : idx + len_type].decode(
                    spec[field_key]["len_enc"]
                )
            except LookupError:
                raise DecodeError(
                    "Failed to decode field length, unknown encoding specified",
                    s,
                    doc_dec,
                    doc_enc,
                    idx,
                    field_key,
                ) from None
            except Exception:
                raise DecodeError(
                    "Failed to decode field length, invalid data",
                    s,
                    doc_dec,
                    doc_enc,
                    idx,
                    field_key,
                ) from None

            try:
                enc_field_len = int(decoded_length)
            except Exception:
                raise DecodeError(
                    "Failed to decode field length, non-numeric data",
                    s,
                    doc_dec,
                    doc_enc,
                    idx,
                    field_key,
                ) from None

        if enc_field_len > spec[field_key]["max_len"]:
            raise DecodeError(
                f"Field data is {enc_field_len} {len_count}, larger than maximum {spec[field_key]['max_len']}",
                s,
                doc_dec,
                doc_enc,
                idx,
                field_key,
            )

    idx += len_type

    # Do not parse zero-length field
    if enc_field_len == 0:
        return idx

    # Encoded field length can be in bytes or half bytes (nibbles)
    # Convert nibbles to bytes if needed
    if len_count == "nibbles":
        if enc_field_len & 1:
            byte_field_len = (enc_field_len + 1) // 2
        else:
            byte_field_len = enc_field_len // 2
    else:
        byte_field_len = enc_field_len

    # Parse field data
    doc_enc[field_key]["data"] = bytes(s[idx : idx + byte_field_len])
    if len(doc_enc[field_key]["data"]) != byte_field_len:
        if len_count == "nibbles":
            actual_field_len = len(doc_enc[field_key]["data"]) * 2
        else:
            actual_field_len = len(doc_enc[field_key]["data"])

        raise DecodeError(
            f"Field data is {actual_field_len} {len_count}, expecting {enc_field_len}",
            s,
            doc_dec,
            doc_enc,
            idx,
            field_key,
        )

    if spec[field_key]["data_enc"] == "b":
        doc_dec[field_key] = doc_enc[field_key]["data"].hex().upper()
        if len_count == "nibbles" and enc_field_len & 1:
            doc_dec[field_key] = _remove_pad_field(
                s, idx, doc_dec, doc_enc, field_key, spec, enc_field_len
            )
    else:
        try:
            doc_dec[field_key] = doc_enc[field_key]["data"].decode(
                spec[field_key]["data_enc"]
            )
        except LookupError:
            raise DecodeError(
                "Failed to decode field, unknown encoding specified",
                s,
                doc_dec,
                doc_enc,
                idx,
                field_key,
            ) from None
        except Exception:
            raise DecodeError(
                "Failed to decode field, invalid data",
                s,
                doc_dec,
                doc_enc,
                idx,
                field_key,
            ) from None

    return idx + byte_field_len


def _remove_pad_field(
    s: Union[bytes, bytearray],
    idx: int,
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    field_key: str,
    spec: SpecDict,
    enc_field_len: int,
) -> str:
    r"""Remove left or right pad from a BCD or hex field.

    Parameters
    ----------
    s : bytes or bytearray
        Encoded ISO8583 data
    idx : int
        Current index in ISO8583 byte array
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    field_key : str
        Field ID to remove pad from
    spec : dict
        A Python dict defining ISO8583 specification.
        See :mod:`iso8583.specs` module for examples.
    enc_field_len : int
        Number of nibbles expected in the field

    Returns
    -------
    str
        Field data without pad

    Raises
    ------
    DecodeError
        An error decoding ISO8583 bytearray.
    """
    pad: str = spec[field_key].get("left_pad", "")[:1]
    if len(pad) > 0 and doc_dec[field_key][:1] == pad:
        return doc_dec[field_key][1:]

    pad = spec[field_key].get("right_pad", "")[:1]
    if len(pad) > 0 and doc_dec[field_key][-1:] == pad:
        return doc_dec[field_key][:-1]

    raise DecodeError(
        f"Field data is {len(doc_dec[field_key])} nibbles, expecting {enc_field_len}",
        s,
        doc_dec,
        doc_enc,
        idx,
        field_key,
    )
