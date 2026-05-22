# Local SOC Automation System

Sistem automasi Security Operations Center (SOC) ringan berbasis Python yang menerapkan arsitektur *Hybrid Triage System*. Proyek ini dirancang untuk menggabungkan disiplin ilmu Cybersecurity, Automasi Scripting (Software Engineering), dan AI Orchestration yang efisien untuk memenuhi standarisasi tugas akhir multi-skill.

Arsitektur ini berhasil mengatasi kendala latensi tinggi dan batas kuota (*rate limit*) API eksternal (Error 429) dengan mengalihkan proses deteksi awal (triase) ke logika deterministik lokal, sementara Agen AI bertindak sebagai pelapor *state* akhir yang aman dari halusinasi data.

## Arsitektur & Multi-Skill Implementation
- **Sensor Data (Networking):** Memantau lalu lintas email lokal secara *real-time* memanfaatkan MailHog API (`/api/v2/messages`) untuk menangkap payload data yang masuk.
- **Triage Engine (Cybersecurity):** Menggunakan logika deterministik berbasis aturan (*Rule-based filtering*) di tingkat lokal untuk mengklasifikasikan indikator ancaman (*phishing*) atau email aman dalam hitungan milidetik tanpa membebani resource eksternal.
- **State Management (Software Engineering):** Menerapkan teknik *JSON Overwrite* melalui berkas fisik `security_report.json` sebagai *Single Source of Truth* untuk menyimpan status keamanan terbaru secara konsisten, mandiri, dan bersifat *stateful*.
- **AI Orchestration (OpenClaw Integration):** Mengintegrasikan Agen AI (OpenClaw) sebagai komponen pelaporan tingkat akhir. Dengan memanfaatkan pembacaan data memori lokal, Agen AI terhindar dari risiko halusinasi data, menghemat penggunaan token/kuota API, dan mampu memberikan respon instan (*Direct Answer*).

## Struktur File Proyek
- `soc_watcher_new.py` : Skrip *watchdog* utama yang melakukan pemantauan (*polling*) berkala secara otomatis setiap 5 detik di latar belakang.
- `phish_catcher_new.py` : Mesin pemroses data yang mengekstrak subjek email dari MailHog, menjalankan klasifikasi logis, dan memperbarui *state* laporan keamanan.
- `safe_mail.py` : Skrip simulator internal untuk menguji pengiriman email sah komunikasi internal perusahaan (PT Ithaca Resources).
- `.gitignore` : Berkas konfigurasi untuk mencegah file *state/log* (`security_report.json`) ikut terunggah ke repositori Git publik.

## Panduan Menjalankan Simulasi

1. **Pastikan Layanan Sensor Aktif:**
   Pastikan **MailHog** telah berjalan di lingkungan lokal (*localhost*) Anda pada port web `8025` (dashboard) dan port SMTP `1025`.

2. **Jalankan Watchdog Otomatis (Terminal 1):**
   Buka terminal utama Anda, masuk ke direktori proyek `soc-automation`, lalu aktifkan sistem pengawas:
   ```bash
   python3 soc_watcher_new.py

3. Simulasikan Email Masuk (Terminal 2):
Buka tab terminal baru (Terminal 2), kemudian jalankan simulator untuk mengirimkan email percobaan sah:

  python3 safe_mail.py
  
Catatan: Sistem di Terminal 1 secara otomatis akan langsung menangkap email tersebut dan melakukan overwrite instan pada berkas security_report.json.

5. Aktifkan Antarmuka AI (Terminal 3):
Buka tab terminal ketiga (Terminal 3) untuk menjalankan antarmuka OpenClaw TUI Anda:

openclaw tui

6. Prompt Eksekusi & Analisis Akhir (Copy ke OpenClaw TUI):
Gunakan prompt terstruktur dan kaku berikut ini di dalam OpenClaw TUI untuk memaksa AI membaca berkas memori statis lokal tanpa melakukan interpretasi bebas (halusinasi):

Jalankan perintah `cat security_report.json` di terminal sekarang. Baca isi output tersebut, lalu berikan laporan akhir HANYA dalam format raw di bawah ini tanpa tambahan salam, basa-basi bahasa natural, atau kalimat penutup apa pun:

[STATUS] = (Aman / Phishing)
[SEVERITY] = (Low / Medium / High / Critical)
[INDICATOR] = (Ambil langsung dari data JSON)


Laporan  =  https://docs.google.com/document/d/1Gufs5lmRy8Zrp9Se_f9XwgWuYE9on93LKja7rfObyzY/edit?usp=sharing
Video  =  https://drive.google.com/file/d/1aT6_5yfVsJoF_dmOZ_QLsAYjIZtG5WkX/view?usp=sharing
