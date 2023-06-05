import copy
import pickle

import iso8583
import iso8583.specs
import pytest
import typing


def test_DecodeError_exception() -> None:
    """
    Validate DecodeError class
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_DecodeError_exception_pickle() -> None:
    """
    Validate DecodeError class with pickle
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_input_type() -> None:
    """
    Decode accepts only bytes or bytesarray.
    """
    spec = copy.deepcopy(iso8583.specs.default)
    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not dict"
    ):
        iso8583.decode({}, spec=spec)  # type: ignore

    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not list"
    ):
        iso8583.decode([], spec=spec)  # type: ignore

    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not tuple"
    ):
        iso8583.decode((0, 0), spec=spec)  # type: ignore

    with pytest.raises(
        TypeError, match="Encoded ISO8583 data must be bytes or bytearray, not str"
    ):
        iso8583.decode("spam", spec=spec)  # type: ignore


def test_header_ascii_absent() -> None:
    """
    ASCII header is not required by spec and not provided
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_header_ascii_present() -> None:
    """
    ASCII header is required by spec and provided
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


# fmt: off
@pytest.mark.parametrize(
    ["type_data", "type_data_decoded", "type_enc"],
    [
        (b"0210", "0210", "ascii"),
        (b"ABCD", "ABCD", "ascii"),
        (b"\xf0\xf2\xf1\xf0", "0210", "cp500"),
        (b"\x02\x10", "0210", "b"),
        (b"\xab\xcd", "ABCD", "b"),
    ]
)
# fmt: on
def test_type_decoding(
    type_data: bytes,
    type_data_decoded: str,
    type_enc: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = type_enc
    spec["p"]["data_enc"] = "ascii"

    s = type_data + b"0000000000000000"
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == type_data
    assert doc_dec["t"] == type_data_decoded

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"0000000000000000"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["t", "p"])


