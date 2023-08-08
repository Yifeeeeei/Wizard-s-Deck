import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import textwrap
import os


class Config:
    def __init__(self) -> None:
        self.width = 250
        self.width = 400
        self.icon_path = ""
        self.drawing_path = ""


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


class CardMaker:
    def __init__(self, config: Config) -> None:
        self.config = config

    def adjust_image(self, image):
        width, height = image.size
        card_width, card_height = self.config.width, self.config.height
        if width >= card_width and height >= card_height:
            left = (width - card_width) / 2
            top = (height - card_height) / 2
            right = (width + card_width) / 2
            bottom = (height + card_height) / 2
            image = image.crop((left, top, right, bottom))
        else:
            image = image.resize((card_width, card_height))
        return image

    def get_drawing(self, card_info: CardInfo):
        extension_list = [".png", ".jpg", ".jpeg"]
        for ext in extension_list:
            if os.path.exists(
                os.path.join(self.config.drawing_path, card_info.name + ext)
            ):
                raw_img = PIL.Image.open(
                    os.path.join(self.config.drawing_path, card_info.name + ".jpg")
                )

        print("could not find drawing for card: " + card_info.name)
        return None

    # 准备好底板，除了描述和血量，元素消耗之类的其他东西，包括原画
    def prepare_outline(self, card_info: CardInfo):
        pass

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
