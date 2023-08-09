import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import textwrap
import os


"""
配置文件
"""


class Config:
    def __init__(self) -> None:
        self.card_width = 590
        self.card_height = 860
        self.drawing_width = 510
        self.drawing_height = 510
        self.drawing_to_upper = 40
        self.border_width = 560
        self.border_height = 830
        self.general_path = ""  # 通用素材
        self.drawing_path = ""  # 卡牌原画
        self.font_path = ""  # 字体


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

        # 获取边框
        border_image = self.get_border()
        base_image.paste(
            border_image,
            (
                int((self.config.card_width - self.config.border_width) / 2),
                int((self.config.card_height - self.config.border_height) / 2),
            ),
            mask=border_image,
        )

        # 添加边框

        return base_image

    def make_unit_card(self, card_info: CardInfo):
        pass

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
