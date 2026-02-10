# src/trainer.py
import json
import ollama
import os
import time
from datetime import datetime

# Pfad zu denn Json-Datein
TEST_DATA = "data/test_data.json"
PROGRESS_FILE = "data/progress.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def run_training():
    questions = load_json(TEST_DATA)
    progress = load_json(PROGRESS_FILE)
    
    if not questions:
        print("Keine Trainingsdaten gefunden.")
        return
    
    print(f"--- Willkommen zum Lead-Dojo Training! ---\n")
    print(f"Dein aktueller Gürtel: {progress.get('level', 'Weißer Gürtel')}")

    for topic, content in questions.items():
        # Falls deine test.json anders strukturiert ist, passen wir das hier an
        question = content.get("frage") 
        print(f"\nPRÜFUNG: {topic}\nFrage: {question}")
        
        # STOPPUHR START
        start_time = time.time()
        
        response = ollama.chat(model='gemma2:2b', messages=[
            {'role': 'system', 'content': 'Du bist ein technischer Mentor für RAG-Systeme. Antworte präzise und fachlich korrekt.'},
            {'role': 'user', 'content': question},
        ])
        
        # STOPPUHR STOPP
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        ki_antwort = response['message']['content']
        print(f"\n--- SENSEI ANTWORT ({duration} Sek.) ---\n{ki_antwort}\n----------------------")
        
        score = input(f"\nBewertung (0-10) für {topic}: ")
        comment = input("Feedback: ")
        
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": topic,
            "score": int(score),
            "duration_sec": duration, # <--- Zeit wird gespeichert
            "feedback": comment
        }
        
        if "history" not in progress: progress["history"] = []
        progress["history"].append(entry)
        progress["completed_katas"] = progress.get("completed_katas", 0) + 1
        
        save_json(PROGRESS_FILE, progress)
        print(f"✅ Gespeichert. Latenz: {duration}s")
        
        if input("Nächste Frage? (j/n): ") != 'j': break

if __name__ == "__main__":
    run_training()