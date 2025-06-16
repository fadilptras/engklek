from ursina import *

class OpeningScene(Entity):
    def __init__(self, game_controller, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        
        self.game_controller = game_controller
        color.pohon = color.rgb(118/255, 69/255, 59/255)

        # Entitas-entitas ini sekarang jadi 'anak' dari OpeningScene
        # Saat OpeningScene dihancurkan, semua anaknya ikut hancur.
        self.background = Entity(
            parent=self, model='quad', texture='assets/img/opening-bg.png',
            scale=(camera.aspect_ratio, 1), z=10
        )
        
        bar_width = 0.60
        Entity(parent=self, model='quad', color=color.white10, scale=(bar_width, 0.05), position=(-0.3, -0.15), z=5)
        
        self.progress_bar = Entity(
            parent=self, model='quad', color=color.pohon,
            scale=(0.001, 0.04), position=(-0.7, -0.1), origin=(-0.5, 0), z=4
        )

        self.progress = 0
        self.bar_width = bar_width

    def update(self):
        """Metode update akan dipanggil Ursina secara otomatis setiap frame."""
        if self.progress < 100:
            self.progress += 20 * time.dt
            self.progress_bar.scale_x = min(self.progress / 100 * self.bar_width, self.bar_width)
        else:
            # 1. Nonaktifkan update untuk scene ini terlebih dahulu.
            self.enabled = False
            
            # 2. Baru panggil controller untuk menghancurkan scene ini dan pindah ke scene berikutnya.
            self.game_controller.go_to_main_menu()