"""Test length measured in half bytes (nibbles). Nibbles were added in v2.1"""

import copy

import iso8583
import iso8583.specs
import pytest


# fmt: off
@pytest.mark.parametrize(
    ["data_enc", "len_enc", "len_type", "max_len", "len_count", "result", "result_f2_len"],
    [
        ("ascii", "ascii", 2, 8, "bytes",   b"02004000000000000000041234", b"04"),
        ("ascii", "ascii", 2, 8, "nibbles", b"02004000000000000000081234", b"08"),
        ("ascii", "bcd",   2, 8, "bytes",   b"02004000000000000000\x00\x041234", b"\x00\x04"),
        ("ascii", "bcd",   2, 8, "nibbles", b"02004000000000000000\x00\x081234", b"\x00\x08"),
        ("b",     "ascii", 2, 8, "bytes",   b"0200400000000000000002\x12\x34", b"02"),
        ("b",     "ascii", 2, 8, "nibbles", b"0200400000000000000004\x12\x34", b"04"),
        ("b",     "bcd",   2, 8, "bytes",   b"02004000000000000000\x00\x02\x12\x34", b"\x00\x02"),
        ("b",     "bcd",   2, 8, "nibbles", b"02004000000000000000\x00\x04\x12\x34", b"\x00\x04"),
        ("ascii", "ascii", 0, 4, "bytes",   b"020040000000000000001234", b""),
        ("ascii", "ascii", 0, 8, "nibbles", b"020040000000000000001234", b""),
        ("b",     "ascii", 0, 2, "bytes",   b"02004000000000000000\x12\x34", b""),
        ("b",     "ascii", 0, 4, "nibbles", b"02004000000000000000\x12\x34", b""),
    ],
)
# fmt: on
def test_encode_nibbles(
    data_enc: str,
    len_enc: str,
    len_type: int,
    max_len: int,
    len_count: str,
    result: bytes,
    result_f2_len: bytes,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = data_enc
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["len_count"] = len_count

    decoded = {"t": "0200", "2": "1234"}

    s, encoded = iso8583.encode(decoded, spec)

    assert s == result
    assert encoded["2"]["len"] == result_f2_len


# fmt: off
@pytest.mark.parametrize(
    ["len_enc", "len_type", "max_len", "len_count", "pad", "result", "result_f2_len"],
    [
        ("ascii", 2, 8, "nibbles", "0", b"0200400000000000000003\x01\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "0", b"02004000000000000000\x00\x03\x01\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "0", b"02004000000000000000\x01\x23", b""),
        ("ascii", 2, 8, "nibbles", "F", b"0200400000000000000003\xF1\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "F", b"02004000000000000000\x00\x03\xF1\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F", b"02004000000000000000\xF1\x23", b""),
        ("ascii", 2, 8, "nibbles", "01", b"0200400000000000000003\x01\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "01", b"02004000000000000000\x00\x03\x01\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "01", b"02004000000000000000\x01\x23", b""),
        ("ascii", 2, 8, "nibbles", "F1", b"0200400000000000000003\xF1\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "F1", b"02004000000000000000\x00\x03\xF1\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F1", b"02004000000000000000\xF1\x23", b""),
    ],
)
# fmt: on
def test_encode_nibbles_odd_left_pad(
    len_enc: str,
    len_type: int,
    max_len: int,
    len_count: str,
    pad: str,
    result: bytes,
    result_f2_len: bytes,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["len_count"] = len_count
    spec["2"]["left_pad"] = pad

    decoded = {"t": "0200", "2": "123"}

    s, encoded = iso8583.encode(decoded, spec)

    assert s == result
    assert encoded["2"]["len"] == result_f2_len


# fmt: off
@pytest.mark.parametrize(
    ["len_enc", "len_type", "max_len", "len_count", "pad", "result", "result_f2_len"],
    [
        ("ascii", 2, 8, "nibbles", "0", b"0200400000000000000003\x12\x30", b"03"),
        ("bcd",   2, 8, "nibbles", "0", b"02004000000000000000\x00\x03\x12\x30", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "0", b"02004000000000000000\x12\x30", b""),
        ("ascii", 2, 8, "nibbles", "F", b"0200400000000000000003\x12\x3F", b"03"),
        ("bcd",   2, 8, "nibbles", "F", b"02004000000000000000\x00\x03\x12\x3F", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F", b"02004000000000000000\x12\x3F", b""),
        ("ascii", 2, 8, "nibbles", "01", b"0200400000000000000003\x12\x30", b"03"),
        ("bcd",   2, 8, "nibbles", "01", b"02004000000000000000\x00\x03\x12\x30", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "01", b"02004000000000000000\x12\x30", b""),
        ("ascii", 2, 8, "nibbles", "F1", b"0200400000000000000003\x12\x3F", b"03"),
        ("bcd",   2, 8, "nibbles", "F1", b"02004000000000000000\x00\x03\x12\x3F", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F1", b"02004000000000000000\x12\x3F", b""),
    ],
)
# fmt: on
def test_encode_nibbles_odd_right_pad(
    len_enc: str,
    len_type: int,
    max_len: int,
    len_count: str,
    pad: str,
    result: bytes,
    result_f2_len: bytes,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["len_count"] = len_count
    spec["2"]["right_pad"] = pad

    decoded = {"t": "0200", "2": "123"}

    s, encoded = iso8583.encode(decoded, spec)

    assert s == result
    assert encoded["2"]["len"] == result_f2_len


def test_encode_nibbles_odd_no_pad() -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "bcd"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 8
    spec["2"]["len_count"] = "nibbles"

    decoded = {"t": "0200", "2": "1"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode field, odd-length nibble data, specify pad: field 2",
    ):
        iso8583.encode(decoded, spec=spec)


def test_encode_nibbles_non_hex() -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "bcd"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 8
    spec["2"]["len_count"] = "nibbles"
    spec["2"]["right_pad"] = "f"

    decoded = {"t": "0200", "2": "x"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode field, non-hex data: field 2",
    ):
        iso8583.encode(decoded, spec=spec)


# fmt: off
@pytest.mark.parametrize(
    ["data_enc", "len_enc", "len_type", "max_len", "len_count", "data", "result_f2_len"],
    [
        ("ascii", "ascii", 2, 8, "bytes",   b"02004000000000000000041234", b"04"),
        ("ascii", "ascii", 2, 8, "nibbles", b"02004000000000000000081234", b"08"),
        ("ascii", "bcd",   2, 8, "bytes",   b"02004000000000000000\x00\x041234", b"\x00\x04"),
        ("ascii", "bcd",   2, 8, "nibbles", b"02004000000000000000\x00\x081234", b"\x00\x08"),
        ("b",     "ascii", 2, 8, "bytes",   b"0200400000000000000002\x12\x34", b"02"),
        ("b",     "ascii", 2, 8, "nibbles", b"0200400000000000000004\x12\x34", b"04"),
        ("b",     "bcd",   2, 8, "bytes",   b"02004000000000000000\x00\x02\x12\x34", b"\x00\x02"),
        ("b",     "bcd",   2, 8, "nibbles", b"02004000000000000000\x00\x04\x12\x34", b"\x00\x04"),
        ("ascii", "ascii", 0, 4, "bytes",   b"020040000000000000001234", b""),
        ("ascii", "ascii", 0, 8, "nibbles", b"020040000000000000001234", b""),
        ("b",     "ascii", 0, 2, "bytes",   b"02004000000000000000\x12\x34", b""),
        ("b",     "ascii", 0, 4, "nibbles", b"02004000000000000000\x12\x34", b""),
    ],
)
# fmt: on
def test_decode_nibbles(
    data_enc: str,
    len_enc: str,
    len_type: int,
    max_len: int,
    len_count: str,
    data: bytes,
    result_f2_len: bytes,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = data_enc
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["len_count"] = len_count

    decoded, encoded = iso8583.decode(data, spec)

    assert decoded["2"] == "1234"
    assert encoded["2"]["len"] == result_f2_len


# fmt: off
@pytest.mark.parametrize(
    ["len_enc", "len_type", "max_len", "len_count", "pad", "data", "result_f2_len"],
    [
        ("ascii", 2, 8, "nibbles", "0", b"0200400000000000000003\x01\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "0", b"02004000000000000000\x00\x03\x01\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "0", b"02004000000000000000\x01\x23", b""),
        ("ascii", 2, 8, "nibbles", "F", b"0200400000000000000003\xF1\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "F", b"02004000000000000000\x00\x03\xF1\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F", b"02004000000000000000\xF1\x23", b""),
        ("ascii", 2, 8, "nibbles", "01", b"0200400000000000000003\x01\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "01", b"02004000000000000000\x00\x03\x01\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "01", b"02004000000000000000\x01\x23", b""),
        ("ascii", 2, 8, "nibbles", "F1", b"0200400000000000000003\xF1\x23", b"03"),
        ("bcd",   2, 8, "nibbles", "F1", b"02004000000000000000\x00\x03\xF1\x23", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F1", b"02004000000000000000\xF1\x23", b""),
    ],
)
# fmt: on
def test_decode_nibbles_left_pad(
    len_enc: str,
    len_type: int,
    max_len: int,
    len_count: str,
    pad: str,
    data: bytes,
    result_f2_len: bytes,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["len_count"] = len_count
    spec["2"]["left_pad"] = pad

    decoded, encoded = iso8583.decode(data, spec)

    assert decoded["2"] == "123"
    assert encoded["2"]["len"] == result_f2_len


# fmt: off
@pytest.mark.parametrize(
    ["len_enc", "len_type", "max_len", "len_count", "pad", "data", "result_f2_len"],
    [
        ("ascii", 2, 8, "nibbles", "0", b"0200400000000000000003\x12\x30", b"03"),
        ("bcd",   2, 8, "nibbles", "0", b"02004000000000000000\x00\x03\x12\x30", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "0", b"02004000000000000000\x12\x30", b""),
        ("ascii", 2, 8, "nibbles", "F", b"0200400000000000000003\x12\x3F", b"03"),
        ("bcd",   2, 8, "nibbles", "F", b"02004000000000000000\x00\x03\x12\x3F", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F", b"02004000000000000000\x12\x3F", b""),
        ("ascii", 2, 8, "nibbles", "01", b"0200400000000000000003\x12\x30", b"03"),
        ("bcd",   2, 8, "nibbles", "01", b"02004000000000000000\x00\x03\x12\x30", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "01", b"02004000000000000000\x12\x30", b""),
        ("ascii", 2, 8, "nibbles", "F1", b"0200400000000000000003\x12\x3F", b"03"),
        ("bcd",   2, 8, "nibbles", "F1", b"02004000000000000000\x00\x03\x12\x3F", b"\x00\x03"),
        ("ascii", 0, 3, "nibbles", "F1", b"02004000000000000000\x12\x3F", b""),
    ],
)
# fmt: on
def test_decode_nibbles_right_pad(
    len_enc: str,
    len_type: int,
    max_len: int,
    len_count: str,
    pad: str,
    data: bytes,
    result_f2_len: bytes,
) -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = len_enc
    spec["2"]["len_type"] = len_type
    spec["2"]["max_len"] = max_len
    spec["2"]["len_count"] = len_count
    spec["2"]["right_pad"] = pad

    decoded, encoded = iso8583.decode(data, spec)

    assert decoded["2"] == "123"
    assert encoded["2"]["len"] == result_f2_len


def test_decode_nibbles_odd_no_pad() -> None:
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "bcd"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 8
    spec["2"]["len_count"] = "nibbles"

    data = b"02004000000000000000\x00\x03\x12\x30"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 4 nibbles, expecting 3: field 2 pos 22",
    ):
        iso8583.decode(data, spec=spec)


def test_encode_nibbles_variable_over_max() -> None:
    """Variable field length is over maximum allowed"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    decoded = {"t": "0200", "2": "1234"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 8 nibbles, larger than maximum 4: field 2",
    ):
        iso8583.encode(decoded, spec=spec)


def test_encode_nibbles_fixed_partial() -> None:
    """Fixed field is provided partially"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    decoded = {"t": "0200", "2": "1"}
    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 2 nibbles, expecting 4: field 2",
    ):
        iso8583.encode(decoded, spec=spec)


def test_encode_nibbles_fixed_missing() -> None:
    """Fixed field is missing"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    decoded = {"t": "0200", "2": ""}
    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 nibbles, expecting 4: field 2",
    ):
        iso8583.encode(decoded, spec=spec)


def test_decode_nibbles_variable_over_max() -> None:
    """Variable field length is over maximum allowed"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    s = b"02004000000000000000081234"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 8 nibbles, larger than maximum 4: field 2 pos 20",
    ):
        iso8583.decode(s, spec=spec)


def test_decode_nibbles_variable_partial() -> None:
    """Variable field is provided partially"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    s = b"02004000000000000000041"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 2 nibbles, expecting 4: field 2 pos 22",
    ):
        iso8583.decode(s, spec=spec)


def test_decode_nibbles_variable_missing() -> None:
    """Variable field is missing"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    s = b"0200400000000000000004"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 nibbles, expecting 4: field 2 pos 22",
    ):
        iso8583.decode(s, spec=spec)


def test_decode_nibbles_fixed_partial() -> None:
    """Fixed field is provided partially"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    s = b"020040000000000000001"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 2 nibbles, expecting 4: field 2 pos 20",
    ):
        iso8583.decode(s, spec=spec)


def test_decode_nibbles_fixed_missing() -> None:
    """Fixed field is missing"""
    spec = copy.deepcopy(iso8583.specs.default)
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 4
    spec["2"]["len_count"] = "nibbles"

    s = b"02004000000000000000"
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 nibbles, expecting 4: field 2 pos 20",
    ):
        iso8583.decode(s, spec=spec)
