import time
import os

# Konfigurasi
INTERVAL_DETIK = 5
DETEKTOR = 'phish_catcher_new.py'

print("🛡️  SOC Watchdog Aktif. Memantau lalu lintas email...")
print(f"[*] Menggunakan detektor: {DETEKTOR}")

while True:
    # Menjalankan mesin deteksi
    # Perintah ini akan mengecek MailHog dan otomatis overwrite JSON
    os.system(f'python3 {DETEKTOR}')
    
    # Jeda agar tidak memakan CPU
    time.sleep(INTERVAL_DETIK)
