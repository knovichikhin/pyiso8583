import pickle

import iso8583
import pytest

spec = {
    "h": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 0,
        "desc": "Message Header",
    },
    "t": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Message Type",
    },
    "p": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Bitmap, Primary",
    },
    "1": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Bitmap, Secondary",
    },
    "2": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 19,
        "desc": "Primary Account Number (PAN)",
    },
    "3": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 6,
        "desc": "Processing Code",
    },
    "4": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Amount, Transaction",
    },
    "5": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Amount, Settlement",
    },
    "6": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Amount, Cardholder Billing",
    },
    "7": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Transmission Date and Time",
    },
    "8": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Amount, Cardholder Billing Fee",
    },
    "9": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Conversion Rate, Settlement",
    },
    "10": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Conversion Rate, Cardholder Billing",
    },
    "11": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 6,
        "desc": "System Trace Audit Number",
    },
    "12": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 6,
        "desc": "Time, Local Transaction",
    },
    "13": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Date, Local Transaction",
    },
    "14": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Date, Expiration",
    },
    "15": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Date, Settlement",
    },
    "16": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Date, Conversion",
    },
    "17": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Date, Capture",
    },
    "18": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Merchant Type",
    },
    "19": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Acquiring Institution Country Code",
    },
    "20": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "PAN Country Code",
    },
    "21": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Forwarding Institution Country Code",
    },
    "22": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Point-of-Service Entry Mode",
    },
    "23": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "PAN Sequence Number",
    },
    "24": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Network International ID (NII)",
    },
    "25": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 2,
        "desc": "Point-of-Service Condition Code",
    },
    "26": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 2,
        "desc": "Point-of-Service Capture Code",
    },
    "27": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 1,
        "desc": "Authorizing ID Response Length",
    },
    "28": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 9,
        "desc": "Amount, Transaction Fee",
    },
    "29": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 9,
        "desc": "Amount, Settlement Fee",
    },
    "30": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 9,
        "desc": "Amount, Transaction Processing Fee",
    },
    "31": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 9,
        "desc": "Amount, Settlement Processing Fee",
    },
    "32": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 11,
        "desc": "Acquiring Institution ID Code",
    },
    "33": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 11,
        "desc": "Forwarding Institution ID Code",
    },
    "34": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 28,
        "desc": "Primary Account Number, Extended",
    },
    "35": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 37,
        "desc": "Track 2 Data",
    },
    "36": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 104,
        "desc": "Track 3 Data",
    },
    "37": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Retrieval Reference Number",
    },
    "38": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 6,
        "desc": "Authorization ID Response",
    },
    "39": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 2,
        "desc": "Response Code",
    },
    "40": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Service Restriction Code",
    },
    "41": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Card Acceptor Terminal ID",
    },
    "42": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 15,
        "desc": "Card Acceptor ID Code",
    },
    "43": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 40,
        "desc": "Card Acceptor Name/Location",
    },
    "44": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 25,
        "desc": "Additional Response Data",
    },
    "45": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 76,
        "desc": "Track 1 Data",
    },
    "46": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Additional Data - ISO",
    },
    "47": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Additional Data - National",
    },
    "48": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Additional Data - Private",
    },
    "49": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Currency Code, Transaction",
    },
    "50": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Currency Code, Settlement",
    },
    "51": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Currency Code, Cardholder Billing",
    },
    "52": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "PIN",
    },
    "53": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 16,
        "desc": "Security-Related Control Information",
    },
    "54": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 240,
        "desc": "Additional Amounts",
    },
    "55": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 255,
        "desc": "ICC data",
    },
    "56": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved ISO",
    },
    "57": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved National",
    },
    "58": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved National",
    },
    "59": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved National",
    },
    "60": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved National",
    },
    "61": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved Private",
    },
    "62": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved Private",
    },
    "63": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved Private",
    },
    "64": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "MAC",
    },
    "65": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Bitmap, Extended",
    },
    "66": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 1,
        "desc": "Settlement Code",
    },
    "67": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 2,
        "desc": "Extended Payment Code",
    },
    "68": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Receiving Institution Country Code",
    },
    "69": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Settlement Institution Country Code",
    },
    "70": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 3,
        "desc": "Network Management Information Code",
    },
    "71": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Message Number",
    },
    "72": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 4,
        "desc": "Message Number, Last",
    },
    "73": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 6,
        "desc": "Date, Action",
    },
    "74": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Credits, Number",
    },
    "75": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Credits, Reversal Number",
    },
    "76": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Debits, Number",
    },
    "77": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Debits, Reversal Number",
    },
    "78": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Transfer, Number",
    },
    "79": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Transfer, Reversal Number",
    },
    "80": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Inquiries, Number",
    },
    "81": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 10,
        "desc": "Authorizations, Number",
    },
    "82": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Credits, Processing Fee Amount",
    },
    "83": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Credits, Transaction Fee Amount",
    },
    "84": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Debits, Processing Fee Amount",
    },
    "85": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 12,
        "desc": "Debits, Transaction Fee Amount",
    },
    "86": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 16,
        "desc": "Credits, Amount",
    },
    "87": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 16,
        "desc": "Credits, Reversal Amount",
    },
    "88": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 16,
        "desc": "Debits, Amount",
    },
    "89": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 16,
        "desc": "Debits, Reversal Amount",
    },
    "90": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 42,
        "desc": "Original Data Elements",
    },
    "91": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 1,
        "desc": "File Update Code",
    },
    "92": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 2,
        "desc": "File Security Code",
    },
    "93": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 5,
        "desc": "Response Indicator",
    },
    "94": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 7,
        "desc": "Service Indicator",
    },
    "95": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 42,
        "desc": "Replacement Amounts",
    },
    "96": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "Message Security Code",
    },
    "97": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 17,
        "desc": "Amount, Net Settlement",
    },
    "98": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 25,
        "desc": "Payee",
    },
    "99": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 11,
        "desc": "Settlement Institution ID Code",
    },
    "100": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 11,
        "desc": "Receiving Institution ID Code",
    },
    "101": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 17,
        "desc": "File Name",
    },
    "102": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 28,
        "desc": "Account ID 1",
    },
    "103": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 2,
        "max_len": 28,
        "desc": "Account ID 2",
    },
    "104": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 100,
        "desc": "Transaction Description",
    },
    "105": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "106": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "107": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "108": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "109": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "110": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "111": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for ISO Use",
    },
    "112": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "113": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "114": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "115": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "116": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "117": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "118": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "119": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for National Use",
    },
    "120": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "121": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "122": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "123": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "124": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "125": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "126": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "127": {
        "data_enc": "ascii",
        "len_enc": "ascii",
        "len_type": 3,
        "max_len": 999,
        "desc": "Reserved for Private Use",
    },
    "128": {
        "data_enc": "b",
        "len_enc": "ascii",
        "len_type": 0,
        "max_len": 8,
        "desc": "MAC",
    },
}


