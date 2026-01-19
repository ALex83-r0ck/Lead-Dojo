#  Lead-Dojo/src/ingestor.py (#type: ignore == mypy und pylance fehlern obwohl vorhanden!)
import chromadb #type: ignore
from chromadb.utils import embedding_functions

# 1. Das setup der DB (lokal im Ordner ./db gespeichert)
client = chromadb.PersistentClient(path="./db")

# 2. Hier erstelle ich eine "Collection" (wie einen Table in einer DB)
# mit dem Namen 'knowledge_dojo'
collection = client.get_or_create_collection(name="knowledge_dojo")

def add_lead(element_id, element_name, leads_list):
    """Fügt einen neuen Wissens-Baustein (Lead dt. Hinweis) der DB hinzu"""

    # Hier werden die "Hinweise" zu einem Text zusammengefügt, damit die DB diese auch verstehen kann
    lead_text = f"{element_name}: " + ", ".join(leads_list)

    collection.add(
        documents=[lead_text],
        metadatas=[{"name": element_name, "type": "lead_card"}],
        ids=[element_id]
    )
    print(f"✅ Lead für '{element_name}' erfolgreich gespeichert!")

# --- Test-Lauf ---
if __name__ == "__main__":
    # Testdaten der 'Gold-Lead' wird hier eingefügt
    add_lead(
        element_id="obst_001",
        element_name="Apfel",
        leads_list=["Kernobst", "wächst an Bäumen", "essbare Schale", "festes Fruchtfleisch"]
    )