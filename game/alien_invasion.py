import sys

import pygame

from game.alien import Alien
from game.setting import Settings
from game.ship import Ship
from bullet import Bullet


class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen_width = self.screen.get_rect().width
        # self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()
            self._create_fleet()
            self._update_screen()


            pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            print('right')
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            print('left')
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
            print('up')
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
            print('down')
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            print('fire')
        elif event.key == pygame.K_q:
            print('quit')
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

    def _update_bullet(self):
        self.bullet.update()
        for blt in self.bullet.sprites():
            if blt.rect.bottom < 0:
                self.bullet.remove(blt)


    def _create_fleet(self):
        alien = Alien(self)
        self.aliens.add(alien)
        alien_width = alien.rect.width

        current_x = alien_width
        while current_x < self.settings.screen_width - 2* alien_width:
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = new_alien.x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullets in self.bullet.sprites():
            bullets.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