def test_EncodeError_exception():
    """
    Validate EncodeError class
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"t": ""}

    try:
        iso8583.encode(doc_dec, spec=spec)
    except iso8583.EncodeError as e:
        assert e.doc_dec == doc_dec
        assert e.doc_enc == ({})
        assert e.msg == "Field data is required according to specifications"
        assert e.field == "h"
        assert (
            e.args[0] == "Field data is required according to specifications: field h"
        )


def test_EncodeError_exception_pickle():
    """
    Validate EncodeError class with pickle
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"t": ""}

    try:
        iso8583.encode(doc_dec, spec=spec)
    except iso8583.EncodeError as e:
        p = pickle.dumps(e)
        e_unpickled = pickle.loads(p)

        assert e.doc_dec == e_unpickled.doc_dec
        assert e.doc_enc == e_unpickled.doc_enc
        assert e.msg == e_unpickled.msg
        assert e.field == e_unpickled.field
        assert e.args[0] == e_unpickled.args[0]


def test_input_type():
    """
    Encode accepts only dict.
    """
    s = b""
    with pytest.raises(TypeError, match="Decoded ISO8583 data must be dict, not bytes"):
        iso8583.encode(s, spec=spec)


def test_header_no_key():
    """
    Message header is required and key is not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"t": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is required according to specifications: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_ascii_absent():
    """
    ASCII header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert ("h" in doc_enc) is False
    assert ("h" in doc_dec) is True

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_ascii_present():
    """
    ASCII header is required by spec and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_ebcdic_absent():
    """
    EBCDIC header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert ("h" in doc_enc) is False
    assert ("h" in doc_dec) is True

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_ebcdic_present():
    """
    EBCDIC header is required by spec and provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\x88\x85\x81\x84\x85\x990200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"\x88\x85\x81\x84\x85\x99"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_bdc_absent():
    """
    BDC header is not required by spec and not provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert ("h" in doc_enc) is False
    assert ("h" in doc_dec) is True

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_bcd_present():
    """
    BCD header is required by spec and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "A1A2A3A4A5A6", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xA1\xA2\xA3\xA4\xA5\xA60200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"\xA1\xA2\xA3\xA4\xA5\xA6"
    assert doc_dec["h"] == "A1A2A3A4A5A6"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_not_required_provided():
    """
    String header is not required by spec but provided.
    No error. Header is not included in the message.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["max_len"] = 0
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert ("h" in doc_enc) is False
    assert ("h" in doc_dec) is True

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_header_negative_missing():
    """
    String header is required by spec but not provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0200", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 6: field h"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_partial():
    """
    String header is required by spec but partially provided.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "head", "t": "0200", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 4 bytes, expecting 6: field h"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_incorrect_encoding():
    """
    String header is required by spec and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "invalid"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_incorrect_ascii_data():
    """
    ASCII header is required by spec and provided.
    However, the data is not ASCII
    CPython and PyPy throw differently worded exception
    CPython: 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)
    PyPy:    'ascii' codec can't encode character '\\xff' in position 0: ordinal not in range(128)
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {
        "h": b"\xff\xff\xff\xff\xff\xff".decode("latin-1"),
        "t": "0200",
        "bm": set(),
        "p": "",
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode character.*: ordinal not in range.128..: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_header_negative_incorrect_bcd_data():
    """
    BCD header is required by spec and provided.
    However, the data is not hex
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 0.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_ascii_over_max():
    """
    ASCII variable header is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    doc_dec = {"h": "header12", "t": "0210", "bm": set()}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 8 bytes, larger than maximum 6: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_ascii_present():
    """
    ASCII variable header is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"06header0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"06"
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set([])
    assert doc_dec["bm"] == set([])


def test_variable_header_ascii_present_zero_legnth():
    """
    ASCII zero-length variable header
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"000210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"00"
    assert doc_enc["h"]["data"] == b""
    assert doc_dec["h"] == ""

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set([])
    assert doc_dec["bm"] == set([])


def test_variable_header_ebcdic_over_max():
    """
    EBCDIC variable header is required and over max provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"

    doc_dec = {"h": "header1", "t": "0210", "bm": set()}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 7 bytes, larger than maximum 6: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_ebcdic_present():
    """
    EBCDIC variable header is required and provided
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xf0\xf6\x88\x85\x81\x84\x85\x990210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\xf0\xf6"
    assert doc_enc["h"]["data"] == b"\x88\x85\x81\x84\x85\x99"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set([])
    assert doc_dec["bm"] == set([])


def test_variable_header_ebcdic_present_zero_legnth():
    """
    EBCDIC zero-length variable header
    """
    spec["h"]["data_enc"] = "cp500"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xf0\xf00210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\xf0\xf0"
    assert doc_enc["h"]["data"] == b""
    assert doc_dec["h"] == ""

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set([])
    assert doc_dec["bm"] == set([])


def test_variable_header_bdc_over_max():
    """
    BDC variable header is required and over max is provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 2
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcdef", "t": "0210", "bm": set()}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 3 bytes, larger than maximum 2: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_bdc_odd():
    """
    BDC variable header is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 5
    PyPy:    non-hexadecimal number found in fromhex() arg at position 4
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcde", "t": "0210", "bm": set()}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 4|5.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_header_bdc_ascii_length():
    """
    BDC variable header
    The length is in ASCII.
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "ascii"
    spec["h"]["len_type"] = 3
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"002\xab\xcd0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"002"
    assert doc_enc["h"]["data"] == b"\xab\xcd"
    assert doc_dec["h"] == "abcd"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_variable_header_bdc_ebcdic_length():
    """
    BDC variable header is required and provided
    The length is in EBCDIC.
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "cp500"
    spec["h"]["len_type"] = 3
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\xf0\xf0\xf2\xab\xcd0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\xf0\xf0\xf2"
    assert doc_enc["h"]["data"] == b"\xab\xcd"
    assert doc_dec["h"] == "abcd"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_variable_header_bcd_present():
    """
    BCD variable header is required and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\x00\x02\xab\xcd0210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\x00\x02"
    assert doc_enc["h"]["data"] == b"\xab\xcd"
    assert doc_dec["h"] == "abcd"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_variable_header_bcd_present_zero_length():
    """
    BCD zero-length variable header is required and provided
    """
    spec["h"]["data_enc"] = "b"
    spec["h"]["len_enc"] = "b"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "", "t": "0210", "bm": set()}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"\x00\x000210\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b"\x00\x00"
    assert doc_enc["h"]["data"] == b""
    assert doc_dec["h"] == ""

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_variable_header_incorrect_encoding():
    """
    variable header is required and provided.
    However, the spec encoding is not correct for length
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_enc"] = "invalid"
    spec["h"]["len_type"] = 2
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "abcd", "t": "0210", "bm": set()}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode length .unknown encoding: invalid.: field h",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_no_key():
    """
    Message type is required and key is not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"h": "header", "2": ""}

    with pytest.raises(iso8583.EncodeError, match="Field data is required: field t"):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_absent():
    """
    ASCII message type is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_partial():
    """
    ASCII message type is required and partial is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 2 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_over_max():
    """
    ASCII message type is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02101", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 5 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_incorrect_data():
    """
    ASCII message type is required and provided.
    However, the data is not ASCII
    CPython and PyPy throw differently worded exception
    CPython: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
    PyPy:    'ascii' codec can't encode character '\\xff' in position 0: ordinal not in range(128)
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {
        "h": "header",
        "t": b"\xff\xff\xff\xff".decode("latin-1"),
        "bm": set(),
        "p": "",
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode character.*: ordinal not in range.128..: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ascii_present():
    """
    ASCII message type is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0200\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_type_ebcdic_absent():
    """
    EBCDIC message type is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ebcdic_partial():
    """
    EBCDIC message type is required and partial provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 2 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ebcdic_over_max():
    """
    EBCDIC message type is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02101", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 5 bytes, expecting 4: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_ebcdic_present():
    """
    EBCDIC message type is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "cp500"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header\xf0\xf2\xf0\xf0\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"\xf0\xf2\xf0\xf0"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_type_bdc_absent():
    """
    BDC message type is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_partial():
    """
    BDC message type is required and partial is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "02", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_over_max():
    """
    BDC message type is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "021000", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field t"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_odd():
    """
    BDC message type is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 3
    PyPy:    non-hexadecimal number found in fromhex() arg at position 2
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "021", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 2|3.: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bdc_non_hex():
    """
    BDC message type is required and provided
    However, the data is not hex
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "021x", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 3.: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_type_bcd_present():
    """
    BCD message type is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "b"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"\x02\x00"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "0000000000000000"

    assert doc_enc["bm"] == set()
    assert doc_dec["bm"] == set()


