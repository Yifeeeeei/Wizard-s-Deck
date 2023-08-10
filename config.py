"""
配置文件
"""


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
        self.name_font_size = 36
        self.name_font = "ZCOOLXiaoWei-Regular.ttf"
        self.name_rect_height = 60
        self.name_rect_left = 60
        self.name_rect_top = 20
        self.name_rect_radius = 10
        self.name_rect_fill = (255, 195, 0)
        self.name_text_to_left = 90
        self.name_rect_outline_color = (255, 255, 255)
        self.name_rect_outline_width = 5
        self.name_text_font_color = (0, 0, 0)
        self.name_category_width = 80
        self.name_category_left = 0
        self.name_category_top = 10
        # 路径
        self.general_path = "resources/gerneral"  # 通用素材
        self.drawing_path = "resources/drawings"  # 卡牌原画
        self.font_path = "resources/fonts"  # 字体
