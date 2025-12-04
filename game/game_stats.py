

# 游戏统计，如果角色死了就重新生成飞船，重新生成外星人，清空子弹，重置位置
class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_state()

    #
    def reset_state(self):
        self.ships_left = self.settings.ship_limit