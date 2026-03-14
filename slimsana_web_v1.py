import streamlit as st
import pandas as pd
import time
import logging
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from streamlit_gsheets import GSheetsConnection

# -----------------------------
# CONFIGURAÇÃO DE LOG
# -----------------------------
def salvar_log_evento(evento, detalhe):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        params = st.query_params

        origem = params.get("utm_source", "direto")
        if isinstance(origem, list):
            origem = origem[0]

        cidade = params.get("utm_city", "Indefinida")
        if isinstance(cidade, list):
            cidade = cidade[0]

        novo_log = pd.DataFrame([{
            "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Origem": origem,
            "Evento": evento,
            "Detalhe": detalhe,
            "Cidade": cidade
        }])

        try:
            dados = conn.read(worksheet="Página1", ttl=0)
            df_final = pd.concat([dados, novo_log], ignore_index=True)
        except:
            df_final = novo_log

        conn.update(worksheet="Página1", data=df_final)

    except Exception as e:
        logging.exception("Erro ao salvar log")


# -----------------------------
# LÓGICA DE SCORE
# -----------------------------
def calcular_score():
    score = 78

    if st.session_state.get("res2") == "Ja":
        score -= 8
    elif st.session_state.get("res2") == "Manchmal":
        score -= 4

    if st.session_state.get("res5") == "Ja, sehr häufig":
        score -= 10
    elif st.session_state.get("res5") == "Manchmal":
        score -= 5

    if st.session_state.get("res4") == "Nach dem Mittagessen":
        score -= 4

    p_map = {
        "Bauchfett": 4,
        "Müdigkeit": 3,
        "Heißhunger": 5
    }

    score -= p_map.get(st.session_state.get("problem"), 0)

    return max(min(score, 85), 55)


# -----------------------------
# IDADE METABÓLICA
# -----------------------------
def calcular_idade_metabolica(idade_real, score):

    acrescimo = 2

    if score <= 58:
        acrescimo = 7
    elif score <= 62:
        acrescimo = 5
    elif score <= 66:
        acrescimo = 4
    elif score <= 70:
        acrescimo = 3

    return idade_real + acrescimo


# -----------------------------
# PERFIL METABÓLICO
# -----------------------------
def definir_label_metabolico():

    prob = st.session_state.get("problem")

    if prob == "Bauchfett":
        return "Typ A – Verlangsamter Stoffwechsel"

    elif prob == "Müdigkeit":
        return "Typ B – Energie-Dysbalance"

    else:
        return "Typ C – Hunger-Regulationsmuster"


def obter_detalhes_perfil(label):

    if "Typ A" in label:
        return {
            "desc": "Dieses Profil deutet auf eine reduzierte metabolische Aktivität hin.",
            "hinweise": [
                "langsamere Fettverbrennung",
                "geringere Energieverfügbarkeit"
            ]
        }

    elif "Typ B" in label:
        return {
            "desc": "Dieses Profil weist auf ein Ungleichgewicht in der Energieverteilung hin.",
            "hinweise": [
                "Energieabfall nach Mahlzeiten",
                "instabile Belastbarkeit"
            ]
        }

    else:
        return {
            "desc": "Dieses Profil deutet auf eine Dysbalance der Hunger-Regulation hin.",
            "hinweise": [
                "starke Heißhungerimpulse",
                "instabile Sättigung"
            ]
        }


# -----------------------------
# GERAR PDF
# -----------------------------
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

    c.roundRect(50, 570, 220, 55, 8)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(65, 608, "METABOLISCHER INDEX")

    c.setFont("Helvetica-Bold", 24)
    c.drawString(65, 582, f"{score}/100")

    c.setFont("Helvetica", 12)
    c.drawString(50, 550, f"Stoffwechsel-Profil: {label}")

    c.drawString(50, 530, f"Geschätztes Stoffwechsel-Alter: {idade_meta} Jahre")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 490, "2. Profilbeschreibung")

    text = c.beginText(50, 470)

    text.textLines(detalhes["desc"])
    text.textLine("")
    text.textLine("Typische Hinweise:")

    for h in detalhes["hinweise"]:
        text.textLine(f"- {h}")

    c.drawText(text)

    c.save()

    return file_name


# -----------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------
LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

st.set_page_config(
    page_title="BioReset Analysis",
    page_icon="🔬"
)


# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "mostrar_email" not in st.session_state:
    st.session_state.mostrar_email = False


# -----------------------------
# DETECTAR ORIGEM DO TRÁFEGO
# -----------------------------
if "pagina" not in st.session_state:

    utm_source = st.query_params.get("utm_source", "")

    if isinstance(utm_source, list):
        utm_source = utm_source[0]

    if utm_source in ["facebook", "instagram", "meta", "taboola", "outbrain"]:
        st.session_state.pagina = "advertorial"
    else:
        st.session_state.pagina = "home"


