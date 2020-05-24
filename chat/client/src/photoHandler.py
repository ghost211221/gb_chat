from PIL import Image, ImageDraw 
from PIL.ImageQt import ImageQt

def make_shaped_photo(fname):
    image = Image.open(fname)

    width = 890
    height = 450

    draw = ImageDraw.Draw(image)

    image = image.resize((width, height), Image.ANTIALIAS)

    image = image.crop((0, 0, 310, 450))

    return ImageQt(image.convert('RGBA'))