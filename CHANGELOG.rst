Unreleased
----------
- Provide friendlier error messages when failing to decode field, field length, and bitmap.

2.1.0 - 2020-12-24
------------------
- Added support for fields measured in nibbles (half-bytes).

2.0.2 - 2020-11-20
------------------
- Fixed issue `#4 <https://github.com/knovichikhin/pyiso8583/issues/4>`_. Encode secondary bitmap in upper case.

2.0.1 - 2020-08-22
------------------
- Include inline type information into the distribution according to `PEP 561 <https://www.python.org/dev/peps/pep-0561/>`_.
- Address remaining type hint issues.

2.0.0 - 2020-02-21
------------------
**Backwards incompatible**:
  - :func:`iso8583.decode` is updated not to produce bitmap key ``'bm'``.
  - :func:`iso8583.encode` is updated not to expect bitmap key ``'bm'`` to define
    fields to encode. The decision on what fields to encode is based on
    numeric fields in the range of ``'1'-'128'`` present in the decoded
    dictionary.
  - :func:`iso8583.add_field` and :func:`iso8583.del_field` are removed. With the
    removal of bitmap set ``'bm'`` default Python dictionary methods are
    enough.
  - :func:`iso8583.encode` now removes secondary bitmap key ``'1'`` from the decoded
    dictionary if no ``'65'-'128'`` fields are present.
  - :func:`iso8583.pp` function signature changed. The first parameter is renamed
    from ``doc_dec`` to ``doc``.
Other changes:
  - :func:`iso8583.pp` handles both encoded and decoded dictionary output.
  - :func:`iso8583.pp` handles output folding. The defaul line width is set to 80.
    Line width can be configured using new ``line_width`` parameter.

1.0.2 - 2020-01-11
------------------
- Optional proprietary header can now be parsed
  using standard field settings
- Documentation improvements

1.0.1 - 2019-11-11
------------------
- :func:`iso8583.decode` and :func:`iso8583.decode` now return a tuple
- :func:`iso8583.decode` returns a tuple of decoded dict instance
  and encoded dict instance
- :func:`iso8583.encode` returns a tuple of encoded bytes instance
  and encoded dict instance
- Encoded and decoded dict instance keys are now all strings
- Specification keys are now all strings

1.0.0 - 2019-11-04
------------------
Initial release.
