import copy
from io import StringIO

import iso8583
import iso8583.specs
import typing
from iso8583.tools import _wrap_bytes_repr, _wrap_str_repr


def test_pp(capsys: typing.Any) -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 6
    spec["h"]["len_type"] = 0
    doc_dec: typing.Dict[str, str] = {}
    iso8583.pp(doc_dec, spec)

    captured = capsys.readouterr()

    r = captured.out.split("\n")

    assert r[0] == ""
    assert len(r) == 1

    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"
    doc_dec["2"] = "12345678"
    doc_dec["44"] = "123"
    doc_dec["123"] = "123"
    _, doc_enc = iso8583.encode(doc_dec, spec)

    iso8583.pp(doc_dec, spec)
    captured = capsys.readouterr()
    r = captured.out.split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == "p   Bitmap, Primary               : 'C000000000100000'"
    assert r[3] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[4] == "2   Primary Account Number (PAN)  : '12345678'"
    assert r[5] == "44  Additional Response Data      : '123'"
    assert r[6] == "123 Reserved for Private Use      : '123'"
    assert r[7] == ""
    assert len(r) == 8

    iso8583.pp(doc_enc, spec)
    captured = capsys.readouterr()
    r = captured.out.split("\n")
    assert r[0] == "h   Message Header                : b'header'"
    assert r[1] == "t   Message Type                  : b'0200'"
    assert r[2] == "p   Bitmap, Primary               : b'\\xc0\\x00\\x00\\x00\\x00\\x10\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[4] == "2   Primary Account Number (PAN)  : b'08' b'12345678'"
    assert r[5] == "44  Additional Response Data      : b'03' b'123'"
    assert r[6] == "123 Reserved for Private Use      : b'003' b'123'"
    assert r[7] == ""
    assert len(r) == 8
    # fmt: on


def test_pp_variable_header(capsys: typing.Any) -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 6
    spec["h"]["len_type"] = 2
    doc_dec = {}
    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"
    doc_dec["2"] = "12345678"
    doc_dec["44"] = "123"
    doc_dec["123"] = "123"
    _, doc_enc = iso8583.encode(doc_dec, spec)

    iso8583.pp(doc_dec, spec)
    captured = capsys.readouterr()
    r = captured.out.split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == "p   Bitmap, Primary               : 'C000000000100000'"
    assert r[3] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[4] == "2   Primary Account Number (PAN)  : '12345678'"
    assert r[5] == "44  Additional Response Data      : '123'"
    assert r[6] == "123 Reserved for Private Use      : '123'"
    assert r[7] == ""
    assert len(r) == 8

    iso8583.pp(doc_enc, spec)
    captured = capsys.readouterr()
    r = captured.out.split("\n")
    assert r[0] == "h   Message Header                : b'06' b'header'"
    assert r[1] == "t   Message Type                  : b'0200'"
    assert r[2] == "p   Bitmap, Primary               : b'\\xc0\\x00\\x00\\x00\\x00\\x10\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[4] == "2   Primary Account Number (PAN)  : b'08' b'12345678'"
    assert r[5] == "44  Additional Response Data      : b'03' b'123'"
    assert r[6] == "123 Reserved for Private Use      : b'003' b'123'"
    assert r[7] == ""
    assert len(r) == 8

    doc_dec["h"] = ""
    _, doc_enc = iso8583.encode(doc_dec, spec)

    iso8583.pp(doc_dec, spec)
    captured = capsys.readouterr()
    r = captured.out.split("\n")
    assert r[0] == "h   Message Header                : ''"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == "p   Bitmap, Primary               : 'C000000000100000'"
    assert r[3] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[4] == "2   Primary Account Number (PAN)  : '12345678'"
    assert r[5] == "44  Additional Response Data      : '123'"
    assert r[6] == "123 Reserved for Private Use      : '123'"
    assert r[7] == ""
    assert len(r) == 8

    iso8583.pp(doc_enc, spec)
    captured = capsys.readouterr()
    r = captured.out.split("\n")
    assert r[0] == "h   Message Header                : b'00' b''"
    assert r[1] == "t   Message Type                  : b'0200'"
    assert r[2] == "p   Bitmap, Primary               : b'\\xc0\\x00\\x00\\x00\\x00\\x10\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[4] == "2   Primary Account Number (PAN)  : b'08' b'12345678'"
    assert r[5] == "44  Additional Response Data      : b'03' b'123'"
    assert r[6] == "123 Reserved for Private Use      : b'003' b'123'"
    assert r[7] == ""
    assert len(r) == 8
    # fmt: on


