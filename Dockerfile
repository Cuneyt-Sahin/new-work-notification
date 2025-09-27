# 1. Adım: Resmi Python 3.11 imajını temel alarak başla
FROM python:3.11-slim

# 2. Adım: Proje dosyalarının kopyalanacağı bir çalışma dizini oluştur
WORKDIR /app

# 3. Adım: Önce sadece requirements dosyasını kopyala
COPY requirements.txt .

# 4. Adım: Gerekli Python kütüphanelerini kur
# --no-cache-dir, imaj boyutunu küçük tutmaya yardımcı olur
RUN pip install --no-cache-dir -r requirements.txt

# 5. Adım: Playwright'in ihtiyaç duyduğu Firefox tarayıcısını kur
RUN playwright install firefox

# 6. Adım: Projendeki diğer tüm dosyaları (.py, .json vb.) kopyala
COPY . .

# 7. Adım: Konteyner başladığında hangi komutun çalışacağını belirt
# Bu, senin "Start Command" komutundur
CMD ["python", "oto.py"]