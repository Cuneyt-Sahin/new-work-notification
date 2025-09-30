# 1. Adım: Playwright'in resmi, tarayıcıların ve Python'ın kurulu olduğu imajını temel al
# Bu imaj, "Executable doesn't exist" hatasını çözer çünkü tarayıcılar içinde hazır gelir.
FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

# 2. Adım: Proje dosyaları için çalışma dizinini ayarla
WORKDIR /app

# --- Güvenlik İyileştirmesi ---
# İmaj içindeki dosyaların sahibi olarak root yerine normal bir kullanıcıyı ('pwuser') ayarlayalım.
# Bu, güvenlik açısından en iyi pratiktir.
# Playwright imajı, bu iş için hazır 'pwuser' kullanıcısını içerir.
COPY --chown=pwuser:pwuser requirements.txt .
COPY --chown=pwuser:pwuser oto.py .

# --- Optimizasyon ---
# Bağımlılıkları kurarken gereksiz önbellek dosyaları oluşturmayarak imaj boyutunu küçültelim.
RUN pip install --no-cache-dir -r requirements.txt

# --- Güvenlik İyileştirmesi ---
# Konteyneri root yetkileriyle değil, standart bir kullanıcıyla çalıştır.
USER pwuser

# 5. Adım: Konteyner başladığında çalıştırılacak varsayılan komut
CMD ["python", "oto.py"]