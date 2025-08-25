from typing import Any, Dict, Literal, Mapping, MutableMapping, Set, Tuple, Type
import binascii

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

    # Secondary bitmaps will be calculated as needed
    doc_dec.pop("1", None)
    # Extended bitmap indicator must not be an actual field
    doc_dec.pop("65", None)

    s += _encode_header(doc_dec, doc_enc, spec)
    s += _encode_type(doc_dec, doc_enc, spec)

    try:
        fields: Set[int] = set([int(k) for k in doc_dec.keys() if k.isnumeric()])
    except AttributeError:
        raise EncodeError(
            f"Dictionary contains invalid fields {[k for k in doc_dec.keys() if not isinstance(k, str)]}",
            doc_dec,
            doc_enc,
            "p",
        ) from None

    # Verify valid field range: 1-192
    if not fields.issubset(range(1, 193)):
        raise EncodeError(
            f"Dictionary contains fields outside of 1-192 range {sorted(fields.difference(range(1, 193)))}",
            doc_dec,
            doc_enc,
            "p",
        )

    # Add tertiary bitmap if any 129-192 fields are present
    tertiary_fields = fields.intersection(range(129, 193))
    if tertiary_fields:
        fields.add(65)

    # Add secondary bitmap if any 65-128 fields are present
    secondary_fields = fields.intersection(range(65, 129))
    if secondary_fields:
        fields.add(1)

    s += _encode_bitmap(
        doc_dec,
        doc_enc,
        "p",
        spec["p"],
        0,
        False,
        fields.intersection(range(1, 65)),
    )

    if 1 in fields:
        s += _encode_bitmap(
            doc_dec,
            doc_enc,
            "1",
            spec["1"],
            64,
            False,
            secondary_fields,
        )
        fields.remove(1)

    if 65 in fields:
        s += _encode_bitmap(
            doc_dec,
            doc_enc,
            "1",
            spec["1"],
            128,
            True,
            tertiary_fields,
        )
        fields.remove(65)

    for field_key in [str(i) for i in sorted(fields)]:
        s += _encode_field(doc_dec, doc_enc, field_key, spec[field_key])

    return s, doc_enc


#
# Private interface
#

_FieldSpecDict = Mapping[str, Any]


def _encode_header(
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    spec: SpecDict,
) -> bytes:
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
    if "h" not in doc_dec:
        raise EncodeError(
            "Field data is required according to specifications", doc_dec, doc_enc, "h"
        )

    return _encode_field(doc_dec, doc_enc, "h", spec["h"])


def _encode_type(
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    spec: SpecDict,
) -> bytes:
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
    if "t" not in doc_dec:
        raise EncodeError("Field data is required", doc_dec, doc_enc, "t")

    # Message type is a set length in ISO8583
    if spec["t"]["data_enc"] == "b":
        expected_field_len = 2
    else:
        expected_field_len = 4

    doc_enc["t"] = {"len": b"", "data": b""}

    if spec["t"]["data_enc"] == "b":
        doc_enc["t"]["data"], enc_field_len = _encode_bindary_field(
            doc_dec,
            doc_enc,
            doc_dec["t"],
            "t",
            spec["t"],
            "bytes",
        )
    else:
        doc_enc["t"]["data"], enc_field_len = _encode_text_field(
            doc_dec,
            doc_enc,
            doc_dec["t"],
            "t",
            spec["t"],
            "bytes",
        )

    if enc_field_len != expected_field_len:
        raise EncodeError(
            f"Field data is {enc_field_len} bytes, expecting {expected_field_len}",
            doc_dec,
            doc_enc,
            "t",
        )

    return doc_enc["t"]["data"]


