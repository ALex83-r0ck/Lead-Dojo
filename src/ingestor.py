#  Lead-Dojo/src/ingestor.py (#type: ignore == mypy und pylance fehlern obwohl vorhanden!)
import chromadb #type: ignore
import json
import os

# 1. Das setup der DB (lokal im Ordner ./db gespeichert)
client = chromadb.PersistentClient(path="./db") 
collection = client.get_or_create_collection(name="knowledge_dojo")

def import_knowledge_from_json(file_path):
    """Fügt Hinweise aus einer Json Datei hinzu"""
    # überprüfung ob Date oder Dateipath existiert
    if not os.path.exists(file_path):
        print(f"❌ Fehler: Datei {file_path} nicht gefunden!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        e_id = entry['id']
        e_name = entry['name'] 
        e_leads = entry['leads'] 

        # kategorien automatisch aus der ID ableiten (z.b. 'obst' aus 'obst_001')
        category = e_id.split('_')[0] if '_' in e_id else "gerneral"

        # hinweise zu einem textblock zusammenfügen
        lead_text = f"{e_name}: " + ", ".join(e_leads)  

        # 'upsert' worde an statt 'add' gewählt um errors bei doppelten 'IDs' zu verhindern
        collection.upsert(
            documents=[lead_text],
            metadatas=[{
                "name": e_name, 
                "category": category,
                "type": "lead_card"
                }],
            ids=[e_id]
        )
        print(f"✅ Ingestriert: {e_name} [{e_id}] in Kategorie: {category}")

def delete_lead(element_id):
    """Option zum löschen nicht mehr benötigter Einträge aus der DB"""
    collection.delete(ids=[element_id])
    print(f"🪣 Lead {element_id} wurde erfolgreich entfernt.")

# --- Test-Lauf ---
if __name__ == "__main__":
    # pfad zur json 
    json_path = "Lead-Dojo/data/leads.json"
    import_knowledge_from_json(json_path)
    print("\n---- Dojo-Update abgeschlossen! ---")