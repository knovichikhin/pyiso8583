import pytest
import iso8583

spec = {
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

def test_header_no_key():
    '''
    Message header is required and key is not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[1]['len_type'] = 0
    spec[1]['max_len'] = 0

    d = {
        'h': {},
        't': {}
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.'h'..'d'.: field h"):
        iso8583.encode(d, spec=spec)

    d = {
        't': {}
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.'h'..'d'.: field h"):
        iso8583.encode(d, spec=spec)

def test_header_ascii_absent():
    '''
    ASCII header is not required by spec and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 0
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': ''
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'0200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert ('e' in d['h']) == False
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_ascii_present():
    '''
    ASCII header is required by spec and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_ebcdic_absent():
    '''
    EBCDIC header is not required by spec and not provided
    '''
    spec['h']['data_encoding'] = 'cp500'
    spec['h']['max_len'] = 0
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': ''
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'0200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert ('e' in d['h']) == False
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_ebcdic_present():
    '''
    EBCDIC header is required by spec and provided
    '''
    spec['h']['data_encoding'] = 'cp500'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'\x88\x85\x81\x84\x85\x990200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'\x88\x85\x81\x84\x85\x99'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_bdc_absent():
    '''
    BDC header is not required by spec and not provided
    '''
    spec['h']['data_encoding'] = 'b'
    spec['h']['max_len'] = 0
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': ''
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'0200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert ('e' in d['h']) == False
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_bcd_present():
    '''
    BCD header is required by spec and provided
    '''
    spec['h']['data_encoding'] = 'b'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'A1A2A3A4A5A6'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'\xA1\xA2\xA3\xA4\xA5\xA60200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'\xA1\xA2\xA3\xA4\xA5\xA6'
    assert d['h']['d'] == 'A1A2A3A4A5A6'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_not_required_provided():
    '''
    String header is not required by spec but provided.
    No error. Header is not included in the message.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 0
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'0200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert ('e' in d['h']) == False
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_header_negative_missing():
    '''
    String header is required by spec but not provided.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': ''
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 6: field h"):
        iso8583.encode(d, spec=spec)

def test_header_negative_partial():
    '''
    String header is required by spec but partially provided.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'head'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 4 bytes, expecting 6: field h"):
        iso8583.encode(d, spec=spec)

def test_header_negative_incorrect_encoding():
    '''
    String header is required by spec and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_encoding'] = 'invalid'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field h"):
        iso8583.encode(d, spec=spec)

def test_header_negative_incorrect_ascii_data():
    '''
    ASCII header is required by spec and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': b'\xff\xff\xff\xff\xff\xff'.decode('latin-1')
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode characters in position 0-5: ordinal not in range.128..: field h"):
        iso8583.encode(d, spec=spec)

def test_header_negative_incorrect_bcd_data():
    '''
    BCD header is required by spec and provided.
    However, the data is not hex
    '''
    spec['h']['data_encoding'] = 'b'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 0.: field h"):
        iso8583.encode(d, spec=spec)

def test_type_no_key():
    '''
    Message type is required and key is not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[1]['len_type'] = 0
    spec[1]['max_len'] = 0

    d = {
        'h': {
            'd': 'header'
        },
        't': {},
        2: {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.'t'..'d'.: field t"):
        iso8583.encode(d, spec=spec)

    d = {
        'h': {
            'd': 'header'
        },
        2: {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.'t'..'d'.: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ascii_absent():
    '''
    ASCII message type is required and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': ''
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 4: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ascii_partial():
    '''
    ASCII message type is required and partial is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '02'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 2 bytes, expecting 4: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ascii_over_max():
    '''
    ASCII message type is required and over max is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '02101'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 5 bytes, expecting 4: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ascii_incorrect_data():
    '''
    ASCII message type is required and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': b'\xff\xff\xff\xff'.decode('latin-1')
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode characters in position 0-3: ordinal not in range.128..: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ascii_present():
    '''
    ASCII message type is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0200\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_type_ebcdic_absent():
    '''
    EBCDIC message type is required and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'cp500'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': ''
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 4: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ebcdic_partial():
    '''
    EBCDIC message type is required and partial provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'cp500'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '02'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 2 bytes, expecting 4: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ebcdic_over_max():
    '''
    EBCDIC message type is required and over max provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'cp500'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '02101'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 5 bytes, expecting 4: field t"):
        iso8583.encode(d, spec=spec)

def test_type_ebcdic_present():
    '''
    EBCDIC message type is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'cp500'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0200'
        },
        'bm': set(),
        'p': {
            'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header\xf0\xf2\xf0\xf0\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'\xf0\xf2\xf0\xf0'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_type_bdc_absent():
    '''
    BDC message type is required and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'b'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': ''
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 2: field t"):
        iso8583.encode(d, spec=spec)

def test_type_bdc_partial():
    '''
    BDC message type is required and partial is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'b'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '02'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 1 bytes, expecting 2: field t"):
        iso8583.encode(d, spec=spec)

def test_type_bdc_over_max():
    '''
    BDC message type is required and over max is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'b'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '021000'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 3 bytes, expecting 2: field t"):
        iso8583.encode(d, spec=spec)

def test_type_bdc_odd():
    '''
    BDC message type is required and odd length is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'b'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '021'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 3.: field t"):
        iso8583.encode(d, spec=spec)

def test_type_bdc_non_hex():
    '''
    BDC message type is required and provided
    However, the data is not hex
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'b'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '021x'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 3.: field t"):
        iso8583.encode(d, spec=spec)

def test_type_bcd_present():
    '''
    BCD message type is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'b'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0200'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'\x02\x00'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '0000000000000000'
    assert d['bm'] == set()

def test_type_incorrect_encoding():
    '''
    String message type is required and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'invalid'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0200'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field t"):
        iso8583.encode(d, spec=spec)

def test_bitmap_no_key():
    '''
    ASCII fixed field is required and 'bm' key is not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[1]['len_type'] = 0
    spec[1]['max_len'] = 0

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        2: {
            'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.'bm'.: field p"):
        iso8583.encode(d, spec=spec)

def test_bitmap_range():
    '''
    ISO8583 bitmaps must be between 1 and 128.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0200'
        },
        'bm': set(),
        'p': {
             'd': ''
        }
    }

    d['bm'] = set([0])
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm"):
        iso8583.encode(d, spec=spec)

    d['bm'] = set([129])
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm"):
        iso8583.encode(d, spec=spec)

    d['bm'] = set(range(0, 129))
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm"):
        iso8583.encode(d, spec=spec)

    d['bm'] = set(range(1, 130))
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm"):
        iso8583.encode(d, spec=spec)

def test_bitmap_remove_secondary():
    '''
    If 65-128 fields are not in bitmap then remove field 1.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['data_encoding'] = 'ascii'
    spec[2]['len_encoding'] = 'ascii'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 19

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0200'
        },
        'bm': set(),
        'p': {
             'd': ''
        },
        2: {
             'd': '1234567890'
        },
    }

    d['bm'] = set([1, 2])
    s = iso8583.encode(d, spec=spec)
    print(d)
    assert s == b'header0200\x40\x00\x00\x00\x00\x00\x00\x00101234567890'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'10'
    assert d[2]['e']['data'] == b'1234567890'
    assert d[2]['d'] == '1234567890'
    assert d['bm'] == set([2])

