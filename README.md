# Game Engklek 3D
Selamat datang di repositori game Engklek 3D! Ini adalah sebuah prototipe game yang dibuat menggunakan Ursina Engine, sebuah game engine berbasis Python. Game ini mengadaptasi permainan tradisional Indonesia, Engklek, ke dalam format 3D first-person.

# Deskripsi
Game ini menantang pemain untuk melompat melintasi serangkaian petak (ubin) untuk mencapai petak kemenangan. Mirip seperti engklek, ada aturan yang harus diikuti: pemain tidak boleh jatuh dari petak dan tidak boleh menginjak petak terlarang berwarna merah.

Saat ini, game terdiri dari beberapa adegan (scene):
- Opening Scene: Layar pembuka dengan bar pemuatan sederhana.
- Main Menu: Menu utama tempat pemain bisa memilih untuk memulai permainan atau keluar.
- Level Selection: Adegan untuk memilih level yang ingin dimainkan.
- Level Scene: Adegan utama tempat permainan berlangsung.

# Fitur Utama
- Gameplay 3D First-Person: Pemain akan merasakan pengalaman bermain engklek dari sudut pandang orang pertama.
- Mekanisme Lompat: Pemain harus melompat dari satu petak ke petak lainnya.
- Kondisi Menang & Kalah:
- Menang: Berhasil mendarat di petak hijau (petak kemenangan).
- Kalah: Jatuh dari petak atau mendarat di tengah petak merah.
- Manajemen Adegan (Scene Management): Proyek ini memiliki struktur yang jelas untuk mengelola transisi antar adegan, seperti dari menu utama ke pemilihan level, lalu ke dalam permainan. Hal ini ditangani oleh GameController.
- Musik Latar: Game ini menggunakan pygame.mixer untuk memutar musik latar "Cublak-Cublak Suweng" secara berulang.
- Aset Eksternal: Menggunakan aset seperti gambar latar, font, dan musik yang disimpan dalam direktori assets.
