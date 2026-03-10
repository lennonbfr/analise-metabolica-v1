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

# --- 2. CONFIGURAÇÕES ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

if 'origem' not in st.session_state:
    params = st.query_params
    st.session_state.origem = params.get("utm_content", "FacebookAds_DE_AT")

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
    .quiz-container { background-color: #f0f8ff; padding: 30px; border-radius: 15px; border: 1px solid #d1e2ff; }
    .main-title { color: #1e3a5f; text-align: center; font-size: 2.2em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME (CORRIGIDA PARA ALEMÃO) ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Test: Warum Ihr Körper nach dem 30. Lebensjahr "blockiert"?</h1>', unsafe_allow_html=True)
    st.write("---")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    st.info("Finden Sie heraus, warum herkömmliche Diäten nicht für Ihr genetisches Profil funktionieren.")
    
    if st.button("🔥 MEINEN STOFFWECHSEL JETZT FREISCHALTEN"):
        salvar_log_google("SYSTEM", "HOME_BETRETEN")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO (ALEMÃO) ---
elif st.session_state.pagina == 'quiz':
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    st.subheader("📋 Persönliche Angaben")
    
    with st.form("quiz_form"):
        nome_input = st.text_input("Vollständiger Name")
        c1, c2 = st.columns(2)
        with c1:
            peso_input = st.number_input("Gewicht (kg)", min_value=40.0, max_value=200.0, value=75.0, step=0.1)
        with c2:
            altura_input = st.number_input("Größe (cm)", min_value=120, max_value=220, value=170, step=1)
        
        st.write("---")
        
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                          ["Bauchfett verlieren", "Mehr Energie im Alltag", "Heißhungerattacken stoppen", "Stoffwechsel beschleunigen"])
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                      ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf, aber keine Energie"])
        q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", 
                          ["Vormittags", "Nachmittags (Stress)", "Abends/Nachts"])
        q4 = st.radio("4. Fühlen Sie sich nach dem Essen oft aufgebläht?", 
                      ["Ja, fast jeden Tag", "Manchmal", "Selten"])
    
        q5 = st.slider("5. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ANALYSE STARTEN"):
            st.session_state.nome_usuario = nome_input if nome_input else "Besucher"
            st.session_state.peso_usuario = peso_input
            st.session_state.altura_usuario = altura_input
            st.session_state.q1 = q1
            st.session_state.q2 = q2
            st.session_state.q5 = q5
            st.session_state.pagina = 'resultado'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TELA 3: RESULTADO (ALEMÃO) ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung der Bio-Indikatoren...", expanded=True) as status:
        st.write("🧬 Zell-Marker werden analysiert...")
        time.sleep(1.5)
        st.write("🔍 Suche nach Blockaden...")
        time.sleep(1.5)
        status.update(label="Analyse Abgeschlossen!", state="complete", expanded=False)

    salvar_log_google("ABGESCHLOSSEN", f"Name: {st.session_state.nome_usuario} | {st.session_state.peso_usuario}kg | {st.session_state.altura_usuario}cm")
    
    st.balloons()
    st.success("✅ ANALYSE ABGESCHLOSSEN!")
    
    st.markdown(f"""
    <div style="background-color: white; padding: 25px; border-radius: 10px; border: 1px solid #eee; color: #1e3a5f;">
    <h3 style="color: #1e3a5f; margin-top: 0;">Ihr Ergebnis: <b>Stoffwechsel-Blockade Typ 3</b></h3>
    <p style="color: #1e3a5f;">Hallo <b>{st.session_state.nome_usuario}</b>, basierend auf Ihrem Alter ({st.session_state.q5}), 
    Ihrem Gewicht ({st.session_state.peso_usuario} kg) und Ihrer Größe ({st.session_state.altura_usuario} cm), 
    haben wir ein enzymatisches Ungleichgewicht festgestellt, das durch <b>{st.session_state.q2.lower()}</b> Schlaf verursacht wird.</p>
    <p style="color: #1e3a5f;">Das SlimSana-Protokoll wurde zu 98% als kompatibel mit Ihrem Profil eingestuft.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("🔥 JETZT ZUM SLIMSANA-PROTOKOLL", LINK_AFILIADO)
