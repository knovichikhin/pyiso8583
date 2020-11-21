import copy
import pickle

import iso8583
import iso8583.specs
import pytest

spec = copy.deepcopy(iso8583.specs.default)


def test_DecodeError_exception():
    """
    Validate DecodeError class
    """
    s = b""

    try:
        iso8583.decode(s, spec=spec)
    except iso8583.DecodeError as e:
        assert e.doc_dec == ({"t": ""})
        assert e.doc_enc == ({"t": {"data": b"", "len": b""}})
        assert e.msg == "Field data is 0 bytes, expecting 4"
        assert e.field == "t"
        assert e.pos == 0
        assert e.args[0] == "Field data is 0 bytes, expecting 4: field t pos 0"


def test_DecodeError_exception_pickle():
    """
    Validate DecodeError class with pickle
    """
    s = b""

    try:
        iso8583.decode(s, spec=spec)
    except iso8583.DecodeError as e:
        p = pickle.dumps(e)
        e_unpickled = pickle.loads(p)

        assert e.doc_dec == e_unpickled.doc_dec
        assert e.doc_enc == e_unpickled.doc_enc
        assert e.msg == e_unpickled.msg
        assert e.field == e_unpickled.field
        assert e.pos == e_unpickled.pos
        assert e.args[0] == e_unpickled.args[0]


def test_input_type():
    """
    Decode accepts only bytes or bytesarray.
    """
    s = {}
    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not dict"
    ):
        iso8583.decode(s, spec=spec)

    s = []
    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not list"
    ):
        iso8583.decode(s, spec=spec)

    s = (0, 0)
    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not tuple"
    ):
        iso8583.decode(s, spec=spec)

    s = "spam"
    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not str"
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_missing():
    """
    Header length is required but not provided
    The parser assumes that "he" is the header length.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .invalid literal for int.. with base 10: 'he'.: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_partial():
    """
    Header length is required but partially provided.
    The parser assumes that "1h" is the header length.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"1header02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .invalid literal for int.. with base 10: '1h'.: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_incorrect_encoding():
    """
    Header length is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "invalid"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"06header02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .unknown encoding: invalid.: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_incorrect_ascii_data():
    """
    Header length is required and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"\xff\xffheader02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_incorrect_not_numeric():
    """
    Header length is required and provided.
    However, the length is not numeric ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"ggheader02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .invalid literal for int.. with base 10: 'gg'.: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_incorrect_bcd_data():
    """
    BCD Header length is required and provided.
    However, the data is not hex.
    Note: this passes, "g" is valid hex data when decoding.
    It will fail on field parsing, because not sufficient field data was provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 1
    spec["h"]["max_len"] = 99
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"gheader02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 26 bytes, expecting 67: field h pos 1"
    ):
        iso8583.decode(s, spec=spec)


def test_header_length_negative_over_max():
    """
    Header length is required and provided.
    However, it's over the specified maximum.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 1
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"8header02000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 8 bytes, larger than maximum 6: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_ascii_absent():
    """
    ASCII header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"02100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["t", "p"])


def test_header_ascii_present():
    """
    ASCII header is required by spec and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_ebcdic_absent():
    """
    EBCDIC header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"02100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["t", "p"])


def test_header_ebcdic_present():
    """
    EBCDIC header is required by spec and provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"\x88\x85\x81\x84\x85\x9902100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"\x88\x85\x81\x84\x85\x99"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_bcd_absent():
    """
    BDC header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"02100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["t", "p"])


def test_header_bcd_present():
    """
    BCD header is required by spec and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"\xA1\xA2\xA3\xA4\xA5\xA602100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"\xA1\xA2\xA3\xA4\xA5\xA6"
    assert doc_dec["h"] == "A1A2A3A4A5A6"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_negative_missing():
    """
    String header is required by spec but not provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b""
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 6: field h pos 0"
    ):
        iso8583.decode(s, spec=spec)


