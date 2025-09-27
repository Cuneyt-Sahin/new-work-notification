# 1. Adım: Resmi Python 3.11 imajını temel alarak başla
FROM python:3.11-slim

# 2. Adım: Proje dosyalarının kopyalanacağı bir çalışma dizini oluştur
WORKDIR /app

# --- YENİ EKLENEN KISIM ---
# 3. Adım: Playwright'in ihtiyaç duyduğu sistem kütüphanelerini kur
# Önce paket listesini güncelle, sonra bağımlılıkları kur
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    libgtk-3-0 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
# --- YENİ KISMIN SONU ---

# 4. Adım: Önce sadece requirements dosyasını kopyala
COPY requirements.txt .

# 5. Adım: Gerekli Python kütüphanelerini kur
RUN pip install --no-cache-dir -r requirements.txt

# 6. Adım: Playwright'in ihtiyaç duyduğu Firefox tarayıcısını kur
RUN playwright install firefox

# 7. Adım: Projendeki diğer tüm dosyaları (.py, .json vb.) kopyala
COPY . .

# 8. Adım: Konteyner başladığında hangi komutun çalışacağını belirt
CMD ["python", "oto.py"]