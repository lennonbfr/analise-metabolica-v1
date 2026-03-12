import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DE LOG (MELHORIA EVA: COLUNAS PADRONIZADAS) ---
def salvar_log_evento(evento, detalhe):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        params = st.query_params
        origem = params.get("utm_source", "Direto/Teste")
        cidade = params.get("utm_city", "Indefinida")
        
        novo_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Origem": origem,
            "Cidade": cidade,
            "Evento": evento,
            "Detalhe": detalhe
        }])
        
        try:
            dados_atuais = conn.read(worksheet="Página1", ttl=0)
            df_final = pd.concat([dados_atuais, novo_log], ignore_index=True)
        except:
            df_final = novo_log
            
        conn.update(worksheet="Página1", data=df_final)
    except Exception as e:
        st.error(f"Erro no log: {e}")

# --- 2. GERAÇÃO DE PDF ---
def gerar_pdf_report(nome, score, m_type):
    file_name = f"Analyse_{nome.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "BIO-RESET METABOLISCHE ANALYSE")
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Erstellt für: {nome}")
    c.drawString(50, 700, f"Datum: {datetime.now().strftime('%d.%m.%Y')}")
    c.line(50, 690, 550, 690)
    c.drawString(50, 660, f"Stoffwechsel-Typ: {m_type}")
    c.drawString(50, 640, f"Metabolic Score: {score}/100")
    c.save()
    return file_name

# --- 3. INICIALIZAÇÃO E CONFIGS ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"
CIDADES_ELITE = ["Berlin", "München", "Hamburg", "Wien", "Zürich", "Frankfurt"]

st.set_page_config(page_title="BioReset Analysis", page_icon="🔬")

# MELHORIA EVA: Garantir que o 'step' exista sempre
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'pagina' not in st.session_state:
    params = st.query_params
    if params.get("utm_source") in ["taboola", "outbrain", "facebook"]:
        st.session_state.pagina = 'advertorial'
    else:
        st.session_state.pagina = 'home'

# --- TELA: ADVERTORIAL ---
if st.session_state.pagina == 'advertorial':
    cidade = st.query_params.get("utm_city", random.choice(CIDADES_ELITE))
    
    # Log de entrada automática (Sugerido pela Eva)
    if 'log_advertorial' not in st.session_state:
        salvar_log_evento("Acesso Advertorial", f"Cidade: {cidade}")
        st.session_state.log_advertorial = True

    st.markdown(f"**Wissenschaft & Gesundheit | {cidade} | {datetime.now().strftime('%d.%m.%Y')}**")
    st.markdown(f"# Neuer 30-Sekunden-Test zeigt möglichen Stoffwechsel-Block bei Erwachsenen in {cidade}")
    st.image("https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=800&q=80")
    
    st.info(f"📊 Aktuelle Schätzung: Hohes Analyse-Aufkommen in {cidade}.")
    
    if st.button(f"👉 KOSTENLOSE ANALYSE STARTEN", use_container_width=True):
        salvar_log_evento("Iniciou Quiz", f"Origem: Advertorial ({cidade})")
        st.session_state.pagina = 'quiz'
        st.rerun()
    
    st.caption("Hinweis: Dieser Test ersetzt keine medizinische Beratung.")

# --- TELA: HOME ---
elif st.session_state.pagina == 'home':
    st.markdown("# 🔬 BioReset Stoffwechsel-Analyse")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    if st.button("JETZT ANALYSE STARTEN"):
        salvar_log_evento("Iniciou Quiz", "Origem: Home")
        st.session_state.pagina = 'quiz'
        st.rerun()