def test_header_negative_partial():
    """
    String header is required by spec but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"head"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 4 bytes, expecting 6: field h pos 0"
    ):
        iso8583.decode(s, spec=spec)


def test_header_negative_incorrect_encoding():
    """
    String header is required by spec and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "invalid"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02100000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_negative_incorrect_ascii_data():
    """
    ASCII header is required by spec and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"\xff\xff\xff\xff\xff\xff02100000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field h pos 0",
    ):
        iso8583.decode(s, spec=spec)


def test_header_negative_incorrect_bcd_data():
    """
    BCD header is required by spec and provided.
    However, the data is not hex.
    Note: this passes, "header" is valid hex data when decoding.
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "686561646572"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_ascii_absent():
    """
    ASCII message type is required by spec and not provided
    Note: here parser picks up message type as "0000" and fails at primary bitmap.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 12 bytes, expecting 16: field p pos 10",
    ):
        iso8583.decode(s, spec=spec)


def test_type_ascii_present():
    """
    ASCII message type is required by spec and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_ebcdic_absent():
    """
    EBCDIC message type is required by spec and not provided
    Note: here parser picks up message type as "0000" and fails at primary bitmap.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 12 bytes, expecting 16: field p pos 10",
    ):
        iso8583.decode(s, spec=spec)


def test_type_ebcdic_present():
    """
    ASCII message type is required by spec and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "ascii"

    s = b"header\xf0\xf2\xf1\xf00000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"\xf0\xf2\xf1\xf0"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_bcd_absent():
    """
    BCD message type is required by spec and not provided
    Note: here parser picks up message type as "\x30\x30" and fails at primary bitmap.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0000000000000000"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 14 bytes, expecting 16: field p pos 8"
    ):
        iso8583.decode(s, spec=spec)


def test_type_bcd_present():
    """
    ASCII message type is required by spec and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "ascii"

    s = b"header\x02\x100000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"\x02\x10"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_negative_missing():
    """
    Type is required for all messages
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 4: field t pos 6"
    ):
        iso8583.decode(s, spec=spec)


def test_type_negative_partial():
    """
    Message type is required all messages but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 2 bytes, expecting 4: field t pos 6"
    ):
        iso8583.decode(s, spec=spec)


def test_type_negative_incorrect_encoding():
    """
    Message type is required by spec and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "invalid"
    spec["p"]["data_enc"] = "ascii"

    s = b"header02100000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field t pos 6",
    ):
        iso8583.decode(s, spec=spec)


def test_type_negative_incorrect_ascii_data():
    """
    Message type is required by spec and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header\xff\xff\xff\xff0000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field t pos 6",
    ):
        iso8583.decode(s, spec=spec)


def test_type_negative_incorrect_bcd_data():
    """
    BCD message type is required by spec and provided.
    However, the data is not hex.
    Note: this passes, "ab" is valid hex data when decoding.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "ascii"

    s = b"headerab0000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"ab"
    assert doc_dec["t"] == "6162"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def util_set2bitmap(bm):
    """
    Enable bits specified in a bm set and return a bitmap bytearray
    """
    s = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    # Disable secondary bitmap if no 65-128 fields are present
    if bm.isdisjoint(range(65, 129)):
        bm.discard(1)
    else:
        bm.add(1)

    for f in bm:
        f -= 1  # bms start at 1. Make them zero-bound
        byte = int(f / 8)  # Place this particular bit in a byte where it belongs
        bit = 7 - (
            f - byte * 8
        )  # Determine bit to enable. 7th or left-most is fields 1, 9, 17, etc.
        s[byte] |= 1 << bit

    if 1 in bm:
        return s
    else:
        return s[0:8]


def util_set2field_data(bm, spec, data_enc, len_enc, len_type):
    """
    Create dummy field data for fields specified in a bm set and return a bytearray
    Assume that field data is always 2 or 4 bytes representing field number.
    For example, field #65 is represented as "0065" with length 4 or
    \x00\x65 with length 2.
    """

    s = bytearray()
    for f in [str(i) for i in sorted(bm)]:
        # Secondary bitmap is already appended
        if f == "1":
            continue

        # BCD data is always half of ASCII/EBCDIC data
        if data_enc == "b":
            spec[f]["max_len"] = 2
        else:
            spec[f]["max_len"] = 4

        spec[f]["data_enc"] = data_enc
        spec[f]["len_enc"] = len_enc
        spec[f]["len_type"] = len_type

        # Append length according to type and encoding
        if len_type > 0:
            if len_enc == "b":
                # odd length is not allowed, double it up for string translation, e.g.:
                # length "2" must be "02" to translate to \x02
                # length "02" must be "0004" to translate to \x00\x02
                s += bytearray.fromhex(
                    "{:0{len_type}d}".format(spec[f]["max_len"], len_type=len_type * 2)
                )
            else:
                s += bytearray(
                    "{:0{len_type}d}".format(spec[f]["max_len"], len_type=len_type),
                    len_enc,
                )

        # Append data according to encoding
        if data_enc == "b":
            s += bytearray.fromhex("{:04d}".format(int(f)))
        else:
            s += bytearray("{:04d}".format(int(f)), data_enc)

    return s


def test_primary_bitmap_ascii():
    """
    This test will validate bitmap decoding for fields 1-64
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "ascii")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])

    bm = set()
    for i in range(64, 2, -1):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "ascii")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


