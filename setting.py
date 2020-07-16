class Setting():

    def __init__(self):
        self.screen_width=1200
        self.screen_hight=800
        self.color=(230,230,230)


        self.ship_limit=3


        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullets_allow=10


        self.fleet_drop_speed=10


        self.speedup_scale=2
        self.alien_points=50

        self.initialize_dynamic_setting()

        #把数据分开，上边是不变量，下边是需要更新的量
    def initialize_dynamic_setting(self):
        self.ship_speed_factor=1.5
        self.bullet_speed_factor=3
        self.alien_speed_factor=1

        self.fleet_direction=1

    def increase_speed(self):
        self.alien_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.ship_speed_factor*=self.speedup_scale
