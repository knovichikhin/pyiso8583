import pickle
import pytest
import iso8583

spec = {
    "h":   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 0,   'desc': 'Message Header'},
    "t":   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Message Type'},
    "p":   {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Bitmap, Primary'},
    '1':   {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Bitmap, Secondary'},
    '2':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 19,  'desc': 'Primary Account Number (PAN)'},
    '3':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Processing Code'},
    '4':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Amount, Transaction'},
    '5':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Amount, Settlement'},
    '6':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Amount, Cardholder Billing'},
    '7':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Transmission Date and Time'},
    '8':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Amount, Cardholder Billing Fee'},
    '9':   {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Conversion Rate, Settlement'},
    '10':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Conversion Rate, Cardholder Billing'},
    '11':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'System Trace Audit Number'},
    '12':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Time, Local Transaction'},
    '13':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Local Transaction'},
    '14':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Expiration'},
    '15':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Settlement'},
    '16':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Conversion'},
    '17':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Date, Capture'},
    '18':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Merchant Type'},
    '19':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Acquiring Institution Country Code'},
    '20':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'PAN Country Code'},
    '21':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Forwarding Institution Country Code'},
    '22':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Point-of-Service Entry Mode'},
    '23':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'PAN Sequence Number'},
    '24':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Network International ID (NII)'},
    '25':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Point-of-Service Condition Code'},
    '26':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Point-of-Service Capture Code'},
    '27':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 1,   'desc': 'Authorizing ID Response Length'},
    '28':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Transaction Fee'},
    '29':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Settlement Fee'},
    '30':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Transaction Processing Fee'},
    '31':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 9,   'desc': 'Amount, Settlement Processing Fee'},
    '32':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Acquiring Institution ID Code'},
    '33':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Forwarding Institution ID Code'},
    '34':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 28,  'desc': 'Primary Account Number, Extended'},
    '35':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 37,  'desc': 'Track 2 Data'},
    '36':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 104, 'desc': 'Track 3 Data'},
    '37':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Retrieval Reference Number'},
    '38':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Authorization ID Response'},
    '39':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Response Code'},
    '40':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Service Restriction Code'},
    '41':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Card Acceptor Terminal ID'},
    '42':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 15,  'desc': 'Card Acceptor ID Code'},
    '43':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 40,  'desc': 'Card Acceptor Name/Location'},
    '44':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 25,  'desc': 'Additional Response Data'},
    '45':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 76,  'desc': 'Track 1 Data'},
    '46':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Additional Data - ISO'},
    '47':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Additional Data - National'},
    '48':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Additional Data - Private'},
    '49':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Currency Code, Transaction'},
    '50':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Currency Code, Settlement'},
    '51':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Currency Code, Cardholder Billing'},
    '52':  {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'PIN'},
    '53':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Security-Related Control Information'},
    '54':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 240, 'desc': 'Additional Amounts'},
    '55':  {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 3, 'max_len': 255, 'desc': 'ICC data'},
    '56':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved ISO'},
    '57':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    '58':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    '59':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    '60':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved National'},
    '61':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved Private'},
    '62':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved Private'},
    '63':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved Private'},
    '64':  {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'MAC'},
    '65':  {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Bitmap, Extended'},
    '66':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 1,   'desc': 'Settlement Code'},
    '67':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'Extended Payment Code'},
    '68':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Receiving Institution Country Code'},
    '69':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Settlement Institution Country Code'},
    '70':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 3,   'desc': 'Network Management Information Code'},
    '71':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Message Number'},
    '72':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 4,   'desc': 'Message Number, Last'},
    '73':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 6,   'desc': 'Date, Action'},
    '74':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Credits, Number'},
    '75':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Credits, Reversal Number'},
    '76':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Debits, Number'},
    '77':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Debits, Reversal Number'},
    '78':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Transfer, Number'},
    '79':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Transfer, Reversal Number'},
    '80':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Inquiries, Number'},
    '81':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 10,  'desc': 'Authorizations, Number'},
    '82':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Credits, Processing Fee Amount'},
    '83':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Credits, Transaction Fee Amount'},
    '84':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Debits, Processing Fee Amount'},
    '85':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 12,  'desc': 'Debits, Transaction Fee Amount'},
    '86':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Credits, Amount'},
    '87':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Credits, Reversal Amount'},
    '88':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Debits, Amount'},
    '89':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 16,  'desc': 'Debits, Reversal Amount'},
    '90':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 42,  'desc': 'Original Data Elements'},
    '91':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 1,   'desc': 'File Update Code'},
    '92':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 2,   'desc': 'File Security Code'},
    '93':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 5,   'desc': 'Response Indicator'},
    '94':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 7,   'desc': 'Service Indicator'},
    '95':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 42,  'desc': 'Replacement Amounts'},
    '96':  {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'Message Security Code'},
    '97':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 17,  'desc': 'Amount, Net Settlement'},
    '98':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 0, 'max_len': 25,  'desc': 'Payee'},
    '99':  {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Settlement Institution ID Code'},
    '100': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 11,  'desc': 'Receiving Institution ID Code'},
    '101': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 17,  'desc': 'File Name'},
    '102': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 28,  'desc': 'Account ID 1'},
    '103': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 2, 'max_len': 28,  'desc': 'Account ID 2'},
    '104': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 100, 'desc': 'Transaction Description'},
    '105': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '106': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '107': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '108': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '109': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '110': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '111': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for ISO Use'},
    '112': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '113': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '114': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '115': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '116': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '117': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '118': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '119': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for National Use'},
    '120': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '121': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '122': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '123': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '124': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '125': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '126': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '127': {'data_enc': 'ascii', 'len_enc': 'ascii', 'len_type': 3, 'max_len': 999, 'desc': 'Reserved for Private Use'},
    '128': {'data_enc': 'b',     'len_enc': 'ascii', 'len_type': 0, 'max_len': 8,   'desc': 'MAC'}
}

