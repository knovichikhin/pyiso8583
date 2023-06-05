import sys as _sys
from typing import Any, Callable, Dict, Generator, Mapping, Optional, TextIO, Union

__all__ = ["pp"]

DecodedDict = Mapping[str, str]
EncodedDict = Mapping[str, Mapping[str, bytes]]
SpecDict = Mapping[str, Mapping[str, Any]]


def pp(
    doc: Union[DecodedDict, EncodedDict],
    spec: SpecDict,
    desc_width: int = 30,
    stream: Optional[TextIO] = None,
    line_width: int = 80,
) -> None:
    r"""Pretty Print Python dict containing ISO8583 data.

    Parameters
    ----------
    doc : dict
        Dict containing ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See iso8583.specs module for examples.
    desc_width : int, optional
        Field description width (default 30).
        Specify 0 to print no descriptions.
    stream : stream, optional
        An output stream. The only method used on the stream
        object is the file protocol's write() method.
        If not specified, the :func:`iso8583.pp` adopts
        `sys.stdout`.
    line_width : int, optional
        Attempted maximum width of output line (default 80).

    Notes
    -----
    For the most correct information to be displayed by :func:`iso8583.pp`
    it's recommended to call it after :func:`iso8583.encode` or
    :func:`iso8583.decode`.

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b"02004010100000000000161234567890123456123456840"
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> iso8583.pp(doc_dec, spec)
    t   Message Type                  : '0200'
    p   Bitmap, Primary               : '4010100000000000'
    2   Primary Account Number (PAN)  : '1234567890123456'
    12  Time, Local Transaction       : '123456'
    20  PAN Country Code              : '840'
    """

    desc_width = int(desc_width)
    line_width = int(line_width)

    if stream is None:
        stream = _sys.stdout

    if "h" in doc and spec["h"]["max_len"] > 0:
        _pp_field(doc, spec, desc_width, stream, line_width, "h")

    if "t" in doc:
        _pp_field(doc, spec, desc_width, stream, line_width, "t")

    if "p" in doc:
        _pp_field(doc, spec, desc_width, stream, line_width, "p")

    for field_key in sorted(
        [k for k in doc.keys() if isinstance(k, str) and k.isnumeric()], key=int
    ):
        _pp_field(doc, spec, desc_width, stream, line_width, field_key)


def _pp_field(
    doc: Union[DecodedDict, EncodedDict],
    spec: SpecDict,
    desc_width: int,
    stream: TextIO,
    line_width: int,
    field_key: str,
) -> None:
    indent = 5
    stream.write("{index:3s}".format(index=str(field_key)))

    if desc_width > 0:
        stream.write(
            " {desc: <{desc_width}}".format(
                desc=spec[field_key]["desc"][:desc_width],
                desc_width=desc_width,
            )
        )
        indent += desc_width + 1

    stream.write(": ")

    doc_field = doc[field_key]

    if isinstance(doc_field, dict):
        field_length = doc_field.get("len", b"")
        if len(field_length) > 0:
            stream.write("{} ".format(repr(field_length)))
            indent += len(repr(field_length)) + 1

        obj = doc_field.get("data", b"")
    else:
        obj = doc_field

    rep = repr(obj)
    if len(rep) + indent > line_width:
        p = _dispatch.get(type(obj).__repr__, None)
        if p is not None:
            p(obj, stream, indent, line_width)
            stream.write("\n")
            return

    stream.write("{}\n".format(repr(obj)))


_dispatch: Dict[Any, Callable[[Any, TextIO, int, int], None]] = {}


def _pprint_str(obj: str, stream: TextIO, indent: int, width: int) -> None:
    if len(obj) <= 1:
        stream.write(repr(obj))
        return

    delim = ""
    for rep in _wrap_str_repr(obj, width - indent):
        stream.write(delim)
        stream.write(rep)
        if not delim:
            delim = "\n" + " " * indent


_dispatch[str.__repr__] = _pprint_str


def _pprint_bytes(obj: bytes, stream: TextIO, indent: int, width: int) -> None:
    if len(obj) <= 1:
        stream.write(repr(obj))
        return

    delim = ""
    for rep in _wrap_bytes_repr(obj, width - indent):
        stream.write(delim)
        stream.write(rep)
        if not delim:
            delim = "\n" + " " * indent


_dispatch[bytes.__repr__] = _pprint_bytes


def _wrap_str_repr(obj: str, width: int) -> Generator[str, None, None]:
    # because this functions yields entire width of a string at a time,
    # reduce width by 2 to account for '' around repr(str)
    if width > 3:
        width -= 2
    else:
        width = 1

    for i in range(0, len(obj), width):
        yield repr(obj[i : i + width])


def _wrap_bytes_repr(obj: bytes, width: int) -> Generator[str, None, None]:
    current = b""

    for i in range(0, len(obj)):
        part = obj[i : i + 1]
        candidate = current + part

        if len(repr(candidate)) > width:
            if current:
                yield repr(current)
            current = part
        else:
            current = candidate

    if current:
        yield repr(current)
