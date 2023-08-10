import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import textwrap
import os

from config import Config


"""
用来存储各种属性值
"""


class Elements:
    def __init__(self, elements_dict) -> None:
        self.elements_dict = elements_dict
        all_elements = ["光", "暗", "火", "水", "地", "?"]
        for ele in all_elements:
            if ele not in elements_dict:
                elements_dict[ele] = 0

    def total_cost(self):
        return sum(self.elements_dict.values())


class CardInfo:
    def __init__(self) -> None:
        self.type = ""  # 生物、技能、道具三选一
        self.name = ""
        self.category = ""  # 火水地光暗?

        self.explanation = ""  # 说明，传奇异兽、道具、咒术、法术之类的名词
        self.description = ""  # 描述
        self.elements_cost = Elements({})  # 左上角元素消耗
        self.elements_gain = Elements({})  # 右下角元素负载
        # 以下是生物卡的独有属性

        self.life = 0  # 生命值

        # 以下是技能卡的独有属性
        self.cool_down = 0  # 冷却回合数

        # 以下是道具卡的独有属性


"""
卡牌制作类
"""


class CardMaker:
    def __init__(self, config: Config) -> None:
        self.config = config

    def translator(self, chi):
        if chi == "光":
            return "light"
        elif chi == "暗":
            return "dark"
        elif chi == "火":
            return "fire"
        elif chi == "水":
            return "water"
        elif chi == "风":
            return "wind"
        elif chi == "地":
            return "earth"
        elif chi == "?":
            return "none"
        else:
            print("invalid chi encounterd: " + chi)
            return None

    def adjust_image(self, image, target_width_and_height):
        width, height = image.size
        target_width, target_height = target_width_and_height
        if width / height > target_width / target_width:
            ideal_width = target_width / target_width * height
            left = (width - ideal_width) / 2
            right = (width + ideal_width) / 2
            image = image.crop((left, 0, right, height))
        if width / height < target_width / target_width:
            ideal_width = target_width / target_width * height
            top = (height - ideal_width) / 2
            bottom = (height + ideal_width) / 2
            image = image.crop((0, top, width, bottom))
        image = image.resize((target_width, target_height))
        return image

    def get_image_without_extension(self, image_name):
        extension_list = [".png", ".jpg", ".jpeg"]
        for ext in extension_list:
            if os.path.exists(image_name + ext):
                return PIL.Image.open(image_name + ext).convert("RGBA")
        print("could not find image: " + image_name)
        return None

    def get_drawing(self, card_info: CardInfo):
        return self.get_image_without_extension(
            os.path.join(self.config.drawing_path, card_info.name)
        )

    def get_background(self, card_info: CardInfo):
        bg_image = self.get_image_without_extension(
            os.path.join(
                self.config.general_path, "back_" + self.translator(card_info.category)
            )
        )
        bg_image = self.adjust_image(
            bg_image, (self.config.card_width, self.config.card_height)
        )
        return bg_image

    def get_border(self):
        border_image = self.get_image_without_extension(
            os.path.join(self.config.general_path, "border")
        )
        border_image = self.adjust_image(
            border_image, (self.config.border_width, self.config.border_height)
        )
        return border_image

    def draw_bottom_block(self, base_image):
        new_image = PIL.Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        draw = PIL.ImageDraw.Draw(new_image)
        top = self.config.drawing_to_upper + self.config.drawing_height
        left = (self.config.card_width - self.config.bottom_block_width) / 2
        bottom = (
            self.config.drawing_to_upper
            + self.config.drawing_height
            + self.config.bottom_block_height
        )
        right = left + self.config.bottom_block_width

        draw.rectangle(
            ((left, top), (right, bottom)),
            fill=self.config.bottom_block_color
            + (self.config.bottom_block_transparency,),
        )
        out = PIL.Image.alpha_composite(base_image, new_image)
        return out

    # 准备好底板，除了描述和血量，元素消耗之类的其他东西，包括原画
    def prepare_outline(self, card_info: CardInfo):
        # 添加背景
        base_image = self.get_background(card_info)
        # 添加卡牌原画
        drawing_image = self.get_drawing(card_info)
        # 添加原画
        base_image.paste(
            drawing_image,
            (
                int((self.config.card_width - self.config.drawing_width) / 2),
                self.config.drawing_to_upper,
            ),
        )
        # 添加底部文字背景
        base_image = self.draw_bottom_block(base_image)

        # 获取边框
        border_image = self.get_border()
        # 添加边框
        base_image.paste(
            border_image,
            (
                int((self.config.card_width - self.config.border_width) / 2),
                int((self.config.card_height - self.config.border_height) / 2),
            ),
            mask=border_image,
        )

        return base_image

    def estimate_text_size(self, text, font_size):
        text = str(text)
        return font_size * len(text)

    def draw_round_corner_rectangle(
        self, image, left_top_right_bottom, radius, color, outline=None, width=1
    ):
        """Draws a round corner rectangle on the given image.

        Args:
            image: The image to draw the rectangle on.
            top_left: The top-left corner of the rectangle.
            bottom_right: The bottom-right corner of the rectangle.
            radius: The radius of the corners.
            color: The color of the rectangle.
            outline: The color of the outline of the rectangle.
            width: The width of the outline of the rectangle.

        Returns:
            The image with the rectangle drawn on it.
        """

        # Create a drawing context for the image.
        draw = PIL.ImageDraw.Draw(image)

        # Draw the rectangle on the image.
        draw.rounded_rectangle(
            left_top_right_bottom, radius, fill=color, outline=outline, width=width
        )

        return image

    def add_text_on_image(self, image, text, left_top, font, color):
        draw = PIL.ImageDraw.Draw(image)
        draw.text(left_top, text, font=font, fill=color)
        return image

    def get_category_image(self, card_info: CardInfo):
        return self.get_image_without_extension(
            os.path.join(
                self.config.general_path, "ele_" + self.translator(card_info.category)
            )
        )

    def draw_category_and_name(self, card_info: CardInfo, base_image: PIL.Image):
        # add name
        length_estimate = self.estimate_text_size(
            card_info.name, self.config.name_font_size
        )
        rectangle_width = length_estimate + 2 * (
            self.config.name_text_to_left - self.config.name_rect_left
        )
        left = self.config.name_rect_left
        top = self.config.name_rect_top
        right = left + rectangle_width
        bottom = top + self.config.name_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (left, top, right, bottom),
            self.config.name_rect_radius,
            self.config.name_rect_fill,
            self.config.name_rect_outline_color,
            self.config.name_rect_outline_width,
        )
        text_left = self.config.name_text_to_left
        text_top = (
            self.config.name_rect_top
            + (self.config.name_rect_height - self.config.name_font_size) / 2
        )
        text_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.name_font),
            self.config.name_font_size,
        )
        base_image = self.add_text_on_image(
            base_image,
            card_info.name,
            (text_left, text_top),
            text_font,
            self.config.name_text_font_color,
        )

        # add category

        category_image = self.get_category_image(card_info)
        category_image = self.adjust_image(
            category_image,
            (
                self.config.name_category_width,
                self.config.name_category_width,
            ),
        )
        base_image.paste(
            category_image,
            (self.config.name_category_left, self.config.name_category_top),
            mask=category_image,
        )

        return base_image

    def make_unit_card(self, card_info: CardInfo):
        # 准备底层
        base_image = self.prepare_outline(card_info)
        # 准备左上角元素+名称
        base_image = self.draw_category_and_name(card_info, base_image)
        return base_image

    def make_ability_card(self, card_info: CardInfo):
        pass

    def make_item_card(self, card_info: CardInfo):
        pass

    def make_card(self, card_info: CardInfo):
        if card_info.type == "生物":
            result = self.make_unit_card(card_info)
            return result
        elif card_info.type == "技能":
            result = self.make_ability_card(card_info)
            return result
        elif card_info.type == "道具":
            result = self.make_item_card(card_info)
            return result
