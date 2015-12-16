__author__ = 'wenjusun'


from io import BytesIO
from captcha.image import ImageCaptcha
import random

image = ImageCaptcha(fonts=['/var/shijing/Abyssinica_SIL.ttf', '/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf'])

data = image.generate('1234')
#assert isinstance(data, BytesIO)
image.write('1234', 'out.png')


class CaptchImage():
    def get_path(self):
        return ""

    def generate_captch(self):

        return ""

ch_az=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
       'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
       '0','1','2','3','4','5','6','7','8','9']

def get_random_characters(width=4):

    return random.sample(ch_az,width)

