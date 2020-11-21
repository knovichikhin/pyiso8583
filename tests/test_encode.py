import copy
import pickle

import iso8583
import iso8583.specs
import pytest

spec = copy.deepcopy(iso8583.specs.default)


def test_EncodeError_exception():
    """
    Validate EncodeError class
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"t": ""}

    try:
        iso8583.encode(doc_dec, spec=spec)
    except iso8583.EncodeError as e:
        assert e.doc_dec == doc_dec
        assert e.doc_enc == ({})
        assert e.msg == "Field data is required according to specifications"
        assert e.field == "h"
        assert (
            e.args[0] == "Field data is required according to specifications: field h"
        )


def test_EncodeError_exception_pickle():
    """
    Validate EncodeError class with pickle
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"t": ""}

    try:
        iso8583.encode(doc_dec, spec=spec)
    except iso8583.EncodeError as e:
        p = pickle.dumps(e)
        e_unpickled = pickle.loads(p)

        assert e.doc_dec == e_unpickled.doc_dec
        assert e.doc_enc == e_unpickled.doc_enc
        assert e.msg == e_unpickled.msg
        assert e.field == e_unpickled.field
        assert e.args[0] == e_unpickled.args[0]


def test_non_string_field_keys():
    """
    Input dictionary contains non
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["3"]["len_type"] = 2
    spec["3"]["max_len"] = 10
    spec["3"]["data_enc"] = "ascii"
    spec["3"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", 2: "1122"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec = {"h": "header", "t": "0210", 2: "1122", 3: "3344"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2, 3.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec = {"h": "header", "t": "0210", 2.5: "1122", 3.5: "3344"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2.5, 3.5.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec = {"h": "header", "t": "0210", 2.5: "1122", 3.5: "3344"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2.5, 3.5.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec = {"h": "header", "t": "0210", (1, 2): "1122", (3, 4): "3344"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields ..1, 2., .3, 4..: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_input_type():
    """
    Encode accepts only dict.
    """
    s = b""
    with pytest.raises(TypeError, match="Decoded ISO8583 data must be dict, not bytes"):
        iso8583.encode(s, spec=spec)


def test_header_no_key():
    """
    Message header is required and key is not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"t": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is required according to specifications: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_ascii_absent():
    """
    ASCII header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_ascii_present():
    """
    ASCII header is required by spec and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
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
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_ebcdic_present():
    """
    EBCDIC header is required by spec and provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\x88\x85\x81\x84\x85\x990200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"\x88\x85\x81\x84\x85\x99"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_bdc_absent():
    """
    BDC header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_bcd_present():
    """
    BCD header is required by spec and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "A1A2A3A4A5A6", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xA1\xA2\xA3\xA4\xA5\xA60200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"\xA1\xA2\xA3\xA4\xA5\xA6"
    assert doc_dec["h"] == "A1A2A3A4A5A6"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_not_required_provided():
    """
    String header is not required by spec but provided.
    No error. Header is not included in the message.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_header_negative_missing():
    """
    String header is required by spec but not provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 6: field h"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_partial():
    """
    String header is required by spec but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "head", "t": "0200"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 4 bytes, expecting 6: field h"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_incorrect_encoding():
    """
    String header is required by spec and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "invalid"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_incorrect_ascii_data():
    """
    ASCII header is required by spec and provided.
    However, the data is not ASCII
    CPython and PyPy throw differently worded exception
    CPython: 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)
    PyPy:    'ascii' codec can't encode character '\\xff' in position 0: ordinal not in range(128)
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {
        "h": b"\xff\xff\xff\xff\xff\xff".decode("latin-1"),
        "t": "0200",
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode character.*: ordinal not in range.128..: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_incorrect_bcd_data():
    """
    BCD header is required by spec and provided.
    However, the data is not hex
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 0.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_ascii_over_max():
    """
    ASCII variable header is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    doc_dec = {"h": "header12", "t": "0210"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 8 bytes, larger than maximum 6: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_ascii_present():
    """
    ASCII variable header is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"06header0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"06"
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_ascii_present_zero_legnth():
    """
    ASCII zero-length variable header
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"000210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"00"
    assert doc_enc["h"]["data"] == b""
    assert doc_dec["h"] == ""

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_ebcdic_over_max():
    """
    EBCDIC variable header is required and over max provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    doc_dec = {"h": "header1", "t": "0210"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 7 bytes, larger than maximum 6: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_ebcdic_present():
    """
    EBCDIC variable header is required and provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xf0\xf6\x88\x85\x81\x84\x85\x990210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\xf0\xf6"
    assert doc_enc["h"]["data"] == b"\x88\x85\x81\x84\x85\x99"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_ebcdic_present_zero_legnth():
    """
    EBCDIC zero-length variable header
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xf0\xf00210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\xf0\xf0"
    assert doc_enc["h"]["data"] == b""
    assert doc_dec["h"] == ""

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_bdc_over_max():
    """
    BDC variable header is required and over max is provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 2
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcdef", "t": "0210"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 3 bytes, larger than maximum 2: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_bdc_odd():
    """
    BDC variable header is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 5
    PyPy:    non-hexadecimal number found in fromhex() arg at position 4
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcde", "t": "0210"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 4|5.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_bdc_ascii_length():
    """
    BDC variable header
    The length is in ASCII.
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 3
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"002\xab\xcd0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"002"
    assert doc_enc["h"]["data"] == b"\xab\xcd"
    assert doc_dec["h"] == "abcd"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_bdc_ebcdic_length():
    """
    BDC variable header is required and provided
    The length is in EBCDIC.
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 3
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xf0\xf0\xf2\xab\xcd0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\xf0\xf0\xf2"
    assert doc_enc["h"]["data"] == b"\xab\xcd"
    assert doc_dec["h"] == "abcd"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_bcd_present():
    """
    BCD variable header is required and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\x00\x02\xab\xcd0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\x00\x02"
    assert doc_enc["h"]["data"] == b"\xab\xcd"
    assert doc_dec["h"] == "abcd"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_bcd_present_zero_length():
    """
    BCD zero-length variable header is required and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0210"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\x00\x000210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\x00\x00"
    assert doc_enc["h"]["data"] == b""
    assert doc_dec["h"] == ""

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_variable_header_incorrect_encoding():
    """
    variable header is required and provided.
    However, the spec encoding is not correct for length
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "invalid"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode length .unknown encoding: invalid.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_no_key():
    """
    Message type is required and key is not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"h": "header", "2": ""}

    with pytest.raises(iso8583.EncodeError, match="Field data is required: field t"):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_absent():
    """
    ASCII message type is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_partial():
    """
    ASCII message type is required and partial is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 2 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_over_max():
    """
    ASCII message type is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02101"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 5 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_incorrect_data():
    """
    ASCII message type is required and provided.
    However, the data is not ASCII
    CPython and PyPy throw differently worded exception
    CPython: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
    PyPy:    'ascii' codec can't encode character '\\xff' in position 0: ordinal not in range(128)
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {
        "h": "header",
        "t": b"\xff\xff\xff\xff".decode("latin-1"),
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode character.*: ordinal not in range.128..: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_present():
    """
    ASCII message type is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_ebcdic_absent():
    """
    EBCDIC message type is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ebcdic_partial():
    """
    EBCDIC message type is required and partial provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 2 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ebcdic_over_max():
    """
    EBCDIC message type is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02101"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 5 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ebcdic_present():
    """
    EBCDIC message type is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header\xf0\xf2\xf0\xf0\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"\xf0\xf2\xf0\xf0"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_bdc_absent():
    """
    BDC message type is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_partial():
    """
    BDC message type is required and partial is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_over_max():
    """
    BDC message type is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "021000"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_odd():
    """
    BDC message type is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 3
    PyPy:    non-hexadecimal number found in fromhex() arg at position 2
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "021"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 2|3.: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_non_hex():
    """
    BDC message type is required and provided
    However, the data is not hex
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "021x"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 3.: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bcd_present():
    """
    BCD message type is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"\x02\x00"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc.keys() == set(["h", "t", "p"])
    assert doc_dec.keys() == set(["h", "t", "p"])


def test_type_incorrect_encoding():
    """
    String message type is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "invalid"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_bitmap_range():
    """
    ISO8583 bitmaps must be between 1 and 128.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200"}

    doc_dec["0"] = ""
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains fields outside of 1-128 range .0.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    del doc_dec["0"]
    doc_dec["129"] = ""
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains fields outside of 1-128 range .129.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    for f in range(0, 130):
        doc_dec[str(f)] = ""
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains fields outside of 1-128 range .0, 129.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)

    for f in range(0, 131):
        doc_dec[str(f)] = ""
    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains fields outside of 1-128 range .0, 129, 130.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_bitmap_remove_secondary():
    """
    If 65-128 fields are not in bitmap then remove field 1.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 19

    doc_dec = {
        "h": "header",
        "t": "0200",
        "1": "not needed",
        "2": "1234567890",
    }

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0200\x40\x00\x00\x00\x00\x00\x00\x00101234567890"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"10"
    assert doc_enc["2"]["data"] == b"1234567890"
    assert doc_dec["2"] == "1234567890"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_bitmap_add_secondary():
    """
    If one of 65-128 fields are in bitmap then add field 1.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["66"]["data_enc"] = "ascii"
    spec["66"]["len_enc"] = "ascii"
    spec["66"]["len_type"] = 2
    spec["66"]["max_len"] = 19

    doc_dec = {
        "h": "header",
        "t": "0200",
        "66": "1234567890",
    }

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        s
        == b"header0200\x80\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00101234567890"
    )

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x80\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert doc_enc["1"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["1"] == "4000000000000000"

    assert doc_enc["66"]["len"] == b"10"
    assert doc_enc["66"]["data"] == b"1234567890"
    assert doc_dec["66"] == "1234567890"

    assert doc_enc.keys() == set(["h", "t", "p", "1", "66"])
    assert doc_dec.keys() == set(["h", "t", "p", "1", "66"])


def test_primary_bitmap_incorrect_encoding():
    """
    Incorrect encoding specified for primary bitmap
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "invalid"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_secondary_bitmap_incorrect_encoding():
    """
    Incorrect encoding specified for secondary bitmap
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 16
    spec["1"]["data_enc"] = "invalid"

    doc_dec = {"h": "header", "t": "0210", "65": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field 1",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_bitmaps_ascii():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"
    spec["105"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "105": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header021080000000000000000000000000800000000"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert doc_enc["1"]["data"] == b"0000000000800000"
    assert doc_dec["1"] == "0000000000800000"

    assert doc_enc["105"]["len"] == b"000"
    assert doc_enc["105"]["data"] == b""
    assert doc_dec["105"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "1", "105"])
    assert doc_dec.keys() == set(["h", "t", "p", "1", "105"])


def test_bitmaps_ebcidic():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "cp500"
    spec["1"]["data_enc"] = "cp500"
    spec["105"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "105": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        s
        == b"header0210\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xf0"
        + b"\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0"
        + b"\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf8\xf0\xf0\xf0\xf0\xf0000"
    )

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert (
        doc_enc["p"]["data"]
        == b"\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0"
    )
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert (
        doc_enc["1"]["data"]
        == b"\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf8\xf0\xf0\xf0\xf0\xf0"
    )
    assert doc_dec["1"] == "0000000000800000"

    assert doc_enc["105"]["len"] == b"000"
    assert doc_enc["105"]["data"] == b""
    assert doc_dec["105"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "1", "105"])
    assert doc_dec.keys() == set(["h", "t", "p", "1", "105"])


def test_bitmaps_bcd():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["1"]["data_enc"] = "b"
    spec["105"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "105": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        s
        == b"header0210\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00000"
    )

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x80\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert doc_enc["1"]["data"] == b"\x00\x00\x00\x00\x00\x80\x00\x00"
    assert doc_dec["1"] == "0000000000800000"

    assert doc_enc["105"]["len"] == b"000"
    assert doc_enc["105"]["data"] == b""
    assert doc_dec["105"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "1", "105"])
    assert doc_dec.keys() == set(["h", "t", "p", "1", "105"])