def test_bitmap_add_secondary():
    '''
    If one of 65-128 fields are in bitmap then add field 1.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[66]['data_encoding'] = 'ascii'
    spec[66]['len_encoding'] = 'ascii'
    spec[66]['len_type'] = 2
    spec[66]['max_len'] = 19

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0200'
        },
        'bm': set(),
        'p': {
             'd': ''
        },
        66: {
             'd': '1234567890'
        },
    }

    d['bm'] = set([66])
    s = iso8583.encode(d, spec=spec)
    print(d)
    assert s == b'header0200\x80\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00101234567890'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0200'
    assert d['t']['d'] == '0200'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x80\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '8000000000000000'
    assert d[1]['e']['len'] == b''
    assert d[1]['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d[1]['d'] == '4000000000000000'
    assert d[66]['e']['len'] == b'10'
    assert d[66]['e']['data'] == b'1234567890'
    assert d[66]['d'] == '1234567890'
    assert d['bm'] == set([1, 66])

def test_field_no_key():
    '''
    Field is required and not key provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[1]['len_type'] = 0
    spec[1]['max_len'] = 0

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {}
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.2..'d'.: field 2"):
        iso8583.encode(d, spec=spec)

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2])
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Define d.2..'d'.: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ascii_absent():
    '''
    ASCII fixed field is required and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ascii_partial():
    '''
    ASCII fixed field is required and partially provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 1 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ascii_over_max():
    '''
    ASCII fixed field is required and over max provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '123'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 3 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ascii_incorrect_data():
    '''
    ASCII fixed field is required and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': b'\xff\xff'.decode('latin-1')
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode characters in position 0-1: ordinal not in range.128..: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ascii_present():
    '''
    ASCII fixed field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '22'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x0022'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b''
    assert d[2]['e']['data'] == b'22'
    assert d[2]['d'] == '22'
    assert d['bm'] == set([2])

def test_fixed_field_ascii_present_zero_legnth():
    '''
    ASCII zero-length fixed field is required and provided
    This is pointless but should work.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 0
    spec[2]['data_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b''
    assert d[2]['e']['data'] == b''
    assert d[2]['d'] == ''
    assert d['bm'] == set([2])

def test_fixed_field_ebcdic_absent():
    '''
    EBCDIC fixed field is required and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ebcdic_partial():
    '''
    EBCDIC fixed field is required and partially provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 1 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ebcdic_over_max():
    '''
    EBCDIC fixed field is required and over max provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '123'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 3 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_ebcdic_present():
    '''
    EBCDIC fixed field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '22'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf2\xf2'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b''
    assert d[2]['e']['data'] == b'\xf2\xf2'
    assert d[2]['d'] == '22'
    assert d['bm'] == set([2])

def test_fixed_field_ebcdic_present_zero_legnth():
    '''
    EBCDIC zero-length fixed field is required and provided
    This is pointless but should work.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 0
    spec[2]['data_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b''
    assert d[2]['e']['data'] == b''
    assert d[2]['d'] == ''
    assert d['bm'] == set([2])

def test_fixed_field_bdc_absent():
    '''
    BDC fixed field is required and not provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 0 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_bdc_partial():
    '''
    BDC fixed field is required and partial is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '12'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 1 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_bdc_over_max():
    '''
    BDC fixed field is required and over max is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '123456'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 3 bytes, expecting 2: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_bdc_odd():
    '''
    BDC fixed field is required and odd length is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '12345'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 5.: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_bdc_non_hex():
    '''
    BDC fixed field is required and provided
    However, the data is not hex
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '11xx'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 2.: field 2"):
        iso8583.encode(d, spec=spec)

def test_fixed_field_bcd_present():
    '''
    BCD fixed field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\x11\x22'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b''
    assert d[2]['e']['data'] == b'\x11\x22'
    assert d[2]['d'] == '1122'
    assert d['bm'] == set([2])

def test_fixed_field_bcd_present_zero_length():
    '''
    BCD zero-length fixed field is required and provided
    This is pointless but should work.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 0
    spec[2]['data_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b''
    assert d[2]['e']['data'] == b''
    assert d[2]['d'] == ''
    assert d['bm'] == set([2])

def test_fixed_field_incorrect_encoding():
    '''
    Fixed field is required and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 0
    spec[2]['max_len'] = 2
    spec[2]['data_encoding'] = 'invalid'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field 2"):
        iso8583.encode(d, spec=spec)

def test_variable_field_ascii_over_max():
    '''
    ASCII variable field is required and over max provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'ascii'
    spec[2]['len_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '12345678901'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 11 bytes, larger than maximum 10: field 2"):
        iso8583.encode(d, spec=spec)

def test_variable_field_ascii_present():
    '''
    ASCII variable field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'ascii'
    spec[2]['len_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'04'
    assert d[2]['e']['data'] == b'1122'
    assert d[2]['d'] == '1122'
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00041122'
    assert d['bm'] == set([2])

def test_variable_field_ascii_present_zero_legnth():
    '''
    ASCII zero-length variable field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'ascii'
    spec[2]['len_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'00'
    assert d[2]['e']['data'] == b''
    assert d[2]['d'] == ''
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x0000'
    assert d['bm'] == set([2])

def test_variable_field_ebcdic_over_max():
    '''
    EBCDIC variable field is required and over max provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'ascii'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'cp500'
    spec[2]['len_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '12345678901'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 11 bytes, larger than maximum 10: field 2"):
        iso8583.encode(d, spec=spec)

def test_variable_field_ebcdic_present():
    '''
    EBCDIC variable field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'cp500'
    spec[2]['len_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'\xf0\xf4'
    assert d[2]['e']['data'] == b'\xf1\xf1\xf2\xf2'
    assert d[2]['d'] == '1122'
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf4\xf1\xf1\xf2\xf2'
    assert d['bm'] == set([2])

def test_variable_field_ebcdic_present_zero_legnth():
    '''
    EBCDIC zero-length variable field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'cp500'
    spec[2]['len_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'\xf0\xf0'
    assert d[2]['e']['data'] == b''
    assert d[2]['d'] == ''
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf0'
    assert d['bm'] == set([2])

def test_variable_field_bdc_over_max():
    '''
    BDC variable field is required and over max is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 5
    spec[2]['data_encoding'] = 'b'
    spec[2]['len_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '123456789012'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 6 bytes, larger than maximum 5: field 2"):
        iso8583.encode(d, spec=spec)

def test_variable_field_bdc_odd():
    '''
    BDC variable field is required and odd length is provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'b'
    spec[2]['len_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '12345'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 5.: field 2"):
        iso8583.encode(d, spec=spec)

def test_variable_field_bdc_ascii_length():
    '''
    BDC variable field is required and provided
    The length is in ASCII.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 3
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'b'
    spec[2]['len_encoding'] = 'ascii'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'002'
    assert d[2]['e']['data'] == b'\x11\x22'
    assert d[2]['d'] == '1122'
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00002\x11\x22'
    assert d['bm'] == set([2])

def test_variable_field_bdc_ebcdic_length():
    '''
    BDC variable field is required and provided
    The length is in WBCDIC.
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 3
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'b'
    spec[2]['len_encoding'] = 'cp500'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'\xf0\xf0\xf2'
    assert d[2]['e']['data'] == b'\x11\x22'
    assert d[2]['d'] == '1122'
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf0\xf2\x11\x22'
    assert d['bm'] == set([2])

def test_variable_field_bcd_present():
    '''
    BCD variable field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'b'
    spec[2]['len_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': '1122'
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'\x00\x02'
    assert d[2]['e']['data'] == b'\x11\x22'
    assert d[2]['d'] == '1122'
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\x00\x02\x11\x22'
    assert d['bm'] == set([2])

def test_variable_field_bcd_present_zero_length():
    '''
    BCD zero-length variable field is required and provided
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'b'
    spec[2]['len_encoding'] = 'b'

    d = {
        'h': {
             'd': 'header'
        },
        't': {
             'd': '0210'
        },
        'bm': set([2]),
        2: {
             'd': ''
        }
    }

    s = iso8583.encode(d, spec=spec)
    assert d['h']['e']['len'] == b''
    assert d['h']['e']['data'] == b'header'
    assert d['h']['d'] == 'header'
    assert d['t']['e']['len'] == b''
    assert d['t']['e']['data'] == b'0210'
    assert d['t']['d'] == '0210'
    assert d['p']['e']['len'] == b''
    assert d['p']['e']['data'] == b'\x40\x00\x00\x00\x00\x00\x00\x00'
    assert d['p']['d'] == '4000000000000000'
    assert d[2]['e']['len'] == b'\x00\x00'
    assert d[2]['e']['data'] == b''
    assert d[2]['d'] == ''
    assert s == b'header0210\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert d['bm'] == set([2])

def test_variable_field_incorrect_encoding():
    '''
    Variable field is required and provided.
    However, the spec encoding is not correct for length
    '''
    spec['h']['data_encoding'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_encoding'] = 'ascii'
    spec['p']['data_encoding'] = 'b'
    spec[2]['len_type'] = 2
    spec[2]['max_len'] = 10
    spec[2]['data_encoding'] = 'ascii'
    spec[2]['len_encoding'] = 'invalid'

    d = {
        'h': {
            'd': 'header'
        },
        't': {
            'd': '0210'
        },
        'bm': set([2]),
        2: {
            'd': '1122'
        }
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode length .unknown encoding: invalid.: field 2"):
        iso8583.encode(d, spec=spec)
