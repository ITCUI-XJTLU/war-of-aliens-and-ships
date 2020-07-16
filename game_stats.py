#游戏进行时的统计参数
class Gamestats():
    def __init__(self,ai_setting):
        self.ai_setting=ai_setting
        self.game_active=False
        self.reset_stats()
        self.high_score=0
        self.level=1


    def reset_stats(self):
        self.ship_left=self.ai_setting.ship_limit

        self.score=0


