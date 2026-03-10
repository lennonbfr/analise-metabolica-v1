import streamlit as st
import uuid
import time
import csv
import os
from datetime import datetime

# --- 1. MÓDULO DE LOG (MONITORAMENTO DE CONVERSÃO) ---
def salvar_log_quiz(pergunta, resultado):
    arquivo_log = 'logs_bioreset_performance.csv'
    colunas = ['timestamp', 'origem', 'dificuldade', 'resultado_final']
    file_exists = os.path.isfile(arquivo_log)
    try:
        # Usamos utf-8-sig para que o Excel abra os acentos corretamente no Windows
        with open(arquivo_log, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'origem': 'FacebookAds_DE_AT', 
                'dificuldade': pergunta,
                'resultado_final': resultado
            })
    except Exception as e:
        print(f"Erro no Log: {e}")

# --- 2. CONFIGURAÇÃO DO LINK DE AFILIADO (VERIFICADO) ---
# Link corrigido com '?' para garantir o rastreamento da sua comissão
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

st.set_page_config(page_title="Teste do Metabolismo - Oficial", page_icon="🥗")

# CSS para Interface Clean
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
st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80", caption="Análise baseada em hábitos diários")

st.info("⚠️ Este teste leva apenas 60 segundos e revela o seu Índice de Bloqueio Metabólico.")

# --- O QUIZ ---
with st.container():
    pergunta1 = st.selectbox("Qual sua maior dificuldade hoje?", 
                            ["Gordura abdominal insistente", "Falta de energia durante o dia", "Vontade incontrolável de doces"])
    
    pergunta2 = st.radio("Quantas vezes você já tentou dietas que não funcionaram?", 
                            ["1-2 vezes", "Mais de 5 vezes", "Já desisti de contar"])
    
    pergunta3 = st.slider("Qual sua idade?", 18, 80, 32)

    if st.button("REVELAR MEU RESULTADO PERSONALIZADO"):
        # Efeito de carregamento para valorizar a análise
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01) 
            progress_bar.progress(percent_complete + 1)
        
        # DISPARO DO LOG (Agora com os dados reais do usuário)
        salvar_log_quiz(pergunta1, "Bloqueio Nível 2")
        
        st.balloons()
        
        # --- RESULTADO E OFERTA ---
        st.success("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # Imagem do Produto
            st.image("https://myslimsana.com/images/slimsana-bottle.png", width=150)
        
        with col2:
            st.subheader("Seu Resultado: Bloqueio Nível 2")
            st.write(f"Detectamos que sua dificuldade com '{pergunta1}' é causada por um desajuste enzimático.")
            st.write("A solução alemã **SlimSana** foi identificada como 98% compatível com o seu perfil.")
        
        st.divider()
        st.markdown("### 🎁 Oferta Especial para Novos Usuários")
        
        # BOTÃO FINAL - O seu "pote de ouro"
        st.link_button("🔥 QUERO DESBLOQUEAR MEU METABOLISMO AGORA", LINK_AFILIADO)
        
        st.caption(f"Protocolo de rastreamento LTA: {str(uuid.uuid4())[:8]}")
