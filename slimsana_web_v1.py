import streamlit as st
import uuid
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. FUNÇÃO DE LOG ---
def salvar_log_google(pergunta, resultado):
    try:
        # Tenta conectar usando os Secrets configurados
        conn = st.connection("gsheets", type=GSheetsConnection)
        origem_final = st.session_state.get('origem', 'Direto/Organico')
        
        novo_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Origem": origem_final,
            "Dificuldade": pergunta,
            "Resultado": resultado
        }])
        
        # Lê dados existentes para não sobrescrever
        try:
            dados_atuais = conn.read()
            df_final = pd.concat([dados_atuais, novo_log], ignore_index=True)
        except:
            df_final = novo_log
            
        conn.update(data=df_final)
    except Exception as e:
        # Debug silencioso (não interrompe a experiência do usuário)
        print(f"Erro de Log: {e}")

# --- 2. CONFIGURAÇÕES ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

if 'origem' not in st.session_state:
    # Captura parâmetros da URL (utm_content)
    st.session_state.origem = st.query_params.get("utm_content", "FacebookAds_DE_AT")

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- 3. CSS ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        border: 2px solid black !important;
        border-radius: 10px;
        font-weight: 800 !important;
        font-size: 1.3em !important;
        height: 4.5em;
        text-shadow: 1px 1px 2px black;
    }
    .main-title { color: #1e3a5f; text-align: center; font-size: 2.2em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Teste: Por que seu corpo "trava" após os 30?</h1>', unsafe_allow_html=True)
    st.write("---")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    if st.button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA"):
        # LOG DE ENTRADA: Registra que alguém clicou no anúncio e entrou no site
        salvar_log_google("SISTEMA", "ENTROU_NA_HOME")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUIZ ---
elif st.session_state.pagina == 'quiz':
    st.subheader("📋 Persönliche Angaben")
    with st.form("quiz_form"):
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", ["Bauchfett verlieren", "Mehr Energie", "Heißhunger stoppen", "Stoffwechsel"])
        q5 = st.slider("5. Wie alt sind Sie?", 18, 80, 43)
        if st.form_submit_button("ANALYSE STARTEN"):
            st.session_state.q1 = q1
            st.session_state.q5 = q5
            st.session_state.pagina = 'resultado'
            st.rerun()

# --- TELA 3: RESULTADO ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung...", expanded=True) as status:
        time.sleep(2)
        status.update(label="Analyse Abgeschlossen!", state="complete")

    # LOG FINAL: Registra que o usuário completou o funil
    salvar_log_google(st.session_state.q1, f"Idade: {st.session_state.q5} | FINALIZOU")
    
    st.balloons()
    st.success("✅ ANÁLISE CONCLUÍDA!")
    st.link_button("🔥 ACESSAR PROTOCOLO SLIMSANA AGORA", LINK_AFILIADO)