def _encode_bitmap(
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    field_key: str,
    field_spec: _FieldSpecDict,
    field_offset: Literal[0, 64, 128],
    is_extended: bool,
    fields: Set[int],
) -> bytes:
    r"""Encode ISO8583 bitmap.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    field_key : str
        Field ID to be encoded
    field_spec : dict
        A Python dict defining ISO8583 specification for this field.
        See :mod:`iso8583.specs` module for examples.
    field_offset : int
        Offset by which to adjust fields to fit into 1-64 range.
    is_extended : bool
        If true then processing an extension of an already processed bitmap
    fields: set
        Will be populated with enabled field numbers

    Returns
    -------
    bytes
        Encoded ISO8583 bitmap data

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """

    bitmap = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00")

    for field in fields:
        # Fields start at 1. Make them zero-bound for easier conversion.
        # Offset fields to fit into 0-7 byte.
        field -= 1 + field_offset

        # Place this particular field in a byte where it belongs.
        # E.g. field 8 belongs to byte 0, field 64 belongs to byte 7.
        byte = field // 8

        # Determine bit to enable. ISO8583 bitmaps are left-aligned.
        # E.g. fields 1, 9, 17, etc. enable bit 7 in bytes 0, 1, 2, etc.
        bit = 7 - (field - byte * 8)
        bitmap[byte] |= 1 << bit

    hex_bitmap = bitmap.hex().upper()

    if is_extended:
        doc_dec[field_key] = doc_dec[field_key] + hex_bitmap
    else:
        doc_dec[field_key] = hex_bitmap
        doc_enc[field_key] = {"len": b"", "data": b""}

    if field_spec["data_enc"] == "b":
        encoded_data = bytes(bitmap)
    else:
        encoded_data, _ = _encode_text_field(
            doc_dec,
            doc_enc,
            hex_bitmap,
            field_key,
            field_spec,
            "bytes",
        )

    if is_extended:
        doc_enc[field_key]["data"] = doc_enc[field_key]["data"] + encoded_data
    else:
        doc_enc[field_key]["data"] = encoded_data

    return encoded_data


