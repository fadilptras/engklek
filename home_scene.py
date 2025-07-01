# home_scene.py
from ursina import *

class MainMenuScene(Entity):
    def __init__(self, game_controller, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.game_controller = game_controller

        Text.default_font = 'assets/font/CaliforniaVibes.ttf'
        color.ijoterang = color.rgb(127/255, 145/255, 103/255)
        color.merahredup = color.rgb(144/255, 70/255, 70/255)

        Entity(parent=self, model='quad', texture='assets/img/home-bg.png', scale_x=camera.aspect_ratio, z=4)
        
        Button(
            parent=self, text='Mulai Yuk', scale=(0.15, 0.05), color=color.ijoterang,
            position=(-0.08, 0.03), on_click=self.game_controller.go_to_level_selection
        )
        Button(
            parent=self, text='Udahan Ah', scale=(0.15, 0.05), color=color.merahredup,
            position=(0.08, 0.03), on_click=application.quit
        )

class LevelSelectionScene(Entity):
    def __init__(self, game_controller, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.game_controller = game_controller

        Text.default_font = 'assets/font/CaliforniaVibes.ttf'
        color.ijoterang = color.rgb(127/255, 145/255, 103/255)
        color.merahredup = color.rgb(144/255, 70/255, 70/255)

        Entity(parent=self, model='quad', texture='assets/img/level-bg.png', scale_x=camera.aspect_ratio, z=4)

        Button(
            parent=self, text='Gajadi Main', scale=(0.15, 0.05), position=(0.7, 0.4),
            color=color.merahredup, on_click=self.game_controller.go_to_main_menu
        )
        
        max_levels = 11 
        for i in range(max_levels):
            x = i * 0.15 - 0.3 if i < 5 else (i - 5) * 0.15 - 0.375
            y = 0.3 if i < 5 else 0.17
            
            level_num = i + 1
            Button(
                parent=self, model='circle', text=str(level_num), color=color.ijoterang,
                scale=(0.1, 0.1), position=(x, y),
                on_click=lambda num=level_num: self.start_selected_level(num)
            )

    def start_selected_level(self, level_num):
        self.game_controller.start_level(level_num)
