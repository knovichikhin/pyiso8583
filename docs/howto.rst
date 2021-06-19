=======================================================
How-To
=======================================================

Create Own/Proprietary Specifications
-------------------------------------
:mod:`iso8583` comes with specification samples in `iso8583.specs.py`_.
Feel free to copy sample specification and modify it to your needs.

Multiple specifications can be supported at the same time.
Simply declare additional specification dictionary.

Refer to :mod:`iso8583.specs` for configuration details.

.. _iso8583.specs.py: https://github.com/knovichikhin/pyiso8583/blob/master/iso8583/specs.py

Create ISO8583 Message
----------------------
:mod:`iso8583` converts a regular Python ``dict`` into a ``bytearray``.
This dictionary must consist of ``str`` keys and ``str`` values.

At the minimum it must have key ``'t'`` which is the message
type (e.g. ``'0200'``).

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> decoded = {'t': '0200'}
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02000000000000000000')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'0000000000000000'}}
    >>> pprint.pp(decoded)
    {'t': '0200', 'p': '0000000000000000'}

Note that primary bitmap was generated automatically.

An ISO8583 message without any fields is not very useful.
To add fields to the message simply add ``'2'-'128'``
keys with ``str`` data and re-encode.

.. code-block:: python

    >>> decoded['2'] = 'cardholder PAN'
    >>> decoded['3'] = '111111'
    >>> decoded['21'] = '021'
    >>>
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'0200600008000000000014cardholder PAN111111021')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'6000080000000000'},
     '2': {'len': b'14', 'data': b'cardholder PAN'},
     '3': {'len': b'', 'data': b'111111'},
     '21': {'len': b'', 'data': b'021'}}
    >>> pprint.pp(decoded)
    {'t': '0200',
     'p': '6000080000000000',
     '2': 'cardholder PAN',
     '3': '111111',
     '21': '021'}

Let's remove some fields and re-encode.

.. code-block:: python

    >>> decoded.pop('2', None)
    'cardholder PAN'
    >>> decoded.pop('3', None)
    '111111'
    >>>
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02000000080000000000021')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'0000080000000000'},
     '21': {'len': b'', 'data': b'021'}}
    >>> pprint.pp(decoded)
    {'t': '0200', 'p': '0000080000000000', '21': '021'}

Add Secondary Bitmap
--------------------
There is no need to explicitly add or remove secondary bitmap.
It's auto generated when at least one ``'65'-'128'``
fields is present.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> decoded = {
    ...     't': '0200',
    ...     '102': '111111'}
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02008000000000000000000000000400000006111111')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'8000000000000000'},
     '1': {'len': b'', 'data': b'0000000004000000'},
     '102': {'len': b'06', 'data': b'111111'}}
    >>> pprint.pp(decoded)
    {'t': '0200', '102': '111111', 'p': '8000000000000000', '1': '0000000004000000'}

Even if secondary (or primary) bitmap is
specified it's overwritten with correct value.

.. code-block:: python

    >>> decoded = {
    ...     't': '0200',
    ...     'p': 'spam',
    ...     '1': 'eggs',
    ...     '102': '111111'}
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02008000000000000000000000000400000006111111')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'8000000000000000'},
     '1': {'len': b'', 'data': b'0000000004000000'},
     '102': {'len': b'06', 'data': b'111111'}}
    >>> pprint.pp(decoded)
    {'t': '0200', 'p': '8000000000000000', '102': '111111', '1': '0000000004000000'}

Secondary bitmap is removed if it's not required.

.. code-block:: python

    >>> decoded = {
    ...     't': '0200',
    ...     'p': 'spam',
    ...     '1': 'eggs',
    ...     '21': '051'}
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02000000080000000000051')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'0000080000000000'},
     '21': {'len': b'', 'data': b'051'}}
    >>> pprint.pp(decoded)
    {'t': '0200', 'p': '0000080000000000', '21': '051'}

Check for Mandatory Fields
--------------------------
Many ISO8583 implementations need to check if all mandatory fields
are received. It's easy to do this using a set of mandatory fields
and checking if it's a subset of the received fields.