def test_pp_stream() -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 6
    spec["h"]["len_type"] = 0
    doc_dec = {}
    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"
    doc_dec["2"] = "12345678"
    doc_dec["44"] = "123"
    doc_dec["123"] = "123"
    _, doc_enc = iso8583.encode(doc_dec, spec)

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == "p   Bitmap, Primary               : 'C000000000100000'"
    assert r[3] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[4] == "2   Primary Account Number (PAN)  : '12345678'"
    assert r[5] == "44  Additional Response Data      : '123'"
    assert r[6] == "123 Reserved for Private Use      : '123'"
    assert r[7] == ""
    assert len(r) == 8

    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : b'header'"
    assert r[1] == "t   Message Type                  : b'0200'"
    assert r[2] == "p   Bitmap, Primary               : b'\\xc0\\x00\\x00\\x00\\x00\\x10\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[4] == "2   Primary Account Number (PAN)  : b'08' b'12345678'"
    assert r[5] == "44  Additional Response Data      : b'03' b'123'"
    assert r[6] == "123 Reserved for Private Use      : b'003' b'123'"
    assert r[7] == ""
    assert len(r) == 8
    # fmt: on


def test_pp_optional_fields() -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 6
    spec["h"]["len_type"] = 0

    # Empty
    doc_dec: typing.Dict[str, str] = {}

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == ""
    assert len(r) == 1

    # Add header
    doc_dec = {}
    doc_dec["h"] = "header"

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == ""
    assert len(r) == 2

    # Add header, type
    doc_dec = {}
    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == ""
    assert len(r) == 3

    # Add header, type, field 2
    doc_dec = {}
    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"
    doc_dec["2"] = "12345678"

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == "2   Primary Account Number (PAN)  : '12345678'"
    assert r[3] == ""
    assert len(r) == 4

    # Add header, type, field 123 + encode
    doc_dec = {}
    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"
    doc_dec["123"] = "123"
    _, doc_enc = iso8583.encode(doc_dec, spec)

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : 'header'"
    assert r[1] == "t   Message Type                  : '0200'"
    assert r[2] == "p   Bitmap, Primary               : '8000000000000000'"
    assert r[3] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[4] == "123 Reserved for Private Use      : '123'"
    assert r[5] == ""
    assert len(r) == 6

    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "h   Message Header                : b'header'"
    assert r[1] == "t   Message Type                  : b'0200'"
    assert r[2] == "p   Bitmap, Primary               : b'\\x80\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[4] == "123 Reserved for Private Use      : b'003' b'123'"
    assert r[5] == ""
    assert len(r) == 6
    # fmt: on


def test_pp_header_present_but_not_in_spec() -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 0
    spec["h"]["len_type"] = 0

    # Empty
    doc_dec: typing.Dict[str, str] = {}

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == ""
    assert len(r) == 1

    # Add header
    doc_dec = {}
    doc_dec["h"] = "header"

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == ""
    assert len(r) == 1

    # Add header, type
    doc_dec = {}
    doc_dec["h"] = "header"
    doc_dec["t"] = "0200"

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0200'"
    assert r[1] == ""
    assert len(r) == 2
    # fmt: on