def _encode_field(
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    field_key: str,
    field_spec: _FieldSpecDict,
) -> bytes:
    r"""Encode ISO8583 individual field from `doc_dec[field_key]`.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    field_key : str
        Field ID to be encoded
    field_spec : dict
        A Python dict defining ISO8583 specification for this field.
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

    # Optional field added in v2.1. Prior specs do not have it.
    len_count = field_spec.get("len_count", "bytes")

    # Binary data: either hex or BCD
    if field_spec["data_enc"] == "b":
        doc_enc[field_key]["data"], enc_field_len = _encode_bindary_field(
            doc_dec,
            doc_enc,
            doc_dec[field_key],
            field_key,
            field_spec,
            len_count,
        )
    # Text data
    else:
        doc_enc[field_key]["data"], enc_field_len = _encode_text_field(
            doc_dec,
            doc_enc,
            doc_dec[field_key],
            field_key,
            field_spec,
            len_count,
        )

    len_type = field_spec["len_type"]

    # Handle fixed length field. No need to calculate length.
    if len_type == 0:
        if enc_field_len != field_spec["max_len"]:
            raise EncodeError(
                f"Field data is {enc_field_len} {len_count}, expecting {field_spec['max_len']}",
                doc_dec,
                doc_enc,
                field_key,
            )

        doc_enc[field_key]["len"] = b""
        return doc_enc[field_key]["data"]

    # Continue with variable length field.

    if enc_field_len > field_spec["max_len"]:
        raise EncodeError(
            f"Field data is {enc_field_len} {len_count}, larger than maximum {field_spec['max_len']}",
            doc_dec,
            doc_enc,
            field_key,
        )

    # Encode binary field length
    if field_spec["len_enc"] == "b":
        try:
            doc_enc[field_key]["len"] = (enc_field_len).to_bytes(
                len_type, "big", signed=False
            )
        except OverflowError:
            raise EncodeError(
                "Failed to encode field length, field length does not fit into configured field size",
                doc_dec,
                doc_enc,
                field_key,
            ) from None
    # Encode BCD field length
    elif field_spec["len_enc"] == "bcd":
        # Odd field length type is not allowed when translating string BCD. Pad it, e.g.:
        # BCD LVAR length \x09 must be string "09"
        # BCD LLVAR length \x99 must be string "99"
        # BCD LLLVAR length \x09\x99 must be string "0999"
        # BCD LLLLVAR length \x99\x99 must be string "9999"
        bcd_field_len = "{:0{len_type}d}".format(enc_field_len, len_type=len_type * 2)

        if len(bcd_field_len) > (len_type * 2):
            raise EncodeError(
                "Failed to encode field length, field length does not fit into configured field size",
                doc_dec,
                doc_enc,
                field_key,
            ) from None

        doc_enc[field_key]["len"] = binascii.a2b_hex(bcd_field_len)
    else:
        try:
            doc_enc[field_key]["len"] = bytes(
                "{:0{len_type}d}".format(enc_field_len, len_type=len_type),
                field_spec["len_enc"],
            )
        except LookupError:
            raise EncodeError(
                "Failed to encode field length, unknown encoding specified",
                doc_dec,
                doc_enc,
                field_key,
            ) from None
        # It does not seem to be possible to hit this because regular
        # numeric characters seem to be always encodable.
        # However, keeping this, because you just never know.
        except Exception as e:  # pragma: no cover
            raise EncodeError(
                f"Failed to encode field length, {e}",
                doc_dec,
                doc_enc,
                field_key,
            ) from None

        if len(doc_enc[field_key]["len"]) > len_type:
            raise EncodeError(
                "Failed to encode field length, field length does not fit into configured field size",
                doc_dec,
                doc_enc,
                field_key,
            ) from None

    return doc_enc[field_key]["len"] + doc_enc[field_key]["data"]


def _encode_bindary_field(
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    field_data: str,
    field_key: str,
    field_spec: _FieldSpecDict,
    len_count: str,
) -> Tuple[bytes, int]:
    r"""Encode ISO8583 individual field.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    field_data : str
        Field data to encode
    field_key : str
        Field ID to be encoded
    field_spec : dict
        A Python dict defining ISO8583 specification for this field.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    tuple(bytes, int)
        Encoded data and length of the encoded ISO8583 field data. The length is either nibbles or bytes.

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """
    try:
        # Odd length nibbles need to be padded because it's not possible to send half a byte
        if len_count == "nibbles" and len(field_data) & 1:
            data_to_encode = _add_pad_field(field_data, field_spec)
        else:
            data_to_encode = field_data
        encoded_data = binascii.a2b_hex(data_to_encode)
    except Exception:
        if len_count == "nibbles" and len(data_to_encode) % 2 == 1:
            raise EncodeError(
                "Failed to encode field, odd-length nibble data, specify pad",
                doc_dec,
                doc_enc,
                field_key,
            ) from None
        if len(data_to_encode) % 2 == 1:
            raise EncodeError(
                "Failed to encode field, odd-length hex data",
                doc_dec,
                doc_enc,
                field_key,
            ) from None
        raise EncodeError(
            "Failed to encode field, non-hex data",
            doc_dec,
            doc_enc,
            field_key,
        ) from None

    # Encoded field length can be in bytes or half bytes (nibbles).
    # Encoded nibble length directly corresponds to the count of received nibbles.
    if len_count == "nibbles":
        return (encoded_data, len(field_data))
    else:
        return (encoded_data, len(encoded_data))


def _add_pad_field(
    field_data: str,
    field_spec: _FieldSpecDict,
) -> str:
    r"""Pad a BCD or hex field from the left or right.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    field_data : str
        Field data to encode
    field_key : str
        Field ID to pad
    field_spec : dict
        A Python dict defining ISO8583 specification for this field.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    str
        Padded field data
    """
    pad: str = field_spec.get("left_pad", "")[:1]
    if len(pad) > 0:
        return pad + field_data

    pad = field_spec.get("right_pad", "")[:1]
    if len(pad) > 0:
        return field_data + pad

    return field_data


def _encode_text_field(
    doc_dec: DecodedDict,
    doc_enc: EncodedDict,
    field_data: str,
    field_key: str,
    field_spec: _FieldSpecDict,
    len_count: str,
) -> Tuple[bytes, int]:
    r"""Encode ISO8583 individual field.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    doc_enc : dict
        Dict containing encoded ISO8583 data
    field_data : str
        Field data to encode
    field_key : str
        Field ID to be encoded
    field_spec : dict
        A Python dict defining ISO8583 specification for this field.
        See :mod:`iso8583.specs` module for examples.

    Returns
    -------
    tuple(bytes, int)
        Encoded data and length of the encoded ISO8583 field data. The length is either nibbles or bytes.

    Raises
    ------
    EncodeError
        An error encoding ISO8583 bytearray.
    """
    try:
        encoded_data = field_data.encode(field_spec["data_enc"])
    except LookupError:
        raise EncodeError(
            "Failed to encode field, unknown encoding specified",
            doc_dec,
            doc_enc,
            field_key,
        ) from None
    except Exception:
        raise EncodeError(
            "Failed to encode field, invalid data",
            doc_dec,
            doc_enc,
            field_key,
        ) from None

    # Encoded field length can be in bytes or half bytes (nibbles)
    # Encoded nibble length directly corresponds to the count of received nibbles.
    if len_count == "nibbles":
        return (encoded_data, len(encoded_data) * 2)
    else:
        return (encoded_data, len(encoded_data))
