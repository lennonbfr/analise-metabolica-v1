import streamlit as st
import uuid
import time

# --- CONFIGURAÇÃO DA MÁQUINA ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe#aff=lennonbfr"

# Configuração da página (Título que aparece na aba do navegador)
st.set_page_config(page_title="Análise Metabólica Avançada", page_icon="⚖️")

# Estilização básica para ficar com cara de software de saúde
st.title("🔬 Sistema de Diagnóstico Metabólico")
st.write("Complete o teste de 2 minutos para receber sua recomendação personalizada.")

# --- O QUIZ (INTERFACE) ---
with st.form("quiz_form"):
    st.subheader("Dados de Avaliação")
    
    objetivo = st.selectbox("Qual seu principal objetivo?", 
                            ["Emagrecimento Rápido", "Energia e Disposição", "Saúde Longevidade"])
    
    dificuldade = st.radio("Sente que seu metabolismo é lento?", 
                            ["Sim, tenho muita dificuldade", "Médio", "Não, meu metabolismo é normal"])
    
    idade = st.slider("Qual sua faixa etária?", 18, 80, 40)
    
    submit = st.form_submit_button("GERAR ANÁLISE AGORA")

# --- LÓGICA DE PROCESSAMENTO ---
if submit:
    with st.spinner('Processando dados e gerando ID de rastreamento LTA...'):
        time.sleep(2) # Simula o processamento da "máquina"
        track_id = str(uuid.uuid4())[:8]
        
        st.success(f"Análise Concluída! ID de Rastreamento: {track_id}")
        
        # O veredito personalizado
        st.subheader("📋 Veredito Técnico")
        st.info(f"Detectamos que seu perfil de '{objetivo}' requer uma abordagem direta na quebra de resistência celular.")
        
        st.write("""
        **Recomendação:** Com base nos seus dados, o uso do **SlimSana** é o mais indicado 
        para otimizar seus resultados em até 30 dias.
        """)
        
        # O BOTÃO DE OURO (Seu link)
        st.link_button("👉 ACESSAR RECOMENDAÇÃO OFICIAL", LINK_AFILIADO, type="primary")

st.divider()
st.caption("Tecnologia de rastreamento LTA ativa. Todos os direitos reservados.")