def test_pp_no_desc() -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 0
    spec["h"]["len_type"] = 0

    doc_dec = {}
    doc_dec["t"] = "0200"
    doc_dec["2"] = "12345678"
    doc_dec["44"] = "123"
    doc_dec["123"] = "123"
    _, doc_enc = iso8583.encode(doc_dec, spec)

    sio = StringIO()
    iso8583.pp(doc_dec, spec, 0, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "t  : '0200'"
    assert r[1] == "p  : 'C000000000100000'"
    assert r[2] == "1  : '0000000000000020'"
    assert r[3] == "2  : '12345678'"
    assert r[4] == "44 : '123'"
    assert r[5] == "123: '123'"
    assert r[6] == ""
    assert len(r) == 7

    sio = StringIO()
    iso8583.pp(doc_enc, spec, 0, stream=sio)
    r = sio.getvalue().split("\n")
    assert r[0] == "t  : b'0200'"
    assert r[1] == "p  : b'\\xc0\\x00\\x00\\x00\\x00\\x10\\x00\\x00'"
    assert r[2] == "1  : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[3] == "2  : b'08' b'12345678'"
    assert r[4] == "44 : b'03' b'123'"
    assert r[5] == "123: b'003' b'123'"
    assert r[6] == ""
    assert len(r) == 7
    # fmt: on


def test_pp_folding() -> None:
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 0
    spec["h"]["len_type"] = 0

    doc_dec = {}
    doc_dec["t"] = "0200"
    doc_dec["123"] = "123456789012345678901234567890123456789012345678901234567890"
    _, doc_enc = iso8583.encode(doc_dec, spec)

    # standard width = 80
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=80)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0200'"
    assert r[1] == "p   Bitmap, Primary               : '8000000000000000'"
    assert r[2] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[3] == "123 Reserved for Private Use      : '123456789012345678901234567890123456789012'"
    assert r[4] == "                                    '345678901234567890'"
    assert r[5] == ""
    assert len(r) == 6

    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=80)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b'0200'"
    assert r[1] == "p   Bitmap, Primary               : b'\\x80\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"
    assert r[2] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00 '"
    assert r[3] == "123 Reserved for Private Use      : b'060' b'1234567890123456789012345678901234'"
    assert r[4] == "                                           b'56789012345678901234567890'"
    assert r[5] == ""
    assert len(r) == 6

    # reduced width = 80
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=60)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0200'"
    assert r[1] == "p   Bitmap, Primary               : '8000000000000000'"
    assert r[2] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[3] == "123 Reserved for Private Use      : '1234567890123456789012'"
    assert r[4] == "                                    '3456789012345678901234'"
    assert r[5] == "                                    '5678901234567890'"
    assert r[6] == ""
    assert len(r) == 7

    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=60)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b'0200'"
    assert r[1] == "p   Bitmap, Primary               : b'\\x80\\x00\\x00\\x00\\x00'"
    assert r[2] == "                                    b'\\x00\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00'"
    assert r[4] == "                                    b'\\x00\\x00 '"
    assert r[5] == "123 Reserved for Private Use      : b'060' b'12345678901234'"
    assert r[6] == "                                           b'56789012345678'"
    assert r[7] == "                                           b'90123456789012'"
    assert r[8] == "                                           b'34567890123456'"
    assert r[9] == "                                           b'7890'"
    assert r[10] == ""
    assert len(r) == 11

    # even chunks
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=68)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0200'"
    assert r[1] == "p   Bitmap, Primary               : '8000000000000000'"
    assert r[2] == "1   Bitmap, Secondary             : '0000000000000020'"
    assert r[3] == "123 Reserved for Private Use      : '123456789012345678901234567890'"
    assert r[4] == "                                    '123456789012345678901234567890'"
    assert r[5] == ""
    assert len(r) == 6

    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=61)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b'0200'"
    assert r[1] == "p   Bitmap, Primary               : b'\\x80\\x00\\x00\\x00\\x00'"
    assert r[2] == "                                    b'\\x00\\x00\\x00'"
    assert r[3] == "1   Bitmap, Secondary             : b'\\x00\\x00\\x00\\x00\\x00'"
    assert r[4] == "                                    b'\\x00\\x00 '"
    assert r[5] == "123 Reserved for Private Use      : b'060' b'123456789012345'"
    assert r[6] == "                                           b'678901234567890'"
    assert r[7] == "                                           b'123456789012345'"
    assert r[8] == "                                           b'678901234567890'"
    assert r[9] == ""
    assert len(r) == 10

    # This is a test scenario where "b''" triggers a fold
    doc_dec = {}
    doc_dec["t"] = "0200"
    doc_dec["123"] = "12"
    _, doc_enc = iso8583.encode(doc_dec, spec)
    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=44)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b'0200'"
    assert r[1] == "p   Bitmap, Primary               : b'\\x80'"
    assert r[2] == "                                    b'\\x00'"
    assert r[3] == "                                    b'\\x00'"
    assert r[4] == "                                    b'\\x00'"
    assert r[5] == "                                    b'\\x00'"
    assert r[6] == "                                    b'\\x00'"
    assert r[7] == "                                    b'\\x00'"
    assert r[8] == "                                    b'\\x00'"
    assert r[9] == "1   Bitmap, Secondary             : b'\\x00'"
    assert r[10] == "                                    b'\\x00'"
    assert r[11] == "                                    b'\\x00'"
    assert r[12] == "                                    b'\\x00'"
    assert r[13] == "                                    b'\\x00'"
    assert r[14] == "                                    b'\\x00'"
    assert r[15] == "                                    b'\\x00 '"
    assert r[16] == "123 Reserved for Private Use      : b'002' b'1'"
    assert r[17] == "                                           b'2'"
    assert r[18] == ""
    assert len(r) == 19

    # This is a test scenario where "''" triggers a fold
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=37)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0'"
    assert r[1] == "                                    '2'"
    assert r[2] == "                                    '0'"
    assert r[3] == "                                    '0'"
    assert r[4] == "p   Bitmap, Primary               : '8'"
    assert r[5] == "                                    '0'"
    assert r[6] == "                                    '0'"
    assert r[7] == "                                    '0'"
    assert r[8] == "                                    '0'"
    assert r[9] == "                                    '0'"
    assert r[10] == "                                    '0'"
    assert r[11] == "                                    '0'"
    assert r[12] == "                                    '0'"
    assert r[13] == "                                    '0'"
    assert r[14] == "                                    '0'"
    assert r[15] == "                                    '0'"
    assert r[16] == "                                    '0'"
    assert r[17] == "                                    '0'"
    assert r[18] == "                                    '0'"
    assert r[19] == "                                    '0'"
    assert r[20] == "1   Bitmap, Secondary             : '0'"
    assert r[21] == "                                    '0'"
    assert r[22] == "                                    '0'"
    assert r[23] == "                                    '0'"
    assert r[24] == "                                    '0'"
    assert r[25] == "                                    '0'"
    assert r[26] == "                                    '0'"
    assert r[27] == "                                    '0'"
    assert r[28] == "                                    '0'"
    assert r[29] == "                                    '0'"
    assert r[30] == "                                    '0'"
    assert r[31] == "                                    '0'"
    assert r[32] == "                                    '0'"
    assert r[33] == "                                    '0'"
    assert r[34] == "                                    '2'"
    assert r[35] == "                                    '0'"
    assert r[36] == "123 Reserved for Private Use      : '1'"
    assert r[37] == "                                    '2'"
    assert r[38] == ""
    assert len(r) == 39

    # This is a test scenario where _pprint_bytes does not
    # try to fold because the data is <= 1
    doc_dec = {}
    doc_dec["t"] = "0200"
    doc_dec["123"] = ""
    _, doc_enc = iso8583.encode(doc_dec, spec)
    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=44)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b'0200'"
    assert r[1] == "p   Bitmap, Primary               : b'\\x80'"
    assert r[2] == "                                    b'\\x00'"
    assert r[3] == "                                    b'\\x00'"
    assert r[4] == "                                    b'\\x00'"
    assert r[5] == "                                    b'\\x00'"
    assert r[6] == "                                    b'\\x00'"
    assert r[7] == "                                    b'\\x00'"
    assert r[8] == "                                    b'\\x00'"
    assert r[9] == "1   Bitmap, Secondary             : b'\\x00'"
    assert r[10] == "                                    b'\\x00'"
    assert r[11] == "                                    b'\\x00'"
    assert r[12] == "                                    b'\\x00'"
    assert r[13] == "                                    b'\\x00'"
    assert r[14] == "                                    b'\\x00'"
    assert r[15] == "                                    b'\\x00 '"
    assert r[16] == "123 Reserved for Private Use      : b'000' b''"
    assert r[17] == ""
    assert len(r) == 18

    # This is a test scenario where _pprint_str does not
    # try to fold because the data is <= 1
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=37)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0'"
    assert r[1] == "                                    '2'"
    assert r[2] == "                                    '0'"
    assert r[3] == "                                    '0'"
    assert r[4] == "p   Bitmap, Primary               : '8'"
    assert r[5] == "                                    '0'"
    assert r[6] == "                                    '0'"
    assert r[7] == "                                    '0'"
    assert r[8] == "                                    '0'"
    assert r[9] == "                                    '0'"
    assert r[10] == "                                    '0'"
    assert r[11] == "                                    '0'"
    assert r[12] == "                                    '0'"
    assert r[13] == "                                    '0'"
    assert r[14] == "                                    '0'"
    assert r[15] == "                                    '0'"
    assert r[16] == "                                    '0'"
    assert r[17] == "                                    '0'"
    assert r[18] == "                                    '0'"
    assert r[19] == "                                    '0'"
    assert r[20] == "1   Bitmap, Secondary             : '0'"
    assert r[21] == "                                    '0'"
    assert r[22] == "                                    '0'"
    assert r[23] == "                                    '0'"
    assert r[24] == "                                    '0'"
    assert r[25] == "                                    '0'"
    assert r[26] == "                                    '0'"
    assert r[27] == "                                    '0'"
    assert r[28] == "                                    '0'"
    assert r[29] == "                                    '0'"
    assert r[30] == "                                    '0'"
    assert r[31] == "                                    '0'"
    assert r[32] == "                                    '0'"
    assert r[33] == "                                    '0'"
    assert r[34] == "                                    '2'"
    assert r[35] == "                                    '0'"
    assert r[36] == "123 Reserved for Private Use      : ''"
    assert r[37] == ""
    assert len(r) == 38

    # This is a test scenario where _pprint_bytes does not
    # try to fold because the data is <= 1
    doc_dec = {}
    doc_dec["t"] = "0200"
    doc_dec["123"] = "1"
    _, doc_enc = iso8583.encode(doc_dec, spec)
    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=44)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b'0200'"
    assert r[1] == "p   Bitmap, Primary               : b'\\x80'"
    assert r[2] == "                                    b'\\x00'"
    assert r[3] == "                                    b'\\x00'"
    assert r[4] == "                                    b'\\x00'"
    assert r[5] == "                                    b'\\x00'"
    assert r[6] == "                                    b'\\x00'"
    assert r[7] == "                                    b'\\x00'"
    assert r[8] == "                                    b'\\x00'"
    assert r[9] == "1   Bitmap, Secondary             : b'\\x00'"
    assert r[10] == "                                    b'\\x00'"
    assert r[11] == "                                    b'\\x00'"
    assert r[12] == "                                    b'\\x00'"
    assert r[13] == "                                    b'\\x00'"
    assert r[14] == "                                    b'\\x00'"
    assert r[15] == "                                    b'\\x00 '"
    assert r[16] == "123 Reserved for Private Use      : b'001' b'1'"
    assert r[17] == ""
    assert len(r) == 18

    # This is a test scenario where _pprint_str does not
    # try to fold because the data is <= 1
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=37)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : '0'"
    assert r[1] == "                                    '2'"
    assert r[2] == "                                    '0'"
    assert r[3] == "                                    '0'"
    assert r[4] == "p   Bitmap, Primary               : '8'"
    assert r[5] == "                                    '0'"
    assert r[6] == "                                    '0'"
    assert r[7] == "                                    '0'"
    assert r[8] == "                                    '0'"
    assert r[9] == "                                    '0'"
    assert r[10] == "                                    '0'"
    assert r[11] == "                                    '0'"
    assert r[12] == "                                    '0'"
    assert r[13] == "                                    '0'"
    assert r[14] == "                                    '0'"
    assert r[15] == "                                    '0'"
    assert r[16] == "                                    '0'"
    assert r[17] == "                                    '0'"
    assert r[18] == "                                    '0'"
    assert r[19] == "                                    '0'"
    assert r[20] == "1   Bitmap, Secondary             : '0'"
    assert r[21] == "                                    '0'"
    assert r[22] == "                                    '0'"
    assert r[23] == "                                    '0'"
    assert r[24] == "                                    '0'"
    assert r[25] == "                                    '0'"
    assert r[26] == "                                    '0'"
    assert r[27] == "                                    '0'"
    assert r[28] == "                                    '0'"
    assert r[29] == "                                    '0'"
    assert r[30] == "                                    '0'"
    assert r[31] == "                                    '0'"
    assert r[32] == "                                    '0'"
    assert r[33] == "                                    '0'"
    assert r[34] == "                                    '2'"
    assert r[35] == "                                    '0'"
    assert r[36] == "123 Reserved for Private Use      : '1'"
    assert r[37] == ""
    assert len(r) == 38


    # Negative line parameters
    doc_dec = {}
    doc_dec["t"] = "0200"
    doc_dec["123"] = "1"
    _, doc_enc = iso8583.encode(doc_dec, spec)
    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, desc_width=-99, line_width=-99)
    r = sio.getvalue().split("\n")
    assert r[0] == "t  : b'0'"
    assert r[1] == "     b'2'"
    assert r[2] == "     b'0'"
    assert r[3] == "     b'0'"
    assert r[4] == "p  : b'\\x80'"
    assert r[5] == "     b'\\x00'"
    assert r[6] == "     b'\\x00'"
    assert r[7] == "     b'\\x00'"
    assert r[8] == "     b'\\x00'"
    assert r[9] == "     b'\\x00'"
    assert r[10] == "     b'\\x00'"
    assert r[11] == "     b'\\x00'"
    assert r[12] == "1  : b'\\x00'"
    assert r[13] == "     b'\\x00'"
    assert r[14] == "     b'\\x00'"
    assert r[15] == "     b'\\x00'"
    assert r[16] == "     b'\\x00'"
    assert r[17] == "     b'\\x00'"
    assert r[18] == "     b'\\x00'"
    assert r[19] == "     b' '"
    assert r[20] == "123: b'001' b'1'"
    assert r[21] == ""
    assert len(r) == 22

    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, desc_width=-99, line_width=-99)
    r = sio.getvalue().split("\n")
    assert r[0] == "t  : '0'"
    assert r[1] == "     '2'"
    assert r[2] == "     '0'"
    assert r[3] == "     '0'"
    assert r[4] == "p  : '8'"
    assert r[5] == "     '0'"
    assert r[6] == "     '0'"
    assert r[7] == "     '0'"
    assert r[8] == "     '0'"
    assert r[9] == "     '0'"
    assert r[10] == "     '0'"
    assert r[11] == "     '0'"
    assert r[12] == "     '0'"
    assert r[13] == "     '0'"
    assert r[14] == "     '0'"
    assert r[15] == "     '0'"
    assert r[16] == "     '0'"
    assert r[17] == "     '0'"
    assert r[18] == "     '0'"
    assert r[19] == "     '0'"
    assert r[20] == "1  : '0'"
    assert r[21] == "     '0'"
    assert r[22] == "     '0'"
    assert r[23] == "     '0'"
    assert r[24] == "     '0'"
    assert r[25] == "     '0'"
    assert r[26] == "     '0'"
    assert r[27] == "     '0'"
    assert r[28] == "     '0'"
    assert r[29] == "     '0'"
    assert r[30] == "     '0'"
    assert r[31] == "     '0'"
    assert r[32] == "     '0'"
    assert r[33] == "     '0'"
    assert r[34] == "     '2'"
    assert r[35] == "     '0'"
    assert r[36] == "123: '1'"
    assert r[37] == ""
    assert len(r) == 38
    # fmt: on


