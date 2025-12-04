import pygame


# 创建的外星人的类，形状，颜色，位置
class Alien(pygame.sprite.Sprite):
    # 初始化外星人
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('../images/alien.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    # 保证外星人在屏幕之内
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right > screen_rect.right) or (self.rect.left <= 0)

    # 更新外星人的移动方式
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
