iso8583
-------

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

Decode raw iso8583 message using `iso8583.decode <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.decode>`_.
It returns two dictionaries: one with decoded data and one with encoded data.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b'02004000000000000000101234567890'
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> pprint.pp(doc_dec) # Decoded data
    {'bm': {2}, 't': '0200', 'p': '4000000000000000', '2': '1234567890'}
    >>> pprint.pp(doc_enc) # Broken down encoded data
    {'bm': {2},
     't': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'4000000000000000'},
     '2': {'len': b'10', 'data': b'1234567890'}}

Modify the decoded message to send a response back.
Change message type from '0200' to '0210'.
Remove field 2 (PAN). And add field 39 (Response Code).

.. code-block:: python

    >>> doc_dec['t'] = '0210'
    >>> doc_dec['bm'].discard(2)
    >>> doc_dec['bm'].add(39)
    >>> doc_dec['39'] = '05'

Encode updated ISO8583 message using `iso8583.encode <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.encode>`_.
It returns a raw ISO8583 message and a dictionary with encoded data.

.. code-block:: python

    >>> s, doc_enc = iso8583.encode(doc_dec, spec)
    >>> s
    bytearray(b'0210000000000200000005')
    >>> pprint.pp(doc_enc)
    {'t': {'len': b'', 'data': b'0210'},
     'bm': {39},
     'p': {'len': b'', 'data': b'0000000002000000'},
     '39': {'len': b'', 'data': b'05'}}

Optional Helper Functions
-------------------------

    * Pretty print a decoded dictionary using `iso8583.pp <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.pp>`_
    * Add/update fields in a decoded dictionary using `iso8583.add_field <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.add_field>`_
    * Remove fields in a decoded dictionary using `iso8583.del_field <https://pyiso8583.readthedocs.io/en/latest/functions.html#iso8583.del_field>`_

Contribute
----------

`iso8583` package is hosted on `GitHub <https://github.com/manoutoftime/pyiso8583>`_.

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