def test_pp_invalid_types() -> None:
    """Invalid types should simply be printed as repr()
    If encoded dictionary does not have required 'len' and 'data'
    keys then no data should be printed.
    """
    # fmt: off
    spec = copy.deepcopy(iso8583.specs.default)
    spec["h"]["max_len"] = 0
    spec["h"]["len_type"] = 0

    doc_dec: typing.Dict[str, str] = {}
    doc_dec["t"] = [1, 2, 3, 4] # type: ignore
    doc_dec["123"] = set([1, 2, 3]) # type: ignore

    # standard width = 80
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=80)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : [1, 2, 3, 4]"
    assert r[1] == "123 Reserved for Private Use      : {1, 2, 3}"
    assert r[2] == ""
    assert len(r) == 3

    # trigger unkown dispatch with reduced width = 1 
    sio = StringIO()
    iso8583.pp(doc_dec, spec, stream=sio, line_width=1)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : [1, 2, 3, 4]"
    assert r[1] == "123 Reserved for Private Use      : {1, 2, 3}"
    assert r[2] == ""
    assert len(r) == 3

    # invalid encoded data
    doc_enc: typing.Dict[str, str] = {}
    doc_enc["t"] = {} # type: ignore
    doc_enc["1"] = {"len": b"len"} # type: ignore
    doc_enc["2"] = {"data": b"data"} # type: ignore
    doc_enc["3"] = {"spam": b"eggs"} # type: ignore

    sio = StringIO()
    iso8583.pp(doc_enc, spec, stream=sio, line_width=80)
    r = sio.getvalue().split("\n")
    assert r[0] == "t   Message Type                  : b''"
    assert r[1] == "1   Bitmap, Secondary             : b'len' b''"
    assert r[2] == "2   Primary Account Number (PAN)  : b'data'"
    assert r[3] == "3   Processing Code               : b''"
    assert r[4] == ""
    assert len(r) == 5
    # fmt: on


def test_pp_no_yield_on_empty_string(capsys: typing.Any) -> None:
    for _ in _wrap_bytes_repr(b"", 10):
        print("spam")

    for _ in _wrap_str_repr("", 10):
        print("eggs")

    captured = capsys.readouterr()
    assert captured.out == ""
