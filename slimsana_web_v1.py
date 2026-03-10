import streamlit as st
import uuid
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURAÇÃO DE LOG (GOOGLE SHEETS) ---
def salvar_log_google(pergunta, resultado):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Recupera a origem salva na sessão (ou usa o padrão se não existir)
        origem_final = st.session_state.get('origem', 'FacebookAds_DE_AT')
        
        novo_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Origem": origem_final,
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

# Lógica de Captura de UTM (Origem do Anúncio)
if 'origem' not in st.session_state:
    # Captura o parâmetro 'utm_content' da URL
    params = st.query_params
    st.session_state.origem = params.get("utm_content", "FacebookAds_DE_AT")

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- 3. ESTILIZAÇÃO CSS (FOCO EM CONVERSÃO) ---
st.markdown("""
    <style>
    /* Botão da Home: Verde, Borda Preta, Texto Branco e Negrito Extra */
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
    
    /* Container Suave para o Questionário */
    .quiz-container {
        background-color: #f0f8ff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #d1e2ff;
        margin-bottom: 20px;
    }
    
    .main-title { color: #1e3a5f; text-align: center; font-size: 2.2em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME (ENTRADA) ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Teste: Por que seu corpo "trava" após os 30?</h1>', unsafe_allow_html=True)
    st.write("---")
    
    # Imagem intuitiva (Maçã)
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    st.info("Descubra por que dietas comuns não funcionam para o seu perfil genético.")
    
    if st.button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA"):
        # ÚNICA INCLUSÃO: Registra que o usuário entrou no funil
        salvar_log_google("SISTEMA", "ENTROU_NA_HOME")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO (ESTILIZADO) ---
elif st.session_state.pagina == 'quiz':
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.subheader("📋 Persönliche Angaben")
    
    with st.form("quiz_form"):
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                          ["Bauchfett verlieren (hartnäckig)", "Mehr Energie im Alltag", "Heißhungerattacken stoppen", "Stoffwechsel beschleunigen"])
        
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                      ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf, mas nenhuma energia"])
        
        q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", 
                          ["Vormittags", "Nachmittags (Stress)", "Abends/Nachts"])
        
        q4 = st.radio("4. Fühlen Sie sich nach dem Essen oft aufgebläht?", 
                      ["Ja, quase todos os dias", "Manchmal", "Raramente"])
        
        q5 = st.slider("5. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ANALYSE STARTEN"):
            st.session_state.q1 = q1
            st.session_state.q2 = q2
            st.session_state.q5 = q5
            st.session_state.pagina = 'resultado'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TELA 3: RESULTADO (FINAL) ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung der Bio-Indikatoren...", expanded=True) as status:
        st.write("🧬 Analysiere Zell-Marker...")
        time.sleep(1.5)
        st.write("🔍 Suche nach Blockaden...")
        time.sleep(1.5)
        status.update(label="Analyse Abgeschlossen!", state="complete", expanded=False)

    # Registro de Log - Agora com a Origem Dinâmica
    salvar_log_google(st.session_state.q1, f"Idade: {st.session_state.q5} | Sono: {st.session_state.q2}")
    
    st.balloons()
    st.success("✅ ANÁLISE CONCLUÍDA!")
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee;">
    <h3>Ihr Ergebnis: <b>Stoffwechsel-Blockade Typ 3</b></h3>
    <p>Lennon, basierend auf Ihrem Alter ({st.session_state.q5}) und Ihrem Ziel (<b>{st.session_state.q1}</b>), 
    identificamos um desajuste enzimático causado por sono <b>{st.session_state.q2.lower()}</b>.</p>
    <p>O protocolo SlimSana foi identificado como 98% compatível com seu perfil.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("🔥 ACESSAR PROTOCOLO SLIMSANA AGORA", LINK_AFILIADO)
