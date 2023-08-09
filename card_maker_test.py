import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import textwrap
from card_maker import *

# Load the base image
base_image = PIL.Image.open(
    "素材/Emma_Watson_as_a_powerful_mysterious_sorceress__summoning_lightning__d_S1600129147_St20_G7.5.jpeg"
)

card_width = 250
card_height = 400


# crop the base image from the center if it is too big, stretch it if it is too small
def adjust_image(image):
    width, height = image.size
    if width >= card_width and height >= card_height:
        left = (width - card_width) / 2
        top = (height - card_height) / 2
        right = (width + card_width) / 2
        bottom = (height + card_height) / 2
        image = image.crop((left, top, right, bottom))
    else:
        image = image.resize((card_width, card_height))
    return image


base_image = adjust_image(base_image)


# Create a drawing object
draw = PIL.ImageDraw.Draw(base_image)

# Draw a circle


# Load the overlay image
overlay_image = PIL.Image.open("素材/download (4).jpg")

# Paste the overlay image on top of the base image
# base_image.paste(overlay_image, (0, 0), overlay_image)
# draw.ellipse((100, 100, 200, 200), fill=(255, 0, 0))

# text = "哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈"

# # Wrap the text
# wrapped_text = textwrap.wrap(text, width=10)
# font = PIL.ImageFont.truetype("FangZhengKaiTiJianTi/FangZhengKaiTiJianTi-1.ttf", 30)
# # Add the text to the image
# for i, line in enumerate(wrapped_text):
#     print(line)
#     draw.text((100, 100 + i * 30), line, font=font, fill=(0, 0, 255))


# # Save the image
# base_image.save("final.png")


config = Config()
config.general_path = "resources/general"
config.drawing_path = "resources/drawings"
cm = CardMaker(config)

ci = CardInfo()
ci.category = "水"
ci.name = "test"
card_image = cm.prepare_outline(ci)
card_image.save("ci.png")