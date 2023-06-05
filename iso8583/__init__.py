r"""`iso8583` package serializes and deserializes ISO8583 data between a
``bytes`` or ``bytearray`` instance containing ISO8583 data and a Python ``dict``.

`iso8583` package supports custom specifications. See `iso8583.specs` module.

Use `iso8583.decode` to decode raw iso8583 message.
It returns two dictionaries: one with decoded data and one with encoded data.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> encoded_raw = b'02004000000000000000101234567890'
    >>> decoded, encoded = iso8583.decode(encoded_raw, spec)
    >>> pprint.pprint(decoded)
    {'2': '1234567890', 'p': '4000000000000000', 't': '0200'}
    >>> pprint.pprint(encoded)
    {'2': {'data': b'1234567890', 'len': b'10'},
     'p': {'data': b'4000000000000000', 'len': b''},
     't': {'data': b'0200', 'len': b''}}

Use `iso8583.encode` to encode updated ISO8583 message.
It returns a raw ISO8583 message and a dictionary with encoded data.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> decoded = {
    ...     "t": "0200",
    ...     "2": "1234567890",
    ...     "39": "00"
    ... }
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'0200400000000200000010123456789000')
    >>> pprint.pprint(decoded)
    {'2': '1234567890', '39': '00', 'p': '4000000002000000', 't': '0200'}
    >>> pprint.pprint(encoded)
    {'2': {'data': b'1234567890', 'len': b'10'},
     '39': {'data': b'00', 'len': b''},
     'p': {'data': b'4000000002000000', 'len': b''},
     't': {'data': b'0200', 'len': b''}}

Use `iso8583.pp` to pretty print ISO8583 message.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> encoded_raw = b'02004000000000000000101234567890'
    >>> decoded, encoded = iso8583.decode(encoded_raw, spec)
    >>> iso8583.pp(decoded, spec)
    t   Message Type                  : '0200'
    p   Bitmap, Primary               : '4000000000000000'
    2   Primary Account Number (PAN)  : '1234567890'
    >>> iso8583.pp(encoded, spec)
    t   Message Type                  : b'0200'
    p   Bitmap, Primary               : b'4000000000000000'
    2   Primary Account Number (PAN)  : b'10' b'1234567890'
"""

__version__ = "3.0.0"
__all__ = [
    "pp",
    "decode",
    "DecodeError",
    "encode",
    "EncodeError",
]
__author__ = "Konstantin Novichikhin <konstantin.novichikhin@gmail.com>"

from iso8583.decoder import DecodeError, decode
from iso8583.encoder import EncodeError, encode
from iso8583.tools import pp
