import streamlit as st
import ollama
import chromadb
import os
import logging
import sys
import json
import base64
import time
from pathlib import Path
from PIL import Image

# --- PFAD-LOGIK ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db"
ICON_PATH = BASE_DIR / "assets" / "icons" / "Sensei_logo1.jpg"
BG_PATH = BASE_DIR / "assets" / "Backgrounds-Dojo" / "temple-6963458_1280.jpg"

# Verzeichnisse sicherstellen
DB_PATH.mkdir(parents=True, exist_ok=True)

# --- LOGGER ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("LeadDojo")

# --- HILFSFUNKTIONEN FÜR DESIGN ---
def get_base64_bin_file(bin_file):
    if not bin_file.exists(): 
        logger.warning(f"Datei nicht gefunden: {bin_file}")
        return ""
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def set_design():
    bin_str = get_base64_bin_file(BG_PATH)
    bg_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
        }}
        [data-testid="stChatMessageContainer"] {{
            background-image: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85));
            backdrop-filter: blur(5px);
            border-radius: 15px;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(21, 34, 43, 0.9);
        }}
        .status-badge {{
            padding: 5px 10px;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            color: white;
        }}
        .status-online {{ background-color: #238636; }}
        .status-offline {{ background-color: #da3633; }}
        </style>
        """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- INGESTION LOGIK ---
def ingest_data(file):
    try:
        data = json.load(file)
        text_snippets = []
        
        # 1. Metadaten (Dojo Infos)
        if "dojo" in data:
            text_snippets.append(f"Dojo: {data['dojo']['name_de']} ({data['dojo']['name_jp']}). Ziel: {data['dojo']['purpose']['de']}")
        
        # 2. Übungen (Exercises)
        if "training_day" in data and "exercises" in data["training_day"]:
            for ex in data["training_day"]["exercises"]:
                snippet = (f"Thema: {ex['name_de']} / {ex['name_jp']} (Typ: {ex['type']}). "
                           f"Anleitung: {ex['instruction_de']}. "
                           f"Sensei-Check: {ex['sensei_check']['de']}")
                text_snippets.append(snippet)
        
        if text_snippets:
            client = chromadb.PersistentClient(path=str(DB_PATH))
            collection = client.get_or_create_collection(name="knowledge_dojo")
            ids = [f"id_{time.time()}_{i}" for i in range(len(text_snippets))]
            collection.add(documents=text_snippets, ids=ids)
            logger.info(f"Erfolgreich {len(text_snippets)} Snippets in {DB_PATH} gespeichert.")
            return True
        return False
    except Exception as e:
        logger.error(f"Ingestion Fehler: {e}")
        return False

# --- UI INITIALISIERUNG ---
logo = Image.open(str(ICON_PATH)) if ICON_PATH.exists() else None
st.set_page_config(page_title="Lead-Dojo Sensei", page_icon=logo, layout="wide")
set_design()

# --- VERBINDUNGS-CHECK ---
def check_connections():
    status = {"ollama": False, "db": False}
    try:
        chromadb.PersistentClient(path=str(DB_PATH)).heartbeat()
        status["db"] = True
    except: pass
    try:
        host = "http://host.docker.internal:11434" if os.getenv("DOCKER_ENV") else "http://localhost:11434"
        ollama.Client(host=host).list()
        status["ollama"] = True
    except: pass
    return status

# --- SIDEBAR ---
with st.sidebar:
    if logo: st.image(logo, use_container_width=True)
    st.title("🥋 Dojo Control")
    conn = check_connections()
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="status-badge {"status-online" if conn["db"] else "status-offline"}">DB: {"ON" if conn["db"] else "OFF"}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="status-badge {"status-online" if conn["ollama"] else "status-offline"}">AI: {"ON" if conn["ollama"] else "OFF"}</div>', unsafe_allow_html=True)
    
    st.divider()
    try:
        host = "http://host.docker.internal:11434" if os.getenv("DOCKER_ENV") else "http://localhost:11434"
        models = [m['name'] for m in ollama.Client(host=host).list()['models']]
        sel_model = st.selectbox("Modell wählen", models, index=0) or "gemma2:2b"
    except: sel_model = "gemma2:2b"
    
    temp = st.slider("Sensei-Schärfe (Temperature)", 0.0, 1.0, 0.3)
    
    st.divider()
    files = st.file_uploader("Training (JSON)", type=['json'], accept_multiple_files=True)
    if files:
        for f in files:
            if ingest_data(f):
                st.success(f"{f.name} absorbiert!")
                st.balloons()

# --- CHAT ---
st.title("🥋 Lead-Dojo Sensei")
st.caption("Verifiziertes Wissen | RAG-Technologie v2.3 | @Alexander Rothe")

if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar=logo if m["role"]=="assistant" else "👤"):
        st.markdown(m["content"])

if prompt := st.chat_input("Frage den Sensei..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar=logo):
        with st.spinner("Sensei meditiert über die Antwort..."):
            try:
                client = chromadb.PersistentClient(path=str(DB_PATH))
                coll = client.get_or_create_collection(name="knowledge_dojo")
                res = coll.query(query_texts=[prompt], n_results=3)
                
                ctx = "\n".join(res['documents'][0]) if res['documents'] else "Kein Dojo-Wissen gefunden."
                
                host = "http://host.docker.internal:11434" if os.getenv("DOCKER_ENV") else "http://localhost:11434"
                client_ai = ollama.Client(host=host)
                
                sys_p = (f"Du bist der Sensei des Urushi Juku. Nutze AUSSCHLIESSLICH diesen Kontext: {ctx}. "
                         f"Antworte weise und präzise. Wenn das Wissen nicht im Kontext steht, "
                         f"sage höflich: 'Dieses Wissen liegt noch außerhalb meines Dojos.'")
                
                resp = client_ai.generate(model=sel_model, prompt=f"{sys_p}\n\nFrage: {prompt}", stream=False)
                ans = resp['response']
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.error(f"Fehler im Dojo: {e}")