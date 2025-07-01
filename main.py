import pygame
from ursina import *
from opening_scene import OpeningScene
from home_scene import MainMenuScene, LevelSelectionScene
from level_scene import LevelScene

class GameController:
    def __init__(self, app):
        self.app = app
        self.current_scene = None

        pygame.init()
        pygame.mixer.music.load('assets/music/cublak-cublak.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def _clear_current_scene(self):
        """Menghancurkan scene saat ini sebelum beralih ke scene baru."""
        if self.current_scene:
            print(f"Clearing scene: {self.current_scene.__class__.__name__}")
            destroy(self.current_scene)
            self.current_scene = None

    def go_to_opening(self):
        self._clear_current_scene()
        self.current_scene = OpeningScene(game_controller=self)

    def go_to_main_menu(self):
        self._clear_current_scene()
        self.current_scene = MainMenuScene(game_controller=self)

    def go_to_level_selection(self):
        self._clear_current_scene()
        self.current_scene = LevelSelectionScene(game_controller=self)

    def start_level(self, level_num):
        self._clear_current_scene()
        self.current_scene = LevelScene(game_controller=self, level_num=level_num)

if __name__ == '__main__':
    app = Ursina(title='Engklek', fullscreen=True)

    Sky()
    sun = DirectionalLight(shadows=True)
    sun.look_at(Vec3(1, -1, -1))

    game_controller = GameController(app)
    game_controller.go_to_opening()

    app.run()