.. code-block:: python

    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> encoded_raw = b'02008000080000000000000000000400000005106111111'
    >>> decoded, encoded = iso8583.decode(encoded_raw, spec)
    >>> pprint.pp(decoded)
    {'t': '0200',
     'p': '8000080000000000',
     '1': '0000000004000000',
     '21': '051',
     '102': '111111'}
    >>> mandatory_fields = frozenset(['2', '21', '102'])
    >>> mandatory_fields.issubset(decoded.keys())
    False
    >>> mandatory_fields = frozenset(['21', '102'])
    >>> mandatory_fields.issubset(decoded.keys())
    True

Convert to and from JSON
------------------------
:mod:`iso8583` output is JSON compatible.

.. code-block:: python

    >>> import json
    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> encoded_raw = b'0200600008000000000014cardholder PAN111111021'
    >>> decoded, encoded = iso8583.decode(encoded_raw, spec)
    >>> pprint.pp(decoded)
    {'t': '0200',
     'p': '6000080000000000',
     '2': 'cardholder PAN',
     '3': '111111',
     '21': '021'}
    >>> decoded_json = json.dumps(decoded)
    >>> decoded_json
    '{"t": "0200", "p": "6000080000000000", "2": "cardholder PAN", "3": "111111", "21": "021"}'

And back.

.. code-block:: python

    >>> encoded_raw, encoded = iso8583.encode(json.loads(decoded_json), spec)
    >>> encoded_raw
    bytearray(b'0200600008000000000014cardholder PAN111111021')

:mod:`iso8583.specs` specifications are also JSON compatible.

.. code-block:: python

    >>> import json
    >>> import pprint
    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> spec_json = json.dumps(spec)
    >>> decoded = {
    ...     't': '0200',
    ...     '2': 'PAN'}
    >>> encoded_raw, encoded = iso8583.encode(decoded, json.loads(spec_json))
    >>> encoded_raw
    bytearray(b'0200400000000000000003PAN')
    >>> pprint.pp(encoded)
    {'t': {'len': b'', 'data': b'0200'},
     'p': {'len': b'', 'data': b'4000000000000000'},
     '2': {'len': b'03', 'data': b'PAN'}}
    >>> pprint.pp(decoded)
    {'t': '0200', '2': 'PAN', 'p': '4000000000000000'}

Sending Binary Data
-------------------
Sometimes data needs to be sent in binary.
Let's add some EMV data as a hexchar string.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> decoded = {
    ...     't': '0200',
    ...     '55': '9F02060000000123455F340102'}

Let's define field 55 as an LLLVAR binary field with ascii length.
Normally, this should be defined in the specification itself.
But for demonstration purposes specification can be changed on the fly.

.. code-block:: python

    >>> spec['55']['data_enc'] = 'b'
    >>> spec['55']['len_enc'] = 'ascii'
    >>> spec['55']['len_type'] = 3
    >>> spec['55']['max_len'] = 999

And encode the data.

.. code-block:: python

    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02000000000000000200013\x9f\x02\x06\x00\x00\x00\x01#E_4\x01\x02')

Sending Binary Coded Decimal Data
---------------------------------
Some ancient systems require data to be sent in BCD.
Let's send an odd length PAN as an LLVAR BCD field with BCD length.
Since, this field has to handle odd data, let's also define a PAD digit.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> decoded = {
    ...     't': '0200',
    ...     '2': '121200000002121'}

Let's define field 2 as an LLVAR BCD field with BCD length measured in nibbles.
The field is padded on the right with a ``'0'`` because half a byte cannot be sent by itself.

.. code-block:: python

    >>> spec['2']['data_enc'] = 'b'
    >>> spec['2']['len_enc'] = 'b'
    >>> spec['2']['len_type'] = 1
    >>> spec['2']['max_len'] = 19
    >>> spec['2']['len_count'] = 'nibbles'
    >>> spec['2']['right_pad'] = '0'

And encode the data.

.. code-block:: python

    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)
    >>> encoded_raw
    bytearray(b'02004000000000000000\x15\x12\x12\x00\x00\x00\x02\x12\x10')
