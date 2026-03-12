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
        origem = params.get("utm_source", "direto")
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

def calcular_idade_metabolica(idade_real, score):
    if score <= 58: acrescimo = 7
    elif score <= 62: acrescimo = 5
    elif score <= 66: acrescimo = 4
    elif score <= 70: acrescimo = 3
    else: acrescimo = 2
    return idade_real + acrescimo

def definir_label_metabolico():
    prob = st.session_state.get("problem")
    if prob == "Bauchfett": return "Typ A – Verlangsamter Stoffwechsel"
    elif prob == "Müdigkeit": return "Typ B – Energie-Dysbalance"
    else: return "Typ C – Hunger-Regulationsmuster"

def obter_detalhes_perfil(label):
    if "Typ A" in label:
        return {
            "desc": "Dieses Profil deutet auf eine reduzierte metabolische Aktivität hin. Häufig zeigen sich dabei eine langsamere Reaktion auf Gewichtsveränderungen.",
            "sinais": ["langsamere Fettverbrennung", "geringere Energieverfügbarkeit"]
        }
    elif "Typ B" in label:
        return {
            "desc": "Dieses Profil weist auf ein Ungleichgewicht in der Energieverteilung hin. Betroffene berichten oft über starke Leistungsschwankungen.",
            "sinais": ["Energieabfall nach Mahlzeiten", "instabile Belastbarkeit"]
        }
    else:
        return {
            "desc": "Dieses Profil deutet auf eine Dysbalance in der Hunger-Regulation hin. Typisch sind wiederkehrende Heißhungerphasen.",
            "sinais": ["starke Heißhungerimpulse", "instabile Sättigung"]
        }

# --- 3. GERAÇÃO DE PDF ---
def gerar_pdf_report(nome, score, label, idade_real, idade_meta):
    detalhes = obter_detalhes_perfil(label)
    file_name = f"Analyse_{nome.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "BIO-RESET METABOLISCHE ANALYSE")
    c.setFont("Helvetica", 10)
    c.drawString(50, 735, "Persönlicher Gesundheitsbericht | Vertraulich")
    c.line(50, 730, 550, 730)
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 710, f"Erstellt für: {nome}")
    c.drawString(50, 695, f"Datum: {datetime.now().strftime('%d.%m.%Y')}")
    c.drawString(50, 680, f"Chronologisches Alter: {idade_real} Jahre")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 640, "1. Analyse-Ergebnis")
    c.roundRect(50, 570, 220, 55, 8, stroke=1, fill=0) 
    c.setFont("Helvetica-Bold", 11)
    c.drawString(65, 608, "METABOLISCHER INDEX")
    c.setFont("Helvetica-Bold", 24)
    c.drawString(65, 582, f"{score}/100")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 550, f"Stoffwechsel-Profil: {label}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 510, "2. Vergleich mit Ihrer Altersgruppe")
    c.setFont("Helvetica", 12)
    c.drawString(50, 490, "Ihr Index liegt unter dem Durchschnitt Ihrer Altersgruppe.")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 475, f"Geschätztes metabolisches Alter: ca. {idade_meta} Jahre")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 430, "3. Profilbeschreibung")
    c.setFont("Helvetica", 11)
    text_object = c.beginText(50, 410)
    text_object.textLines(detalhes["desc"])
    text_object.textLine("")
    text_object.textLine("Typische Hinweise:")
    for s in detalhes["sinais"]:
        text_object.textLine(f"- {s}")
    c.drawText(text_object)

    c.line(50, 250, 550, 250)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 230, "Nächste Schritte:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 215, "Es gibt spezifische Methoden, um dieses Gleichgewicht wiederherzustellen.")
    c.drawString(50, 200, "Sehen Sie sich die Video-Analyse für detaillierte Empfehlungen an.")
    
    c.save()
    return file_name

# --- 4. CONFIGURAÇÕES E FLUXO ---
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"
st.set_page_config(page_title="BioReset Analysis", page_icon="🔬")

if 'step' not in st.session_state: st.session_state.step = 1
if 'pagina' not in st.session_state:
    p = st.query_params.get("utm_source")
    st.session_state.pagina = 'advertorial' if p in ["facebook", "instagram", "meta", "taboola", "outbrain"] else 'home'

# --- TELA: ADVERTORIAL ---
if st.session_state.pagina == 'advertorial':
    if 'log_view_adv' not in st.session_state:
        salvar_log_evento("Visualizou Advertorial", "Entrada via Tráfego Pago")
        st.session_state.log_view_adv = True

    st.markdown(f"**Wissenschaft & Gesundheit | {datetime.now().strftime('%d.%m.%Y')}**")
    st.markdown("# Neuer 30-Sekunden-Test zeigt möglichen Stoffwechsel-Block ab 40")
    
    # Ajuste: Linhas em branco para melhor visualização
    st.markdown("""
    Viele Erwachsene bemerken im Alltag erste Veränderungen ihres Stoffwechsels:

    • **Zunehmendes Bauchfett** trotz normaler Ernährung  
    • **Energieabfall** nach dem Mittagessen  
    • **Wiederkehrende Heißhunger-Phasen**

    Ein kurzer Analyse-Test kann erste Hinweise auf mögliche Ursachen geben.
    """)
    
    st.image("https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=800&q=80")
    if st.button("👉 JETZT 30-SEKUNDEN-TEST STARTEN", use_container_width=True):
        salvar_log_evento("Iniciou Quiz", "Origem: Advertorial")
        st.session_state.step = 1
        st.session_state.pagina = 'quiz'; st.rerun()

