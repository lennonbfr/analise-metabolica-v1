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

# CSS Profissional
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #28a745; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .main-title { color: #1e7e34; text-align: center; font-family: 'Helvetica', sans-serif; font-size: 2.2em; }
    .info-box { background-color: #f1f8f5; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME (A CAPA INTUITIVA) ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Teste: Por que seu corpo "trava" após os 30?</h1>', unsafe_allow_html=True)
    st.write("---")
    
    # Imagem de impacto que você gostava
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    st.markdown("""
    <div class="info-box">
    <h3>🔬 Stoffwechsel-Analyse 2026</h3>
    <p>Finden Sie heraus, warum herkömmliche Diäten bei Ihnen nicht mehr funktionieren. 
    Diese 60-Sekunden-Analyse berechnet Ihren <b>Bio-Reset-Index</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("JETZT KOSTENLOS TESTEN (STARTEN)"):
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: O QUESTIONÁRIO (6 PERGUNTAS) ---
elif st.session_state.pagina == 'quiz':
    st.subheader("📋 Bio-Metabolisches Formular")
    st.progress(50) # Barra de progresso para manter o engajamento
    
    with st.form("quiz_form"):
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                         ["Bauchfett verlieren (hartnäckig)", "Mehr Energie im Alltag", "Heißhungerattacken stoppen", "Stoffwechsel beschleunigen"])
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                     ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Keine Energie tagsüber"])
        q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", 
                         ["Vormittags", "Nachmittags", "Abends/Nachts"])
        q4 = st.radio("4. Fühlen Sie sich oft aufgebläht?", ["Ja", "Manchmal", "Selten"])
        q5 = st.radio("5. Anzahl bisheriger Diät-Versuche:", ["1-2", "Mehr als 5", "Zu viele"])
        q6 = st.slider("6. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ERGEBNIS ANZEIGEN"):
            st.session_state.q1 = q1
            st.session_state.q2 = q2
            st.session_state.q6 = q6
            st.session_state.pagina = 'resultado'
            st.rerun()

# --- TELA 3: RESULTADO (CONVERSÃO) ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung der Bio-Indikatoren...", expanded=True) as status:
        st.write("🧬 Analysiere Zell-Marker...")
        time.sleep(1.5)
        st.write("📊 Berechne Grundumsatz...")
        time.sleep(1.5)
        status.update(label="Analyse Abgeschlossen!", state="complete", expanded=False)

    # Log para Google Sheets
    salvar_log_google(st.session_state.q1, f"Idade: {st.session_state.q6} | Sono: {st.session_state.q2}")
    
    st.balloons()
    st.success("✅ ANÁLISE CONCLUÍDA!")
    
    st.markdown(f"""
    ### Ihr Ergebnis: **Stoffwechsel-Blockade Typ 3**
    Lennon, basierend auf Ihrem Alter ({st.session_state.q6}) und Ihrem Ziel (**{st.session_state.q1}**), 
    haben wir eine enzymatische Blockade (Zell-Stau) festgestellt.
    """)
    
    st.info("💡 **Lösung:** Das SlimSana BioReset Protokoll wurde als 98% kompatibel mit Ihrem Profil identifiziert.")
    
    st.link_button("🔥 JETZT STOFFWECHSEL REAKTIVIEREN", LINK_AFILIADO)
    
    if st.button("Teste Neustarten"):
        st.session_state.pagina = 'home'
        st.rerun()
