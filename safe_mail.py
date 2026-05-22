import smtplib
from email.message import EmailMessage

def send_safe_mail():
    msg = EmailMessage()
    
    # Konten Email Internal Perusahaan
    msg.set_content("""Halo tim,

Terlampir draft perencanaan konten media sosial untuk PT Ithaca Resources bulan depan. 
Tolong segera di-review oleh divisi Corporate Creative & Communication sebelum kita jadwalkan postingannya.

Terima kasih.""")
    
    msg['Subject'] = 'Review Draft Konten Ithaca'
    msg['From'] = 'internal@ithacaresources.com'
    msg['To'] = 'target@mailhog.local'
    
    try:
        # Menembak ke port SMTP default MailHog
        server = smtplib.SMTP('127.0.0.1', 1025)
        server.send_message(msg)
        server.quit()
        print("[+] Safe Mail 'Review Draft Konten Ithaca' berhasil dikirim ke MailHog!")
    except Exception as e:
        print(f"[-] Gagal mengirim email: {e}")

if __name__ == "__main__":
    send_safe_mail()
