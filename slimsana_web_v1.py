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
        
        # Recupera a origem salva na sessão
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

if 'origem' not in st.session_state:
    params = st.query_params
    st.session_state.origem = params.get("utm_content", "FacebookAds_DE_AT")

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- 3. ESTILIZAÇÃO CSS ---
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

# --- TELA 1: HOME ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Teste: Por que seu corpo "trava" após os 30?</h1>', unsafe_allow_html=True)
    st.write("---")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    st.info("Descubra por que dietas comuns não funcionam para o seu perfil genético.")
    
    if st.button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA"):
        salvar_log_google("SISTEMA", "ENTROU_NA_HOME")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO (COM NOVOS CAMPOS) ---
elif st.session_state.pagina == 'quiz':
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.subheader("📋 Persönliche Angaben")
    
    with st.form("quiz_form"):
        # Novos campos solicitados para credibilidade
        nome_input = st.text_input("Vollständiger Name (Nome Completo)")
        c1, c2 = st.columns(2)
        with c1:
            peso_input = st.number_input("Gewicht (Peso em kg)", min_value=40.0, max_value=200.0, value=75.0, step=0.1)
        with c2:
            altura_input = st.number_input("Größe (Altura em cm)", min_value=120, max_value=220, value=170, step=1)
        
        st.write("---")
        
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                          ["Bauchfett verlieren (hartnäckig)", "Mehr Energie im Alltag", "Heißhungerattacken stoppen", "Stoffwechsel beschleunigen"])
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                      ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf, aber keine Energie"])
        q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", 
                          ["Vormittags", "Nachmittags (Stress)", "Abends/Nachts"])
        q4 = st.radio("4. Fühlen Sie sich nach dem Essen oft aufgebläht?", 
                      ["Ja, quase todos os dias", "Manchmal", "Raramente"])
        q5 = st.slider("5. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ANALYSE STARTEN"):
            # Salva os novos dados na sessão
            st.session_state.nome_usuario = nome_input if nome_input else "Besucher"
            st.session_state.peso_usuario = peso_input
            st.session_state.altura_usuario = altura_input
            
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

    # Log com o novo formato de nome
    salvar_log_google("FINALIZOU", f"Nome: {st.session_state.nome_usuario} | Peso: {st.session_state.peso_usuario}kg | Alt: {st.session_state.altura_usuario}cm")
    
    st.balloons()
    st.success("✅ ANÁLISE CONCLUÍDA!")
    
    # Quadrante de resultado com correção de cor e personalização
    st.markdown(f"""
    <div style="background-color: white; padding: 25px; border-radius: 10px; border: 1px solid #eee; color: #1e3a5f;">
    <h3 style="color: #1e3a5f; margin-top: 0;">Ihr Ergebnis: <b>Stoffwechsel-Blockade Typ 3</b></h3>
    <p style="color: #1e3a5f;">Hallo <b>{st.session_state.nome_usuario}</b>, basierend auf Ihrem Alter ({st.session_state.q5}), 
    Ihrem Gewicht ({st.session_state.peso_usuario} kg) und Ihrer Größe ({st.session_state.altura_usuario} cm), 
    haben wir ein enzymatisches Ungleichgewicht festgestellt, das durch <b>{st.session_state.q2.lower()}</b> Schlaf verursacht wird.</p>
    <p style="color: #1e3a5f;">Das SlimSana-Protokoll wurde als 98% kompatibel mit Ihrem Profil identifiziert.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("🔥 ACESSAR PROTOCOLO SLIMSANA AGORA", LINK_AFILIADO)
