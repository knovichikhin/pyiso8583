r'''`ISO8583 <https://en.wikipedia.org/wiki/ISO_8583>`_
is an international standard for financial transaction card originated
interchange messaging. It is the ISO standard for systems that exchange
electronic transactions initiated by cardholders using payment cards.

:mod:`iso8583` serializes and deserializes ISO8583 data between a ``bytes`` or
``bytearray`` instance containing ISO8583 data and a Python ``dict``.
'''

__version__ = '1.0.1'
__all__ = [
    'add_field', 'del_field', 'pp',
    'decode', 'DecodeError',
    'encode', 'EncodeError',
]
__author__ = 'Konstantin Novichikhin <konstantin.novichikhin@gmail.com>'

from iso8583.decoder import decode, DecodeError
from iso8583.encoder import encode, EncodeError
from iso8583.tools import add_field, del_field, pp
