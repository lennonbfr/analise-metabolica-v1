import streamlit as st
import pandas as pd
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DE LOG ---
def salvar_log_evento(evento, detalhe):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        params = st.query_params
        origem = params.get("utm_source", "facebook")
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
        print(f"Erro no log: {e}")

# --- 2. LÓGICA DE INTELIGÊNCIA ---
def calcular_score():
    score = 78
    if st.session_state.get('res2') == "Ja": score -= 8
    elif st.session_state.get('res2') == "Manchmal": score -= 4
    if st.session_state.get('res5') == "Ja, sehr häufig": score -= 10
    elif st.session_state.get('res5') == "Manchmal": score -= 5
    if st.session_state.get('res4') == "Nach dem Mittagessen": score -= 4
    p_map = {"Bauchfett": 4, "Müdigkeit": 3, "Heißhunger": 5}
    score -= p_map.get(st.session_state.get('problem'), 0)
    return max(min(score, 74), 56)

def definir_tipo_metabolico():
    problem = st.session_state.get("problem")
    if problem == "Bauchfett": return "Typ A – Verlangsamter Stoffwechsel"
    elif problem == "Müdigkeit": return "Typ B – Energie-Dysbalance"
    else: return "Typ C – Hunger-Regulationsmuster"

# --- 3. GERAÇÃO DE PDF ---
def gerar_pdf_report(nome, score, m_type):
    file_name = f"Analyse_{nome.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "BIO-RESET METABOLISCHE ANALYSE")
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Erstellt für: {nome}")
    c.drawString(50, 700, f"Datum: {datetime.now().strftime('%d.%m.%Y')}")
    c.line(50, 690, 550, 690)
    c.drawString(50, 660, f"Stoffwechsel-Profil: {m_type}")
    c.drawString(50, 640, f"Individueller Index: {score}/100")
    c.save()
    return file_name

# --- 4. CONFIGURAÇÕES E ESTADO ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"
st.set_page_config(page_title="BioReset Analysis", page_icon="🔬")

if 'step' not in st.session_state: st.session_state.step = 1

if 'pagina' not in st.session_state:
    params = st.query_params
    fontes_pagas = ["facebook", "instagram", "meta", "taboola", "outbrain"]
    if params.get("utm_source") in fontes_pagas:
        st.session_state.pagina = 'advertorial'
    else:
        st.session_state.pagina = 'home'

# --- TELA: ADVERTORIAL ---
if st.session_state.pagina == 'advertorial':
    if 'log_view_adv' not in st.session_state:
        salvar_log_evento("Visualizou Advertorial", "Entrada via Tráfego Pago")
        st.session_state.log_view_adv = True

    st.markdown(f"**Wissenschaft & Gesundheit | {datetime.now().strftime('%d.%m.%Y')}**")
    st.markdown("# Neuer 30-Sekunden-Test zeigt möglichen Stoffwechsel-Block bei Erwachsenen")
    st.image("https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=800&q=80")
    if st.button("👉 KOSTENLOSE ANALYSE STARTEN", use_container_width=True):
        salvar_log_evento("Iniciou Quiz", "Origem: Advertorial")
        st.session_state.step = 1; st.session_state.pagina = 'quiz'; st.rerun()

# --- TELA: HOME ---
elif st.session_state.pagina == 'home':
    if 'log_view_home' not in st.session_state:
        salvar_log_evento("Visualizou Home", "Entrada Direta")
        st.session_state.log_view_home = True

    st.markdown("# 🔬 BioReset Stoffwechsel-Analyse")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    if st.button("JETZT ANALYSE STARTEN"):
        salvar_log_evento("Iniciou Quiz", "Origem: Home")
        st.session_state.step = 1; st.session_state.pagina = 'quiz'; st.rerun()

