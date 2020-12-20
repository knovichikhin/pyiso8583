"""Test length measured in half bytes (nibbles). Nibbles were added in v2.1"""

import copy

import iso8583
import iso8583.specs
import pytest

spec = copy.deepcopy(iso8583.specs.default)


# fmt: off
@pytest.mark.parametrize(
    ["data_enc", "len_enc", "len_type", "max_len", "len_count", "result", "result_f2_len"],
    [
        ("ascii", "ascii", 2, 8, "bytes",   b"02004000000000000000041234", b"04"),
        ("ascii", "ascii", 2, 8, "nibbles", b"02004000000000000000081234", b"08"),
        ("ascii", "b",     2, 8, "bytes",   b"02004000000000000000\x00\x041234", b"\x00\x04"),
        ("ascii", "b",     2, 8, "nibbles", b"02004000000000000000\x00\x081234", b"\x00\x08"),
        ("b",     "ascii", 2, 8, "bytes",   b"0200400000000000000002\x12\x34", b"02"),
        ("b",     "ascii", 2, 8, "nibbles", b"0200400000000000000004\x12\x34", b"04"),
        ("b",     "b",     2, 8, "bytes",   b"02004000000000000000\x00\x02\x12\x34", b"\x00\x02"),
        ("b",     "b",     2, 8, "nibbles", b"02004000000000000000\x00\x04\x12\x34", b"\x00\x04"),
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
    ["data_enc", "len_enc", "len_type", "max_len", "len_count", "data", "result_f2_len"],
    [
        ("ascii", "ascii", 2, 8, "bytes",   b"02004000000000000000041234", b"04"),
        ("ascii", "ascii", 2, 8, "nibbles", b"02004000000000000000081234", b"08"),
        ("ascii", "b",     2, 8, "bytes",   b"02004000000000000000\x00\x041234", b"\x00\x04"),
        ("ascii", "b",     2, 8, "nibbles", b"02004000000000000000\x00\x081234", b"\x00\x08"),
        ("b",     "ascii", 2, 8, "bytes",   b"0200400000000000000002\x12\x34", b"02"),
        ("b",     "ascii", 2, 8, "nibbles", b"0200400000000000000004\x12\x34", b"04"),
        ("b",     "b",     2, 8, "bytes",   b"02004000000000000000\x00\x02\x12\x34", b"\x00\x02"),
        ("b",     "b",     2, 8, "nibbles", b"02004000000000000000\x00\x04\x12\x34", b"\x00\x04"),
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


def test_decode_nibbles_variable_over_max() -> None:
    """Variable field length is over maximum allowed"""
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
