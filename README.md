# 🥋 Lead-Dojo: Hybrid System-1 & System-2 Thinking for LLMs

**Lead-Dojo** ist ein Proof-of-Concept für eine zuverlässige KI-Acrhitektur. Es kombiniert die kreative Sprachgewalt von LLMs (System-1) mit der logischen Stabilität einer vektorbasierten Lead-Datenbank (Hinweis-Datenbank "System-2"). Anstatt sich auf die oft unzuverlässigen Halluzinationen von Sprachmodellen zu verlassen, nutze ich in mit diesem System einen "Sensei-Ansatz": Jede Antwort wird erst gegen verifizierte Fakten (Leads/Hinweise) aus einer ChromaDB geprüft und ergänzt.

## 🚀 (Aktuelle) Kern-Features

- **Hybrid Reasoning:** Verknüpfung von Ollama (Model: Gemma 2B) mit ChromaDB.
- **Dynamic Ingestion:** Batch-Verarbeitung von Wissen über strukturierte JSON-Leads.
- **Upsert-Logik:** Intelligente Wissens-Aktualisierung ohne Dubletten (Redundanzen).
- **Tutor-Mode:** Ein speziell entwickelter System-Prompt für pädagogische wertvolle Antworten statt bloß stupiden "Fakten-Nachplapperei".
- **Categorization:** Automatische Themen-Trennung für skalierbare Wissensdatenbanken.

## 🛠️ Tech-Stack

- **LLM:** Google Gemma2:2b (via Ollama).
- **Vector-DB:** ChromaDB.
- **Sprache:** Python 3.13
- **Infrastructure:** Docker & Kubernetes (in 🚧)
- **Security:** Snyk Container & Library Scanning

## 📂 Projektstruktur

```text
/Lead-Dojo
  ├── data/               # Wissensbasis (JSON Leads)
  ├── db/                 # Persistente ChromaDB (Vektorspeicher)
  ├── Docs/               # Architektur-Diagramme & Deep-Dives
  ├── src/
  │   ├── ingestor.py     # Daten-Import & Kategorisierung
  │   ├── main.py         # Hybrid Chat-Loop & Sensei-Logik
  │   └── query_test.py   # DB-Integrationstests
  └── requirements.txt    # Abhängigkeiten 
  ```

## 🏗 Roadmap

- [x] Prototyp: Verbindung LLM & Vektor-DB
- [x] Batch-Ingestion & Upsert-Logik
- [x] Pädagogisches Prompt-Refining
- [ ] Next: Containerisierung (Docker & K8s Deployment)
- [ ] Next: Web-GUI mit Streamlit
- [ ] Next: Automatisierte Lead-Extraktion (Web-Scraper)

## 🔧 Installation & Start

1. Repository klonen
2. Abhängigkeiten installieren: pip install -r requirements.txt
3. Leads laden: python src/ingestor.py
4. Dojo starten: python src/main.py
