import sys as _sys
from typing import Optional, TextIO


def add_field(doc_dec: dict, field: str, val: str) -> None:
    r"""Add or override field and its value in ISO8583 dictionary.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    field : str
        Field key to be added
    val : str
        Field value to be added

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b"02004010100000000000161234567890123456123456840"
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> iso8583.pp(doc_dec, spec)
    'bm'  Enabled Fields                      : [2, 12, 20]
    't'   Message Type                        : [0200]
    'p'   Bitmap, Primary                     : [4010100000000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]
    '20'  PAN Country Code                    : [840]
    >>> iso8583.add_field(doc_dec, "t", "0210")
    >>> iso8583.add_field(doc_dec, "39", "00")
    >>> s, doc_enc = iso8583.encode(doc_dec, spec)
    >>> iso8583.pp(doc_dec, spec)
    'bm'  Enabled Fields                      : [2, 12, 20, 39]
    't'   Message Type                        : [0210]
    'p'   Bitmap, Primary                     : [4010100002000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]
    '20'  PAN Country Code                    : [840]
    '39'  Response Code                       : [00]
    """
    if "bm" not in doc_dec:
        doc_dec["bm"] = set()

    if field.isnumeric():
        doc_dec["bm"].add(int(field))

    doc_dec[field] = val


def del_field(doc_dec: dict, field: str) -> Optional[str]:
    r"""Delete field from ISO8583 dictionary.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    field : int or str
        Field key to be deleted

    Returns
    -------
    Key Value or None
        Deleted field value. None if the field did not exist.

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b"02004010100000000000161234567890123456123456840"
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> iso8583.pp(doc_dec, spec)
    'bm'  Enabled Fields                      : [2, 12, 20]
    't'   Message Type                        : [0200]
    'p'   Bitmap, Primary                     : [4010100000000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]
    '20'  PAN Country Code                    : [840]
    >>> iso8583.del_field(doc_dec, "20")
    '840'
    >>> s, doc_enc = iso8583.encode(doc_dec, spec)
    >>> iso8583.pp(doc_dec, spec)
    'bm'  Enabled Fields                      : [2, 12]
    't'   Message Type                        : [0200]
    'p'   Bitmap, Primary                     : [4010000000000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]
    """
    if "bm" not in doc_dec:
        doc_dec["bm"] = set()

    if field.isnumeric():
        doc_dec["bm"].discard(int(field))

    return doc_dec.pop(field, None)


def pp(
    doc_dec: dict, spec: dict, desc_width: int = 36, stream: Optional[TextIO] = None
) -> None:
    r"""Pretty Print Python dict containing decoded ISO8583 data.

    Parameters
    ----------
    doc_dec : dict
        Dict containing decoded ISO8583 data
    spec : dict
        A Python dict defining ISO8583 specification.
        See iso8583.specs module for examples.
    desc_width : int, optional
        Width of field description that's printed (default 36).
        Specify 0 to print no descriptions.
    stream : stream, optional
        An output stream. The only method used on the stream
        object is the file protocol's write() method.
        If not specified, the :func:`iso8583.pp` adopts
        `sys.stdout`.

    Notes
    -----
    For :func:`iso8583.pp` to work in all circumstances it's recommended
    to be used after :func:`iso8583.encode` or :func:`iso8583.decode`.

    Examples
    --------
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b"02004010100000000000161234567890123456123456840"
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> iso8583.pp(doc_dec, spec)
    'bm'  Enabled Fields                      : [2, 12, 20]
    't'   Message Type                        : [0200]
    'p'   Bitmap, Primary                     : [4010100000000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]
    '20'  PAN Country Code                    : [840]
    """
    if stream is None:
        stream = _sys.stdout

    try:
        bm = doc_dec["bm"]
    except KeyError:
        bm = set()

    stream.write(
        "{index:5s} {desc: <{desc_width}}: {val}\n".format(
            index=repr("bm"),
            desc="Enabled Fields"[:desc_width],
            desc_width=desc_width,
            val=sorted(bm),
        )
    )

    if "h" in doc_dec:
        _pp_field(doc_dec, spec, desc_width, stream, "h")

    if "t" in doc_dec:
        _pp_field(doc_dec, spec, desc_width, stream, "t")

    if "p" in doc_dec:
        _pp_field(doc_dec, spec, desc_width, stream, "p")

    # Sorted list of field numbers as strings
    for f_id in [str(i) for i in sorted(bm)]:
        _pp_field(doc_dec, spec, desc_width, stream, f_id)


def _pp_field(
    doc_dec: dict, spec: dict, desc_width: int, stream: TextIO, f_id: str
) -> None:
    stream.write(
        "{index:5s} {desc: <{desc_width}}: ".format(
            index=repr(f_id),
            desc=spec[f_id]["desc"][:desc_width],
            desc_width=desc_width,
        )
    )

    if spec[f_id]["len_type"] > 0:
        stream.write(
            "{length:0{length_type}d} ".format(
                length=len(doc_dec[f_id]), length_type=spec[f_id]["len_type"]
            )
        )

    stream.write("[{val}]\n".format(val=doc_dec[f_id]))
