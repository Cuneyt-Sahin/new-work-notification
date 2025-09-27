import os
import time

print("--- DEBUG SCRIPT BAŞLADI ---")
print("Bu mesajı görüyorsan, Python script'in en azından çalışmaya başlıyor demektir.")

# Test 1: Gizli değişkenleri okumayı dene
print("\n--- Test 1: Gizli Değişkenler (Secrets) ---")
username = os.environ.get('BIONLUK_USERNAME')
password = os.environ.get('BIONLUK_PASSWORD')

if username:
    # Güvenlik için şifrenin sadece varlığını kontrol edip, kendisini yazdırmıyoruz
    print("BAŞARILI: BIONLUK_USERNAME bulundu.")
else:
    print("!!! HATA: BIONLUK_USERNAME bulunamadı veya boş! Railway'deki 'Variables' sekmesini kontrol et. !!!")

if password:
    print("BAŞARILI: BIONLUK_PASSWORD bulundu.")
else:
    print("!!! HATA: BIONLUK_PASSWORD bulunamadı veya boş! Railway'deki 'Variables' sekmesini kontrol et. !!!")

# Test 2: Programın hayatta kaldığından emin olmak için
print("\n--- Test 2: Programın Hayatta Kalması ---")
print("Program 60 saniye boyunca uyuyacak ve sonra kapanacak...")
time.sleep(60)
print("60 saniye geçti.")

print("\n--- DEBUG SCRIPT BİTTİ ---")