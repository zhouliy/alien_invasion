import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        self.image = pygame.image.load('../images/alien.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)