# src/progress_manager.py
import json
import os

PROGRESS_FILE = "data/progress.json"

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {"level": "Weißer Gürtel", "completed_katas": 0, "history": []}
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def update_progress(topic, score):
    progress = load_progress()
    progress["completed_katas"] += 1
    progress["history"].append({"topic": topic, "score": score})
    # Gürtel-Upgrade Logik (vereinfacht)
    if progress["completed_katas"] >= 10: progress["level"] = "Gelber Gürtel"
    if progress["completed_katas"] >= 20: progress["level"] = "Oranger Gürtel"
    if progress["completed_katas"] >= 30: progress["level"] = "Grüner Gürtel"
    if progress["completed_katas"] >= 40: progress["level"] = "Blauer Gürtel"
    if progress["completed_katas"] >= 50: progress["level"] = "Brauner Gürtel"
    if progress["completed_katas"] >= 60: progress["level"] = "Schwarzgürtel"

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=4)