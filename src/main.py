# Lead-Dojo/src/main.py (#type: ignore)
import chromadb
import ollama

# 1. Verbindungs setup
client = chromadb.PersistentClient(path="./db")
collection = client.get_collection(name="knowledge_dojo")

def hole_leads(frage):
    results = collection.query(query_texts=[frage], n_results=1)
    documents = results.get('documents')

    if documents is not None and len(documents) > 0:
        first_result_list = documents[0]

        if first_result_list is not None and len(first_result_list) > 0:
            return first_result_list[0]
        
    return "Keine Hinweise auffindbar!"

def hybrid_chat():
    print("🥋 Willkommen im Lead-Dojo! (Schreibe 'exit' zum Beenden)")
    
    while True:
        user_input = input("\nDu: ")
        if user_input.lower() == 'exit':
            break
        
        # --- SYSTEM 2: LEADS HOLEN ---
        leads = hole_leads(user_input)
        
        # --- SYSTEM 1: GEMMA MIT LEADS FÜTTERN (PROMPT ENHANCEMENT) ---
        prompt = f"""
            DU BIST DER 'LEARNBUDDY-SENSEI', EIN FREUNDLICHER UND KOMPETENTER TUTOR.

            DEINE AUFGABE:
            Erkläre dem Schüler das Thema basierend auf den unten stehenden LEADS. 
            Verwende eine pädagogische, ermutigende Sprache. 

            DEINE QUELLE (LEADS):
            {leads}

            REGELN:
            1. Sei erklärend und freundlich, nicht nur eine Liste von Fakten.
            2. Wenn du keine passenden LEADS hast, antworte als freundlicher Tutor: 
            "Das ist eine spannende Frage! Leider habe ich dazu in meinem aktuellen Dojo-Wissen noch keine Details. Sollen wir uns gemeinsam ein anderes Thema anschauen?"
            3. Wenn der User 'Danke' sagt oder grüßt, antworte höflich und bleib in deiner Rolle als Sensei.

            NUTZERFRAGE:
            {user_input}
            """
        
        response = ollama.generate(
            model='gemma2:2b', 
            prompt=prompt,
            options={
                'temperature': 0.5,
                'top_p': 0.9
            }
        )
        
        print(f"\nSensei-Gemma: {response['response']}")

if __name__ == "__main__":
    hybrid_chat()