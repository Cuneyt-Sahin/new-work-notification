# 1. Adım: Playwright'in resmi, her şeyin kurulu olduğu Python imajını temel al
FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

# 2. Adım: Proje dosyalarının kopyalanacağı bir çalışma dizini oluştur
WORKDIR /app

# 3. Adım: Gerekli proje dosyalarını konteynerin içine kopyala
COPY requirements.txt .
COPY oto.py .

# 4. Adım: Sadece Python kütüphanelerini kur
RUN pip install -r requirements.txt

