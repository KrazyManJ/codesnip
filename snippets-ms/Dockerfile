# Použijeme oficiální odlehčenou verzi Pythonu
FROM python:3.13-slim

# Nastavíme pracovní adresář uvnitř kontejneru
WORKDIR /app

# Nejprve zkopírujeme jen requirements (kvůli cacheování Docker vrstev)
COPY requirements.txt .

# Nainstalujeme závislosti
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Zkopírujeme zbytek kódů aplikace
COPY . .

# Spustíme aplikaci
# POZOR: V Dockeru je nutné nastavit host na 0.0.0.0, aby byla aplikace dostupná zvenčí
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--host", "0.0.0.0"]