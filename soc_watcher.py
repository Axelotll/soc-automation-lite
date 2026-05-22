import urllib.request
import json
import time
import os

def get_email_count():
    try:
        # Menghubungi API MailHog lokal
        req = urllib.request.urlopen('http://127.0.0.1:8025/api/v2/messages')
        data = json.loads(req.read())
        return data['total']
    except Exception:
        return 0

print("🛡️  SOC Watchdog Aktif. Memantau lalu lintas email...")
last_count = get_email_count()

while True:
    time.sleep(3) # Mengecek API setiap 3 detik secara diam-diam
    current_count = get_email_count()
    
    if current_count > last_count:
        print("\n[!!!] ALERT: Lalu Lintas Email Baru Terdeteksi! [!!!]")
        print("⏳ Mengekstrak data metadata email...")
        os.system('python3 phish_catcher_new.py')
        print("✅ Data berhasil dibungkus ke dalam security_report.json")
        print("\n🚨 OPENCLAW: TUGAS BARU! BACA LAPORAN SEKARANG DAN BERIKAN ANALISA!")
        last_count = current_count
        # Menghentikan loop agar AI bisa mengambil alih terminal