# fmt: off
@pytest.mark.parametrize(
    ["data", "type_enc", "expected_error"],
    [
        (b"\xff\xff\xff\xff0000000000000000", "ascii", "Failed to decode field, invalid data: field t pos 0"),
        (b"02100000000000000000", "invalid_encoding", "Failed to decode field, unknown encoding specified: field t pos 0"),
        (b"02", "ascii", "Field data is 2 bytes, expecting 4: field t pos 0"),
        (b"", "ascii", "Field data is 0 bytes, expecting 4: field t pos 0"),
    ]
)
# fmt: on
def test_type_decoding_negative(
    data: bytes,
    type_enc: str,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = type_enc
    spec["p"]["data_enc"] = "ascii"

    with pytest.raises(iso8583.DecodeError) as e:
        iso8583.decode(data, spec=spec)
    assert e.value.args[0] == expected_error


def util_set2bitmap(bm: typing.Set[int]) -> bytearray:
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


def util_set2field_data(
    bm: typing.Set[int],
    spec: typing.Mapping[str, typing.MutableMapping[str, typing.Any]],
    data_enc: str,
    len_enc: str,
    len_type: int,
) -> bytearray:
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

        # Binary data is always half of ASCII/EBCDIC data
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
                s += (spec[f]["max_len"]).to_bytes(len_type, "big", signed=False)
            elif len_enc == "bcd":
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


# fmt: off
@pytest.mark.parametrize(
    ["bitmap_data", "bitmap_data_decoded"],
    [
        (b"0AA0000000000000", "0AA0000000000000"), # Upper case
        (b"0Aa0000000000000", "0Aa0000000000000"), # Mixed case
        (b"0aa0000000000000", "0aa0000000000000"), # Lower case
    ]
)
# fmt: on
def test_primary_bitmap_ascii_mixed_case(
    bitmap_data: bytes,
    bitmap_data_decoded: str,
) -> None:
    """
    This test makes sure that lower, upper and mixed case bitmap is
    decoded the same way.
    """
    spec = copy.deepcopy(iso8583.specs.default_ascii)
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

    s = b"0200" + bitmap_data + b"ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == bitmap_data_decoded
    assert doc_dec["5"] == "A"
    assert doc_dec["7"] == "B"
    assert doc_dec["9"] == "C"
    assert doc_dec["11"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == bitmap_data
    assert doc_enc["5"]["data"] == b"A"
    assert doc_enc["7"]["data"] == b"B"
    assert doc_enc["9"]["data"] == b"C"
    assert doc_enc["11"]["data"] == b"D"


# fmt: off
@pytest.mark.parametrize(
    ["bitmap_enc", "start", "stop", "step"],
    [
        ("ascii", 2, 65, 1),
        ("cp500", 2, 65, 1),
        ("b", 2, 65, 1),
        ("ascii", 64, 2, -1),
        ("cp500", 64, 2, -1),
        ("b", 64, 2, -1),
    ]
)
# fmt: on
def test_primary_bitmap_decoding(
    bitmap_enc: str,
    start: int,
    stop: int,
    step: int,
) -> None:
    """This test will validate bitmap decoding for fields 1-64"""
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = bitmap_enc

    bm = set()
    for i in range(start, stop, step):
        bm.add(i)
        s = bytearray(b"header0210")
        if bitmap_enc == "b":
            s += util_set2bitmap(bm)
        else:
            s += bytearray(util_set2bitmap(bm).hex(), bitmap_enc)
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


# fmt: off
@pytest.mark.parametrize(
    ["bitmap_data", "bitmap_enc", "expected_error"],
    [
        # Primary bitmap does not enable any field - extra data present
        (b"0000000000000000extra", "ascii", "Extra data after last field: field p pos 20"),
        (b"incorrecthexdata", "ascii", "Failed to decode field, non-hex data: field p pos 4"),
        # Non-ascii data
        (b"\xff000000000000000", "ascii", "Failed to decode field, invalid data: field p pos 4"),
        (b"0000000000000000", "invalid_encoding", "Failed to decode field, unknown encoding specified: field p pos 4"),
        # Partial data
        (b"0000", "ascii", "Field data is 4 bytes, expecting 16: field p pos 4"),
        (b"", "ascii", "Field data is 0 bytes, expecting 16: field p pos 4"),
    ]
)
# fmt: on
def test_primary_bitmap_decoding_negative(
    bitmap_data: bytes,
    bitmap_enc: str,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = bitmap_enc

    s = b"0210" + bitmap_data
    with pytest.raises(iso8583.DecodeError) as e:
        iso8583.decode(s, spec=spec)
    assert e.value.args[0] == expected_error


# fmt: off
@pytest.mark.parametrize(
    ["bitmap_data", "bitmap_data_decoded"],
    [
        (b"0AA0000000000000", "0AA0000000000000"), # Upper case
        (b"0Aa0000000000000", "0Aa0000000000000"), # Mixed case
        (b"0aa0000000000000", "0aa0000000000000"), # Lower case
    ]
)
# fmt: on
def test_secondary_bitmap_ascii_mixed_case(
    bitmap_data: bytes,
    bitmap_data_decoded: str,
) -> None:
    """
    This test makes sure that lower, upper and mixed case bitmap is
    decoded the same way.
    """
    spec = copy.deepcopy(iso8583.specs.default_ascii)
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

    s = b"02008000000000000000" + bitmap_data + b"ABCD"
    doc_dec, doc_enc = iso8583.decode(s, spec)
    assert doc_dec["t"] == "0200"
    assert doc_dec["p"] == "8000000000000000"
    assert doc_dec["1"] == bitmap_data_decoded
    assert doc_dec["69"] == "A"
    assert doc_dec["71"] == "B"
    assert doc_dec["73"] == "C"
    assert doc_dec["75"] == "D"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_enc["1"]["data"] == bitmap_data
    assert doc_enc["69"]["data"] == b"A"
    assert doc_enc["71"]["data"] == b"B"
    assert doc_enc["73"]["data"] == b"C"
    assert doc_enc["75"]["data"] == b"D"


# fmt: off
@pytest.mark.parametrize(
    ["bitmap_enc", "start", "stop", "step"],
    [
        ("ascii", 1, 129, 1),
        ("cp500", 1, 129, 1),
        ("b", 1, 129, 1),
        ("ascii", 128, 1, -1),
        ("cp500", 128, 1, -1),
        ("b", 128, 1, -1),
    ]
)
# fmt: on
def test_secondary_bitmap_decoding(
    bitmap_enc: str,
    start: int,
    stop: int,
    step: int,
) -> None:
    """This test will validate bitmap decoding for field 1-128"""
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = bitmap_enc
    spec["1"]["data_enc"] = bitmap_enc

    bm = set()
    for i in range(start, stop, step):
        bm.add(i)
        s = bytearray(b"header0210")
        if bitmap_enc == "b":
            s += util_set2bitmap(bm)
        else:
            s += bytearray(util_set2bitmap(bm).hex(), bitmap_enc)
        s += util_set2field_data(bm, spec, "ascii", "ascii", 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])
        assert doc_dec.keys() ^ set([str(f) for f in bm]) == set(["h", "t", "p"])


# fmt: off
@pytest.mark.parametrize(
    ["bitmap_data", "bitmap_enc", "expected_error"],
    [
        # Secondary bitmap does not enable any field - extra data present
        (b"0000000000000000extra", "ascii", "Extra data after last field: field 1 pos 36"),
        (b"incorrecthexdata", "ascii", "Failed to decode field, non-hex data: field 1 pos 20"),
        # Non-ascii data
        (b"\xff000000000000000", "ascii", "Failed to decode field, invalid data: field 1 pos 20"),
        (b"0000000000000000", "invalid_encoding", "Failed to decode field, unknown encoding specified: field 1 pos 20"),
        # Partial data
        (b"0000", "ascii", "Field data is 4 bytes, expecting 16: field 1 pos 20"),
        (b"", "ascii", "Field data is 0 bytes, expecting 16: field 1 pos 20"),
    ]
)
# fmt: on
def test_secondary_bitmap_decoding_negative(
    bitmap_data: bytes,
    bitmap_enc: str,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = bitmap_enc

    s = b"02108000000000000000" + bitmap_data
    with pytest.raises(iso8583.DecodeError) as e:
        iso8583.decode(s, spec=spec)
    assert e.value.args[0] == expected_error


def test_fields_mix() -> None:
    """
    This test will validate field decoding with BCD, ASCII and EBCDIC mix
    """
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["1"]["data_enc"] = "b"

    field_lenght = [0, 1, 2, 3, 4]
    data_encoding = ["b", "ascii", "cp500"]
    length_encoding = ["b", "bcd", "ascii", "cp500"]

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        for l in field_lenght:
            for data_e in data_encoding:
                for len_e in length_encoding:
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
            for data_e in data_encoding:
                for len_e in length_encoding:
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


# fmt: off
@pytest.mark.parametrize(
    ["data", "data_enc", "len_type", "max_len", "len_enc", "expected_data"],
    [
        (b"", "ascii", 0, 0, "ascii", ""),
        (b"12", "ascii", 0, 2, "ascii", "12"),
        (b"0", "ascii", 1, 2, "ascii", ""),
        (b"212", "ascii", 1, 2, "ascii", "12"),
    ]
)
# fmt: on
def test_field_decoding(
    data: bytes,
    data_enc: str,
    len_type: int,
    max_len: int,
    len_enc: str,
    expected_data: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = data_enc
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len

    doc_dec, doc_enc = iso8583.decode(b"02004000000000000000" + data, spec=spec)

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"4000000000000000"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc.keys() == {"t", "p", "2"}
    assert doc_dec.keys() == {"t", "p", "2"}

    assert doc_enc["2"]["len"] == data[:len_type]
    assert doc_enc["2"]["data"] == data[len_type:]
    assert doc_dec["2"] == expected_data


# fmt: off
@pytest.mark.parametrize(
    ["data", "data_enc", "len_type", "max_len", "len_enc", "expected_error"],
    [
        # Trailing data
        (b"123456", "ascii", 0, 4, "ascii", "Extra data after last field: field 2 pos 24"),
        (b"412345", "ascii", 1, 17, "ascii", "Extra data after last field: field 2 pos 25"),
        (b"012345", "ascii", 1, 17, "ascii", "Extra data after last field: field 2 pos 21"),
        (b"\x1612345678901234567", "ascii", 1, 17, "bcd", "Extra data after last field: field 2 pos 37"),
        (b"\x0012345678901234567", "ascii", 1, 17, "bcd", "Extra data after last field: field 2 pos 21"),
        (b"\x1012345678901234567", "ascii", 1, 17, "b", "Extra data after last field: field 2 pos 37"),
        (b"\x0012345678901234567", "ascii", 1, 17, "b", "Extra data after last field: field 2 pos 21"),
        # Partial data
        (b"12345", "ascii", 0, 6, "ascii", "Field data is 5 bytes, expecting 6: field 2 pos 20"),
        (b"612345", "ascii", 1, 6, "ascii", "Field data is 5 bytes, expecting 6: field 2 pos 21"),
        (b"\x1612345", "ascii", 1, 17, "bcd", "Field data is 5 bytes, expecting 16: field 2 pos 21"),
        (b"\x1012345", "ascii", 1, 17, "b", "Field data is 5 bytes, expecting 16: field 2 pos 21"),
        # No data
        (b"", "ascii", 0, 6, "ascii", "Field data is 0 bytes, expecting 6: field 2 pos 20"),
        (b"6", "ascii", 1, 6, "ascii", "Field data is 0 bytes, expecting 6: field 2 pos 21"),
        (b"\x16", "ascii", 1, 16, "bcd", "Field data is 0 bytes, expecting 16: field 2 pos 21"),
        (b"\x10", "ascii", 1, 16, "b", "Field data is 0 bytes, expecting 16: field 2 pos 21"),
        # Field data over max
        (b"7", "ascii", 1, 6, "ascii", "Field data is 7 bytes, larger than maximum 6: field 2 pos 20"),
        (b"7123456", "ascii", 1, 6, "ascii", "Field data is 7 bytes, larger than maximum 6: field 2 pos 20"),
        (b"\x16123456", "ascii", 1, 15, "bcd", "Field data is 16 bytes, larger than maximum 15: field 2 pos 20"),
        (b"\x10123456", "ascii", 1, 15, "b", "Field data is 16 bytes, larger than maximum 15: field 2 pos 20"),
        # Incorrect encoding
        (b"123456", "invalid", 0, 6, "ascii", "Failed to decode field, unknown encoding specified: field 2 pos 20"),
        (b"5123456", "ascii", 1, 15, "invalid", "Failed to decode field length, unknown encoding specified: field 2 pos 20"),
        # Partial field length
        (b"", "ascii", 1, 17, "ascii", "Field length is 0 bytes wide, expecting 1: field 2 pos 20"),
        (b"1", "ascii", 2, 17, "ascii", "Field length is 1 bytes wide, expecting 2: field 2 pos 20"),
        # Other conditions
        (b"02\xff\xff", "ascii", 2, 4, "ascii", "Failed to decode field, invalid data: field 2 pos 22"),
        (b"g123456", "ascii", 1, 15, "ascii", "Failed to decode field length, non-numeric data: field 2 pos 20"),
        (b"\xff123456", "ascii", 1, 15, "ascii", "Failed to decode field length, invalid data: field 2 pos 20"),
        (b"\x0a123456", "ascii", 1, 15, "bcd", "Failed to decode field length, invalid BCD data: field 2 pos 20"),
    ]
)
# fmt: on
def test_field_decoding_negative(
    data: bytes,
    data_enc: str,
    len_type: int,
    max_len: int,
    len_enc: str,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["data_enc"] = data_enc
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    with pytest.raises(iso8583.DecodeError) as e:
        iso8583.decode(b"02004000000000000000" + data, spec=spec)
    assert e.value.args[0] == expected_error
