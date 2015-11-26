__author__ = 'wenjusun'

from io import BytesIO
from captcha.image import ImageCaptcha

image = ImageCaptcha(fonts=['/home/wenjusun/studio/studio/shijing_img/conf/Abyssinica_SIL.ttf', '/usr/share/fonts/vlgothic/VL-Gothic-Regular.ttf'])

data = image.generate('1234')
#assert isinstance(data, BytesIO)
image.write('1234', 'out.png')
