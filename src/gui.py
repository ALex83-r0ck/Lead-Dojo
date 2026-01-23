import streamlit as st #type: ignore
import ollama
import chromadb
import os

# --- KONFIGURATION ---
st.set_page_config(page_title="LernBuddy Lead-Dojo", page_icon="🥋", layout="centered")

# CSS für ein bisschen Dojo-Feeling
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    .stTextInput { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True) # FIX 1: unsafe_allow_html korrekt benannt

st.title("🥋 Lead-Dojo Sensei")
st.subheader("Dein Tutor für verifiziertes Wissen")

# --- DB-VERBINDUNG ---
@st.cache_resource
def get_db_collection():
    # Wir nutzen einen Pfad, der relativ zum Hauptprojektordner 'Lead-Dojo' funktioniert
    # Wenn wir im Container sind, ist das /app/Lead-Dojo/db
    base_path = os.path.dirname(os.path.dirname(__file__)) # Geht von src eine Ebene hoch
    db_path = os.path.join(base_path, "db")
    
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(name="knowledge_dojo")

collection = get_db_collection()

# --- LOGIK ---
def get_ai_response(user_input):
    # 1. Leads suchen mit Fehlerprüfung (FIX 2)
    results = collection.query(query_texts=[user_input], n_results=1)
    
    # Sicherstellen, dass Dokumente gefunden wurden
    documents = results.get('documents')
    if documents and len(documents) > 0 and len(documents[0]) > 0:
        leads = documents[0][0]
    else:
        leads = "Keine spezifischen Leads gefunden."
    
    # 2. Ollama Client Setup
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
    client = ollama.Client(host=OLLAMA_HOST)
    
    prompt = f"""
    DU BIST DER 'LEARNBUDDY-SENSEI'.
    NUTZE DIESE LEADS ALS BASIS: {leads}
    
    REGEL: Erkläre freundlich und pädagogisch. Wenn die Leads nicht zur Frage passen, 
    antworte als Tutor, dass du dazu noch nichts gelernt hast.
    
    FRAGE: {user_input}
    """
    
    try:
        response = client.generate(model='gemma2:2b', prompt=prompt)
        return response['response']
    except Exception as e:
        return f"Sensei hat gerade Meditationspause (Fehler: {str(e)})"

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Was möchtest du heute lernen?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sensei denkt nach..."):
            full_response = get_ai_response(prompt)
            st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})