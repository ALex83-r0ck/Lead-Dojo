# Die Architektur: Das "Lead-Dojo" System

Diese Architektur trennt die Intuition (das LLM) von der Logik (der Lead-Datenbank).

1. Die Ingestion-Pipeline (Der Lehrer)

- Hier werden deine "Obst", "Tier" oder "Python" Daten in das System geladen.

--> Komponenten:

- Ein Scraper (BeautifulSoup) und ein Lead-Generator (ein kleines lokales Modell, das nur JSON extrahiert).

Warum dieser Weg?
Das Modell wird nicht neu trainiert. Wir bauen eine externe "Bibliothek". Das ist schneller, kostengünstiger und man hat 100% Kontrolle über die Fakten. Wenn doch mal ein Fakt falsch ist, änderst man nur eine Zeile in der DB, statt das Modell 10 Stunden lang neu zu trainieren.
2. Der Knowledge-Store (Die Bibliothek)
Wir nutzen ChromaDB als Vektordatenbank.
Was wird gespeichert? Wir speichern nicht nur Text, sondern strukturierte Lead-Objekte (JSON).
Warum dieser Weg? Normale Datenbanken suchen nach Worten. Eine Vektordatenbank sucht nach Bedeutung. Wenn man nach "Südfrucht" sucht, findet es die "Banane", auch wenn das Wort "Südfrucht" nicht im Text steht.
3. Der Hybrid-Inference-Engine (Der Kampfplatz)
Das ist das Herzstück des Dojos. Es besteht aus drei Phasen:

- Phase A (System 1): Das LLM (Gemma) generiert eine schnelle Antwort.
- Phase B (Sensei-Check): Ein Python-Skript extrahiert die Kernpunkte der Antwort und gleicht sie mit den Leads in der ChromaDB ab.
- Phase C (Feedback-Loop): Wenn der Sensei einen Widerspruch findet (z.B. LLM sagt "Ein Apfel ist ein Gemüse", Lead sagt "Obst"), wird die Antwort blockiert. Das LLM bekommt einen "Klaps" und muss korrigieren.

Warum diese Architektur und nicht anders?
Es gibt zwei andere Wege, die ich bewusst nicht gehe:

| Ansatz                 | Warum wir ihn NICHT wählen                                                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Nur Prompt Engineering | Zu unzuverlässig. Die KI "vergisst" die Regeln oft nach ein paar Sätzen (Context Drift)                                           |
| Full Fine-Tuning       | Zu teuer und starr. Wenn man der KI etwas Neues beibringen will, muss man den ganzen Prozess von vorne starten. Außerdem löst es das Halluzinationsproblem nicht wirklich. |

Der Lead-Dojo-Weg ist die "Goldene Mitte":
Modular: Du kannst "Obst" einfach gegen "Medizin" austauschen.
Transparent: Du kannst genau sehen, warum der Sensei eine Antwort abgelehnt hat.
Hardware-schonend: Es läuft auf so gut wie jedem PC, weil keine Milliarden Parameter neu berechnet werden müssen.
