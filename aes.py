#!/usr/bin/python
# -*- coding: UTF-8 -*-
#

__author__ = 'Kimmo Brunfeldt'


import hashlib
from Crypto.Cipher import AES


def dec2hex(n):
    """Return the hexadecimal string representation of integer n"""
    return "%X" % n


def hex2dec(s):
    """Return the integer value of a hexadecimal string s"""
    return int(s, 16)


def hash_key(key):
    """Return sha256 hash digest"""
    return hashlib.sha256(key).digest()


def encrypt_text(text, key):
    """Encrypt given text with AES algorithm -> CBC=Cipher-block chaining
    LMore information:
    http://en.wikipedia.org/wiki/Block_cipher_modes_of_operation

    Key must be 8, 16 or 32 bits,
    so sha256 hash is made from given key.
    Text can be a unicode object or encoded text
    """
    if isinstance(text, unicode):
        text = text.encode('utf-8')

    BLOCK_SIZE = 16  # Size of block that algorithm uses. MAX IS 16!!!

    # http://www.di-mgt.com.au/cryptopad.html
    # Pad with spaces. If the text length is equal to blocksize,
    # padding is added, The padded text's final char is always the same as the
    # length of padding. Final char is a number in HEX 0-F(0-15). 0 means that
    # length of padding is 1.
    spacepad = (BLOCK_SIZE - len(text) % BLOCK_SIZE)

    # Text length is same as BLOCK_SIZE, we have to add padding so decrypter
    # knows how much padding to remove.
    if spacepad == 0:
        spacepad = BLOCK_SIZE

    # Add padding and padding's length to text
    text = text + ' ' * (spacepad - 1) + dec2hex(spacepad - 1)

    # Get sha256 digest from key.
    key = hash_key(key)

    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode)

    return encryptor.encrypt(text)  # Encrypt text.


def decrypt_text(ciphertext, key):
    """Decrypts given ciphertext with given key. Ciphertext is excepted to be
    encrypted with AES.MODE_CBC
    Plain text is always padded.
    If unicode object was given to encrypt function, the returned plaintext
    is encoded with utf-8.

    Key must be 8, 16 or 32 bits,
    so sha256 hash is made from given key.
    """
    # Get sha256 digest from key.
    key = hash_key(key)

    # Use AES and Cipher-block chaining mode
    mode = AES.MODE_CBC
    decryptor = AES.new(key, mode)

    plain = decryptor.decrypt(ciphertext)  # Get padded plaintext

    try:
        firstpad = -(hex2dec(plain[-1]) + 1)  # Get position of first padding

    except ValueError:  # Last char was not a number
        raise Exception("Probably wrong key!")

    return plain[:firstpad]  # Return plain text in unicode


def print_ords(data):
    print ''.join(str(x) for x in bytearray(data))


if __name__ == '__main__':
    text = 'Test text!'
    print_ords(text)  # Print int values of bytes

    encrypted = encrypt_text(text, 'avain2')
    print_ords(encrypted)  # Ascii values are not the same

    decrypted = decrypt_text(encrypted, 'avain2')
    print_ords(decrypted)  # Now they are

    print repr(decrypted)