def test_DecodeError_exception():
    '''
    Validate DecodeError class
    '''
    s = b''

    try:
        iso8583.decode(s, spec=spec)
    except iso8583.DecodeError as e:
        assert e.doc_dec == ({
            'bm': set(),
            't': ''
        })
        assert e.doc_enc == ({
            'bm': set(),
            't': {
                'data': b'',
                'len': b''
            }
        })
        assert e.msg == "Field data is 0 bytes, expecting 4"
        assert e.field == 't'
        assert e.pos == 0
        assert e.args[0] == "Field data is 0 bytes, expecting 4: field t pos 0"

def test_DecodeError_exception_pickle():
    '''
    Validate DecodeError class with pickle
    '''
    s = b''

    try:
        iso8583.decode(s, spec=spec)
    except iso8583.DecodeError as e:
        p = pickle.dumps(e)
        e_unpickled = pickle.loads(p)

        assert e.doc_dec == e_unpickled.doc_dec
        assert e.doc_enc == e_unpickled.doc_enc
        assert e.msg == e_unpickled.msg
        assert e.field == e_unpickled.field
        assert e.pos == e_unpickled.pos
        assert e.args[0] == e_unpickled.args[0]

def test_input_type():
    '''
    Decode accepts only bytes or bytesarray.
    '''
    s = {}
    with pytest.raises(
        TypeError,
        match="the ISO8583 data must be bytes or bytearray, not dict"):
        iso8583.decode(s, spec=spec)

