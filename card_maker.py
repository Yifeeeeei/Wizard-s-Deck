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
        all_elements = ["光", "暗", "火", "水", "地", "风", "?"]
        for ele in all_elements:
            if ele not in elements_dict:
                elements_dict[ele] = 0

    def total_cost(self):
        return sum(self.elements_dict.values())

    def __getitem__(self, item):
        return self.elements_dict[item]

    def __setitem__(self, key, value):
        self.elements_dict[key] = value

    def keys(self):
        return self.elements_dict.keys()

    def values(self):
        return self.elements_dict.values()


class CardInfo:
    def __init__(self) -> None:
        self.type = ""  # 生物、技能、道具三选一
        self.name = ""
        self.category = ""  # 火水地光暗?

        self.explanation = ""  # 说明，传奇异兽、道具、咒术、法术之类的名词
        self.description = ""  # 描述
        self.quote = ""  # 一段帅气的文字引用
        self.elements_cost = Elements({})  # 左上角元素消耗
        self.elements_gain = Elements({})  # 右下角元素负载
        # 以下是生物卡的独有属性

        self.life = 0  # 生命值

        self.version = ""  # 版本号

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
        if (width / height) > (target_width / target_height):
            # too wide
            ideal_width = target_width / target_height * height
            left = (width - ideal_width) / 2
            right = (width + ideal_width) / 2
            image = image.crop((left, 0, right, height))
        if (width / height) < (target_width / target_height):
            # too tall
            ideal_height = target_height / target_width * width
            top = (height - ideal_height) / 2
            bottom = (height + ideal_height) / 2
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

    def draw_bottom_block(self, base_image, card_info: CardInfo):
        if not self.is_legend(card_info):
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
        else:
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

            draw.rounded_rectangle(
                ((left, top), (right, bottom)),
                self.config.bottom_block_legend_radius,
                fill=self.config.bottom_block_color
                + (self.config.bottom_block_transparency,),
            )
            out = PIL.Image.alpha_composite(base_image, new_image)
            return out

    def is_legend(self, card_info: CardInfo):
        if "传说" in card_info.explanation or "传奇" in card_info.explanation:
            return True
        return False

    # 准备好底板，除了描述和血量，元素消耗之类的其他东西，包括原画
    def prepare_outline(self, card_info: CardInfo):
        if not self.is_legend(card_info):
            # 添加背景
            base_image = self.get_background(card_info)
            # 添加卡牌原画
            drawing_image = self.get_drawing(card_info)
            base_image = self.adjust_image(
                base_image, (self.config.card_width, self.config.card_height)
            )
            drawing_image = self.adjust_image(
                drawing_image, (self.config.drawing_width, self.config.drawing_height)
            )
            # 添加原画
            base_image.paste(
                drawing_image,
                (
                    int((self.config.card_width - self.config.drawing_width) / 2),
                    self.config.drawing_to_upper,
                ),
            )
            # 添加底部文字背景
            base_image = self.draw_bottom_block(base_image, card_info)

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
        else:
            base_image = self.get_drawing(card_info)
            # 添加卡牌原画
            base_image = self.adjust_image(
                base_image, (self.config.card_width, self.config.card_height)
            )
            base_image = self.draw_bottom_block(base_image, card_info)

            return base_image

    def estimate_text_size(self, text, font):
        length = font.getsize(text)[0]
        return length

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

    # def get_category_image(self, card_info: CardInfo):
    #     return self.get_image_without_extension(
    #         os.path.join(
    #             self.config.general_path, "ele_" + self.translator(card_info.category)
    #         )
    #     )

    def get_category_image(self, category: str):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, "ele_" + self.translator(category))
        )

    def draw_category_and_name(self, card_info: CardInfo, base_image: PIL.Image):
        # add name
        text_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.name_font),
            self.config.name_font_size,
        )
        length_estimate = self.estimate_text_size(card_info.name, text_font)
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
        text_height = text_font.getsize(card_info.name)[1]
        text_top = (
            self.config.name_rect_top + (self.config.name_rect_height - text_height) / 2
        )

        base_image = self.add_text_on_image(
            base_image,
            card_info.name,
            (text_left, text_top),
            text_font,
            self.config.name_text_font_color,
        )

        # add category

        category_image = self.get_category_image(card_info.category)
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

    def draw_cost(self, card_info: CardInfo, base_image: PIL.Image):
        # estimate the length
        all_costs = []
        for ele in card_info.elements_cost.keys():
            if card_info.elements_cost[ele] > 0:
                all_costs.append((ele, card_info.elements_cost[ele]))
        # nothing to do here
        if len(all_costs) == 0:
            return base_image

        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.cost_font),
            self.config.cost_font_size,
        )

        number_length = 0
        for tup in all_costs:
            number_length += font.getsize(str(tup[1]))[0]
        category_length = len(all_costs) * self.config.cost_category_width
        total_length = (
            number_length
            + category_length
            + len(all_costs) * self.config.cost_padding * 2
            + self.config.cost_padding
        )
        # draw the rectangle
        rect_top = self.config.cost_rect_top
        rect_left = self.config.cost_rect_left
        rect_right = rect_left + total_length
        rect_bottom = rect_top + self.config.cost_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (rect_left, rect_top, rect_right, rect_bottom),
            self.config.cost_rect_radius,
            self.config.cost_rect_fill,
            self.config.cost_rect_outline_color,
            self.config.cost_rect_outline_width,
        )
        # put in the numbers and categories
        left_pointer = rect_left + self.config.cost_padding
        text_height = font.getsize("1")[1]
        text_top = int(
            rect_top
            + (self.config.cost_rect_height - text_height) / 2
            - self.config.cost_font_compensation
        )
        category_top = int(
            rect_top
            + (self.config.cost_rect_height - self.config.cost_category_width) / 2
        )
        # sort all costs, put the corresponding element to the head
        for tup in all_costs:
            if tup[0] == card_info.category:
                all_costs.remove(tup)
                all_costs.insert(0, tup)
                break
        # draw the elements
        for tup in all_costs:
            # draw the number
            base_image = self.add_text_on_image(
                base_image,
                str(tup[1]),
                (left_pointer, text_top),
                font,
                self.config.cost_font_color,
            )
            left_pointer += font.getsize(str(tup[1]))[0] + self.config.cost_padding

            # draw the category
            category_image = self.get_category_image(tup[0])
            category_image = self.adjust_image(
                category_image,
                (
                    self.config.cost_category_width,
                    self.config.cost_category_width,
                ),
            )
            base_image.paste(
                category_image,
                (left_pointer, category_top),
                mask=category_image,
            )
            left_pointer += self.config.cost_category_width + self.config.cost_padding

        return base_image

    def draw_explanation(self, card_info: CardInfo, base_image: PIL.Image):
        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.explanation_font),
            self.config.explanation_font_size,
        )
        base_image = self.add_text_on_image(
            base_image,
            card_info.explanation,
            (
                self.config.explanation_text_left,
                self.config.explanation_text_to_block_top
                + self.config.drawing_to_upper
                + self.config.drawing_height,
            ),
            font,
            self.config.explanation_font_color,
        )
        return base_image

    def draw_discription_and_quote(self, card_info: CardInfo, base_image: PIL.Image):
        # dynamically adjust font size
        discription_font_size = self.config.explanation_font_size
        quote_font_size = self.config.quote_font_size
        discription_line_spacing = self.config.discription_line_spacing
        quote_line_spacing = self.config.quote_line_spacing
        discription_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.discription_font),
            discription_font_size,
        )

        quote_font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.quote_font),
            quote_font_size,
        )

        estimated_total_height = 0

        # estimate discription height

        discription_textwrap_width_pixel = (
            self.config.card_width - self.config.discription_text_left * 2
        )
        discription_textwrap_width = int(
            discription_textwrap_width_pixel / discription_font.getsize("标")[0]
        )
        discription_wrapped_text = textwrap.wrap(
            card_info.description, width=discription_textwrap_width
        )
        discription_text_height = discription_font.getsize("标")[1]
        discription_height = discription_line_spacing + (
            discription_text_height + discription_line_spacing
        ) * len(discription_wrapped_text)

        # estimate quote height
        quote_textwrap_width_pixel = (
            self.config.card_width - self.config.quote_text_left * 2
        )
        quote_textwrap_width = int(
            quote_textwrap_width_pixel / quote_font.getsize("标")[0]
        )
        quote_wrapped_text = textwrap.wrap(card_info.quote, width=quote_textwrap_width)
        quote_text_height = quote_font.getsize("标")[1]
        quote_height = quote_line_spacing + (
            quote_text_height + quote_line_spacing
        ) * len(quote_wrapped_text)
        estimated_total_height = discription_height + quote_height

        while (
            estimated_total_height
            > self.config.bottom_block_height
            - self.config.discription_text_to_block_top
            - self.config.quote_text_to_block_bottom
        ):
            alpha = 0.9
            discription_font_size = int(discription_font_size * alpha)
            quote_font_size = int(quote_font_size * alpha)
            discription_line_spacing = int(discription_line_spacing * alpha)
            quote_line_spacing = int(quote_line_spacing * alpha)
            discription_font = PIL.ImageFont.truetype(
                os.path.join(self.config.font_path, self.config.discription_font),
                discription_font_size,
            )

            quote_font = PIL.ImageFont.truetype(
                os.path.join(self.config.font_path, self.config.quote_font),
                quote_font_size,
            )

            # estimate discription height

            discription_textwrap_width_pixel = (
                self.config.card_width - self.config.discription_text_left * 2
            )
            discription_textwrap_width = int(
                discription_textwrap_width_pixel / discription_font.getsize("标")[0]
            )
            discription_wrapped_text = textwrap.wrap(
                card_info.description, width=discription_textwrap_width
            )
            discription_text_height = discription_font.getsize("标")[1]
            discription_height = discription_line_spacing + (
                discription_text_height + discription_line_spacing
            ) * len(discription_wrapped_text)

            # estimate quote height
            quote_textwrap_width_pixel = (
                self.config.card_width - self.config.quote_text_left * 2
            )
            quote_textwrap_width = int(
                quote_textwrap_width_pixel / quote_font.getsize("标")[0]
            )
            quote_wrapped_text = textwrap.wrap(
                card_info.quote, width=quote_textwrap_width
            )
            quote_text_height = quote_font.getsize("标")[1]
            quote_height = quote_line_spacing + (
                quote_text_height + quote_line_spacing
            ) * len(quote_wrapped_text)
            estimated_total_height = discription_height + quote_height

        # start drawing
        # draw discription
        discription_top_pointer = (
            self.config.discription_text_to_block_top
            + self.config.drawing_to_upper
            + self.config.drawing_height
        )

        for line in discription_wrapped_text:
            base_image = self.add_text_on_image(
                base_image,
                line,
                (
                    self.config.discription_text_left,
                    discription_top_pointer,
                ),
                discription_font,
                self.config.discription_font_color,
            )
            discription_top_pointer += (
                discription_line_spacing + discription_text_height
            )
        # draw quote
        quote_bottom_pointer = (
            self.config.bottom_block_height
            + self.config.drawing_to_upper
            + self.config.drawing_height
            - self.config.quote_text_to_block_bottom
            - quote_text_height
        )

        for line in reversed(quote_wrapped_text):
            base_image = self.add_text_on_image(
                base_image,
                line,
                (
                    self.config.quote_text_left,
                    quote_bottom_pointer,
                ),
                quote_font,
                self.config.quote_font_color,
            )
            quote_bottom_pointer -= quote_line_spacing + quote_text_height
        return base_image

    def draw_gain(self, card_info: CardInfo, base_image: PIL.Image):
        # estimate the length
        all_gains = []
        for ele in card_info.elements_gain.keys():
            if card_info.elements_gain[ele] > 0:
                all_gains.append((ele, card_info.elements_gain[ele]))
        # nothing to do here
        if len(all_gains) == 0:
            return base_image

        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.gain_font),
            self.config.gain_font_size,
        )

        number_length = 0
        for tup in all_gains:
            number_length += font.getsize(str(tup[1]))[0]
        category_length = len(all_gains) * self.config.gain_category_width
        total_length = (
            number_length
            + category_length
            + len(all_gains) * self.config.gain_padding * 2
            + self.config.gain_padding
        )
        # draw the rectangle
        rect_top = self.config.gain_rect_top
        rect_right = self.config.gain_rect_right
        rect_left = rect_right - total_length
        rect_bottom = rect_top + self.config.gain_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (rect_left, rect_top, rect_right, rect_bottom),
            self.config.gain_rect_radius,
            self.config.gain_rect_fill,
            self.config.gain_rect_outline_color,
            self.config.gain_rect_outline_width,
        )
        # put in the numbers and categories
        text_height = font.getsize("8")[1]
        right_pointer = (
            rect_right - self.config.gain_padding - self.config.gain_category_width
        )

        text_top = int(
            rect_top
            + (self.config.gain_rect_height - text_height) / 2
            - self.config.gain_font_compensation
        )
        category_top = int(
            rect_top
            + (self.config.gain_rect_height - self.config.gain_category_width) / 2
        )
        # sort all gains, put the corresponding element to the head
        for tup in all_gains:
            if tup[0] == card_info.category:
                all_gains.remove(tup)
                all_gains.insert(0, tup)
                break
        all_gains = reversed(all_gains)
        # draw the elements
        for tup in all_gains:
            # draw the category
            category_image = self.get_category_image(tup[0])
            category_image = self.adjust_image(
                category_image,
                (
                    self.config.gain_category_width,
                    self.config.gain_category_width,
                ),
            )
            base_image.paste(
                category_image,
                (right_pointer, category_top),
                mask=category_image,
            )
            right_pointer -= font.getsize(str(tup[1]))[0] + self.config.gain_padding

            # draw the number
            base_image = self.add_text_on_image(
                base_image,
                str(tup[1]),
                (right_pointer, text_top),
                font,
                self.config.gain_font_color,
            )
            right_pointer -= self.config.gain_category_width + self.config.gain_padding

        return base_image

    def get_life_image(self):
        return self.get_image_without_extension(
            os.path.join(self.config.general_path, "life")
        )

    def draw_life(self, card_info: CardInfo, base_image: PIL.Image):
        if card_info.life == 0:
            return base_image
        life_image = self.get_life_image()
        life_image = self.adjust_image(
            life_image, (self.config.life_icon_width, self.config.life_icon_width)
        )
        font = PIL.ImageFont.truetype(
            os.path.join(self.config.font_path, self.config.life_font),
            self.config.life_font_size,
        )
        estimated_length = (
            font.getsize(str(card_info.life))[0]
            + self.config.life_padding * 3
            + self.config.life_icon_width
        )
        left = self.config.life_rect_left
        top = self.config.life_rect_top
        right = left + estimated_length
        bottom = top + self.config.life_rect_height
        base_image = self.draw_round_corner_rectangle(
            base_image,
            (left, top, right, bottom),
            self.config.life_rect_radius,
            self.config.life_rect_fill,
            self.config.life_rect_outline_color,
            self.config.life_rect_outline_width,
        )

        left_pointer = left + self.config.life_padding
        life_top = int(
            self.config.life_rect_top
            + (self.config.life_rect_height - self.config.life_icon_width) / 2
        )
        base_image.paste(
            life_image,
            (left_pointer, life_top),
            mask=life_image,
        )
        left_pointer += self.config.life_icon_width + self.config.life_padding
        life_text_top = int(
            self.config.life_rect_top
            + (self.config.life_rect_height - font.getsize(str(card_info.life))[1]) / 2
            - self.config.life_font_compensation
        )
        base_image = self.add_text_on_image(
            base_image,
            str(card_info.life),
            (left_pointer, life_text_top),
            font,
            self.config.life_font_color,
        )
        return base_image

    def make_unit_card(self, card_info: CardInfo):
        # 准备底层
        base_image = self.prepare_outline(card_info)
        # 准备左上角元素+名称
        base_image = self.draw_category_and_name(card_info, base_image)
        # 准备费用
        base_image = self.draw_cost(card_info, base_image)
        # 准备解释
        base_image = self.draw_explanation(card_info, base_image)
        # 准备卡牌描述和引言
        base_image = self.draw_discription_and_quote(card_info, base_image)
        # 准备底部负载
        base_image = self.draw_gain(card_info, base_image)
        # 准备生命
        base_image = self.draw_life(card_info, base_image)
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
