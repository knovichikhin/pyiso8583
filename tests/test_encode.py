import copy
import pickle
import typing

import iso8583
import iso8583.specs
import pytest


def test_EncodeError_exception() -> None:
    """
    Validate EncodeError class
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_EncodeError_exception_pickle() -> None:
    """
    Validate EncodeError class with pickle
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_non_string_field_keys() -> None:
    """
    Input dictionary contains non
    """
    spec = copy.deepcopy(iso8583.specs.default)
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

    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2.: field p",
    ):
        iso8583.encode({"t": "0210", 2: "1122"}, spec=spec)  # type: ignore

    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2, 3.: field p",
    ):
        iso8583.encode({"t": "0210", 2: "1122", 3: "3344"}, spec=spec)  # type: ignore

    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields .2.5, 3.5.: field p",
    ):
        iso8583.encode({"t": "0210", 2.5: "1122", 3.5: "3344"}, spec=spec)  # type: ignore

    with pytest.raises(
        iso8583.EncodeError,
        match="Dictionary contains invalid fields ..1, 2., .3, 4..: field p",
    ):
        iso8583.encode({"t": "0210", (1, 2): "1122", (3, 4): "3344"}, spec=spec)  # type: ignore


def test_input_type() -> None:
    """
    Encode accepts only dict.
    """
    spec = copy.deepcopy(iso8583.specs.default)
    with pytest.raises(TypeError, match="Decoded ISO8583 data must be dict, not bytes"):
        iso8583.encode(b"", spec=spec)  # type: ignore


def test_header_no_key() -> None:
    """
    Message header is required and key is not provided
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_header_absent() -> None:
    """
    Header is not required by spec and not provided
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_header_present() -> None:
    """
    Header is required by spec and provided
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_header_not_required_provided() -> None:
    """
    Header is not required by spec but provided.
    No error. Header is not included in the message.
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


def test_type_no_key() -> None:
    """
    Message type is required and key is not provided
    """
    spec = copy.deepcopy(iso8583.specs.default)
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