def test_primary_bitmap_ascii_mixed_case():
    """
    This test makes sure that lower, upper and mixed case bitmap is
    decoded the same way.
    """
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["5"]["len_type"] = 0
    spec["5"]["max_len"] = 1
    spec["5"]["data_enc"] = "ascii"
    spec["7"]["len_type"] = 0
    spec["7"]["max_len"] = 1
    spec["7"]["data_enc"] = "ascii"
    spec["9"]["len_type"] = 0
    spec["9"]["max_len"] = 1
    spec["9"]["data_enc"] = "ascii"
    spec["11"]["len_type"] = 0
    spec["11"]["max_len"] = 1
    spec["11"]["data_enc"] = "ascii"

    # Upper case
    s = b"02000AA0000000000000ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "0AA0000000000000"
    assert doc_dec["5"] == "A"
    assert doc_dec["7"] == "B"
    assert doc_dec["9"] == "C"
    assert doc_dec["11"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"0AA0000000000000"
    assert doc_enc["5"]["data"] == b"A"
    assert doc_enc["7"]["data"] == b"B"
    assert doc_enc["9"]["data"] == b"C"
    assert doc_enc["11"]["data"] == b"D"

    # Mixed case
    s = b"02000Aa0000000000000ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "0Aa0000000000000"
    assert doc_dec["5"] == "A"
    assert doc_dec["7"] == "B"
    assert doc_dec["9"] == "C"
    assert doc_dec["11"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"0Aa0000000000000"
    assert doc_enc["5"]["data"] == b"A"
    assert doc_enc["7"]["data"] == b"B"
    assert doc_enc["9"]["data"] == b"C"
    assert doc_enc["11"]["data"] == b"D"

    # Lower case
    s = b"02000aa0000000000000ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "0aa0000000000000"
    assert doc_dec["5"] == "A"
    assert doc_dec["7"] == "B"
    assert doc_dec["9"] == "C"
    assert doc_dec["11"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"0aa0000000000000"
    assert doc_enc["5"]["data"] == b"A"
    assert doc_enc["7"]["data"] == b"B"
    assert doc_enc["9"]["data"] == b"C"
    assert doc_enc["11"]["data"] == b"D"


def test_primary_bitmap_ebcdic():
    """
    This test will validate bitmap decoding for fields 1-64
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "cp500"

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "cp500")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])

    bm = set()
    for i in range(64, 2, -1):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "cp500")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


def test_primary_bitmap_bcd():
    """
    This test will validate bitmap decoding for fields 1-64
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        s = bytearray(b"header0210")
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])

    bm = set()
    for i in range(64, 2, -1):
        bm.add(i)
        s = bytearray(b"header0210")
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


def test_primary_bitmap_negative_missing():
    """
    Primary bitmap is required for all messages
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0200"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 16: field p pos 10"
    ):
        iso8583.decode(s, spec=spec)


def test_primary_bitmap_negative_partial():
    """
    Primary bitmap is required for all messages but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0200FFFF"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 4 bytes, expecting 16: field p pos 10"
    ):
        iso8583.decode(s, spec=spec)


