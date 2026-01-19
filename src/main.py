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
        Du bist ein hilfreicher Assistent im Lead-Dojo.
        Nutze die folgenden verifizierten LEADS, um die Frage des Nutzers zu beantworten.
        Wenn die LEADS nicht zur Frage passen, sage das höflich.

        VERIFIZIERTE LEADS:
        {leads}

        NUTZERFRAGE:
        {user_input}
        """
        
        response = ollama.generate(model='gemma2:2b', prompt=prompt)
        
        print(f"\nSensei-Gemma: {response['response']}")

if __name__ == "__main__":
    hybrid_chat()