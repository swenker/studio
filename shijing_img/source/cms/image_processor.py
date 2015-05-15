__author__ = 'wenjusun'

from PIL import Image,ImageFont,ImageDraw,ImageEnhance

import service_config

config = service_config.config
# def ori_add_watermark_original(in_file, text, out_file='watermark.jpg', angle=23, opacity=0.25):
#     img = Image.open(in_file).convert('RGB')
#     watermark = Image.new('RGBA', img.size, (0,0,0,0))
#     size = 2
#     n_font = ImageFont.truetype(FONT, size)
#     n_width, n_height = n_font.getsize(text)
#     while n_width+n_height < watermark.size[0]:
#         size += 2
#         n_font = ImageFont.truetype(FONT, size)
#         n_width, n_height = n_font.getsize(text)
#     draw = ImageDraw.Draw(watermark, 'RGBA')
#     draw.text(((watermark.size[0] - n_width) / 2,
#               (watermark.size[1] - n_height) / 2),
#               text, font=n_font)
#     watermark = watermark.rotate(angle,Image.BICUBIC)
#     alpha = watermark.split()[3]
#     alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
#     watermark.putalpha(alpha)
#     Image.composite(watermark, img, watermark).save(out_file, 'JPEG')

class ImageProcessor():
    def __init__(self):
        self.FONT=config.img_watermark_text_font
        self.text = config.img_watermark_text
        self.text_size = config.img_watermark_text_size
        self.angle=config.img_watermark_angle
        self.opacity=config.img_watermark_opacity
        print self.text_size
        self.w_font = ImageFont.truetype(self.FONT, self.text_size)
        self.w_font_size = self.w_font.getsize(self.text)


    def add_watermark(self, img):

        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))

        wm_width,wm_height = watermark.size

        f_width, f_height = self.w_font_size

        draw = ImageDraw.Draw(watermark, 'RGBA')

        draw.text((wm_width-f_width-10, wm_height-f_height-20), self.text, font = self.w_font)
        watermark = watermark.rotate(self.angle,Image.BICUBIC)
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
        watermark.putalpha(alpha)

        return Image.composite(watermark, img, watermark)


    def thumbnail(self,infile, inpath):
        width=config.img_thumb_width

        outpath = "/thumb/"+inpath
        outfile = config.img_save_path+outpath

        self.zoom(infile,outfile,width)

        return outpath

    def large(self,infile, inpath):
        width=config.img_large_width

        outpath = "/lar/"+inpath
        outfile = config.img_save_path+ outpath

        self.zoom(infile,outfile,width,water_mark=True)

        return outpath

    def add_watermark_img(self, im):
        watermark_im = Image.open(config.img_save_path+"/"+"")
        w_width,w_height=watermark_im.size
        wbox = {'leftup':(0,0),'rightup':(0,0)}

        # woption={'leftup':(0,0),'rightup':(,0),'leftlow':(0,),'rightlow':(,)}
        im.paste(watermark_im,wbox)

    def zoom(self, infile,outfile,width=0,height=0,water_mark=False):
        im = Image.open(infile)
        om = im.copy()

        ox,oy = om.size
        n_size=width,int(float(width)/ox*oy)

        om.thumbnail(n_size,Image.ANTIALIAS)
        if water_mark:
            om=self.add_watermark(om)

        om.save(outfile)


def test_thumbnail():
    improcessor= ImageProcessor()
    inpath='/2015/05/13/0.jpeg'
    improcessor.thumbnail(inpath)

def test_large():
    improcessor= ImageProcessor()
    inpath='/2015/05/13/0.jpeg'
    improcessor.large(inpath)

def test_zoom():
    improcessor= ImageProcessor()
    infile = '/var/shijing/img'+"/raw/2015/05/13/0.jpeg"
    outfile = '/var/shijing/img'+"/thumb/2015/05/13/03.jpeg"

    improcessor.zoom(infile,outfile,300)

def test_add_watermark():
    improcessor= ImageProcessor()
    infile = '/var/shijing/img'+"/raw/2015/05/13/0.jpeg"
    improcessor.add_watermark(Image.open(infile))



if __name__=='__main__':
    # test_zoom()
    test_thumbnail()
    # test_large()

