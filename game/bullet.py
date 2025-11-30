import pygame
from pygame.sprite import Sprite

# 定义一个子弹类
class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        # 在飞船的当前位置创建子弹
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0，0） 出创建一个表示子弹的矩形，并且把位置放正确咯
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)