def test_header_ascii_absent():
    '''
    ASCII header is not required by spec and not provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 0
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'02100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert ('h' in doc_dec) == False
    assert ('h' in doc_enc) == False

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_header_ascii_present():
    '''
    ASCII header is required by spec and provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header02100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_header_ebcdic_absent():
    '''
    EBCDIC header is not required by spec and not provided
    '''
    spec['h']['data_enc'] = 'cp500'
    spec['h']['max_len'] = 0
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'02100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert ('h' in doc_dec) == False
    assert ('h' in doc_enc) == False

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_header_ebcdic_present():
    '''
    EBCDIC header is required by spec and provided
    '''
    spec['h']['data_enc'] = 'cp500'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'\x88\x85\x81\x84\x85\x9902100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'\x88\x85\x81\x84\x85\x99'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_header_bcd_absent():
    '''
    BDC header is not required by spec and not provided
    '''
    spec['h']['data_enc'] = 'b'
    spec['h']['max_len'] = 0
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'02100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert ('h' in doc_dec) == False
    assert ('h' in doc_enc) == False

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_header_bcd_present():
    '''
    BCD header is required by spec and provided
    '''
    spec['h']['data_enc'] = 'b'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'\xA1\xA2\xA3\xA4\xA5\xA602100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'\xA1\xA2\xA3\xA4\xA5\xA6'
    assert doc_dec['h'] == 'A1A2A3A4A5A6'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_header_negative_missing():
    '''
    String header is required by spec but not provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b''
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 6: field h pos 0"):
        iso8583.decode(s, spec=spec)

def test_header_negative_partial():
    '''
    String header is required by spec but partially provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'head'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 4 bytes, expecting 6: field h pos 0"):
        iso8583.decode(s, spec=spec)

def test_header_negative_incorrect_encoding():
    '''
    String header is required by spec and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_enc'] = 'invalid'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header02100000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field h pos 0"):
        iso8583.decode(s, spec=spec)

def test_header_negative_incorrect_ascii_data():
    '''
    ASCII header is required by spec and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'\xff\xff\xff\xff\xff\xff02100000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field h pos 0"):
        iso8583.decode(s, spec=spec)

def test_header_negative_incorrect_bcd_data():
    '''
    BCD header is required by spec and provided.
    However, the data is not hex.
    Note: this passes, 'header' is valid hex data when decoding.
    '''
    spec['h']['data_enc'] = 'b'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header02100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == '686561646572'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_type_ascii_absent():
    '''
    ASCII message type is required by spec and not provided
    Note: here parser picks up message type as '0000' and fails at primary bitmap.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 12 bytes, expecting 16: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_type_ascii_present():
    '''
    ASCII message type is required by spec and provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header02100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_type_ebcdic_absent():
    '''
    EBCDIC message type is required by spec and not provided
    Note: here parser picks up message type as '0000' and fails at primary bitmap.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'cp500'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 12 bytes, expecting 16: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_type_ebcdic_present():
    '''
    ASCII message type is required by spec and provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'cp500'
    spec['p']['data_enc'] = 'ascii'

    s = b'header\xf0\xf2\xf1\xf00000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'\xf0\xf2\xf1\xf0'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_type_bcd_absent():
    '''
    BCD message type is required by spec and not provided
    Note: here parser picks up message type as '\x30\x30' and fails at primary bitmap.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'b'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 14 bytes, expecting 16: field p pos 8"):
        iso8583.decode(s, spec=spec)

def test_type_bcd_present():
    '''
    ASCII message type is required by spec and provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'b'
    spec['p']['data_enc'] = 'ascii'

    s = b'header\x02\x100000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'\x02\x10'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def test_type_negative_missing():
    '''
    Type is required for all messages
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 4: field t pos 6"):
        iso8583.decode(s, spec=spec)

def test_type_negative_partial():
    '''
    Message type is required all messages but partially provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header02'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 2 bytes, expecting 4: field t pos 6"):
        iso8583.decode(s, spec=spec)

def test_type_negative_incorrect_encoding():
    '''
    Message type is required by spec and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'invalid'
    spec['p']['data_enc'] = 'ascii'

    s = b'header02100000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field t pos 6"):
        iso8583.decode(s, spec=spec)

def test_type_negative_incorrect_ascii_data():
    '''
    Message type is required by spec and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header\xff\xff\xff\xff0000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field t pos 6"):
        iso8583.decode(s, spec=spec)

