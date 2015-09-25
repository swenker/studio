__author__ = 'wenjusun'

from Crypto.Cipher import AES

import base64
import urllib
import binascii


"""
  reference : https://www.dlitz.net/software/pycrypto/api/current/
"""
padding = "ThisisPadding"
CHARSET_UTF8="UTF8"
key=b"abcdefghijklmnop"

originalUrl = "http://stackoverflow.com/questions/25694006/valueerror-input-strings-must-be-a-multiple-of-16-in-length-error-on-decryption"
originalUrl = "http://stackover"*3+"123"

def encrypt(msg):

    #base64_encoded = base64.encodestring(encoded_url) generate multiple lines

    EncodeAES = lambda c,e:c.encrypt(e)

    #AES key must be either 16, 24, or 32 bytes long
    cipher = AES.new(key)

    #The string here must be multiple 16 length
    encrypted_msg = EncodeAES(cipher,msg+padding)

    base64_encoded = base64.b64encode(encrypted_msg)

    encoded = urllib.quote(base64_encoded).encode(CHARSET_UTF8)
    return encoded



def decrypt(msg):

    print "msg:%d" % len(msg)
    decoded_url = urllib.unquote(msg).decode(CHARSET_UTF8)

    print "durl:%d" %len(decoded_url)

    base64_decoded =  base64.decodestring(decoded_url)

    print "b64:%d" %len(base64_decoded)

    DecodeAES = lambda c, e: c.decrypt(e).rstrip(padding)

    cipher = AES.new(key)

    decoded = DecodeAES(cipher, base64_decoded)

    print decoded

enmsg=encrypt(originalUrl)

print enmsg

decrypt(enmsg)