def test_primary_bitmap_negative_incorrect_encoding():
    """
    Primary bitmap is required for all messages and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "invalid"

    s = b"header02100000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field p pos 10",
    ):
        iso8583.decode(s, spec=spec)


def test_primary_bitmap_negative_incorrect_ascii_data():
    """
    Primary bitmap is required for all messages and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0210\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field p pos 10",
    ):
        iso8583.decode(s, spec=spec)


def test_primary_bitmap_negative_incorrect_ascii_hex():
    """
    Primary bitmap is required for all messages and provided.
    However, the data is not ASCII hex
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0210incorrecthexdata"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .non-hexadecimal number found in fromhex.. arg at position 0.: field p pos 10",
    ):
        iso8583.decode(s, spec=spec)


def test_primary_bitmap_negative_incorrect_bcd_data():
    """
    BCD primary bitmap is required for all messages and provided.
    However, the data is not hex.
    Note: this passes, "00000000" is valid hex data when decoding.
    It will fail on field parsing, because no fields were provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["3"]["data_enc"] = "ascii"
    spec["3"]["len_enc"] = "ascii"
    spec["3"]["len_type"] = 0
    spec["3"]["max_len"] = 4

    s = b"header021000000000"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 4: field 3 pos 18"
    ):
        iso8583.decode(s, spec=spec)


def test_primary_bitmap_negative_leftover_data():
    """
    Primary bitmap is required by spec and provided.
    However, there is extra data left in message.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    s = b"header0210000000000000000012"
    with pytest.raises(
        iso8583.DecodeError, match="Extra data after last field: field p pos 26"
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_ascii():
    """
    This test will validate bitmap decoding for field 1-128
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    bm = set()
    for i in range(1, 129):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "ascii")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])

    bm = set()
    for i in range(128, 1, -1):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "ascii")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


def test_secondary_bitmap_ascii_mixed_case():
    """
    This test makes sure that lower, upper and mixed case bitmap is
    decoded the same way.
    """
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    spec["69"]["len_type"] = 0
    spec["69"]["max_len"] = 1
    spec["69"]["data_enc"] = "ascii"
    spec["71"]["len_type"] = 0
    spec["71"]["max_len"] = 1
    spec["71"]["data_enc"] = "ascii"
    spec["73"]["len_type"] = 0
    spec["73"]["max_len"] = 1
    spec["73"]["data_enc"] = "ascii"
    spec["75"]["len_type"] = 0
    spec["75"]["max_len"] = 1
    spec["75"]["data_enc"] = "ascii"

    # Upper case
    s = b"020080000000000000000AA0000000000000ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "8000000000000000"
    assert doc_dec["1"] == "0AA0000000000000"
    assert doc_dec["69"] == "A"
    assert doc_dec["71"] == "B"
    assert doc_dec["73"] == "C"
    assert doc_dec["75"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_enc["1"]["data"] == b"0AA0000000000000"
    assert doc_enc["69"]["data"] == b"A"
    assert doc_enc["71"]["data"] == b"B"
    assert doc_enc["73"]["data"] == b"C"
    assert doc_enc["75"]["data"] == b"D"

    # Mixed case
    s = b"020080000000000000000Aa0000000000000ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "8000000000000000"
    assert doc_dec["1"] == "0Aa0000000000000"
    assert doc_dec["69"] == "A"
    assert doc_dec["71"] == "B"
    assert doc_dec["73"] == "C"
    assert doc_dec["75"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_enc["1"]["data"] == b"0Aa0000000000000"
    assert doc_enc["69"]["data"] == b"A"
    assert doc_enc["71"]["data"] == b"B"
    assert doc_enc["73"]["data"] == b"C"
    assert doc_enc["75"]["data"] == b"D"

    # Lower case
    s = b"020080000000000000000aa0000000000000ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "8000000000000000"
    assert doc_dec["1"] == "0aa0000000000000"
    assert doc_dec["69"] == "A"
    assert doc_dec["71"] == "B"
    assert doc_dec["73"] == "C"
    assert doc_dec["75"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_enc["1"]["data"] == b"0aa0000000000000"
    assert doc_enc["69"]["data"] == b"A"
    assert doc_enc["71"]["data"] == b"B"
    assert doc_enc["73"]["data"] == b"C"
    assert doc_enc["75"]["data"] == b"D"


def test_secondary_bitmap_ebcdic():
    """
    This test will validate bitmap decoding for field 1-128
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "cp500"
    spec["1"]["data_enc"] = "cp500"

    bm = set()
    for i in range(1, 129):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "cp500")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])

    bm = set()
    for i in range(128, 1, -1):
        bm.add(i)
        s = bytearray(b"header0210")
        s += bytearray(util_set2bitmap(bm).hex(), "cp500")
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


def test_secondary_bitmap_bcd():
    """
    This test will validate bitmap decoding for field 1-128
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["1"]["data_enc"] = "b"

    bm = set()
    for i in range(1, 129):
        bm.add(i)
        s = bytearray(b"header0210")
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])

    bm = set()
    for i in range(128, 1, -1):
        bm.add(i)
        s = bytearray(b"header0210")
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


def test_secondary_bitmap_negative_missing():
    """
    Secondary bitmap is required but not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    s = b"header02008000000000000000"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 16: field 1 pos 26"
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_negative_partial():
    """
    Secondary bitmap is required for all messages but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    s = b"header02008000000000000000FFFF"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 4 bytes, expecting 16: field 1 pos 26"
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_negative_incorrect_encoding():
    """
    Secondary bitmap is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "invalid"

    s = b"header021080000000000000000000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field 1 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_negative_incorrect_ascii_data():
    """
    Secondary bitmap is required for all messages and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    s = b"header02108000000000000000\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field 1 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_negative_incorrect_ascii_hex():
    """
    Secondary bitmap is required for all messages and provided.
    However, the data is not ASCII hex
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    s = b"header02108000000000000000incorrecthexdata"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .non-hexadecimal number found in fromhex.. arg at position 0.: field 1 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_negative_incorrect_bcd_data():
    """
    BCD secondary bitmap is required for all messages and provided.
    However, the data is not hex.
    Note: this passes, "00000000" is valid hex data when decoding.
    It will fail on field parsing, because no fields were provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "b"
    spec["67"]["len_enc"] = "ascii"
    spec["67"]["data_enc"] = "ascii"
    spec["67"]["len_type"] = 0
    spec["67"]["max_len"] = 4

    s = b"header0210800000000000000000000000"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 4: field 67 pos 34"
    ):
        iso8583.decode(s, spec=spec)


