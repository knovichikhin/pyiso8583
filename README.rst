iso8583
=======

`iso8583` serializes and deserializes ISO8583 data between a ``bytes`` or
``bytearray`` instance containing ISO8583 data and a Python ``dict``.

Install::

    pip install pyiso8583

Decode iso8583 data received from a socket.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default
    >>> s = b'0200\x40\x10\x10\x10\x00\x00\x00\x00161234567890123456123456111D00000000'
    >>> d = iso8583.decode(s, spec=default)

Print result using Python's `pprint`.

.. code-block:: python

    >>> import pprint
    >>> pprint.pp(d)
    {'bm': {2, 28, 12, 20},
     't': {'e': {'len': b'', 'data': b'0200'}, 'd': '0200'},
     'p': {'e': {'len': b'', 'data': b'@\x10\x10\x10\x00\x00\x00\x00'},
           'd': '4010101000000000'},
     2: {'e': {'len': b'16', 'data': b'1234567890123456'}, 'd': '1234567890123456'},
     12: {'e': {'len': b'', 'data': b'123456'}, 'd': '123456'},
     20: {'e': {'len': b'', 'data': b'111'}, 'd': '111'},
     28: {'e': {'len': b'', 'data': b'D00000000'}, 'd': 'D00000000'}}

Each field is structured as follows::

    'field': { # Can be header, type, primary bitmap, or any other field
        'e': { # Encoded values for length and data as it was received
            'len': b'',
            'data': b''
        },
        'd': '' # Decoded data
    }

    'bm': set() # A set of enabled fields. Includes primary and secondary bitmaps

Print result using `iso8583.pp`.

.. code-block:: python

    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20, 28]
    t   Message Type                        : [0200]
    p   Bitmap, Primary                     : [4010101000000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    28  Amount, Transaction Fee             : [D00000000]

Remove field 28, convert received messaged into a response, and encode it.

.. code-block:: python

    >>> iso8583.del_field(d, 28)
    {'e': {'len': b'', 'data': b'D00000000'}, 'd': 'D00000000'}
    >>> iso8583.add_field(d, 39, '00')
    >>> iso8583.add_field(d, 't', '0210')
    >>> s = iso8583.encode(d, spec=default)
    >>> print(s)
    bytearray(b'0210@\x10\x10\x00\x02\x00\x00\x0016123456789012345612345611100')
    >>> iso8583.pp(d, spec=default)
    bm  Enabled Fields                      : [2, 12, 20, 39]
    t   Message Type                        : [0210]
    p   Bitmap, Primary                     : [4010100002000000]
    2   Primary Account Number (PAN)        : 16 [1234567890123456]
    12  Time, Local Transaction             : [123456]
    20  PAN Country Code                    : [111]
    39  Response Code                       : [00]

For more info `read the docs <http://iso8583.readthedocs.org>`_.

Contribute
==========

`iso8583` is hosted on `GitHub <https://github.com/manoutoftime/pyiso8583>`_.

Feel free to fork and send contributions over.

Developing
==========

Install::

    pip install pyiso8583

Run Tests::

    python -m pytest

Lint::

    flake8 iso8583

Build docs::

    ./docs/make html

