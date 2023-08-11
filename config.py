"""
配置文件
"""
import os


# base class for config
class Config:
    def __init__(self):
        pass


# default config
class Config_default(Config):
    def __init__(self):
        super().__init__()
        # 路径
        self.general_path = os.path.join("resources", "gerneral")  # 通用素材
        self.drawing_path = os.path.join("resources", "drawings")  # 卡牌原画
        self.font_path = os.path.join("resources", "fonts")  # 字体
        # 卡片
        self.card_width = 590
        self.card_height = 860
        # 卡片原画
        self.drawing_width = 540
        self.drawing_height = 540  # 530 ok,
        self.drawing_to_upper = 35
        # 卡片边框
        self.border_width = 580
        self.border_height = 830

        # 底部的白色块
        self.bottom_block_width = 540
        self.bottom_block_height = 260
        self.bottom_block_color = (255, 255, 255)
        self.bottom_block_transparency = 150
        self.bottom_block_legend_radius = 0
        # 左上元素+名称
        self.name_font_size = 40
        self.name_font = "MaShanZheng-Regular.ttf"
        self.name_rect_height = 60
        self.name_rect_left = 60
        self.name_rect_top = 10
        self.name_rect_radius = 10
        self.name_rect_fill = (255, 195, 0)
        self.name_text_to_left = 90
        self.name_rect_outline_color = (255, 255, 255)
        self.name_rect_outline_width = 3
        self.name_text_font_color = (0, 0, 0)
        self.name_category_width = 80
        self.name_category_left = 5
        self.name_category_top = 5
        # 中央消耗
        self.cost_font_size = 24
        self.cost_font = "SplineSansMono-VariableFont_wght.ttf"
        self.cost_category_width = 30
        self.cost_font_compensation = 2
        self.cost_font_color = (0, 0, 0)
        self.cost_padding = 10
        self.cost_rect_top = 530
        self.cost_rect_left = 10
        self.cost_rect_height = 50
        self.cost_rect_radius = 25
        self.cost_rect_fill = (255, 195, 0)
        self.cost_rect_outline_color = (255, 255, 255)
        self.cost_rect_outline_width = 3
        # 标签
        self.tag_font = "FangZhengKaiTiJianTi-1.ttf"
        self.tag_font_size = 24
        self.tag_font_color = (0, 0, 0)
        self.tag_text_left = 50
        self.tag_text_to_block_top = 15
        # 卡牌描述
        self.discription_font = "FangZhengKaiTiJianTi-1.ttf"
        self.discription_font_size = 24
        self.discription_font_color = (0, 0, 0)
        self.discription_text_left = 50
        self.discription_text_to_block_top = 55
        self.discription_line_spacing = 10
        # 卡牌引言
        self.quote_font = "FangZhengKaiTiJianTi-1.ttf"
        self.quote_font_size = 18
        self.quote_font_color = (32, 32, 32)
        self.quote_text_left = 100
        self.quote_text_to_block_bottom = 40
        self.quote_line_spacing = 5
        # 底部负载
        self.gain_font_size = 24
        self.gain_font = "SplineSansMono-VariableFont_wght.ttf"
        self.gain_category_width = 30
        self.gain_font_compensation = 1
        self.gain_font_color = (0, 0, 0)
        self.gain_padding = 10
        self.gain_rect_top = 800
        self.gain_rect_right = 580
        self.gain_rect_height = 50
        self.gain_rect_radius = 25
        self.gain_rect_fill = (255, 195, 0)
        self.gain_rect_outline_color = (255, 255, 255)
        self.gain_rect_outline_width = 3
        # 底部生命
        self.life_font_size = 24
        self.life_font = "SplineSansMono-VariableFont_wght.ttf"
        self.life_icon_width = 30
        self.life_font_compensation = 2
        self.life_font_color = (0, 0, 0)
        self.life_padding = 10
        self.life_rect_top = 800
        self.life_rect_left = 10
        self.life_rect_height = 50
        self.life_rect_radius = 25
        self.life_rect_fill = (255, 195, 0)
        self.life_rect_outline_color = (255, 255, 255)
        self.life_rect_outline_width = 3