# -----------------------------
# ADVERTORIAL
# -----------------------------
if st.session_state.pagina == "advertorial":

    st.markdown(f"**Wissenschaft & Gesundheit | {datetime.now().strftime('%d.%m.%Y')}**")

    st.markdown("# Neuer 30-Sekunden-Test zeigt möglichen Stoffwechsel-Block ab 40")

    st.image(
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31"
    )

    if st.button("👉 JETZT 30-SEKUNDEN-TEST STARTEN", use_container_width=True):

        salvar_log_evento("Iniciou Quiz", "Advertorial")

        st.session_state.pagina = "quiz"

        st.rerun()


# -----------------------------
# QUIZ
# -----------------------------
elif st.session_state.pagina == "quiz":

    st.progress(st.session_state.step / 5)

    st.write(f"Frage {st.session_state.step} von 5")

    if st.session_state.step == 1:

        prob = st.selectbox(
            "Was ist Ihre größte Herausforderung?",
            ["Bauchfett", "Müdigkeit", "Heißhunger"]
        )

        if st.button("Weiter"):

            st.session_state.problem = prob
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:

        res2 = st.radio(
            "Haben Sie das Gefühl, dass Ihr Körper kaum auf Veränderungen reagiert?",
            ["Ja", "Manchmal", "Nein"]
        )

        if st.button("Weiter"):

            st.session_state.res2 = res2
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:

        nome_in = st.text_input("Ihr Vorname")

        idade = st.slider("Alter", 18, 80, 42)

        if st.button("Weiter"):

            st.session_state.nome = nome_in if nome_in else "Besucher"
            st.session_state.idade = idade
            st.session_state.step = 4
            st.rerun()

    elif st.session_state.step == 4:

        res4 = st.radio(
            "Wann fühlen Sie sich besonders energielos?",
            ["Morgens", "Nach dem Mittagessen", "Am späten Nachmittag", "Abends"]
        )

        if st.button("Weiter"):

            st.session_state.res4 = res4
            st.session_state.step = 5
            st.rerun()

    elif st.session_state.step == 5:

        res5 = st.radio(
            "Fällt Gewichtsabnahme schwer?",
            ["Ja, sehr häufig", "Manchmal", "Selten"]
        )

        if st.button("ANALYSE DURCHFÜHREN"):

            st.session_state.res5 = res5

            salvar_log_evento(
                "Quiz Concluído",
                st.session_state.get("nome", "Besucher")
            )

            with st.spinner("Analyse läuft..."):
                time.sleep(1.5)

            st.session_state.pagina = "optin"
            st.rerun()


# -----------------------------
# OPTIN
# -----------------------------
elif st.session_state.pagina == "optin":

    score = calcular_score()

    st.session_state.score = score

    st.metric("Metabolischer Index", f"{score}/100")

    if not st.session_state.mostrar_email:

        st.warning(
            "Ihre Analyse ist bereit. Klicken Sie unten, um den vollständigen Bericht freizuschalten."
        )

        if st.button("🔓 Vollständigen Bericht anzeigen"):

            st.session_state.mostrar_email = True
            st.rerun()

    else:

        email = st.text_input("E-Mail-Adresse")

        if st.button("📄 BERICHT FREISCHALTEN"):

            if re.match(r"[^@]+@[^@]+\.[^@]+", email):

                st.session_state.email = email

                salvar_log_evento("Lead Capturado", email)

                st.session_state.pagina = "report"

                st.rerun()


# -----------------------------
# REPORT
# -----------------------------
elif st.session_state.pagina == "report":

    nome = st.session_state.get("nome", "Besucher")

    st.success(f"Ihr Bericht ist fertig, {nome}!")

    idade_meta = calcular_idade_metabolica(
        st.session_state.idade,
        st.session_state.score
    )

    pdf = gerar_pdf_report(
        nome,
        st.session_state.score,
        definir_label_metabolico(),
        st.session_state.idade,
        idade_meta
    )

    with open(pdf, "rb") as f:

        st.download_button(
            "📥 PDF herunterladen",
            f,
            file_name=pdf
        )

    st.warning(
        f"Ihre Analyse zeigt einen Stoffwechsel-Index von nur {st.session_state.score} Punkten."
    )

    st.info(
        "Die vollständige Erklärung und mögliche Lösungsansätze sehen Sie im folgenden Video."
    )

    if st.button("🔬 ZUR LÖSUNG (VIDEO)"):

        salvar_log_evento(
            "Clicou para VSL",
            st.session_state.get("email", "no-email")
        )

        st.markdown(
            f'<meta http-equiv="refresh" content="0;URL={LINK_AFILIADO}">',
            unsafe_allow_html=True
        )
