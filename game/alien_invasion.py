import inspect
import sys
import time

import pygame

from game.alien import Alien
from game.game_stats import GameStats
from game.setting import Settings
from game.ship import Ship
from bullet import Bullet


class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # 设置游戏屏幕边界
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen_width = self.screen.get_rect().width
        # self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        # 设置飞船
        self.ship = Ship(self)
        # 设置子弹
        self.bullet = pygame.sprite.Group()
        # 设置外星人
        self.aliens = pygame.sprite.Group()
        # 设置外星人编队
        self._create_fleet()
        self.game_active = True

    def run_game(self):
        while True:
            # 键盘的上下左右
            self._check_events()
            if self.game_active:
                self.ship.update()
                # 设置子弹
                self._update_bullet()
                # 设置外星人
                self._update_aliens()
            # 设置屏幕
            self._update_screen()
            # 一次性更新上面所有东西
            pygame.display.flip()
            self.clock.tick(60)

    # 检查键盘输入状态
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # 键盘按下去的状态
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

    # 键位弹起来的状态
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    # 根据子弹数量限制生成子弹
    def _fire_bullet(self):
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

    def _update_bullet(self):
        self.bullet.update()
        for blt in self.bullet.sprites():
            if blt.rect.bottom < 0:
                self.bullet.remove(blt)
        # 检查子弹是否击中了外星人，如果是，就删除子弹和外星人
        self._check_bullet_alien_collisions()

    # 建立编队
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 安全检查
        if alien_width <= 0 or alien_height <= 0:
            print("警告：外星人图像未加载，尺寸为0。")
            return

        screen_width = self.settings.screen_width

        max_y = self.settings.screen_height - 3 * alien_height

        current_x = alien_width
        current_y = alien_height

        row = 0
        # 在建立一列
        while current_y < max_y and row < 4:  # 限制最多4行
            col = 0
            # 先建立一行
            while current_x < screen_width - 2 * alien_width and col < 15:  # 限制每行15个
                self._create_aliens(current_x, current_y)
                current_x += 2 * alien_width
                col += 1
            # 准备下一行
            current_x = alien_width
            current_y += 2 * alien_height
            current_line = inspect.currentframe().f_lineno
            print(f"循环中，x:{current_x} y:{current_y},当前行号：{current_line}")
            row += 1

    # 创造外星人
    def _create_aliens(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    # 检查外星人移动的状态
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_direction()
                break

    # 外形舰队转向
    def _change_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # 设置击中敌人
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullet, self.aliens, True, True)
        if not self.aliens:
            self.bullet.empty()
            self._create_fleet()

    # 击落玩家飞船
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottoms()

    # 飞船被击中
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullet.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            time.sleep(0.5)
        else:
            self.game_active = False

    # 更新屏幕
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullets in self.bullet.sprites():
            bullets.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

    def _check_aliens_bottoms(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()


# todo:记分系统，新增开始按钮，背景乐，提高难度，显示积分与最高分