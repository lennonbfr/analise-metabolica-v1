import streamlit as st
import uuid
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURAÇÃO DE LOG (COMPLETA E SILENCIOSA) ---
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
            # Tenta ler a aba Página1. TTL omitido para evitar cache no log.
            dados_atuais = conn.read(worksheet="Página1")
            df_final = pd.concat([dados_atuais, novo_log], ignore_index=True)
        except:
            df_final = novo_log
            
        conn.update(worksheet="Página1", data=df_final)
    except Exception as e:
        # Erro invisível para o cliente no front-end
        print(f"Log Error: {e}")

# --- 2. CONFIGURAÇÕES ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

if 'origem' not in st.session_state:
    params = st.query_params
    st.session_state.origem = params.get("utm_content", "FacebookAds_DE_AT")

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- 3. CSS (RESTAURADO E AMPLIADO) ---
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
        background-color: rgba(255, 255, 255, 0.05); 
        padding: 30px; 
        border-radius: 15px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
    }
    .main-title { color: #f8fafc; text-align: center; font-size: 2.2em; font-weight: bold; }
    
    /* Garante visibilidade dos inputs no fundo escuro */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        color: #1e293b !important;
        background-color: white !important;
    }
    label { color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME ---
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">🍎 Test: Warum Ihr Körper nach dem 30. Lebensjahr "blockiert"?</h1>', unsafe_allow_html=True)
    st.write("---")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    st.info("Finden Sie heraus, warum herkömmliche Diäten nicht für Ihr genetisches Profil funktionieren.")
    
    if st.button("🔥 MEINEN STOFFWECHSEL JETZT FREISCHALTEN"):
        salvar_log_google("SYSTEM", "HOME_BETRETEN")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO (TODAS AS PERGUNTAS RESTAURADAS) ---
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
                      ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf, mas keine Energie"])
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
            st.session_state.q3 = q3
            st.session_state.q4 = q4
            st.session_state.q5 = q5
            st.session_state.pagina = 'resultado'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TELA 3: RESULTADO (VISUAL PREMIUM CORRIGIDO) ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung der Bio-Indikatoren...", expanded=True) as status:
        st.write("🧬 Zell-Marker werden analysiert...")
        time.sleep(1.5)
        st.write("🔍 Suche nach Blockaden...")
        time.sleep(1.5)
        status.update(label="Analyse Abgeschlossen!", state="complete", expanded=False)

    # Log detalhado com todas as métricas para a planilha
    log_detalhado = (f"Nome: {st.session_state.nome_usuario} | Peso: {st.session_state.peso_usuario}kg | "
                    f"Alt: {st.session_state.altura_usuario}cm | Goal: {st.session_state.q1} | "
                    f"Schlaf: {st.session_state.q2} | Hunger: {st.session_state.q3} | "
                    f"Bläh: {st.session_state.q4} | Alter: {st.session_state.q5}")
    
    salvar_log_google("ABGESCHLOSSEN", log_detalhado)
    
    st.balloons()
    
    # Alerta de sucesso restaurado
    st.success("✅ ANALYSE ABGESCHLOSSEN!")
    
    # CARD PREMIUM RENDEREIZADO (UNSAFE_ALLOW_HTML=TRUE)
    resultado_html = f"""
    <div style="background: rgba(255, 255, 255, 0.95); padding: 35px; border-radius: 20px; color: #1e293b; box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin: 20px 0; border: 1px solid rgba(255, 255, 255, 0.3);">
        <h2 style="color: #2563eb; text-align: center; font-weight: 800; margin-top: 0;">✅ ANALYSE BEREIT</h2>
        <hr style="border: 0; height: 1px; background: linear-gradient(to right, transparent, #2563eb, transparent); margin: 20px 0;">
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="background: #dcfce7; color: #166534; padding: 6px 15px; border-radius: 50px; font-weight: bold; font-size: 0.9rem;">STOFFWECHSEL-BLOCKADE TYP 3</span>
        </div>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #334155;">
            Hallo <b>{st.session_state.nome_usuario}</b>, basierend auf Ihrem Alter ({st.session_state.q5}), 
            Ihrem Gewicht ({st.session_state.peso_usuario} kg) und Ihrer Größe ({st.session_state.altura_usuario} cm), 
            haben wir ein <b>enzymatisches Ungleichgewicht</b> festgestellt, das durch <b>{st.session_state.q2.lower()}</b> Schlaf verursacht wird.
        </p>
        <div style="background: rgba(37, 99, 235, 0.1); padding: 15px; border-radius: 12px; border-left: 5px solid #2563eb; margin-top: 15px;">
            <p style="margin: 0; color: #1e3a8a; font-weight: 600;">🧬 Kompatibilität mit dem SlimSana-Protokoll: 98%</p>
        </div>
    </div>
    """
    st.markdown(resultado_html, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("🔥 JETZT ZUM SLIMSANA-PROTOKOLL", LINK_AFILIADO)
