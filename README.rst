iso8583
=======

|pypi| |docs| |coverage| |downloads|

`iso8583` module serializes and deserializes ISO8583 data between a ``bytes`` or
``bytearray`` instance containing ISO8583 data and a Python ``dict``.

`iso8583` supports custom `specifications <https://pyiso8583.readthedocs.io/en/latest/specifications.html>`_
that can define field encoding (e.g. ASCII, EBCDIC, ISO8859-1, BCD, etc.),
field types (e.g. fixed, LLVAR, LLLVAR, etc.), and maximum length.
Multiple specifications can be supported at the same time (e.g. POS,
ATM, file actions, and so on).

Install::

    pip install pyiso8583

Decode iso8583 data received from a socket using `iso8583.decode <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.decode>`_.
It returns two dictionaries: one with decoded data and one with encoded data.
Encoded data dictionary can be used for verifying MAC and PIN as well as
any other task that requires raw data.

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

Pretty print result using `iso8583.pp <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.pp>`_.
Field description can be optionally omitted. Output can be written
to a stream for logging.

.. code-block:: python

    >>> iso8583.pp(doc_dec, spec=default) # Decoded data only
    'bm'  Enabled Fields                      : [2, 12]
    't'   Message Type                        : [0200]
    'p'   Bitmap, Primary                     : [4010000000000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '12'  Time, Local Transaction             : [123456]

Add or remove fields in decoded data dictionary using
`iso8583.add_field <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.add_field>`_ and
`iso8583.del_field <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.del_field>`_.
`iso8583.add_field <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.add_field>`_
acts as update if the field is already present. It's also possible to
simply edit decoded data, since it's a regular Python dictionary.

.. code-block:: python

    >>> iso8583.del_field(doc_dec, '12')
    '123456'
    >>> doc_dec['t'] = '0210'
    >>> iso8583.add_field(doc_dec, '39', '00')

Encode iso8583 data to send to a socket using `iso8583.encode <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.encode>`_.
It returns bytearray instance with data to send to a socket
and a dictionary with encoded data. Encoded data dictionary can be used
for generating MAC.

.. code-block:: python

    >>> s, doc_enc = iso8583.encode(doc_dec, spec=default)
    >>> s
    bytearray(b'0210@\x00\x00\x00\x02\x00\x00\x0016123456789012345600')
    >>> iso8583.pp(doc_dec, spec=default)
    'bm'  Enabled Fields                      : [2, 39]
    't'   Message Type                        : [0210]
    'p'   Bitmap, Primary                     : [4000000002000000]
    '2'   Primary Account Number (PAN)        : 16 [1234567890123456]
    '39'  Response Code                       : [00]

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

.. |downloads| image:: https://pepy.tech/badge/pyiso8583/month
    :alt: downloads/month
    :target: https://pepy.tech/project/pyiso8583/month
