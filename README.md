# 🥋 Lead-Dojo: Hybrid System 2 Thinking for Local LLMs
## Autonomous RAG Architecture & Logic Engine for LernBuddy

**Lead-Dojo** ist das logische Herzstück des **LernBuddy-Ökosystems**. Es implementiert einen "System 2"-Ansatz für lokale Sprachmodelle (Ollama), um die Lücke zwischen schnellen, aber oft ungenauen KI-Antworten und tiefgründiger, logisch verifizierter Wissensverarbeitung zu schließen.

---

## 🧠 Das Konzept: System 2 Thinking
Während Standard-LLMs oft im "System 1" (schnell, intuitiv, fehleranfällig) reagieren, erzwingt Lead-Dojo einen **Reasoning-Workflow**:
1. **Analysieren:** Zerlegung der Benutzeranfrage.
2. **Reflektieren:** Abgleich mit lokalen Wissensdatenbanken (RAG).
3. **Verifizieren:** Logik-Check der Antwort, bevor sie an LernBuddy ausgegeben wird.

---

## 🛠 Tech Stack & Architektur

* **Orchestrierung:** Python (AsyncIO für parallele Reasoning-Chains)
* **KI-Backend:** Ollama (Support für Llama 3, Mistral & Phi-3)
* **Vektordatenbank:** ChromaDB zur Speicherung und Abfrage von Lerninhalten
* **Embeddings:** HuggingFace / Nomic-Embed-Text
* **Integration:** REST API / Socket-Schnittstelle für die **LernBuddy-App**

---

## 🚀 Key Features

### 1. Hybrid RAG (Retrieval-Augmented Generation)
Lead-Dojo kombiniert statische Dokumente (PDFs/Notizen aus LernBuddy) mit dynamischem Web-Retrieval, um Antworten zu generieren, die faktisch fundiert und aktuell sind.

### 2. Privacy-First (100% Lokal)
Entwickelt für maximale Datensicherheit. Die gesamte Verarbeitung – vom Embedding bis zur Inferenz – findet auf der lokalen Infrastruktur statt. Keine API-Calls zu Drittanbietern, keine Datenabflüsse.

### 3. Agentic Logic Layer
Implementierung von spezialisierten Agenten-Rollen:
- **Der Tutor:** Erklärt komplexe Sachverhalte didaktisch sinnvoll.
- **Der Auditor:** Prüft Antworten auf logische Konsistenz.
- **Der Optimizer:** Komprimiert Wissen für die mobile Darstellung in LernBuddy.

---

## 🏗 Installation (Development)


# Repository klonen
```bash
git clone [https://github.com/ALex83-r0ck/Lead-Dojo.git](https://github.com/ALex83-r0ck/Lead-Dojo.git)
cd Lead-Dojo
```

# Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

# Ollama Modell sicherstellen
```bash
ollama pull llama3
```

## 📈 Roadmap & Vision
[ ] Multi-Modal Support: Integration von Bildanalysen für Lernskripte.

[ ] Advanced Tool-Use: Befähigung der Agenten, Python-Skripte zur Berechnung komplexer Aufgaben auszuführen.

[ ] LernBuddy Sync: Vollständige Synchronisation der Lernfortschritte über die Logic-Engine.

## 🛡 Security & Compliance
Im Rahmen meiner ISC2-Zertifizierung wurde Lead-Dojo nach dem Prinzip des Least Privilege für Datenzugriffe entwickelt. Alle RAG-Abfragen werden validiert, um Prompt-Injection-Risiken zu minimieren.

Kontakt
Entwickelt von Alexander Rothe LinkedIn | Portfolio