# --- TELA: HOME ---
elif st.session_state.pagina == 'home':
    if 'log_view_home' not in st.session_state:
        salvar_log_evento("Visualizou Home", "Entrada Direta")
        st.session_state.log_view_home = True
    st.markdown("# 🔬 BioReset Stoffwechsel-Analyse")
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80")
    if st.button("JETZT ANALYSE STARTEN"):
        salvar_log_evento("Iniciou Quiz", "Origem: Home")
        st.session_state.step = 1
        st.session_state.pagina = 'quiz'; st.rerun()

# --- TELA: QUIZ ---
elif st.session_state.pagina == 'quiz':
    st.write(f"Frage {st.session_state.step} von 5")
    st.progress(st.session_state.step / 5)

    if st.session_state.step == 1:
        with st.form("q1"):
            prob = st.selectbox("Was ist Ihre größte Herausforderung?", ["Bauchfett", "Müdigkeit", "Heißhunger"])
            if st.form_submit_button("Weiter"):
                st.session_state.problem = prob; st.session_state.step = 2; st.rerun()
    elif st.session_state.step == 2:
        if st.session_state.problem == "Bauchfett":
            p = "Haben Sie das Gefühl, dass Ihr Körper trotz Bemühungen kaum auf Veränderungen reagiert?"
        elif st.session_state.problem == "Müdigkeit":
            p = "Fühlen Sie sich trotz ausreichend Schlaf tagsüber häufig erschöpft?"
        else:
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
                st.session_state.nome = nome_in if nome_in else "Besucher"; st.session_state.idade = idade; st.session_state.step = 4; st.rerun()
    elif st.session_state.step == 4:
        with st.form("q4"):
            res4 = st.radio("Wann fühlen Sie sich energielos?", ["Morgens", "Nach dem Mittagessen", "Am späten Nachmittag", "Abends"])
            if st.form_submit_button("Weiter"):
                st.session_state.res4 = res4; st.session_state.step = 5; st.rerun()
    elif st.session_state.step == 5:
        with st.form("q5"):
            res5 = st.radio("Fällt es Ihnen schwer, Gewicht zu verlieren?", ["Ja, sehr häufig", "Manchmal", "Selten"])
            if st.form_submit_button("ANALYSE DURCHFÜHREN"):
                st.session_state.res5 = res5
                salvar_log_evento("Quiz Concluído", f"User: {st.session_state.nome} | Prob: {st.session_state.problem} | Idade: {st.session_state.idade}")
                st.session_state.pagina = 'analyzing'; st.rerun()

# --- TELA: ANALYZING ---
elif st.session_state.pagina == 'analyzing':
    with st.status("🧬 Analysiere BioMarker...", expanded=True) as s:
        time.sleep(1.0)
        s.update(label="🧬 Abgleich mit Altersprofil...", state="running")
        time.sleep(1.0)
        s.update(label="✅ Analyse abgeschlossen!", state="complete")
    st.session_state.pagina = 'optin'; st.rerun()

# --- TELA: OPT-IN ---
elif st.session_state.pagina == 'optin':
    score = calcular_score()
    st.session_state.score = score
    st.session_state.m_label = definir_label_metabolico()
    st.metric("Metabolischer Index", f"{score}/100")
    st.write("### Vergleich mit Ihrer Altersgruppe")
    st.progress(score/100)
    
    # Ajuste: Comparação explícita com a média etária
    st.caption(f"Durchschnitt (Alter {st.session_state.idade-2}-{st.session_state.idade+3}): 74/100")
    
    st.warning("Ihr Ergebnis liegt unter dem Durchschnitt Ihrer Altersgruppe. Der vollständige Bericht zeigt, welche Faktoren Ihren Stoffwechsel aktuell beeinflussen könnten.")
    st.write("### Ihr vollständiger Bericht enthält:")
    st.markdown("- Ihr **metabolisches Profil**\n- eine **Einordnung Ihres Stoffwechsel-Index**\n- eine **orientierende Alterseinschätzung**")
    
    email = st.text_input("E-Mail-Adresse für den ausführlichen Bericht")
    st.caption("Keine lange Registrierung – Ihr Bericht wird sofort freigeschaltet.")
    
    if st.button("📄 PERSÖNLICHEN BERICHT FREISCHALTEN"):
        if "@" in email:
            st.session_state.email = email
            salvar_log_evento("Lead Capturado", email)
            st.session_state.pagina = 'report'; st.rerun()

# --- TELA: REPORT ---
elif st.session_state.pagina == 'report':
    st.success(f"Ihr Bericht ist fertig, {st.session_state.nome}!")
    st.write(f"**Profil:** {st.session_state.m_label}")
    idade_meta = calcular_idade_metabolica(st.session_state.idade, st.session_state.score)
    pdf_path = gerar_pdf_report(st.session_state.nome, st.session_state.score, st.session_state.m_label, st.session_state.idade, idade_meta)
    with open(pdf_path, "rb") as f:
        if st.download_button("📥 PDF Bericht herunterladen", f, file_name=pdf_path):
            salvar_log_evento("Baixou PDF", st.session_state.email)
    if st.button("🔬 ZUR LÖSUNG (VIDEO)"): st.session_state.pagina = 'bridge'; st.rerun()

# --- TELA: BRIDGE ---
elif st.session_state.pagina == 'bridge':
    st.markdown("""<link rel="preconnect" href="https://myslimsana.com"><link rel="dns-prefetch" href="https://myslimsana.com">""", unsafe_allow_html=True)
    st.write(f"Basierend auf Ihrem Index von {st.session_state.score}/100...")
    if st.button("🎥 VIDEO ANSEHEN"):
        salvar_log_evento("Clicou para VSL", st.session_state.email)
        with st.spinner("Video wird geladen..."):
            time.sleep(1.2)
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={LINK_AFILIADO}">', unsafe_allow_html=True)
