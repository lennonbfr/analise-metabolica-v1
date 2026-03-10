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

# --- 2. CONFIGURAÇÕES GERAIS ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

st.set_page_config(page_title="BioReset - Stoffwechsel Analyse", page_icon="🧪")

# CSS para deixar o visual mais "Clínico/Clean"
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #0056b3; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .result-box { background-color: #f8f9fa; border: 2px solid #dee2e6; padding: 20px; border-radius: 10px; }
    h1 { color: #0056b3; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🔬 Stoffwechsel-Check (BioReset)")
st.write("---")
st.warning("⚠️ **Wichtig:** Diese Analyse ist für Personen über 35 Jahre optimiert.")

# --- O NOVO QUIZ (6 PERGUNTAS) ---
with st.form("quiz_form"):
    st.subheader("Persönliche Angaben")
    
    q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                     ["Bauchfett verlieren (hartnäckig)", "Mehr Energie im Alltag", "Heißhungerattacken stoppen", "Stoffwechsel beschleunigen"])
    
    q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                 ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf, aber keine Energie tagsüber"])
    
    q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", 
                     ["Vormittags", "Nachmittags (Stress-Peak)", "Abends/Nachts"])
    
    q4 = st.radio("4. Fühlen Sie sich nach dem Essen oft aufgebläht?", 
                 ["Ja, fast täglich", "Manchmal", "Selten"])
    
    q5 = st.radio("5. Wie viele Diät-Versuche haben Sie bereits hinter sich?", 
                 ["1-2 Versuche", "Mehr als 5", "Ich habe aufgehört zu zählen"])
    
    q6 = st.slider("6. Wie alt sind Sie?", 18, 80, 43)

    submit_button = st.form_submit_button("ANALYSE STARTEN")

# --- LÓGICA DE RESULTADO ---
if submit_button:
    # Simulação de processamento pesado (Efeito N2 de autoridade)
    with st.status("Verarbeitung der Bio-Indikatoren...", expanded=True) as status:
        st.write("🧬 Analysiere Insulinresistenz-Marker...")
        time.sleep(1.2)
        st.write("📊 Berechne Grundumsatz für das Alter...")
        time.sleep(1.0)
        st.write("🔍 Suche nach enzymatischen Blockaden...")
        time.sleep(1.5)
        status.update(label="Analyse Abgeschlossen!", state="complete", expanded=False)

    # Disparo de Log
    log_info = f"Ziel: {q1} | Schlaf: {q2} | Alter: {q6}"
    salvar_log_google(q1, log_info)
    
    st.balloons()

    # --- BOX DE RESULTADO ---
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.header("✅ Ergebnis: Stoffwechsel-Blockade Typ 3")
    
    st.write(f"""
    Lennon, basierend auf Ihrem Alter ({q6} Jahre) und Ihrem Hauptproblem (**{q1}**), 
    hat unser System eine **enzymatische Blockade** festgestellt. 
    
    Wenn der Schlaf **{q2.lower()}** ist, produziert der Körper vermehrt Cortisol, 
    was die Fettverbrennung blockiert – egal wie wenig Sie essen.
    """)
    
    st.error("🚨 **Warnung:** Herkömmliche Diäten werden bei diesem Profil nicht funktionieren.")
    
    st.divider()
    st.subheader("Die Lösung: SlimSana BioReset")
    st.write("Die deutsche SlimSana-Formel wurde entwickelt, um genau diese enzymatischen Schalter umzulegen.")
    
    st.link_button("🔥 JETZT STOFFWECHSEL REAKTIVIEREN", LINK_AFILIADO)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.caption(f"LTA-Tracking-ID: {str(uuid.uuid4())[:8]}")
