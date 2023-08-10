"""
配置文件
"""
import os


class Config:
    def __init__(self) -> None:
        # 卡片
        self.card_width = 590
        self.card_height = 860
        # 卡片原画
        self.drawing_width = 510
        self.drawing_height = 510
        self.drawing_to_upper = 40
        # 卡片边框
        self.border_width = 560
        self.border_height = 830
        # 底部的白色块
        self.bottom_block_width = 510
        self.bottom_block_height = 270
        self.bottom_block_color = (255, 255, 255)
        self.bottom_block_transparency = 180
        # 左上元素+名称
        self.name_font_size = 40
        self.name_font = "MaShanZheng-Regular.ttf"
        self.name_rect_height = 60
        self.name_rect_left = 60
        self.name_rect_top = 20
        self.name_rect_radius = 10
        self.name_rect_fill = (255, 195, 0)
        self.name_text_to_left = 90
        self.name_rect_outline_color = (255, 255, 255)
        self.name_rect_outline_width = 3
        self.name_text_font_color = (0, 0, 0)
        self.name_category_width = 80
        self.name_category_left = 0
        self.name_category_top = 10
        # 中央消耗
        self.cost_font_size = 36
        self.cost_font = "SplineSansMono-VariableFont_wght.ttf"
        self.cost_category_width = 45
        self.cost_font_compensation = 3
        self.cost_font_color = (0, 0, 0)
        self.cost_padding = 10
        self.cost_rect_top = 520
        self.cost_rect_left = 20
        self.cost_rect_height = 60
        self.cost_rect_radius = 10
        self.cost_rect_fill = (255, 195, 0)
        self.cost_rect_outline_color = (255, 255, 255)
        self.cost_rect_outline_width = 3
        # 解释
        self.explanation_font = "FangZhengKaiTiJianTi-1.ttf"
        self.explanation_font_size = 24
        self.explanation_font_color = (0, 0, 0)
        self.explanation_text_left = 70
        self.explanation_text_to_block_top = 40
        # 卡牌描述
        self.discription_font = "FangZhengKaiTiJianTi-1.ttf"
        self.discription_font_size = 24
        self.discription_font_color = (0, 0, 0)
        self.discription_text_left = 70
        self.discription_text_to_block_top = 80
        self.discription_line_spacing = 10
        # 卡牌引言
        self.quote_font = "FangZhengKaiTiJianTi-1.ttf"
        self.quote_font_size = 16
        self.quote_font_color = (32, 32, 32)
        self.quote_text_left = 100
        self.quote_text_to_block_bottom = 30
        self.quote_line_spacing = 5

        # 路径
        self.general_path = os.path.join("resources", "gerneral")  # 通用素材
        self.drawing_path = os.path.join("resources", "drawings")  # 卡牌原画
        self.font_path = os.path.join("resources", "fonts")  # 字体
