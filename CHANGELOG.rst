4.0.0 - 2025-08-10
------------------
- Add support for tertiary bitmap located in field 65.
- Migration from 3.x.x:
   - This library previously ignored field 65.
     It now processes it as a tertiary bitmap containing map for fields 129-192.
     It's a breaking change for users who use field 65 for another purpose.
     If your spec did not re-purpose field 65 then it's safe to update to 4.x.x.

3.0.0 - 2023-06-05
------------------
- Add support for binary field length
- Drop support for Python 3.6
- Migration from 2.x.x:
   - 2.x.x used `len_enc` set to `b` and `bcd` to represent BCD length encoding.
   - 3.x.x changed that where `len_enc` set to `b` represents binary length encoding.
   - To migrate from 2.x.x update `len_enc` in all specificatations from `b` to `bcd`.

2.2.0 - 2022-01-30
------------------
- Provide friendlier error messages when failing to encode/decode field, field length, and bitmap.
- Clarify Binary-coded decimal field length configuration. Added ``bcd`` value to ``len_enc``
  which is the same as the existing ``b`` value. Both mean that the length is to be encoded as BCD.

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
  - `iso8583.decode` is updated not to produce bitmap key ``'bm'``.
  - `iso8583.encode` is updated not to expect bitmap key ``'bm'`` to define
    fields to encode. The decision on what fields to encode is based on
    numeric fields in the range of ``'1'-'128'`` present in the decoded
    dictionary.
  - `iso8583.add_field` and `iso8583.del_field` are removed. With the
    removal of bitmap set ``'bm'`` default Python dictionary methods are
    enough.
  - `iso8583.encode` now removes secondary bitmap key ``'1'`` from the decoded
    dictionary if no ``'65'-'128'`` fields are present.
  - `iso8583.pp` function signature changed. The first parameter is renamed
    from ``doc_dec`` to ``doc``.
Other changes:
  - `iso8583.pp` handles both encoded and decoded dictionary output.
  - `iso8583.pp` handles output folding. The defaul line width is set to 80.
    Line width can be configured using new ``line_width`` parameter.

1.0.2 - 2020-01-11
------------------
- Optional proprietary header can now be parsed
  using standard field settings
- Documentation improvements

1.0.1 - 2019-11-11
------------------
- `iso8583.decode` and `iso8583.decode` now return a tuple
- `iso8583.decode` returns a tuple of decoded dict instance
  and encoded dict instance
- `iso8583.encode` returns a tuple of encoded bytes instance
  and encoded dict instance
- Encoded and decoded dict instance keys are now all strings
- Specification keys are now all strings

1.0.0 - 2019-11-04
------------------
Initial release.
