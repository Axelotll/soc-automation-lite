import json
import urllib.request

# Ambil data dari MailHog
url = 'http://127.0.0.1:8025/api/v2/messages?limit=1'
with urllib.request.urlopen(url) as response:
    data = json.load(response)

if data['total'] > 0:
    email = data['items'][0]
    subject = email['Content']['Headers']['Subject'][0]
    
    # Logika lokal (Tanpa API)
    if "kampus" in subject.lower() or "pemblokiran" in subject.lower():
        laporan = {"STATUS": "Phishing", "SEVERITY": "High", "INDICATOR": "Taktik urgensi."}
    else:
        laporan = {"STATUS": "Aman", "SEVERITY": "Low", "INDICATOR": "Email komunikasi internal."}

    # Tulis file
    with open("security_report.json", "w") as f:
        json.dump(laporan, f, indent=4)
    print("SUCCESS: Laporan diupdate")
