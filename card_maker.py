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

    def adjust_image(self, image, target_weight_and_height):
        width, height = image.size
        card_width, card_height = target_weight_and_height
        if width == card_width and height == card_height:
            return image
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
                    os.path.join(self.config.drawing_path, card_info.name + ext)
                )
                return self.adjust_image(
                    raw_img, (self.config.drawing_width, self.config.drawing_height)
                )

        print("could not find drawing for card: " + card_info.name)
        return None

    def get_background(self, card_info: CardInfo):
        bg_image = PIL.Image.open(
            os.path.join(
                self.config.general_path,
                "back_" + self.translator(card_info.category) + ".png",
            )
        ).convert("RGBA")
        return self.adjust_image(
            bg_image, (self.config.card_width, self.config.card_height)
        )

    # 准备好底板，除了描述和血量，元素消耗之类的其他东西，包括原画
    def prepare_outline(self, card_info: CardInfo):
        base_image = self.get_background(card_info)
        drawing_image = self.get_drawing(card_info)
        base_image.paste(
            drawing_image,
            (
                int((self.config.card_width - self.config.drawing_width) / 2),
                self.config.drawing_to_upper,
            ),
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
