r"""An ISO8583 spec is a Python dict instance. It describes how each field
needs to be encoded or decoded.

Fields
------
These dict keys describe relevant specification field:

- 'h' - Message Header. If specification does not have a header then
  set 'max_len' to 0.
- 't' - Message Type Identifier
- 'p' - Primary Bitmap
- 1 .. 128 - Regular fields

Field Properties
----------------
- 'data_encoding' - type of data encoding where:

  - Use 'b' for binary-coded decimal data, e.g. '\x9F\x02' EMV amount where
    ASCII equivalent is '9F02'.
  - Otherwise, provide any valid Python encoding. For example, 'ascii' or
    'latin-1' for ASCII data and 'cp500' or similar for EBCDIC data.

- 'len_encoding' - the same as 'data_encoding' but for field length.
  Some fields, such as ICC data, have binary data but ASCII length.
  This parameter does not affect fixed-length fields.

- 'len_type' - length of field length in bytes.

  - For ASCII and EBCDIC length:

    - 0 = fixed
    - 1 = LVAR
    - 2 = LLVAR
    - 3 = LLLVAR
    - 4 = LLLLVAR, and so on.

  - For binary-coded decimal length:

    - 0 = fixed
    - 1 = LVAR
    - 1 = LLVAR
    - 2 = LLLVAR
    - 2 = LLLLVAR, and so on.

- 'max_len' - maximum length of field in bytes.
  For 0-length fields (fixed) 'max_len' defines the length of field in bytes.

- 'desc' - Description of field that's printed in a pretty format.

Sample Config
-------------
Field 2 that is a BCD fixed length field of 10 bytes::

    specification[2] = {
        'data_encoding': 'ascii',
        'len_encoding': 'ascii',
        'len_type': 0,
        'max_len': 10
    }

Field 3 that is an ASCII LLVAR field of maximum 20 bytes::

    specification[3] = {
        'data_encoding': 'ascii',
        'len_encoding': 'ascii',
        'len_type': 2,
        'max_len': 20
    }
"""

default = {
    "h": {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 0,   'desc': 'Message Header'},
    "t": {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Message Type'},
    "p": {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Bitmap, Primary'},
    1:   {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Bitmap, Secondary'},
    2:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 19,  'desc': 'Primary Account Number (PAN)'},
    3:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Processing Code'},
    4:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Amount, Transaction'},
    5:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Amount, Settlement'},
    6:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Amount, Cardholder Billing'},
    7:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Transmission Date and Time'},
    8:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Amount, Cardholder Billing Fee'},
    9:   {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Conversion Rate, Settlement'},
    10:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Conversion Rate, Cardholder Billing'},
    11:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'System Trace Audit Number'},
    12:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Time, Local Transaction'},
    13:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Local Transaction'},
    14:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Expiration'},
    15:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Settlement'},
    16:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Conversion'},
    17:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Capture'},
    18:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Merchant Type'},
    19:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Acquiring Institution Country Code'},
    20:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'PAN Country Code'},
    21:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Forwarding Institution Country Code'},
    22:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Point-of-Service Entry Mode'},
    23:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'PAN Sequence Number'},
    24:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Network International ID (NII)'},
    25:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Point-of-Service Condition Code'},
    26:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Point-of-Service Capture Code'},
    27:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 1,   'desc': 'Authorizing ID Response Length'},
    28:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Transaction Fee'},
    29:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Settlement Fee'},
    30:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Transaction Processing Fee'},
    31:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Settlement Processing Fee'},
    32:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Acquiring Institution ID Code'},
    33:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Forwarding Institution ID Code'},
    34:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 28,  'desc': 'Primary Account Number, Extended'},
    35:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 37,  'desc': 'Track 2 Data'},
    36:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 104, 'desc': 'Track 3 Data'},
    37:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Retrieval Reference Number'},
    38:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Authorization ID Response'},
    39:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Response Code'},
    40:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Service Restriction Code'},
    41:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Card Acceptor Terminal ID'},
    42:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 15,  'desc': 'Card Acceptor ID Code'},
    43:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 40,  'desc': 'Card Acceptor Name/Location'},
    44:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 25,  'desc': 'Additional Response Data'},
    45:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 76,  'desc': 'Track 1 Data'},
    46:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Additional Data - ISO'},
    47:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Additional Data - National'},
    48:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Additional Data - Private'},
    49:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Currency Code, Transaction'},
    50:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Currency Code, Settlement'},
    51:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Currency Code, Cardholder Billing'},
    52:  {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'PIN'},
    53:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Security-Related Control Information'},
    54:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 240, 'desc': 'Additional Amounts'},
    55:  {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 3, 'max_len': 255, 'desc': 'ICC data'},
    56:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved ISO'},
    57:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    58:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    59:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    60:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    61:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved Private'},
    62:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved Private'},
    63:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved Private'},
    64:  {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'MAC'},
    65:  {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Bitmap, Extended'},
    66:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 1,   'desc': 'Settlement Code'},
    67:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Extended Payment Code'},
    68:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Receiving Institution Country Code'},
    69:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Settlement Institution Country Code'},
    70:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Network Management Information Code'},
    71:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Message Number'},
    72:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Message Number, Last'},
    73:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Date, Action'},
    74:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Credits, Number'},
    75:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Credits, Reversal Number'},
    76:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Debits, Number'},
    77:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Debits, Reversal Number'},
    78:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Transfer, Number'},
    79:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Transfer, Reversal Number'},
    80:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Inquiries, Number'},
    81:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Authorizations, Number'},
    82:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Credits, Processing Fee Amount'},
    83:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Credits, Transaction Fee Amount'},
    84:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Debits, Processing Fee Amount'},
    85:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Debits, Transaction Fee Amount'},
    86:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Credits, Amount'},
    87:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Credits, Reversal Amount'},
    88:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Debits, Amount'},
    89:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Debits, Reversal Amount'},
    90:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 42,  'desc': 'Original Data Elements'},
    91:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 1,   'desc': 'File Update Code'},
    92:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'File Security Code'},
    93:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 5,   'desc': 'Response Indicator'},
    94:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 7,   'desc': 'Service Indicator'},
    95:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 42,  'desc': 'Replacement Amounts'},
    96:  {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Message Security Code'},
    97:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 17,  'desc': 'Amount, Net Settlement'},
    98:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 0, 'max_len': 25,  'desc': 'Payee'},
    99:  {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Settlement Institution ID Code'},
    100: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Receiving Institution ID Code'},
    101: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 17,  'desc': 'File Name'},
    102: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 28,  'desc': 'Account ID 1'},
    103: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 2, 'max_len': 28,  'desc': 'Account ID 2'},
    104: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 100, 'desc': 'Transaction Description'},
    105: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    106: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    107: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    108: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    109: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    110: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    111: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    112: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    113: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    114: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    115: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    116: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    117: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    118: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    119: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    120: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    121: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    122: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    123: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    124: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    125: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    126: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    127: {'data_encoding': 'ascii', 'len_encoding': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    128: {'data_encoding': 'b',     'len_encoding': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'MAC'}
}
