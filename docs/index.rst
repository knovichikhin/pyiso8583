Python ISO8583 Protocol Serializer & Deserializer
=================================================

:mod:`iso8583` is a Python package that serializes and deserializes ISO8583
data between a ``bytes`` or ``bytearray`` instance containing ISO8583
data and a Python ``dict``.

At a Glance
~~~~~~~~~~~~

:mod:`iso8583` package supports custom specifications. See :mod:`iso8583.specs` module.

Use :func:`iso8583.decode` to decode raw iso8583 message.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> encoded_raw = b'02004000000000000000101234567890'
    >>> decoded, encoded = iso8583.decode(encoded_raw, spec)

Use :func:`iso8583.encode` to encode updated ISO8583 message.
It returns a raw ISO8583 message and a dictionary with encoded data.

.. code-block:: python

    >>> import iso8583
    >>> from iso8583.specs import default_ascii as spec
    >>> decoded = {"t": "0200", "2": "1234567890", "39": "00"}
    >>> encoded_raw, encoded = iso8583.encode(decoded, spec)

To install::

    pip install pyiso8583

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents:

   intro
   howto
   specifications
   functions
   changelog