def test_secondary_bitmap_negative_leftover_data():
    """
    Secondary bitmap is required by spec and provided.
    However, there is extra data left in message.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"

    s = b"header02108000000000000000000000000000000012"
    with pytest.raises(
        iso8583.DecodeError, match="Extra data after last field: field 1 pos 42"
    ):
        iso8583.decode(s, spec=spec)


def test_fields_mix():
    """
    This test will validate field decoding with BCD, ASCII and EBCDIC mix
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["1"]["data_enc"] = "b"

    field_lenght = [0, 1, 2, 3, 4]
    encoding = ["b", "ascii", "cp500"]

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        for l in field_lenght:
            for data_e in encoding:
                for len_e in encoding:
                    s = bytearray(b"0210")
                    s += util_set2bitmap(bm)
                    s += util_set2field_data(bm, spec, data_e, len_e, l)

                    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

                    assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["t", "p"])
                    assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["t", "p"])

                    for f in [k for k in doc_dec.keys() if k.isnumeric()]:
                        if f == "1":
                            continue
                        assert doc_dec[f] == "{0:04}".format(int(f))

    bm = set()
    for i in range(65, 129):
        bm.add(i)
        for l in field_lenght:
            for data_e in encoding:
                for len_e in encoding:
                    s = bytearray(b"0210")
                    s += util_set2bitmap(bm)
                    s += util_set2field_data(bm, spec, data_e, len_e, l)

                    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

                    assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["t", "p"])
                    assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["t", "p"])

                    for f in [k for k in doc_dec.keys() if k.isnumeric()]:
                        if f == "1":
                            continue
                        assert doc_dec[f] == "{0:04}".format(int(f))


