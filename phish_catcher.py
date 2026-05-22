import requests
import json

# ==========================================
# 1. KONFIGURASI API
# ==========================================
api_key = "AIzaSyARdPwTFYbz2vMqtiLWNjF6V3GbBithX-U"
# Kita bypass library Python dan tembak URL API-nya langsung!
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"

print("[*] Menghubungkan ke Gateway MailHog...")

# ==========================================
# 2. TARIK EMAIL DARI MAILHOG
# ==========================================
try:
    response = requests.get('http://127.0.0.1:8025/api/v2/messages?limit=1')
    data = response.json()
except Exception as e:
    print(f"[-] Gagal terhubung ke MailHog: {e}")
    exit()

if data['total'] > 0:
    latest_email = data['items'][0]
    subject = latest_email['Content']['Headers']['Subject'][0]
    body = latest_email['Content']['Body']

    print(f"[+] Menemukan email baru!")
    print(f"    Subjek: {subject}")
    print("[*] Menembak data ke Gemini REST API...")

    # ==========================================
    # 3. REQUEST LANGSUNG KE GEMINI
    # ==========================================
    prompt = f"""
    Analisis email berikut. Apakah ini phishing?
    Subjek: {subject}
    Isi: {body}
    
    Jawab hanya menggunakan format JSON persis seperti ini:
    {{
        "status": "Phishing/Aman",
        "tingkat_ancaman": "Tinggi/Sedang/Rendah",
        "alasan": "Penjelasan singkat"
    }}
    """

    # Format data yang diminta oleh server Google
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Mengirim HTTP POST
    gemini_req = requests.post(gemini_url, json=payload)
    gemini_res = gemini_req.json()

    # ==========================================
    # 4. SIMPAN LAPORAN
    # ==========================================
    try:
        # Menarik teks JSON dari struktur respons Gemini
        hasil_teks = gemini_res['candidates'][0]['content']['parts'][0]['text']
        
        # Bersihkan format markdown jika Gemini bandel
        hasil_teks = hasil_teks.replace("```json\n", "").replace("```", "")
        
        with open("security_report.json", "w") as f:
            f.write(hasil_teks)
            
        print("[+] SUCCESS! Laporan bersih tanpa error disimpan ke 'security_report.json'")
    except KeyError:
        print("[-] API Key salah atau ada error dari server:")
        print(json.dumps(gemini_res, indent=2))

else:
    print("[-] Tidak ada email yang ditemukan di MailHog.")