def test_type_negative_incorrect_bcd_data():
    '''
    BCD message type is required by spec and provided.
    However, the data is not hex.
    Note: this passes, 'ab' is valid hex data when decoding.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'b'
    spec['p']['data_enc'] = 'ascii'

    s = b'headerab0000000000000000'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'ab'
    assert doc_dec['t'] == '6162'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'0000000000000000'
    assert doc_dec['p'] == '0000000000000000'

    assert doc_enc['bm'] == set()
    assert doc_dec['bm'] == set()

def util_set2bitmap(bm):
    '''
    Enable bits specified in a bm set and return a bitmap bytearray
    '''
    s = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    # Disable secondary bitmap if no 65-128 fields are present
    if bm.isdisjoint(range(65, 129)):
        bm.discard(1)
    else:
        bm.add(1)

    for f in bm:
        f -= 1                   # bms start at 1. Make them zero-bound
        byte = int(f / 8)        # Place this particular bit in a byte where it belongs
        bit = 7 - (f - byte * 8) # Determine bit to enable. 7th or left-most is fields 1, 9, 17, etc.
        s[byte] |= 1 << bit

    if 1 in bm:
        return s
    else:
        return s[0:8]

def util_set2field_data(bm, spec, data_enc, len_enc, len_type):
    '''
    Create dummy field data for fields specified in a bm set and return a bytearray
    Assume that field data is always 2 or 4 bytes representing field number.
    For example, field #65 is represented as '0065' with length 4 or
    \x00\x65 with length 2.
    '''

    s = bytearray()
    for f in [str(i) for i in sorted(bm)]:
        # Secondary bitmap is already appended
        if f == '1':
            continue

        # BCD data is always half of ASCII/EBCDIC data
        if data_enc == 'b':
            spec[f]['max_len'] = 2
        else:
            spec[f]['max_len'] = 4

        spec[f]['data_enc'] = data_enc
        spec[f]['len_enc'] = len_enc
        spec[f]['len_type'] = len_type

        # Append length according to type and encoding
        if len_type > 0:
            if len_enc == 'b':
                # odd length is not allowed, double it up for string translation, e.g.:
                # length '2' must be '02' to translate to \x02
                # length '02' must be '0004' to translate to \x00\x02
                s += bytearray.fromhex('{:0{len_type}d}'.format(spec[f]['max_len'], len_type=len_type*2))
            else:
                s += bytearray('{:0{len_type}d}'.format(spec[f]['max_len'], len_type=len_type), len_enc)

        # Append data according to encoding
        if data_enc == 'b':
            s += bytearray.fromhex('{:04d}'.format(int(f)))
        else:
            s += bytearray('{:04d}'.format(int(f)), data_enc)

    return s

def test_primary_bitmap_ascii():
    '''
    This test will validate bitmap decoding for fields 1-64
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'ascii')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

    bm = set()
    for i in range(64, 2, -1):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'ascii')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

def test_primary_bitmap_ebcdic():
    '''
    This test will validate bitmap decoding for fields 1-64
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'cp500'

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'cp500')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

    bm = set()
    for i in range(64, 2, -1):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'cp500')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

def test_primary_bitmap_bcd():
    '''
    This test will validate bitmap decoding for fields 1-64
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'b'

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        s = bytearray(b'header0210')
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

    bm = set()
    for i in range(64, 2, -1):
        bm.add(i)
        s = bytearray(b'header0210')
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

