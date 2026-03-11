import streamlit as st
import uuid
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURAÇÃO DE LOG (OTIMIZADA) ---
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
            dados_atuais = conn.read(worksheet="Página1", ttl=0)
            if not dados_atuais.empty:
                df_final = pd.concat([dados_atuais, novo_log], ignore_index=True)
            else:
                df_final = novo_log
        except:
            df_final = novo_log
            
        conn.update(worksheet="Página1", data=df_final)
    except Exception as e:
        print(f"Erro no log: {e}")

# --- 2. CONFIGURAÇÕES ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

if 'origem' not in st.session_state:
    params = st.query_params
    st.session_state.origem = params.get("utm_content", "FacebookAds_DE_AT")

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

# Trava para evitar repetição de balões e logs de conclusão
if 'log_concluido' not in st.session_state:
    st.session_state.log_concluido = False

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- 3. CSS ORIGINAL ---
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
        width: 100%;
        text-shadow: 1px 1px 2px black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TELA 1: HOME ---
if st.session_state.pagina == 'home':
    st.markdown('# 🍎 Test: Warum Ihr Körper nach dem 30. Lebensjahr "blockiert"?')
    st.write("---")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    
    st.info("Finden Sie heraus, warum herkömmliche Diäten nicht für Ihr genetisches Profil funktionieren.")
    
    if st.button("🔥 MEINEN STOFFWECHSEL JETZT FREISCHALTEN"):
        salvar_log_google("SYSTEM", "HOME_BETRETEN")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO ---
elif st.session_state.pagina == 'quiz':
    st.subheader("📋 Persönliche Angaben")
    with st.form("quiz_form"):
        nome_input = st.text_input("Vollständiger Name")
        c1, c2 = st.columns(2)
        with c1:
            peso_input = st.number_input("Gewicht (kg)", min_value=40.0, max_value=200.0, value=75.0, step=0.1)
        with c2:
            altura_input = st.number_input("Größe (cm)", min_value=120, max_value=220, value=170, step=1)
        
        st.write("---")
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", ["Bauchfett verlieren", "Mehr Energie im Alltag", "Heißhungerattacken stoppen", "Stoffwechsel beschleunigen"])
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", ["Ich wache müde auf", "Leichter/Unterbrochener Schlaf", "Guter Schlaf, mas keine Energie"])
        q3 = st.selectbox("3. Wann verspüren Sie am meisten Hunger?", ["Vormittags", "Nachmittags (Stress)", "Abends/Nachts"])
        q4 = st.radio("4. Fühlen Sie sich nach dem Essen oft aufgebläht?", ["Ja, fast jeden Tag", "Manchmal", "Selten"])
        q5 = st.slider("5. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ANALYSE STARTEN"):
            st.session_state.update({
                "nome_usuario": nome_input if nome_input else "Besucher",
                "peso_usuario": peso_input,
                "altura_usuario": altura_input,
                "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5,
                "pagina": 'resultado',
                "log_concluido": False # Reseta a trava para o novo teste
            })
            st.rerun()

# --- TELA 3: RESULTADO ---
elif st.session_state.pagina == 'resultado':
    # Executa apenas na primeira vez que entra na tela
    if not st.session_state.log_concluido:
        with st.status("Verarbeitung der Bio-Indikatoren...", expanded=True) as status:
            st.write("🧬 Zell-Marker werden analysiert...")
            time.sleep(1.2)
            st.write("🔍 Suche nach Blockaden...")
            time.sleep(1.2)
            status.update(label="Analyse Abgeschlossen!", state="complete", expanded=False)

        log_detalhado = (f"Nome: {st.session_state.nome_usuario} | Peso: {st.session_state.peso_usuario}kg | "
                        f"Alt: {st.session_state.altura_usuario}cm | Goal: {st.session_state.q1} | "
                        f"Schlaf: {st.session_state.q2} | Hunger: {st.session_state.q3} | "
                        f"Bläh: {st.session_state.q4} | Alter: {st.session_state.q5}")
        
        salvar_log_google("ABGESCHLOSSEN", log_detalhado)
        st.balloons()
        st.session_state.log_concluido = True # Ativa a trava

    st.success("✅ ANALYSE ABGESCHLOSSEN!")
    
    st.markdown(f"""
    ### Ihr Ergebnis: Stoffwechsel-Blockade Typ 3
    
    Hallo **{st.session_state.nome_usuario}**, basierend auf Ihrem Alter ({st.session_state.q5}), 
    Ihrem Gewicht ({st.session_state.peso_usuario} kg) und Ihrer Größe ({st.session_state.altura_usuario} cm), 
    haben wir ein enzymatisches Ungleichgewicht festgestellt, das durch **{st.session_state.q2.lower()}** Schlaf verursacht wird.
    
    Das SlimSana-Protokoll wurde zu 98% als kompatibel mit Ihrem Profil eingestuft.
    """)
    
    st.write("")
    
    if st.button("🔥 JETZT ZUM SLIMSANA-PROTOKOLL", use_container_width=True):
        salvar_log_google("CLICK_CHECKOUT", f"Usuario: {st.session_state.nome_usuario}")
        # Redirecionamento via meta-refresh para evitar o duplo clique
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={LINK_AFILIADO}">', unsafe_allow_html=True)
        st.stop()
