=======================================================
iso8583 -- How-To
=======================================================

.. contents:: Table of Contents

Create Own/Proprietary Specifications
-------------------------------------
:mod:`iso8583` comes with specification sample in `iso8583.specs.py`_.
Feel free to copy sample specification ``dict`` and modify it to your needs.
Refer to :mod:`iso8583.specs` for configuration details.

.. _iso8583.specs.py: https://github.com/manoutoftime/pyiso8583/blob/master/iso8583/specs.py

Create ISO8583 Message
----------------------
:mod:`iso8583` converts a Python ``dict`` into a ``bytearray``.
A the minimum the ``dict`` must have

- ``'t'`` key containing message type, e.g. ``'0200'``.
- ``'bm'`` key containing fields numbers to be added to the message.
- ``'1'`` .. ``'128'`` key with data for each field specified in ``'bm'`` set.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> doc_dec = {
    ...     't': '0200',
    ...     'bm': set([3]),
    ...     '3': '111111'}
    >>> raw, doc_enc = iso8583.encode(doc_dec, spec)
    >>> raw
    bytearray(b'02002000000000000000111111')

Let's add another field.

.. code-block:: python

    >>> doc_dec['bm'].add(12)
    >>> doc_dec['12'] = '122530'
    >>> raw, doc_enc = iso8583.encode(doc_dec, spec)
    >>> raw
    bytearray(b'02002010000000000000111111122530')

Add Secondary Bitmap
--------------------
You don't need to explicitly add secondary bitmap.
It's auto generated  when at least one 65-128 field is present.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> doc_dec = {
    ...     't': '0200',
    ...     'bm': set([102]),
    ...     '102': '111111'}
    >>> raw, doc_enc = iso8583.encode(doc_dec, spec)
    >>> raw
    bytearray(b'02008000000000000000000000000400000006111111')
    >>> pprint.pp(doc_enc)
    {'t': {'len': b'', 'data': b'0200'},
     'bm': {1, 102},
     'p': {'len': b'', 'data': b'8000000000000000'},
     '1': {'len': b'', 'data': b'0000000004000000'},
     '102': {'len': b'06', 'data': b'111111'}}

Check for Mandatory Fields
--------------------------
Many ISO8583 implementations need to check if all mandatory fields
are received. It's easy to do this using ``'bm'`` :meth:`set.issuperset`.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b'02004000000000000000101234567890'
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> doc_dec['bm']
    {2}
    >>> mandatory_fields = set([2,3])
    >>> doc_dec['bm'].issuperset(mandatory_fields)
    False
    >>> mandatory_fields = set([2])
    >>> doc_dec['bm'].issuperset(mandatory_fields)
    True

Convert to JSON
----------------
:mod:`iso8583` output is almost JSON ready. All that's required
is to convert ``'bm'`` from :class:`set` to a :class:`list`.

.. code-block:: python

    >>> import json
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> s = b'02004000000000000000101234567890'
    >>> doc_dec, doc_enc = iso8583.decode(s, spec)
    >>> doc_dec['bm'] = sorted(doc_dec['bm'])
    >>> json.dumps(doc_dec)
    '{"bm": [2], "t": "0200", "p": "4000000000000000", "2": "1234567890"}'

Convert from JSON
------------------
Converting :mod:`iso8583` output from JSON back to required dictionary is easy.
All that's required is to convert ``'bm'`` back from :class:`list` to a :class:`set`.

    >>> import json
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> json_data = b'{"bm": [2], "t": "0200", "p": "4000000000000000", "2": "1234567890"}'
    >>> doc_dec = json.loads(json_data)
    >>> doc_dec['bm'] = set(doc_dec['bm'])
    >>> raw, doc_enc = iso8583.encode(doc_dec, spec)
    >>> raw
    bytearray(b'02004000000000000000101234567890')