def test_primary_bitmap_negative_missing():
    '''
    Primary bitmap is required for all messages
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0200'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 16: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_primary_bitmap_negative_partial():
    '''
    Primary bitmap is required for all messages but partially provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0200FFFF'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 4 bytes, expecting 16: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_primary_bitmap_negative_incorrect_encoding():
    '''
    Primary bitmap is required for all messages and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'invalid'

    s = b'header02100000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_primary_bitmap_negative_incorrect_ascii_data():
    '''
    Primary bitmap is required for all messages and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0210\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_primary_bitmap_negative_incorrect_ascii_hex():
    '''
    Primary bitmap is required for all messages and provided.
    However, the data is not ASCII hex
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0210incorrecthexdata'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .non-hexadecimal number found in fromhex.. arg at position 0.: field p pos 10"):
        iso8583.decode(s, spec=spec)

def test_primary_bitmap_negative_incorrect_bcd_data():
    '''
    BCD primary bitmap is required for all messages and provided.
    However, the data is not hex.
    Note: this passes, '00000000' is valid hex data when decoding.
    It will fail on field parsing, because no fields were provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'b'
    spec['3']['data_enc'] = 'ascii'
    spec['3']['len_enc'] = 'ascii'
    spec['3']['len_type'] = 0
    spec['3']['max_len'] = 4

    s = b'header021000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 4: field 3 pos 18"):
        iso8583.decode(s, spec=spec)

def test_primary_bitmap_negative_leftover_data():
    '''
    Primary bitmap is required by spec and provided.
    However, there is extra data left in message.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'

    s = b'header0210000000000000000012'
    with pytest.raises(
        iso8583.DecodeError,
        match="Extra data after last field: field p pos 26"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_ascii():
    '''
    This test will validate bitmap decoding for field 1-128
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'ascii'

    bm = set()
    for i in range(1, 129):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'ascii')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

    bm = set()
    for i in range(128, 1, -1):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'ascii')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

def test_secondary_bitmap_ebcdic():
    '''
    This test will validate bitmap decoding for field 1-128
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'cp500'
    spec['1']['data_enc'] = 'cp500'

    bm = set()
    for i in range(1, 129):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'cp500')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

    bm = set()
    for i in range(128, 1, -1):
        bm.add(i)
        s = bytearray(b'header0210')
        s += bytearray(util_set2bitmap(bm).hex(), 'cp500')
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

def test_secondary_bitmap_bcd():
    '''
    This test will validate bitmap decoding for field 1-128
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'b'
    spec['1']['data_enc'] = 'b'

    bm = set()
    for i in range(1, 129):
        bm.add(i)
        s = bytearray(b'header0210')
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

    bm = set()
    for i in range(128, 1, -1):
        bm.add(i)
        s = bytearray(b'header0210')
        s += util_set2bitmap(bm)
        s += util_set2field_data(bm, spec, 'ascii', 'ascii', 0)
        doc_dec, doc_enc = iso8583.decode(s, spec=spec)
        assert doc_enc['bm']^bm == set()
        assert doc_dec['bm']^bm == set()

def test_secondary_bitmap_negative_missing():
    '''
    Secondary bitmap is required but not provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'ascii'

    s = b'header02008000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 16: field 1 pos 26"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_negative_partial():
    '''
    Secondary bitmap is required for all messages but partially provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'ascii'

    s = b'header02008000000000000000FFFF'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 4 bytes, expecting 16: field 1 pos 26"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_negative_incorrect_encoding():
    '''
    Secondary bitmap is required and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'invalid'

    s = b'header021080000000000000000000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field 1 pos 26"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_negative_incorrect_ascii_data():
    '''
    Secondary bitmap is required for all messages and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'ascii'

    s = b'header02108000000000000000\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field 1 pos 26"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_negative_incorrect_ascii_hex():
    '''
    Secondary bitmap is required for all messages and provided.
    However, the data is not ASCII hex
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'ascii'

    s = b'header02108000000000000000incorrecthexdata'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .non-hexadecimal number found in fromhex.. arg at position 0.: field 1 pos 26"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_negative_incorrect_bcd_data():
    '''
    BCD secondary bitmap is required for all messages and provided.
    However, the data is not hex.
    Note: this passes, '00000000' is valid hex data when decoding.
    It will fail on field parsing, because no fields were provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'b'
    spec['67']['len_enc'] = 'ascii'
    spec['67']['data_enc'] = 'ascii'
    spec['67']['len_type'] = 0
    spec['67']['max_len'] = 4

    s = b'header0210800000000000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 4: field 67 pos 34"):
        iso8583.decode(s, spec=spec)

