iso8583 - a Python package for parsing ISO8583 data
----------------------------------------------------

|pypi| |docs| |coverage|

`iso8583` package serializes and deserializes ISO8583 data between a ``bytes`` or
``bytearray`` instance containing ISO8583 data and a Python ``dict``.

`iso8583` package supports custom `specifications <https://pyiso8583.readthedocs.io/en/latest/specifications.html>`_
that can define

    * Field length and data encoding, such as BCD, ASCII, EBCDIC, etc.
    * Field type, such as fixed, LLVAR, LLLVAR, etc.
    * Maximum length
    * Optional field description

Multiple specifications can co-exist to support ISO8583 messages for POS, ATM,
file actions, and so on. Simply define a new specification dictionary. `iso8583`
package includes a starter specification in `iso8583.specs` module that can be
used as a base to create own custom/proprietary specifications.

Additional information is available on `RTD <http://pyiso8583.readthedocs.org>`_.

Install::

    pip install pyiso8583

Encoding & Decoding
-------------------

Use `iso8583.decode <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.decode>`_
to decode raw ISO8583 message.
It returns two dictionaries: one with decoded data and one with encoded data.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> encoded_raw = b'02004000000000000000101234567890'
    >>> decoded, encoded = iso8583.decode(encoded_raw, spec)
    >>> pprint.pp(decoded)
    {'t': '0200', 'p': '4000000000000000', '2': '1234567890'}
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'4000000000000000'},
     '2': {'len': b'10', 'data': b'1234567890'}}

Modify the decoded message to send a response back.
Change message type from '0200' to '0210'.
Remove field 2 (PAN). And add field 39 (Response Code).

.. code-block:: python

    >>> decoded['t'] = '0210'
    >>> decoded.pop('2', None)
    '1234567890'
    >>> decoded['39'] = '05'

Use `iso8583.encode <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.encode>`_
to encode updated ISO8583 message.
It returns a raw ISO8583 message and a dictionary with encoded data.

.. code-block:: python

    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'0210000000000200000005')
    >>> pprint.pp(decoded)
    {'t': '0210', 'p': '0000000002000000', '39': '05'}
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0210'},
     'p': {'len': b'', 'data': b'0000000002000000'},
     '39': {'len': b'', 'data': b'05'}}

Pretty Print Messages
---------------------

Use `iso8583.pp <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.pp>`_
to pretty print ISO8583 message.

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

Contribute
----------

`iso8583` package is hosted on `GitHub <https://github.com/knovichikhin/pyiso8583>`_.

Feel free to fork and send contributions over.

.. |pypi| image:: https://img.shields.io/pypi/v/pyiso8583.svg
    :alt: PyPI
    :target:  https://pypi.org/project/pyiso8583/

.. |docs| image:: https://readthedocs.org/projects/pyiso8583/badge/?version=latest
    :alt: Documentation Status
    :target: https://pyiso8583.readthedocs.io/en/latest/?badge=latest

.. |coverage| image:: https://codecov.io/gh/knovichikhin/pyiso8583/branch/master/graph/badge.svg
    :alt: Test coverage
    :target: https://codecov.io/gh/knovichikhin/pyiso8583
