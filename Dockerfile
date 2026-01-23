FROM python:3.13-slim

WORKDIR /app

# System-Abhängigkeiten für ChromaDB und Python-Builds
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Erst requirements kopieren für besseres Caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Den gesamten Inhalt (src, data, db) kopieren
COPY . .

# Port für Streamlit
EXPOSE 8501

# Startbefehl via Python-Modul (sicherster Weg)
CMD ["python", "-m", "streamlit", "run", "src/gui.py", "--server.port=8501", "--server.address=0.0.0.0"]