def test_secondary_bitmap_negative_leftover_data():
    '''
    Secondary bitmap is required by spec and provided.
    However, there is extra data left in message.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['1']['data_enc'] = 'ascii'

    s = b'header02108000000000000000000000000000000012'
    with pytest.raises(
        iso8583.DecodeError,
        match="Extra data after last field: field 1 pos 42"):
        iso8583.decode(s, spec=spec)

def test_fields_mix():
    '''
    This test will validate field decoding with BCD, ASCII and EBCDIC mix
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 0
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'b'
    spec['1']['data_enc'] = 'b'

    field_lenght = [0, 1, 2, 3, 4]
    encoding = ['b', 'ascii', 'cp500']

    bm = set()
    for i in range(2, 65):
        bm.add(i)
        for l in field_lenght:
            for data_e in encoding:
                for len_e in encoding:
                    s = bytearray(b'0210')
                    s += util_set2bitmap(bm)
                    s += util_set2field_data(bm, spec, data_e, len_e, l)

                    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

                    assert doc_enc['bm']^bm == set()
                    assert doc_dec['bm']^bm == set()

                    for f in doc_dec['bm']:
                        if f == 1:
                            continue
                        assert doc_dec[str(f)] == '{0:04}'.format(f)

    bm = set()
    for i in range(65, 129):
        bm.add(i)
        for l in field_lenght:
            for data_e in encoding:
                for len_e in encoding:
                    s = bytearray(b'0210')
                    s += util_set2bitmap(bm)
                    s += util_set2field_data(bm, spec, data_e, len_e, l)

                    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

                    assert doc_enc['bm']^bm == set()
                    assert doc_dec['bm']^bm == set()

                    for f in doc_dec['bm']:
                        if f == 1:
                            continue
                        assert doc_dec[str(f)] == '{0:04}'.format(f)

def test_field_zero_length_field():
    '''
    Zero-length field is required and provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header0210400000000000000000'

    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'4000000000000000'
    assert doc_dec['p'] == '4000000000000000'

    assert doc_enc['2']['len'] == b'00'
    assert doc_enc['2']['data'] == b''
    assert doc_dec['2'] == ''

    assert doc_enc['bm'] == set([2])
    assert doc_dec['bm'] == set([2])

def test_field_length_negative_missing():
    '''
    Field length is required but not provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header02004000000000000000'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field length is 0 bytes wide, expecting 2: field 2 pos 26"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_partial():
    '''
    Field length is required but partially provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header020040000000000000001'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field length is 1 bytes wide, expecting 2: field 2 pos 26"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_incorrect_encoding():
    '''
    Field length is required and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'invalid'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header0200400000000000000010'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .unknown encoding: invalid.: field 2 pos 26"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_incorrect_ascii_data():
    '''
    Field length is required and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header02004000000000000000\xff\xff'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field 2 pos 26"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_incorrect_ascii_hex():
    '''
    Field length is required and provided.
    However, the data is not ASCII hex
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header02004000000000000000gg'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode length .invalid literal for int.. with base 10: 'gg'.: field 2 pos 26"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_incorrect_bcd_data():
    '''
    BCD field length is required and provided.
    However, the data is not hex.
    Note: this passes, 'g' is valid hex data when decoding.
    It will fail on field parsing, because no field was provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'b'
    spec['2']['len_type'] = 1
    spec['2']['max_len'] = 99

    s = b'header02004000000000000000g'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 67: field 2 pos 27"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_leftover_data():
    '''
    Field length is required and provided.
    However, there is extra data left in message.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header02104000000000000000003456'
    with pytest.raises(
        iso8583.DecodeError,
        match="Extra data after last field: field 2 pos 28"):
        iso8583.decode(s, spec=spec)

