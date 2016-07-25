__author__ = 'wenjusun'

from Crypto.Cipher import AES
import base64

SECURITY_SALT = 'ThisisAndPadding'
CHARSET_UTF8 = "UTF8"
AES_KEY = b"abcdefghijklmnop"


def encrypt(raw_msg, salt=SECURITY_SALT):
    padding = salt
    EncodeAES = lambda c, e: c.encrypt(e)

    # AES key must be either 16, 24, or 32 bytes long
    cipher = AES.new(AES_KEY)

    #The string here must be multiple 16 length(len raw_msg)+len (padding))
    msg_len = len(raw_msg)
    if msg_len%16 !=0:
        padding = salt[:16-msg_len]
    encrypted_msg = EncodeAES(cipher, raw_msg + padding)

    base64_encoded = base64.b64encode(encrypted_msg)

    #encoded = urllib.quote(base64_encoded).encode(CHARSET_UTF8)
    return base64_encoded


def decrypt(encrypted_msg,end):
    padding = SECURITY_SALT[:end]
    base64_decoded = base64.decodestring(encrypted_msg)

    # print "b64:%d" % len(base64_decoded)

    DecodeAES = lambda c, e: c.decrypt(e).rstrip(padding)

    cipher = AES.new(AES_KEY)

    decoded = DecodeAES(cipher, base64_decoded)

    print padding+";"+decoded
    return decoded

def daystr(daytime):
    return daytime.strftime("%Y-%m-%d")

if __name__ == '__main__':
    # encred = encrypt('shijing_09a')
    # encred = encrypt('shijing_09a')
    encred = encrypt('shijing09')

    print encred

    print decrypt(encred,7)




