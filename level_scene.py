from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

class LevelScene(Entity):
    def __init__(self, game_controller, level_num, **kwargs):
        super().__init__(**kwargs) # Parent scene ini adalah scene 3D, bukan camera.ui
        
        self.game_controller = game_controller
        self.level_num = level_num
        
        # Entitas yang spesifik untuk level ini akan disimpan di sini
        # agar mudah dihancurkan saat keluar dari level.
        self.level_entities = []

        # Atur environment
        Entity.default_shader = lit_with_shadows_shader
        Text.default_font = 'assets/font/CaliforniaVibes.ttf'
        mouse.locked = True
        application.paused = False

        self._build_level()

    def _build_level(self):
        """Membangun semua objek dan UI untuk level."""
        self.ground = Entity(model='plane', texture='grass', texture_scale=(8, 8), scale=(64, 1, 64), collider='box')
        self.level_entities.append(self.ground)

        self.tiles = []
        # Pola level bisa dieksternalisasi ke file konfigurasi jika ingin lebih rapi
        tile_positions = [
            (0, 12, 1), (0, 11, 2), (0, 10, 3), (-0.5, 9, 4), (0.5, 9, 4),
            (0, 8, 5), (-0.5, 7, 6), (0.5, 7, 6), (-1, 6, 7), (0, 6, 7),
            (1, 6, 7), (0, 5, 7)
        ]
        for x, z, num in tile_positions:
            self._make_tile(x, z, num)
            
        # Player Setup
        self.player = FirstPersonController(
            model='cube', color=color.white33, origin_y=-0.5, collider='box', speed=5,
            position=self.tiles[0].position + Vec3(0, 1, 0), gravity=1, jump_height=1.5,
            jump_duration=0.4
        )
        self.player.collider = BoxCollider(self.player, Vec3(0, 1, 0), Vec3(0.8, 2, 0.8))
        self.level_entities.append(self.player)
        self.player.speed = 0  # Disable default movement
        self.movement_enabled = False  # Flag untuk pergerakan manual


        # UI Setup
        self._setup_ui()

    def _make_tile(self, x, z, number):
        is_win_flag = (number == 7)
        red_tile = (number == 2)
        
        if is_win_flag: current_tile_color = color.green
        elif red_tile: current_tile_color = color.red
        else: current_tile_color = color.white

        tile = Entity(
            model='cube', color=current_tile_color, scale=(1, 0.2, 1),
            position=(x, 0.1, z), texture='white_cube', collider='box'
        )
        tile.is_win = is_win_flag
        self.level_entities.append(tile)

        text = Text(parent=tile, text=str(number), color=color.black, scale=5,
                    position=(0, 0.55, 0), billboard=True, origin=(0, 0))
        self.level_entities.append(text)
        self.tiles.append(tile)

    def _setup_ui(self):
        """Membuat semua elemen UI dan menyimpannya sebagai atribut."""
        self.win_text = Text(text='YEAYYY, KAMU MENANG!', origin=(0,0), scale=3, color=color.green, enabled=False)
        self.lose_text = Text(text='yah kamu kalah!', origin=(0, 0), scale=3, color=color.red, enabled=False)
        
        self.retry_button = Button(text='mau ulang gak?', color=color.black, scale=(0.15, 0.05), position=(-0.1, -0.1), on_click=self.retry_level, enabled=False)
        self.back_button = Button(text='coba level lain yuk!', color=color.black, scale=(0.20, 0.05), position=(0.08, -0.1), on_click=self.back_to_menu, enabled=False)
        self.next_button = Button(text='lanjut level 2 ahh', color=color.black, scale=(0.25, 0.05), position=(0, -0.1), on_click=self.back_to_menu, enabled=False)
        
        # UI juga bagian dari level_entities agar ikut hancur
        self.level_entities.extend([self.win_text, self.lose_text, self.retry_button, self.back_button, self.next_button])

    def retry_level(self):
        self.player.position = self.tiles[0].position + Vec3(0, 1, 0)
        self.player.rotation = (0,0,0)
        
        self.lose_text.enabled = False
        self.win_text.enabled = False
        self.retry_button.enabled = False
        self.back_button.enabled = False
        self.next_button.enabled = False
        
        application.paused = False
        mouse.locked = True

    def back_to_menu(self):
        mouse.locked = False
        application.paused = False
        self.game_controller.go_to_level_selection()

    def input(self, key):
        if application.paused or self.lose_text.enabled:
            return

        if key == 'space' and self.player.grounded:
            self.player.jump_height = 2.8 if held_keys['left shift'] else 1.5
            self.player.jump()
            self.movement_enabled = True  # Hanya aktif saat loncat

    def update(self):
        if application.paused or self.win_text.enabled:
            return

        # Manual movement control
        if self.movement_enabled and not self.player.grounded:
            direction = Vec3(
                int(held_keys['d']) - int(held_keys['a']),
                0,
                int(held_keys['w']) - int(held_keys['s'])
            ).normalized()
            self.player.position += self.player.forward * direction.z * time.dt * 5
            self.player.position += self.player.right * direction.x * time.dt * 5
        else:
            self.movement_enabled = False  # Matikan movement kalau grounded lagi

        # Posisi pemain sekarang
        player_pos = self.player.position

        # Cek apakah berada di atas tile
        on_tile = any(
            abs(player_pos.x - t.x) < t.scale_x / 2 and abs(player_pos.z - t.z) < t.scale_z / 2
            for t in self.tiles
        )

        # Menang jika injak petak hijau
        stepped_on_win_tile = any(
            t.is_win and abs(player_pos.x - t.x) < t.scale_x / 2 and abs(player_pos.z - t.z) < t.scale_z / 2
            for t in self.tiles
        )

        if stepped_on_win_tile:
            self.win_text.enabled = True
            self.next_button.enabled = True
            mouse.locked = False
            application.paused = True
            return

        # Kalah jika jatuh
        if not on_tile and player_pos.y < self.ground.y + 0.5:
            self.lose_text.enabled = True
            self.retry_button.enabled = True
            self.back_button.enabled = True
            mouse.locked = False
            application.paused = True
            return

        # Kalah jika benar-benar menginjak tengah petak merah
        for t in self.tiles:
            if t.color == color.red:
                if distance_2d((player_pos.x, player_pos.z), (t.x, t.z)) < 0.3 and abs(player_pos.y - t.y) < 1:
                    self.lose_text.enabled = True
                    self.retry_button.enabled = True
                    self.back_button.enabled = True
                    mouse.locked = False
                    application.paused = True
                    return
            
    def on_destroy(self):
        """Dipanggil otomatis oleh Ursina saat `destroy(self)` dieksekusi."""
        # Membersihkan semua entitas yang dibuat secara manual
        # Ini PENTING untuk mencegah memory leak.
        for e in self.level_entities:
            destroy(e)
        self.level_entities.clear()
        
        # Mengembalikan shader default jika diubah
        Entity.default_shader = None

    def distance_2d(a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