def test_field_length_negative_over_max():
    '''
    Field length is required and provided.
    However, it's over the specified maximum.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 1
    spec['2']['max_len'] = 4

    s = b'header020040000000000000008'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 8 bytes, larger than maximum 4: field 2 pos 26"):
        iso8583.decode(s, spec=spec)

def test_field_negative_missing():
    '''
    Field is required but not provided
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header0200400000000000000002'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 0 bytes, expecting 2: field 2 pos 28"):
        iso8583.decode(s, spec=spec)

def test_field_negative_partial():
    '''
    Field is required but partially provided.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header02004000000000000000021'
    with pytest.raises(
        iso8583.DecodeError,
        match="Field data is 1 bytes, expecting 2: field 2 pos 28"):
        iso8583.decode(s, spec=spec)

def test_field_negative_incorrect_encoding():
    '''
    Field is required and provided.
    However, the spec encoding is not correct
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'invalid'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header0200400000000000000002xx'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .unknown encoding: invalid.: field 2 pos 28"):
        iso8583.decode(s, spec=spec)

def test_field_negative_incorrect_ascii_data():
    '''
    Field is required and provided.
    However, the data is not ASCII
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header0200400000000000000002\xff\xff'
    with pytest.raises(
        iso8583.DecodeError,
        match="Failed to decode .'ascii' codec can't decode byte 0xff in position 0: ordinal not in range.128..: field 2 pos 28"):
        iso8583.decode(s, spec=spec)

def test_field_negative_incorrect_ascii_hex():
    '''
    Field is required and provided.
    However, the data is not ASCII hex
    Note: this passes, 'gg' is valid hex data when decoding.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 2
    spec['2']['max_len'] = 4

    s = b'header0210400000000000000002gg'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'4000000000000000'
    assert doc_dec['p'] == '4000000000000000'

    assert doc_enc['2']['len'] == b'02'
    assert doc_enc['2']['data'] == b'gg'
    assert doc_dec['2'] == 'gg'

    assert doc_enc['bm'] == set([2])
    assert doc_dec['bm'] == set([2])

def test_field_negative_incorrect_bcd_data():
    '''
    BCD Field is required and provided.
    However, the data is not hex.
    Note: this passes, 'g' is valid hex data when decoding.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'b'
    spec['2']['len_type'] = 1
    spec['2']['max_len'] = 99

    s = b'header02104000000000000000\x01g'
    doc_dec, doc_enc = iso8583.decode(s, spec=spec)

    assert doc_enc['h']['len'] == b''
    assert doc_enc['h']['data'] == b'header'
    assert doc_dec['h'] == 'header'

    assert doc_enc['t']['len'] == b''
    assert doc_enc['t']['data'] == b'0210'
    assert doc_dec['t'] == '0210'

    assert doc_enc['p']['len'] == b''
    assert doc_enc['p']['data'] == b'4000000000000000'
    assert doc_dec['p'] == '4000000000000000'

    assert doc_enc['2']['len'] == b'\x01'
    assert doc_enc['2']['data'] == b'g'
    assert doc_dec['2'] == 'g'

    assert doc_enc['bm'] == set([2])
    assert doc_dec['bm'] == set([2])

def test_field_negative_leftover_data():
    '''
    Field is required and provided.
    However, there is extra data left in message.
    '''
    spec['h']['data_enc'] = 'ascii'
    spec['h']['max_len'] = 6
    spec['t']['data_enc'] = 'ascii'
    spec['p']['data_enc'] = 'ascii'
    spec['2']['data_enc'] = 'ascii'
    spec['2']['len_enc'] = 'ascii'
    spec['2']['len_type'] = 0
    spec['2']['max_len'] = 4

    s = b'header02004000000000000000123456'
    with pytest.raises(iso8583.DecodeError, match="Extra data after last field: field 2 pos 30"):
        iso8583.decode(s, spec=spec)