def test_primary_bitmap_ascii_upper_case():
    """
    This test makes sure that encoded primary bitmap is in upper case.
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

    doc_dec = {"t": "0200", "5": "A", "7": "B"}
    s, doc_enc = iso8583.encode(doc_dec, spec)
    assert s == b"02000A00000000000000AB"
    assert doc_dec["p"] == "0A00000000000000"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"0A00000000000000"
    assert doc_enc["5"]["data"] == b"A"
    assert doc_enc["7"]["data"] == b"B"


def test_secondary_bitmap_ascii_upper_case():
    """
    This test makes sure that encoded secondary bitmap is in upper case.
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

    doc_dec = {"t": "0200", "69": "A", "71": "B"}
    s, doc_enc = iso8583.encode(doc_dec, spec)
    assert s == b"020080000000000000000A00000000000000AB"
    assert doc_dec["p"] == "8000000000000000"
    assert doc_dec["1"] == "0A00000000000000"
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_enc["1"]["data"] == b"0A00000000000000"
    assert doc_enc["69"]["data"] == b"A"
    assert doc_enc["71"]["data"] == b"B"


def test_fixed_field_ascii_absent():
    """
    ASCII fixed field is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_partial():
    """
    ASCII fixed field is required and partially provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": "1"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_over_max():
    """
    ASCII fixed field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": "123"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_incorrect_data():
    """
    ASCII fixed field is required and provided.
    However, the data is not ASCII
    CPython and PyPy throw differently worded exception
    CPython: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
    PyPy:    'ascii' codec can't encode character '\\xff' in position 0: ordinal not in range(128)
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {
        "h": "header",
        "t": "0210",
        "2": b"\xff\xff".decode("latin-1"),
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode character.*: ordinal not in range.128..: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_present():
    """
    ASCII fixed field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": "22"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x0022"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b"22"
    assert doc_dec["2"] == "22"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_fixed_field_ascii_present_zero_legnth():
    """
    ASCII zero-length fixed field is required and provided
    This is pointless but should work.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 0
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_fixed_field_ebcdic_absent():
    """
    EBCDIC fixed field is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ebcdic_partial():
    """
    EBCDIC fixed field is required and partially provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": "1"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ebcdic_over_max():
    """
    EBCDIC fixed field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": "123"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ebcdic_present():
    """
    EBCDIC fixed field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": "22"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf2\xf2"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b"\xf2\xf2"
    assert doc_dec["2"] == "22"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_fixed_field_ebcdic_present_zero_legnth():
    """
    EBCDIC zero-length fixed field is required and provided
    This is pointless but should work.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 0
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_fixed_field_bdc_absent():
    """
    BDC fixed field is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_partial():
    """
    BDC fixed field is required and partial is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "12"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_over_max():
    """
    BDC fixed field is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "123456"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_odd():
    """
    BDC fixed field is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 5
    PyPy:    non-hexadecimal number found in fromhex() arg at position 4
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "12345"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 4|5.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_non_hex():
    """
    BDC fixed field is required and provided
    However, the data is not hex
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "11xx"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 2.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bcd_present():
    """
    BCD fixed field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_fixed_field_bcd_present_zero_length():
    """
    BCD zero-length fixed field is required and provided
    This is pointless but should work.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 0
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_fixed_field_incorrect_encoding():
    """
    Fixed field is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "invalid"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_ascii_over_max():
    """
    ASCII variable field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": "12345678901"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 11 bytes, larger than maximum 10: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_ascii_present():
    """
    ASCII variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00041122"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"04"
    assert doc_enc["2"]["data"] == b"1122"
    assert doc_dec["2"] == "1122"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_ascii_present_zero_legnth():
    """
    ASCII zero-length variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x0000"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"00"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_ebcdic_over_max():
    """
    EBCDIC variable field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "cp500"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": "12345678901"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 11 bytes, larger than maximum 10: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_ebcdic_present():
    """
    EBCDIC variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "cp500"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf4\xf1\xf1\xf2\xf2"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\xf0\xf4"
    assert doc_enc["2"]["data"] == b"\xf1\xf1\xf2\xf2"
    assert doc_dec["2"] == "1122"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_ebcdic_present_zero_legnth():
    """
    EBCDIC zero-length variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "cp500"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf0"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\xf0\xf0"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_bdc_over_max():
    """
    BDC variable field is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 5
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "123456789012"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 6 bytes, larger than maximum 5: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_bdc_odd():
    """
    BDC variable field is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 5
    PyPy:    non-hexadecimal number found in fromhex() arg at position 4
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "12345"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 4|5.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_bdc_ascii_length():
    """
    BDC variable field is required and provided
    The length is in ASCII.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 3
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00002\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"002"
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_bdc_ebcdic_length():
    """
    BDC variable field is required and provided
    The length is in EBCDIC.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 3
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf0\xf2\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\xf0\xf0\xf2"
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_bcd_present():
    """
    BCD variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\x00\x02\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\x00\x02"
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_bcd_present_zero_length():
    """
    BCD zero-length variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\x00\x00"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc.keys() == set(["h", "t", "p", "2"])
    assert doc_dec.keys() == set(["h", "t", "p", "2"])


def test_variable_field_incorrect_encoding():
    """
    Variable field is required and provided.
    However, the spec encoding is not correct for length
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "invalid"

    doc_dec = {"h": "header", "t": "0210", "2": "1122"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode length .unknown encoding: invalid.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)