# --- TELA: ADAPTIVE QUIZ (MELHORIA EVA: SALVAR RESPOSTAS) ---
elif st.session_state.pagina == 'quiz':
    if st.session_state.step == 1:
        st.write("Frage 1 von 3")
        st.progress(0.33)
        with st.form("quiz_1"):
            problem = st.selectbox("Was ist aktuell Ihre größte Herausforderung?", ["Bauchfett", "Müdigkeit", "Heißhunger"])
            if st.form_submit_button("Weiter"):
                st.session_state.problem = problem
                st.session_state.step = 2
                st.rerun()
    
    elif st.session_state.step == 2:
        st.write("Frage 2 von 3")
        st.progress(0.66)
        p = "Haben Sie oft das Gefühl, dass Ihr Körper 'blockiert'?" if st.session_state.problem == "Bauchfett" else "Fühlen Sie sich nach dem Essen oft schläfrig?"
        with st.form("quiz_2"):
            res2 = st.radio(p, ["Ja", "Manchmal", "Nein"])
            if st.form_submit_button("Weiter"):
                st.session_state.res2 = res2 # MELHORIA EVA: Salvando a resposta
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        st.write("Frage 3 von 3")
        st.progress(0.95)
        with st.form("quiz_3"):
            nome_raw = st.text_input("Ihr Vorname")
            idade = st.slider("Alter", 18, 80, 42)
            if st.form_submit_button("ANALYSE DURCHFÜHREN"):
                # MELHORIA EVA: Tratar nome vazio e log de conclusão
                st.session_state.nome = nome_raw if nome_raw else "Besucher"
                salvar_log_evento("Quiz Concluído", f"Problema: {st.session_state.problem} | Idade: {idade}")
                st.session_state.pagina = 'analyzing'
                st.rerun()

# --- TELA: ANALYZING (SIMULADOR) ---
elif st.session_state.pagina == 'analyzing':
    with st.status("🧬 Analysiere BioMarker...", expanded=True) as s:
        time.sleep(1.2); s.update(label="Abgleich com Datenbank...", state="running")
        time.sleep(1.2); s.update(label="Analyse abgeschlossen!", state="complete")
    st.session_state.pagina = 'optin'; st.rerun()

# --- TELA: OPT-IN ---
elif st.session_state.pagina == 'optin':
    st.metric("Metabolic Score", "62/100")
    st.write("### Erhalten Sie Ihren persönlichen Stoffwechselbericht als PDF")
    email = st.text_input("E-Mail-Adresse")
    if st.button("BERICHT FREISCHALTEN"):
        if "@" in email:
            st.session_state.email = email
            salvar_log_evento("Lead Capturado", email)
            st.session_state.pagina = 'report'; st.rerun()
        else: st.error("Bitte gültige E-Mail eingeben")

# --- TELA: REPORT + PDF (MELHORIA EVA: LOG DE DOWNLOAD) ---
elif st.session_state.pagina == 'report':
    st.markdown(f"## 🧬 Bericht für {st.session_state.nome}")
    pdf_path = gerar_pdf_report(st.session_state.nome, 62, st.session_state.problem)
    with open(pdf_path, "rb") as f:
        # Nota: download_button do Streamlit não permite disparar função ao clicar facilmente sem hack, 
        # mas registramos que ele CHEGOU nesta tela de download.
        if st.download_button("📥 Analyse als PDF speichern", f, file_name=pdf_path):
             salvar_log_evento("PDF Download Realizado", st.session_state.email)

    if st.button("🔬 WEITER ZUR ERKLÄRUNG"):
        st.session_state.pagina = 'bridge'; st.rerun()

# --- TELA: BRIDGE (REDIRECT) ---
elif st.session_state.pagina == 'bridge':
    # Pre-connect para agilizar a VSL
    st.markdown('<link rel="preconnect" href="https://myslimsana.com">', unsafe_allow_html=True)
    st.markdown("# 🔬 Die Lösung")
    st.write("Basierend auf Ihrem Score von 62/100, sehen Sie sich die Video-Präsentation an.")
    if st.button("🎥 VIDEO ANSEHEN"):
        salvar_log_evento("Clicou para VSL", st.session_state.email)
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={LINK_AFILIADO}">', unsafe_allow_html=True)