# fmt: off
@pytest.mark.parametrize(
    ["data_enc", "data", "expected_error"],
    [
        ("unknown_encoding", "0", "Failed to encode field, unknown encoding specified: field t"),
        ("b", "xx", "Failed to encode field, non-hex data: field t"),
        ("ascii", "\xff", "Failed to encode field, invalid data: field t"),
        ("b", "2", "Failed to encode field, odd-length hex data: field t"),
        # No data
        ("b", "", "Field data is 0 bytes, expecting 2: field t"),
        ("ascii", "", "Field data is 0 bytes, expecting 4: field t"),
        ("cp500", "", "Field data is 0 bytes, expecting 4: field t"),
        # Less data than expected
        ("b", "00", "Field data is 1 bytes, expecting 2: field t"),
        ("ascii", "000", "Field data is 3 bytes, expecting 4: field t"),
        ("cp500", "000", "Field data is 3 bytes, expecting 4: field t"),
        # More data than expected
        ("b", "000000", "Field data is 3 bytes, expecting 2: field t"),
        ("ascii", "00000", "Field data is 5 bytes, expecting 4: field t"),
        ("cp500", "00000", "Field data is 5 bytes, expecting 4: field t"),
    ]
)
# fmt: on
def test_type_encoding_negative(
    data_enc: str,
    data: str,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = data_enc
    spec["t"]["len_enc"] = "ascii"

    doc_dec = {"t": data}

    with pytest.raises(iso8583.EncodeError) as e:
        iso8583.encode(doc_dec, spec=spec)
    assert e.value.args[0] == expected_error


# fmt: off
@pytest.mark.parametrize(
    [
        "primary_data_enc",
        "secondary_data_enc",
        "enabled_fields",
        "expected_primary_enc_data",
        "expected_primary_data",
        "expected_secondary_enc_data",
        "expected_secondary_data",
    ],
    [
        # Primary only
        (
            "ascii", "ascii", ["5", "7"],
            b"0A00000000000000", "0A00000000000000",
            None, None
        ),
        (
            "cp500", "cp500", ["5", "7"],
            b"\xf0\xc1\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0", "0A00000000000000",
            None, None
        ),
        (
            "b", "b", ["5", "7"],
            b"\x0A\x00\x00\x00\x00\x00\x00\x00", "0A00000000000000",
            None, None
        ),
        # Secondary bitmap is added when secondary fields are present
        (
            "ascii", "ascii", ["5", "7", "69", "71"],
            b"8A00000000000000", "8A00000000000000",
            b"0A00000000000000", "0A00000000000000"
        ),
        (
            "cp500", "cp500", ["5", "7", "69", "71"],
            b"\xf8\xc1\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0", "8A00000000000000",
            b"\xf0\xc1\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0", "0A00000000000000"
        ),
        (
            "b", "b", ["5", "7", "69", "71"],
            b"\x8A\x00\x00\x00\x00\x00\x00\x00", "8A00000000000000",
            b"\x0A\x00\x00\x00\x00\x00\x00\x00", "0A00000000000000"
        ),
        # Secondary bitmap only
        (
            "ascii", "ascii", ["69", "71"],
            b"8000000000000000", "8000000000000000",
            b"0A00000000000000", "0A00000000000000"
        ),
        (
            "cp500", "cp500", ["69", "71"],
            b"\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0", "8000000000000000",
            b"\xf0\xc1\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0", "0A00000000000000"
        ),
        (
            "b", "b", ["69", "71"],
            b"\x80\x00\x00\x00\x00\x00\x00\x00", "8000000000000000",
            b"\x0A\x00\x00\x00\x00\x00\x00\x00", "0A00000000000000"
        ),
    ]
)
# fmt: on
def test_bitmap_encoding(
    primary_data_enc: str,
    secondary_data_enc: str,
    enabled_fields: typing.Set[str],
    expected_primary_enc_data: bytes,
    expected_primary_data: str,
    expected_secondary_enc_data: typing.Optional[bytes],
    expected_secondary_data: typing.Optional[str],
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["p"]["data_enc"] = primary_data_enc
    spec["1"]["data_enc"] = secondary_data_enc

    doc_dec = {"t": "0200"}
    expected_message_payload: typing.List[bytes] = []

    for enabled_field in enabled_fields:
        spec[enabled_field]["len_type"] = 3
        spec[enabled_field]["max_len"] = 999
        spec[enabled_field]["data_enc"] = "ascii"
        doc_dec[enabled_field] = enabled_field.zfill(3)
        expected_message_payload.append(b"003")
        expected_message_payload.append(bytes(enabled_field.zfill(3), "ascii"))

    s, doc_enc = iso8583.encode(doc_dec, spec)

    if expected_secondary_enc_data is None:
        assert bytes(s) == b"0200" + expected_primary_enc_data + b"".join(
            expected_message_payload
        )
    else:
        assert bytes(
            s
        ) == b"0200" + expected_primary_enc_data + expected_secondary_enc_data + b"".join(
            expected_message_payload
        )

    assert doc_dec["p"] == expected_primary_data
    if expected_secondary_data is not None:
        assert doc_dec["1"] == expected_secondary_data

    assert doc_enc["t"]["data"] == b"0200"
    assert doc_enc["p"]["data"] == expected_primary_enc_data
    if expected_secondary_enc_data is not None:
        assert doc_enc["1"]["data"] == expected_secondary_enc_data
    # Expected field count: enabled_fields + primary bitmap + type + secondary bitmap if expected
    assert (
        len(doc_enc) == len(enabled_fields) + 2 + 0
        if expected_secondary_enc_data is None
        else 1
    )

    for enabled_field in enabled_fields:
        assert doc_dec[enabled_field] == enabled_field.zfill(3)
        assert doc_enc[enabled_field]["data"] == bytes(enabled_field.zfill(3), "ascii")
        assert doc_enc[enabled_field]["len"] == b"003"


# fmt: off
@pytest.mark.parametrize(
    [ "primary_data_enc", "secondary_data_enc", "enabled_fields", "expected_error"],
    [
        ("unknown_encoding", "ascii", ["5", "65"], "Failed to encode field, unknown encoding specified: field p"),
        ("ascii", "unknown_encoding", ["5", "65"], "Failed to encode field, unknown encoding specified: field 1"),
        ("ascii", "ascii", ["0"], "Dictionary contains fields outside of 1-128 range [0]: field p"),
        ("ascii", "ascii", ["129"], "Dictionary contains fields outside of 1-128 range [129]: field p"),
        ("ascii", "ascii", [str(f) for f in range(0, 130)], "Dictionary contains fields outside of 1-128 range [0, 129]: field p"),
        ("ascii", "ascii", [str(f) for f in range(0, 131)], "Dictionary contains fields outside of 1-128 range [0, 129, 130]: field p"),
    ]
)
# fmt: on
def test_bitmap_encoding_negative(
    primary_data_enc: str,
    secondary_data_enc: str,
    enabled_fields: typing.Set[str],
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["p"]["data_enc"] = primary_data_enc
    spec["1"]["data_enc"] = secondary_data_enc

    doc_dec = {"t": "0210"}

    for enabled_field in enabled_fields:
        if enabled_field in spec:
            spec[enabled_field]["len_type"] = 3
            spec[enabled_field]["max_len"] = 999
            spec[enabled_field]["data_enc"] = "ascii"
        doc_dec[enabled_field] = enabled_field.zfill(3)

    with pytest.raises(iso8583.EncodeError) as e:
        iso8583.encode(doc_dec, spec=spec)
    assert e.value.args[0] == expected_error


def test_bitmap_remove_secondary() -> None:
    """If 65-128 fields are not in bitmap then remove field 1."""
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 19

    doc_dec = {
        "t": "0200",
        "1": "not needed",
        "2": "1234567890",
    }

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x40\x00\x00\x00\x00\x00\x00\x00101234567890"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"10"
    assert doc_enc["2"]["data"] == b"1234567890"
    assert doc_dec["2"] == "1234567890"

    assert doc_enc.keys() == set(["t", "p", "2"])
    assert doc_dec.keys() == set(["t", "p", "2"])


# fmt: off
@pytest.mark.parametrize(
    ["data_enc", "data", "len_type", "max_len", "expected_encoded_length", "expected_encoded_data"],
    [
        # Fixed fields
        ("b",     "", 0, 0, b"", b""),
        ("ascii", "", 0, 0, b"", b""),
        ("cp500", "", 0, 0, b"", b""),

        ("ascii", "0", 0, 1, b"", b"0"),
        ("cp500", "0", 0, 1, b"", b"\xf0"),

        ("b",     "01", 0, 1, b"", b"\x01"),
        ("ascii", "01", 0, 2, b"", b"01"),
        ("cp500", "01", 0, 2, b"", b"\xf0\xf1"),

        # Variable fields
        ("b",     "", 3, 999, b"000", b""),
        ("ascii", "", 3, 999, b"000", b""),
        ("cp500", "", 3, 999, b"000", b""),

        ("ascii", "0", 3, 999, b"001", b"0"),
        ("cp500", "0", 3, 999, b"001", b"\xf0"),

        ("b",     "01", 3, 999, b"001", b"\x01"),
        ("ascii", "01", 3, 999, b"002", b"01"),
        ("cp500", "01", 3, 999, b"002", b"\xf0\xf1"),
    ],
)
# fmt: on
def test_field_encoding(
    data_enc: str,
    data: str,
    len_type: int,
    max_len: int,
    expected_encoded_length: bytes,
    expected_encoded_data: bytes,
) -> None:
    """Test various results of field encoding with an ascii length (easier to check correct length)"""
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["data_enc"] = data_enc
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"t": "0210", "2": data}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        bytes(s)
        == b"02104000000000000000" + expected_encoded_length + expected_encoded_data
    )
    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"4000000000000000"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == expected_encoded_length
    assert doc_enc["2"]["data"] == expected_encoded_data
    assert doc_dec["2"] == data

    assert doc_enc.keys() == set(["t", "p", "2"])
    assert doc_dec.keys() == set(["t", "p", "2"])


# fmt: off
@pytest.mark.parametrize(
    ["data_enc", "data", "len_type", "max_len", "expected_error"],
    [
        ("unknown_encoding", "a", 0, 1, "Failed to encode field, unknown encoding specified: field 2"),
        ("b", "xx", 0, 1, "Failed to encode field, non-hex data: field 2"),
        ("ascii", "\xff", 0, 1, "Failed to encode field, invalid data: field 2"),

        # Fixed
        ("b", "a", 0, 1, "Failed to encode field, odd-length hex data: field 2"),
        ("b", "0", 0, 1, "Failed to encode field, odd-length hex data: field 2"),
        # No data
        ("b", "", 0, 1, "Field data is 0 bytes, expecting 1: field 2"),
        ("b", "", 0, 1, "Field data is 0 bytes, expecting 1: field 2"),
        ("ascii", "", 0, 1, "Field data is 0 bytes, expecting 1: field 2"),
        ("cp500", "", 0, 1, "Field data is 0 bytes, expecting 1: field 2"),
        # Less data than expected
        ("b", "aaaa", 0, 3, "Field data is 2 bytes, expecting 3: field 2"),
        ("b", "0000", 0, 3, "Field data is 2 bytes, expecting 3: field 2"),
        ("ascii", "aa", 0, 3, "Field data is 2 bytes, expecting 3: field 2"),
        ("cp500", "aa", 0, 3, "Field data is 2 bytes, expecting 3: field 2"),
        # More data than expected
        ("b", "aaaa", 0, 1, "Field data is 2 bytes, expecting 1: field 2"),
        ("b", "0000", 0, 1, "Field data is 2 bytes, expecting 1: field 2"),
        ("ascii", "aa", 0, 1, "Field data is 2 bytes, expecting 1: field 2"),
        ("cp500", "aa", 0, 1, "Field data is 2 bytes, expecting 1: field 2"),

        # Variable
        ("b", "a", 1, 10, "Failed to encode field, odd-length hex data: field 2"),
        ("b", "0", 1, 10, "Failed to encode field, odd-length hex data: field 2"),
        # More data than expected
        ("b", "aaaa", 1, 1, "Field data is 2 bytes, larger than maximum 1: field 2"),
        ("b", "0000", 1, 1, "Field data is 2 bytes, larger than maximum 1: field 2"),
        ("ascii", "aa", 1, 1, "Field data is 2 bytes, larger than maximum 1: field 2"),
        ("cp500", "aa", 1, 1, "Field data is 2 bytes, larger than maximum 1: field 2"),
    ]
)
# fmt: on
def test_field_encoding_negative(
    data_enc: str,
    data: str,
    len_type: int,
    max_len: int,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["data_enc"] = data_enc
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"t": "0210", "2": data}

    with pytest.raises(iso8583.EncodeError) as e:
        iso8583.encode(doc_dec, spec=spec)
    assert e.value.args[0] == expected_error


# fmt: off
@pytest.mark.parametrize(
    ["len_enc", "len_type", "data_len", "expected_encoded_length"],
    [
        # Fixed field, no data - no length
        # This is pointless but should be encoded correctly.
        ("b",     0, 0, b""),
        ("bcd",   0, 0, b""),
        ("ascii", 0, 0, b""),
        ("cp500", 0, 0, b""),

        # Fixed field, some data - no length
        ("b",     0, 1, b""),
        ("bcd",   0, 1, b""),
        ("ascii", 0, 1, b""),
        ("cp500", 0, 1, b""),

        # Variable field, no data - zero length
        ("b",     1, 0, b"\x00"),
        ("bcd",   1, 0, b"\x00"),
        ("ascii", 1, 0, b"0"),
        ("cp500", 1, 0, b"\xf0"),

        ("b",     2, 0, b"\x00\x00"),
        ("bcd",   2, 0, b"\x00\x00"),
        ("ascii", 2, 0, b"00"),
        ("cp500", 2, 0, b"\xf0\xf0"),

        ("b",     1, 1, b"\x01"),
        ("bcd",   1, 1, b"\x01"),
        ("ascii", 1, 1, b"1"),
        ("cp500", 1, 1, b"\xf1"),

        ("b",     2, 1, b"\x00\x01"),
        ("bcd",   2, 1, b"\x00\x01"),
        ("ascii", 2, 1, b"01"),
        ("cp500", 2, 1, b"\xf0\xf1"),

        ("b",     2, 99, b"\x00\x63"),
        ("bcd",   2, 99, b"\x00\x99"),
        ("ascii", 2, 99, b"99"),
        ("cp500", 2, 99, b"\xf9\xf9"),

        ("b",     1, 16, b"\x10"),
        ("bcd",   1, 16, b"\x16"),
        ("b",     2, 256, b"\x01\x00"),
        ("bcd",   2, 256, b"\x02\x56"),
    ],
)
# fmt: on
def test_field_length_encoding(
    len_enc: str,
    len_type: str,
    data_len: int,
    expected_encoded_length: bytes,
) -> None:
    """Test various results of length encoding with a simple ascii field"""
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = data_len
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = len_enc

    doc_dec = {"t": "0210", "2": "a" * data_len}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert bytes(s) == b"02104000000000000000" + expected_encoded_length + (
        b"a" * data_len
    )
    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"4000000000000000"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == expected_encoded_length
    assert doc_enc["2"]["data"] == b"a" * data_len
    assert doc_dec["2"] == "a" * data_len

    assert doc_enc.keys() == set(["t", "p", "2"])
    assert doc_dec.keys() == set(["t", "p", "2"])


# fmt: off
@pytest.mark.parametrize(
    ["len_enc", "len_type", "data_len", "expected_error"],
    [
        ("unknown_encoding", 1, 1, "Failed to encode field length, unknown encoding specified: field 2"),
        ("b", 1, 256, "Failed to encode field length, field length does not fit into configured field size: field 2"),
        ("ascii", 1, 10, "Failed to encode field length, field length does not fit into configured field size: field 2"),
        ("bcd", 1, 100, "Failed to encode field length, field length does not fit into configured field size: field 2"),
        ("b", 2, 65536, "Failed to encode field length, field length does not fit into configured field size: field 2"),
        ("ascii", 2, 100, "Failed to encode field length, field length does not fit into configured field size: field 2"),
        ("bcd", 2, 10000, "Failed to encode field length, field length does not fit into configured field size: field 2"),
    ],
)
# fmt: on
def test_field_length_encoding_negative(
    len_enc: str,
    len_type: str,
    data_len: int,
    expected_error: str,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default_ascii)
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = data_len
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = len_enc

    doc_dec = {"t": "0210", "2": "a" * data_len}

    with pytest.raises(iso8583.EncodeError) as e:
        t = iso8583.encode(doc_dec, spec=spec)
    assert e.value.args[0] == expected_error
