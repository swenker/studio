__author__ = 'wenjusun'

from Crypto.Cipher import AES

import base64
import urllib
import binascii



key="Droid eats Apple"
padding = "PKCS5Padding"
CHARSET_UTF8="UTF8"

originalStr = "1424999385611,0,https://sg-otaproxy-qa.blurdev.com:443/com-motorola-cds-otapackages-staging/delta-ota-Blur_Version.22.0.1100-22.0.1169.victara_retcn.retcn.en.CN.zip.506276ec-825b-40fd-a269-31cec10fd318?GoogleAccessId=523753976398-pbolclbq5n6i5na989svg6g5loor5fnr%40developer.gserviceaccount.com&Expires=1424999385&Signature=ZlwEffFo8K4ze1n%2B2MphaADo7ni6SZ%2BRJ63XR68ytAq7uZxz1h66jSLm3FunRe1RFCuj047LDOBtcPKiSAaSdQPyg8BihXeq%2FhcmtIljNqWWXwdPwlND8mUYP%2B2Q4PSQ8Jt2YVg9l1IBp7tlgzFPOeNm4ZlzI8SnNdnkjab2QO8%3D,GCS"
requestUrl = "psdFkmX4Komsf69IMV%2Brk3MpVFFyCXDhhohcCRTcm25aKCVqrh%2Fqw09ApGM6xSkIKo1rUCwyCyzisdlrId6rD3fC1ECVyWmLON%2FPrva5DnQXmDdobRiLGKOVfs2FutvLAQUyH%2FxQOTn%2FfBhthm6tmH6oEq620ZltNzqN4%2FCRYKMvLDbAMeR%2FdpNJ8mPCwNukgy8X6XiVbiJGA%2FY2jTHMxf8HdOCIToIv0oZu5BlyY%2B5jBCf1Uzwj70g18OIruPGMpm9ohKoDW816IYa4xNZx%2BF5pVBEU%2FatT64ChtfFpaTRmlqIEsIGzOOIwXACBOMkvZURWzXr%2B68XbehhQIZTXglEzBAkunYEBxB3TZtD%2BQTHZrn%2BWIYFUaWSxPy81yD1hfJm2ARRHaL8jAPz8wkTke1ws6Zl3pGLhctZNxHvSrkagFTEnhaTnhQbepQMhnRU7QLBg8M30NxGACIjY7AzIBEh5zoZiHNbGBido1Y%2BtEiPCLSAKR%2B03iRsFkMDcztYBy54tpFgonsIdJT3tYR8L5TNtl1G86QmTbXlXVJLkVBH0yTV7SQLs8OK3a9oJaWvI1TviTo8RAqHnIC5SWsAurNeSlypiUHGW9zcfpxY0a6WZfya7ZI3YoCXwFEC99mTAc5ZiUxJ3b6BShyCC1d5mapbdxGyPo54BGXvffeApEPY%3D"


def misc():
    decoded_url = urllib.unquote(requestUrl).decode(CHARSET_UTF8)

    print "%d" % len(decoded_url)

    base64_decoded =  base64.decodestring(decoded_url)

    print "%d" % len(base64_decoded)

    DecodeAES = lambda c, e: c.decrypt(e).rstrip(padding)


    #cipher = AES.new(binascii.a2b_qp(key))
    key2=b"Droid eats Apple"
    cipher = AES.new(key2)

    #decoded = DecodeAES(cipher, base64_decoded)
    decoded = DecodeAES(cipher, base64_decoded)

    print decoded


def encrypt(msg):

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

    return decoded

#enmsg=encrypt(originalStr)

#print enmsg
print requestUrl

#print decrypt(enmsg)
decrypted_str = decrypt(requestUrl)
print decrypted_str

print originalStr


#TODO the decrypted string ends with two 

"""
1424999385611,0,https://sg-otaproxy-qa.blurdev.com:443/com-motorola-cds-otapackages-staging/delta-ota-Blur_Version.22.0.1100-22.0.1169.victara_retcn.retcn.en.CN.zip.506276ec-825b-40fd-a269-31cec10fd318?GoogleAccessId=523753976398-pbolclbq5n6i5na989svg6g5loor5fnr%40developer.gserviceaccount.com&Expires=1424999385&Signature=ZlwEffFo8K4ze1n%2B2MphaADo7ni6SZ%2BRJ63XR68ytAq7uZxz1h66jSLm3FunRe1RFCuj047LDOBtcPKiSAaSdQPyg8BihXeq%2FhcmtIljNqWWXwdPwlND8mUYP%2B2Q4PSQ8Jt2YVg9l1IBp7tlgzFPOeNm4ZlzI8SnNdnkjab2QO8%3D,GCS
1424999385611,0,https://sg-otaproxy-qa.blurdev.com:443/com-motorola-cds-otapackages-staging/delta-ota-Blur_Version.22.0.1100-22.0.1169.victara_retcn.retcn.en.CN.zip.506276ec-825b-40fd-a269-31cec10fd318?GoogleAccessId=523753976398-pbolclbq5n6i5na989svg6g5loor5fnr%40developer.gserviceaccount.com&Expires=1424999385&Signature=ZlwEffFo8K4ze1n%2B2MphaADo7ni6SZ%2BRJ63XR68ytAq7uZxz1h66jSLm3FunRe1RFCuj047LDOBtcPKiSAaSdQPyg8BihXeq%2FhcmtIljNqWWXwdPwlND8mUYP%2B2Q4PSQ8Jt2YVg9l1IBp7tlgzFPOeNm4ZlzI8SnNdnkjab2QO8%3D,GCS
"""