def test_field_zero_length_field():
    """
    Zero-length field is required and provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header0210400000000000000000"

    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"4000000000000000"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"00"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == {"h", "t", "p", "2"}
    assert doc_dec.keys() == {"h", "t", "p", "2"}


def test_field_length_negative_missing():
    """
    Field length is required but not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header02004000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field length is 0 bytes wide, expecting 2: field 2 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_partial():
    """
    Field length is required but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header020040000000000000001"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field length is 1 bytes wide, expecting 2: field 2 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_incorrect_encoding():
    """
    Field length is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "invalid"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header0200400000000000000010"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .unknown encoding: invalid.: field 2 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_incorrect_ascii_data():
    """
    Field length is required and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header02004000000000000000\xff\xff"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field 2 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_incorrect_not_numeric():
    """
    Field length is required and provided.
    However, the length is not numeric ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header02004000000000000000gg"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .invalid literal for int.. with base 10: 'gg'.: field 2 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_incorrect_bcd_data():
    """
    BCD field length is required and provided.
    However, the data is not hex.
    Note: this passes, "g" is valid hex data when decoding.
    It will fail on field parsing, because no field was provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "b"
    spec["2"]["len_type"] = 1
    spec["2"]["max_len"] = 99

    s = b"header02004000000000000000g"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 67: field 2 pos 27"
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_leftover_data():
    """
    Field length is required and provided.
    However, there is extra data left in message.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header02104000000000000000003456"
    with pytest.raises(
        iso8583.DecodeError, match="Extra data after last field: field 2 pos 28"
    ):
        iso8583.decode(s, spec=spec)


def test_field_length_negative_over_max():
    """
    Field length is required and provided.
    However, it's over the specified maximum.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 1
    spec["2"]["max_len"] = 4

    s = b"header020040000000000000008"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 8 bytes, larger than maximum 4: field 2 pos 26",
    ):
        iso8583.decode(s, spec=spec)


def test_field_negative_missing():
    """
    Field is required but not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header0200400000000000000002"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 0 bytes, expecting 2: field 2 pos 28"
    ):
        iso8583.decode(s, spec=spec)


def test_field_negative_partial():
    """
    Field is required but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header02004000000000000000021"
    with pytest.raises(
        iso8583.DecodeError, match="Field data is 1 bytes, expecting 2: field 2 pos 28"
    ):
        iso8583.decode(s, spec=spec)


def test_field_negative_incorrect_encoding():
    """
    Field is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "invalid"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header0200400000000000000002xx"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field 2 pos 28",
    ):
        iso8583.decode(s, spec=spec)


def test_field_negative_incorrect_ascii_data():
    """
    Field is required and provided.
    However, the data is not ASCII
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header0200400000000000000002\xff\xff"
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field 2 pos 28",
    ):
        iso8583.decode(s, spec=spec)


def test_field_negative_incorrect_ascii_hex():
    """
    Field is required and provided.
    However, the data is not ASCII hex
    Note: this passes, "gg" is valid hex data when decoding.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4

    s = b"header0210400000000000000002gg"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"4000000000000000"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"02"
    assert doc_enc["2"]["data"] == b"gg"
    assert doc_dec["2"] == "gg"

    assert doc_enc.keys() == {"h", "t", "p", "2"}
    assert doc_dec.keys() == {"h", "t", "p", "2"}


def test_field_negative_incorrect_bcd_data():
    """
    BCD Field is required and provided.
    However, the data is not hex.
    Note: this passes, "g" is valid hex data when decoding.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "b"
    spec["2"]["len_type"] = 1
    spec["2"]["max_len"] = 99

    s = b"header02104000000000000000\x01g"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"4000000000000000"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\x01"
    assert doc_enc["2"]["data"] == b"g"
    assert doc_dec["2"] == "g"

    assert doc_enc.keys() == {"h", "t", "p", "2"}
    assert doc_dec.keys() == {"h", "t", "p", "2"}


def test_field_negative_leftover_data():
    """
    Field is required and provided.
    However, there is extra data left in message.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 4

    s = b"header02004000000000000000123456"
    with pytest.raises(
        iso8583.DecodeError, match="Extra data after last field: field 2 pos 30"
    ):
        iso8583.decode(s, spec=spec)
