class Settings:


    def __init__(self):
        # 分辨率
        self.screen_width = 1920
        self.screen_height = 1080
        # 背景色
        self.bg_color = (255, 255, 255)
        # 飞船移动的速度
        self.ship_speed  = 15
        # 子弹的速度
        self.bullet_speed = 30.0
        # 子弹的宽度
        self.bullet_width = 4
        # 子弹的长度
        self.bullet_height = 20
        # 子弹的颜色
        self.bullet_color = (0, 0, 0)
        # 同时存在的子弹的数量
        self.bullet_allowed = 5
        # 外星人移动的速度
        self.alien_speed = 5.0
        # 飞船下降的速度
        self.fleet_drop_speed = 10.0
        #舰队移动方向
        self.fleet_direction = 1
        # 拥有三艘飞船
        self.ship_limit = 3