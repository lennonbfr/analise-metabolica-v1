import streamlit as st
import uuid
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURAÇÃO DE LOG ---
def salvar_log_google(pergunta, resultado):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        novo_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Origem": "FacebookAds_DE_AT",
            "Dificuldade": pergunta,
            "Resultado": resultado
        }])
        try:
            dados_atuais = conn.read()
            df_final = pd.concat([dados_atuais, novo_log], ignore_index=True)
        except:
            df_final = novo_log
        conn.update(data=df_final)
    except Exception as e:
        print(f"Erro de Log: {e}")

# --- 2. CONFIGURAÇÕES E ESTADO DO APP ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- 3. ESTILIZAÇÃO CSS (VERDE, PRETO E CORES SUAVES) ---
st.markdown("""
    <style>
    /* Botão da Home (Verde e Preto) */
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: black !important;
        border: 2px solid black !important;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.2em;
        height: 4em;
    }
    /* Estilo Suave para o Questionário */
    .quiz-container {
        background-color: #f0f8ff; /* Azul suave */
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #d1e2ff;
    }
    .main-title { color: #1e3a5f; text-align: center; font-size: 2em; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME (CAPA COM IMAGEM) ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Teste: Por que seu corpo "trava" após os 30?</h1>', unsafe_allow_html=True)
    st.write("---")
    
    # Imagem da Maçã/Saúde que gera confiança
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    st.info("Descubra por que dietas comuns não funcionam para o seu perfil genético.")
    
    if st.button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA"):
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO (ESTILIZADO) ---
elif st.session_state.pagina == 'quiz':
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.subheader("📋 Persönliche Angaben (Sua Análise)")
    
    with st.form("quiz_form"):
        st.markdown("**Por favor, responda com sinceridade para um resultado preciso:**")
        
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                         ["Bauchfett verlieren", "Mehr Energie", "Heißhunger stoppen", "Stoffwechsel beschleunigen"])
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                     ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf"])
        q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", 
                         ["Vormittags", "Nachmittags", "Abends/Nachts"])
        q4 = st.radio("4. Fühlen Sie sich oft aufgebläht?", ["Ja, fast täglich", "Manchmal", "Selten"])
        q5 = st.slider("5. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ANALYSE STARTEN"):
            st.session_state.q1 = q1
            st.session_state.q2 = q2
            st.session_state.q5 = q5
            st.session_state.pagina = 'resultado'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TELA 3: RESULTADO ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung...", expanded=False):
        time.sleep(2)
    
    salvar_log_google(st.session_state.q1, f"Idade: {st.session_state.q5} | Sono: {st.session_state.q2}")
    
    st.balloons()
    st.success("✅ ANÁLISE CONCLUÍDA!")
    
    st.markdown(f"""
    ### Ihr Ergebnis: **Stoffwechsel-Blockade Typ 3**
    Lennon, basierend auf Ihrem Alter ({st.session_state.q5}) e no seu sono **{st.session_state.q2.lower()}**, 
    detectamos um 'Zell-Stau' que impede a queima de gordura.
    """)
    
    st.link_button("🔥 ACESSAR PROTOCOLO SLIMSANA", LINK_AFILIADO)