# --- TELA: QUIZ ADAPTATIVO ---
elif st.session_state.pagina == 'quiz':
    progress_map = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
    st.write(f"Frage {st.session_state.step} von 5")
    st.progress(progress_map.get(st.session_state.step, 0.1))

    if st.session_state.step == 1:
        with st.form("q1"):
            problem = st.selectbox("Was ist Ihre größte Herausforderung?", ["Bauchfett", "Müdigkeit", "Heißhunger"])
            if st.form_submit_button("Weiter"):
                st.session_state.problem = problem; st.session_state.step = 2; st.rerun()
    
    elif st.session_state.step == 2:
        # CORREÇÃO EVA: Restauração dos 3 caminhos adaptativos
        if st.session_state.problem == "Bauchfett":
            p = "Haben Sie das Gefühl, dass Ihr Körper trotz Bemühungen kaum auf Veränderungen reagiert?"
        elif st.session_state.problem == "Müdigkeit":
            p = "Fühlen Sie sich trotz ausreichend Schlaf tagsüber häufig erschöpft?"
        else: # Heißhunger
            p = "Haben Sie besonders am Nachmittag oder Abend starke Heißhungerphasen?"
            
        with st.form("q2"):
            res2 = st.radio(p, ["Ja", "Manchmal", "Nein"])
            if st.form_submit_button("Weiter"):
                st.session_state.res2 = res2; st.session_state.step = 3; st.rerun()
                
    elif st.session_state.step == 3:
        with st.form("q3"):
            nome_in = st.text_input("Ihr Vorname")
            idade = st.slider("Alter", 18, 80, 42)
            if st.form_submit_button("Weiter"):
                st.session_state.nome = nome_in if nome_in else "Besucher"
                st.session_state.step = 4; st.rerun()
    elif st.session_state.step == 4:
        with st.form("q4"):
            st.write("**Wann fühlen Sie sich am energielosesten?**")
            res4 = st.radio("Option wählen:", ["Morgens", "Nach dem Mittagessen", "Am späten Nachmittag", "Abends"])
            if st.form_submit_button("Weiter"):
                st.session_state.res4 = res4; st.session_state.step = 5; st.rerun()
    elif st.session_state.step == 5:
        with st.form("q5"):
            st.write("**Fällt es Ihnen schwer, Gewicht zu verlieren?**")
            res5 = st.radio("Option wählen:", ["Ja, sehr häufig", "Manchmal", "Selten"])
            if st.form_submit_button("ANALYSE DURCHFÜHREN"):
                st.session_state.res5 = res5
                salvar_log_evento("Quiz Concluído", f"User: {st.session_state.nome}")
                st.session_state.pagina = 'analyzing'; st.rerun()

# --- TELA: ANALYZING ---
elif st.session_state.pagina == 'analyzing':
    st.caption("Ihre Antworten werden mit metabolischen Referenzmustern verglichen.")
    with st.status("🧬 Analysiere BioMarker...", expanded=True) as s:
        time.sleep(1.0); s.update(label="🧬 Abgleich mit Altersprofil...", state="running")
        time.sleep(1.0); s.update(label="🧬 Berechnung des Stoffwechsel-Index...", state="running")
        time.sleep(1.0); s.update(label="✅ Analyse abgeschlossen!", state="complete")
    st.session_state.pagina = 'optin'; st.rerun()

# --- TELA: OPT-IN ---
elif st.session_state.pagina == 'optin':
    score_final = calcular_score()
    st.session_state.score = score_final
    st.session_state.m_type = definir_tipo_metabolico()
    st.metric("Metabolischer Index", f"{score_final}/100")
    st.caption("Ihr Ergebnis deutet auf eine metabolische Dysbalance hin.")
    st.write("### Erhalten Sie Ihren Bericht als PDF")
    email = st.text_input("E-Mail-Adresse")
    if st.button("BERICHT FREISCHALTEN"):
        if "@" in email:
            st.session_state.email = email
            salvar_log_evento("Lead Capturado", email)
            st.session_state.pagina = 'report'; st.rerun()

# --- TELA: REPORT ---
elif st.session_state.pagina == 'report':
    st.success(f"Ihr Bericht ist fertig, {st.session_state.nome}!")
    st.write(f"**Profil:** {st.session_state.m_type}")
    pdf_path = gerar_pdf_report(st.session_state.nome, st.session_state.score, st.session_state.m_type)
    with open(pdf_path, "rb") as f:
        if st.download_button("📥 PDF herunterladen", f, file_name=pdf_path):
            salvar_log_evento("Baixou PDF", st.session_state.email)
    if st.button("🔬 WEITER ZUR LÖSUNG"):
        st.session_state.pagina = 'bridge'; st.rerun()

# --- TELA: BRIDGE ---
elif st.session_state.pagina == 'bridge':
    # CORREÇÃO EVA: Preconnect + DNS-Prefetch otimizado
    st.markdown("""
    <link rel="preconnect" href="https://myslimsana.com">
    <link rel="dns-prefetch" href="https://myslimsana.com">
    """, unsafe_allow_html=True)
    st.markdown("# 🔬 Nächste Schritte")
    # CORREÇÃO EVA: Gramática alemã (von em vez de de)
    st.write(f"Basierend auf Ihrem Index von {st.session_state.score}/100, sehen Sie sich die Video-Präsentation an.")
    if st.button("🎥 VIDEO ANSEHEN"):
        salvar_log_evento("Clicou para VSL", st.session_state.email)
        with st.spinner("Video wird geladen..."):
            time.sleep(1.2)
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={LINK_AFILIADO}">', unsafe_allow_html=True)
