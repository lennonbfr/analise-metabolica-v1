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

# Inicializa a página como 'home' se for o primeiro acesso
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

st.set_page_config(page_title="BioReset Analyse", page_icon="🧪")

# --- TELA 1: HOME (A TELA DA MAÇÃ QUE VOCÊ QUER) ---
if st.session_state.pagina == 'home':
    st.markdown("<h1 style='text-align: center;'>🍎 Teste: Por que seu corpo 'trava' após os 30?</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # Imagem intuitiva da maçã/saúde
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80", caption="Análise Bio-Metabólica Gratuita")
    
    st.info("Descubra por que dietas comuns não funcionam para o seu perfil genético.")
    
    if st.button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA"):
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA 2: QUESTIONÁRIO (SÓ APARECE APÓS O CLIQUE) ---
elif st.session_state.pagina == 'quiz':
    st.subheader("📋 Persönliche Angaben (Análise em andamento)")
    
    with st.form("quiz_form"):
        q1 = st.selectbox("1. Was ist Ihr Hauptziel?", 
                         ["Bauchfett verlieren", "Mehr Energie", "Heißhunger stoppen", "Stoffwechsel beschleunigen"])
        q2 = st.radio("2. Wie bewerten Sie Ihre Schlafqualität?", 
                     ["Ich wache müde auf", "Leichter Schlaf", "Guter Schlaf"])
        q3 = st.slider("3. Wie alt sind Sie?", 18, 80, 43)
        
        if st.form_submit_button("ANALYSE STARTEN"):
            st.session_state.q1 = q1
            st.session_state.q6 = q3
            st.session_state.pagina = 'resultado'
            st.rerun()

# --- TELA 3: RESULTADO ---
elif st.session_state.pagina == 'resultado':
    with st.status("Verarbeitung...", expanded=False):
        time.sleep(2)
    
    salvar_log_google(st.session_state.q1, f"Idade: {st.session_state.q6}")
    
    st.success("✅ ANÁLISE CONCLUÍDA!")
    st.markdown(f"### Seu Resultado: Bloqueio Nível 3")
    st.write(f"Detectamos que sua idade ({st.session_state.q6} anos) exige um reset celular.")
    
    st.link_button("🔥 ACESSAR PROTOCOLO SLIMSANA", LINK_AFILIADO)
    
    if st.button("Reiniciar Teste"):
        st.session_state.pagina = 'home'
        st.rerun()