def test_type_incorrect_encoding():
    """
    String message type is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "invalid"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field t",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_bitmap_no_key():
    """
    ASCII fixed field is required and "bm" key is not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"h": "header", "t": "0210", "2": ""}

    with pytest.raises(iso8583.EncodeError, match="Field data is required: field bm"):
        iso8583.encode(doc_dec, spec=spec)


def test_bitmap_range():
    """
    ISO8583 bitmaps must be between 1 and 128.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0200", "bm": set(), "p": ""}

    doc_dec["bm"] = set([0])
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec["bm"] = set([129])
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec["bm"] = set(range(0, 129))
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm",
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec["bm"] = set(range(1, 130))
    with pytest.raises(
        iso8583.EncodeError,
        match="Bitmap contains fields outside 1-128 range: field bm",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_bitmap_remove_secondary():
    """
    If 65-128 fields are not in bitmap then remove field 1.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 19

    doc_dec = {
        "h": "header",
        "t": "0200",
        "bm": set(),
        "p": "",
        "2": "1234567890",
    }

    doc_dec["bm"] = set([1, 2])
    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0200\x40\x00\x00\x00\x00\x00\x00\x00101234567890"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"10"
    assert doc_enc["2"]["data"] == b"1234567890"
    assert doc_dec["2"] == "1234567890"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_bitmap_add_secondary():
    """
    If one of 65-128 fields are in bitmap then add field 1.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["66"]["data_enc"] = "ascii"
    spec["66"]["len_enc"] = "ascii"
    spec["66"]["len_type"] = 2
    spec["66"]["max_len"] = 19

    doc_dec = {
        "h": "header",
        "t": "0200",
        "bm": set(),
        "p": "",
        "66": "1234567890",
    }

    doc_dec["bm"] = set([66])
    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        s
        == b"header0200\x80\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00101234567890"
    )

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0200"
    assert doc_dec["t"] == "0200"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x80\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert doc_enc["1"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["1"] == "4000000000000000"

    assert doc_enc["66"]["len"] == b"10"
    assert doc_enc["66"]["data"] == b"1234567890"
    assert doc_dec["66"] == "1234567890"

    assert doc_enc["bm"] == set([1, 66])
    assert doc_dec["bm"] == set([1, 66])


def test_field_no_key():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {
        "h": "header",
        "t": "0210",
        "bm": set([2]),
    }

    with pytest.raises(
        iso8583.EncodeError, match="Field data is required according to bitmap: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)

    doc_dec = {"h": "header", "t": "0210", "bm": set([2])}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is required according to bitmap: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_primary_bitmap_incorrect_encoding():
    """
    Incorrect encoding specified for primary bitmap
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "invalid"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 0

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field p",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_secondary_bitmap_incorrect_encoding():
    """
    Incorrect encoding specified for secondary bitmap
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["len_type"] = 0
    spec["1"]["max_len"] = 16
    spec["1"]["data_enc"] = "invalid"

    doc_dec = {"h": "header", "t": "0210", "bm": set([65]), 65: ""}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field 1",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_ascii_bitmaps():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["1"]["data_enc"] = "ascii"
    spec["105"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([105]), "105": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header021080000000000000000000000000800000000"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"8000000000000000"
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert doc_enc["1"]["data"] == b"0000000000800000"
    assert doc_dec["1"] == "0000000000800000"

    assert doc_enc["105"]["len"] == b"000"
    assert doc_enc["105"]["data"] == b""
    assert doc_dec["105"] == ""

    assert doc_enc["bm"] == set([1, 105])
    assert doc_dec["bm"] == set([1, 105])


def test_ebcidic_bitmaps():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "cp500"
    spec["1"]["data_enc"] = "cp500"
    spec["105"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([105]), "105": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        s
        == b"header0210\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xf0"
        + b"\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0"
        + b"\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf8\xf0\xf0\xf0\xf0\xf0000"
    )

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert (
        doc_enc["p"]["data"]
        == b"\xf8\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0"
    )
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert (
        doc_enc["1"]["data"]
        == b"\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf8\xf0\xf0\xf0\xf0\xf0"
    )
    assert doc_dec["1"] == "0000000000800000"

    assert doc_enc["105"]["len"] == b"000"
    assert doc_enc["105"]["data"] == b""
    assert doc_dec["105"] == ""

    assert doc_enc["bm"] == set([1, 105])
    assert doc_dec["bm"] == set([1, 105])


def test_bcd_bitmaps():
    """
    Field is required and not key provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["1"]["data_enc"] = "b"
    spec["105"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([105]), "105": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert (
        s
        == b"header0210\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00000"
    )

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x80\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "8000000000000000"

    assert doc_enc["1"]["len"] == b""
    assert doc_enc["1"]["data"] == b"\x00\x00\x00\x00\x00\x80\x00\x00"
    assert doc_dec["1"] == "0000000000800000"

    assert doc_enc["105"]["len"] == b"000"
    assert doc_enc["105"]["data"] == b""
    assert doc_dec["105"] == ""

    assert doc_enc["bm"] == set([1, 105])
    assert doc_dec["bm"] == set([1, 105])


def test_fixed_field_ascii_absent():
    """
    ASCII fixed field is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_partial():
    """
    ASCII fixed field is required and partially provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_over_max():
    """
    ASCII fixed field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "123"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_incorrect_data():
    """
    ASCII fixed field is required and provided.
    However, the data is not ASCII
    CPython and PyPy throw differently worded exception
    CPython: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
    PyPy:    'ascii' codec can't encode character '\\xff' in position 0: ordinal not in range(128)
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {
        "h": "header",
        "t": "0210",
        "bm": set([2]),
        "2": b"\xff\xff".decode("latin-1"),
    }

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .'ascii' codec can't encode character.*: ordinal not in range.128..: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ascii_present():
    """
    ASCII fixed field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "22"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x0022"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b"22"
    assert doc_dec["2"] == "22"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_fixed_field_ascii_present_zero_legnth():
    """
    ASCII zero-length fixed field is required and provided
    This is pointless but should work.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 0
    spec["2"]["data_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_fixed_field_ebcdic_absent():
    """
    EBCDIC fixed field is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ebcdic_partial():
    """
    EBCDIC fixed field is required and partially provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ebcdic_over_max():
    """
    EBCDIC fixed field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "123"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_ebcdic_present():
    """
    EBCDIC fixed field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "22"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf2\xf2"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b"\xf2\xf2"
    assert doc_dec["2"] == "22"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_fixed_field_ebcdic_present_zero_legnth():
    """
    EBCDIC zero-length fixed field is required and provided
    This is pointless but should work.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 0
    spec["2"]["data_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_fixed_field_bdc_absent():
    """
    BDC fixed field is required and not provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 0 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_partial():
    """
    BDC fixed field is required and partial is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "12"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 1 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_over_max():
    """
    BDC fixed field is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "123456"}

    with pytest.raises(
        iso8583.EncodeError, match="Field data is 3 bytes, expecting 2: field 2"
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_odd():
    """
    BDC fixed field is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 5
    PyPy:    non-hexadecimal number found in fromhex() arg at position 4
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "12345"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 4|5.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bdc_non_hex():
    """
    BDC fixed field is required and provided
    However, the data is not hex
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "11xx"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 2.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_fixed_field_bcd_present():
    """
    BCD fixed field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_fixed_field_bcd_present_zero_length():
    """
    BCD zero-length fixed field is required and provided
    This is pointless but should work.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 0
    spec["2"]["data_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b""
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_fixed_field_incorrect_encoding():
    """
    Fixed field is required and provided.
    However, the spec encoding is not correct
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 0
    spec["2"]["max_len"] = 2
    spec["2"]["data_enc"] = "invalid"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .unknown encoding: invalid.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_ascii_over_max():
    """
    ASCII variable field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "12345678901"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 11 bytes, larger than maximum 10: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_ascii_present():
    """
    ASCII variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00041122"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"04"
    assert doc_enc["2"]["data"] == b"1122"
    assert doc_dec["2"] == "1122"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_ascii_present_zero_legnth():
    """
    ASCII zero-length variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x0000"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"00"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_ebcdic_over_max():
    """
    EBCDIC variable field is required and over max provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "ascii"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "cp500"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "12345678901"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 11 bytes, larger than maximum 10: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_ebcdic_present():
    """
    EBCDIC variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "cp500"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf4\xf1\xf1\xf2\xf2"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\xf0\xf4"
    assert doc_enc["2"]["data"] == b"\xf1\xf1\xf2\xf2"
    assert doc_dec["2"] == "1122"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_ebcdic_present_zero_legnth():
    """
    EBCDIC zero-length variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "cp500"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf0"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\xf0\xf0"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_bdc_over_max():
    """
    BDC variable field is required and over max is provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 5
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "123456789012"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Field data is 6 bytes, larger than maximum 5: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_bdc_odd():
    """
    BDC variable field is required and odd length is provided
    CPython and PyPy throw differently worded exception
    CPython: non-hexadecimal number found in fromhex() arg at position 5
    PyPy:    non-hexadecimal number found in fromhex() arg at position 4
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "12345"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode .non-hexadecimal number found in fromhex.. arg at position 4|5.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)


def test_variable_field_bdc_ascii_length():
    """
    BDC variable field is required and provided
    The length is in ASCII.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 3
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "ascii"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00002\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"002"
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_bdc_ebcdic_length():
    """
    BDC variable field is required and provided
    The length is in EBCDIC.
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 3
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "cp500"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\xf0\xf0\xf2\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\xf0\xf0\xf2"
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_bcd_present():
    """
    BCD variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\x00\x02\x11\x22"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\x00\x02"
    assert doc_enc["2"]["data"] == b"\x11\x22"
    assert doc_dec["2"] == "1122"

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_bcd_present_zero_length():
    """
    BCD zero-length variable field is required and provided
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "b"
    spec["2"]["len_enc"] = "b"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": ""}

    s, doc_enc = iso8583.encode(doc_dec, spec=spec)

    assert s == b"header0210\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    assert doc_enc["h"]["len"] == b""
    assert doc_enc["h"]["data"] == b"header"
    assert doc_dec["h"] == "header"

    assert doc_enc["t"]["len"] == b""
    assert doc_enc["t"]["data"] == b"0210"
    assert doc_dec["t"] == "0210"

    assert doc_enc["p"]["len"] == b""
    assert doc_enc["p"]["data"] == b"\x40\x00\x00\x00\x00\x00\x00\x00"
    assert doc_dec["p"] == "4000000000000000"

    assert doc_enc["2"]["len"] == b"\x00\x00"
    assert doc_enc["2"]["data"] == b""
    assert doc_dec["2"] == ""

    assert doc_enc["bm"] == set([2])
    assert doc_dec["bm"] == set([2])


def test_variable_field_incorrect_encoding():
    """
    Variable field is required and provided.
    However, the spec encoding is not correct for length
    """
    spec["h"]["data_enc"] = "ascii"
    spec["h"]["len_type"] = 0
    spec["h"]["max_len"] = 6
    spec["t"]["data_enc"] = "ascii"
    spec["p"]["data_enc"] = "b"
    spec["2"]["len_type"] = 2
    spec["2"]["max_len"] = 10
    spec["2"]["data_enc"] = "ascii"
    spec["2"]["len_enc"] = "invalid"

    doc_dec = {"h": "header", "t": "0210", "bm": set([2]), "2": "1122"}

    with pytest.raises(
        iso8583.EncodeError,
        match="Failed to encode length .unknown encoding: invalid.: field 2",
    ):
        iso8583.encode(doc_dec, spec=spec)
