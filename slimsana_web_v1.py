import streamlit as st
import uuid
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA CONEXÃO (GOOGLE SHEETS) ---
def salvar_log_google(pergunta, resultado):
    try:
        # Cria a conexão usando as Secrets do Streamlit
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Prepara o novo dado
        novo_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Origem": "FacebookAds_DE_AT",
            "Dificuldade": pergunta,
            "Resultado": resultado
        }])

        # Tenta ler os dados existentes. Se a planilha estiver vazia, cria o DF
        try:
            dados_atuais = conn.read()
            df_final = pd.concat([dados_atuais, novo_log], ignore_index=True)
        except:
            df_final = novo_log
        
        # Faz o update na nuvem
        conn.update(data=df_final)
    except Exception as e:
        # Log de erro silencioso para não assustar o usuário
        print(f"Erro na planilha: {e}")

# --- 2. CONFIGURAÇÃO VISUAL E LINKS ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

st.set_page_config(page_title="Teste do Metabolismo - Oficial", page_icon="🥗")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; background-color: #28a745; color: white; border-radius: 10px; height: 3em; font-weight: bold; }
    h1 { color: #1e7e34; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stRadio > label { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🍎 Teste: Por que seu corpo 'trava' após os 30?")
st.write("---")
st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")

st.info("⚠️ Este teste leva apenas 60 segundos e revela o seu Índice de Bloqueio Metabólico.")

# --- O QUIZ ---
with st.container():
    pergunta1 = st.selectbox("Qual sua maior dificuldade hoje?", 
                            ["Gordura abdominal insistente", "Falta de energia durante o dia", "Vontade incontrolável de doces"])
    
    pergunta2 = st.radio("Quantas vezes você já tentou dietas que não funcionaram?", 
                            ["1-2 vezes", "Mais de 5 vezes", "Já desisti de contar"])
    
    pergunta3 = st.slider("Qual sua idade?", 18, 80, 43) # Ajustado para sua idade atual

    if st.button("REVELAR MEU RESULTADO PERSONALIZADO"):
        # Efeito de carregamento
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        # --- DISPARO DO LOG PARA O GOOGLE SHEETS ---
        salvar_log_google(pergunta1, "Bloqueio Nível 2")
        
        st.balloons()
        
        # --- RESULTADO E OFERTA ---
        st.success("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://myslimsana.com/images/slimsana-bottle.png", width=150)
        
        with col2:
            st.subheader("Seu Resultado: Bloqueio Nível 2")
            st.write(f"Lennon, detectamos que sua dificuldade com '{pergunta1}' é causada por um desajuste enzimático.")
            st.write("A solução alemã **SlimSana** foi identificada como 98% compatível com o seu perfil.")
        
        st.divider()
        st.markdown("### 🎁 Oferta Especial para Novos Usuários")
        
        # Botão com link corrigido (?aff=)
        st.link_button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA", LINK_AFILIADO)
        
        st.caption(f"Protocolo de rastreamento LTA: {str(uuid.uuid4())[:8]}")
