# Lead-Dojo/src/sensei.py (#type: ignore wegen mypy und Pylance fehlerhaften error wurf)
import chromadb #type: ignore

# 1. herstellung einer verbindung zur aktuellen Datenbank
client = chromadb.PersistentClient(path="./db") 

#2. Laden der Collection, die zuvor im ingestor.py erstellt wurde
collection = client.get_collection(name="knowledge_dojo")  

def frage_den_sensei(frage_text):
    # gesucht wird die Top 1 der passenden Ergebnisse
    results = collection.query(
        query_texts=[frage_text],
        n_results=1
    )
    # hinweise werden zurück gegeben
    if results["documents"][0]:
        return results["documents"][0][0]
    else:
        return "Keine passenden Hinweise (leads) gefunden."
    
#--- Test-Abfrage ---
if __name__ == "__main__":
    test_frage = "Was weißt du über Kernobst, das auf Bäumen wächst?"
    antwort = frage_den_sensei(test_frage)

    print(f"Frage: {test_frage}")
    print(f"Gefundene Leads im Dojo: {antwort}")