iso8583
=======

|pypi| |docs| |coverage|

`iso8583` module serializes and deserializes ISO8583 data between a ``bytes`` or
``bytearray`` instance containing ISO8583 data and a Python ``dict``.

`iso8583` supports custom `specifications <https://pyiso8583.readthedocs.io/en/latest/specifications.html>`_
that can define field encoding (e.g. ASCII, EBCDIC, ISO8859-1, BCD, etc.),
field types (e.g. fixed, LLVAR, LLLVAR, etc.), and maximum length

Install::

    pip install pyiso8583

Decode iso8583 data received from a socket.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default
    >>> s = b'0200\x40\x10\x00\x00\x00\x00\x00\x00161234567890123456123456'
    >>> doc_dec, doc_enc = iso8583.decode(s, spec=default)

Contents of the produced dictionaries.

.. code-block:: python

    >>> import pprint
    >>> pprint.pp(doc_dec) # Decoded data
    {'bm': {2, 12},
     't': '0200',
     'p': '4010000000000000',
     '2': '1234567890123456',
     '12': '123456'}
    >>> pprint.pp(doc_enc) # Encoded data
    {'bm': {2, 12},
     't': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'@\x10\x00\x00\x00\x00\x00\x00'},
     '2': {'len': b'16', 'data': b'1234567890123456'},
     '12': {'len': b'', 'data': b'123456'}}

Pretty print result using `iso8583.pp`.

.. code-block:: python

    >>> iso8583.pp(doc_dec, spec=default) # Decoded data only
    'bm'  Enabled Fields                      : [2, 12]
    't'   Message Type                        : [0200]
    'p'   Bitmap, Primary                     : [4010000000000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]

Add or remove fields.

.. code-block:: python

    >>> iso8583.del_field(doc_dec, '12') # Decoded data only
    '123456'
    >>> doc_dec['t'] = '0210'
    >>> iso8583.add_field(doc_dec, '39', '00')  # Decoded data only

Encode iso8583 data to send to a socket.

.. code-block:: python

    >>> s, doc_enc = iso8583.encode(doc_dec, spec=default)
    >>> print(s)
    bytearray(b'0210@\x00\x00\x00\x02\x00\x00\x0016123456789012345600')

For more info `read the docs <http://pyiso8583.readthedocs.org>`_.

Contribute
==========

`iso8583` is hosted on `GitHub <https://github.com/manoutoftime/pyiso8583>`_.

Feel free to fork and send contributions over.

.. |pypi| image:: https://img.shields.io/pypi/v/pyiso8583.svg
    :alt: PyPI
    :target:  https://pypi.org/project/pyiso8583/

.. |docs| image:: https://readthedocs.org/projects/pyiso8583/badge/?version=latest
    :alt: Documentation Status
    :target: https://pyiso8583.readthedocs.io/en/latest/?badge=latest

.. |coverage| image:: https://codecov.io/gh/manoutoftime/pyiso8583/branch/master/graph/badge.svg
    :alt: Test coverage
    :target: https://codecov.io/gh/manoutoftime/pyiso8583
