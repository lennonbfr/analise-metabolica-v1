import streamlit as st
import time
from datetime import datetime

# ---------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------

LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

st.set_page_config(
    page_title="BioReset Analyse",
    page_icon="🔬",
    layout="centered"
)

# ---------------------------------------------------
# CSS
# ---------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

.block-container {
    max-width: 760px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, h4, h5, h6, p, li, label, div, span {
    color: white;
}

.result-box {
    background: #1e293b;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 18px;
    color: white;
}

.warning-box {
    background: #3b2f1d;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #92400e;
    color: #fde68a;
    margin-top: 16px;
}

.cta-box {
    background: #1e3a5f;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #2563eb;
    margin-top: 16px;
    color: #bfdbfe;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------

def calcular_score():
    score = 78

    if st.session_state.get("res2") == "Ja":
        score -= 8
    elif st.session_state.get("res2") == "Manchmal":
        score -= 4

    if st.session_state.get("res3") == "Ja, sehr häufig":
        score -= 10
    elif st.session_state.get("res3") == "Manchmal":
        score -= 5

    mapa = {
        "Bauchfett": 4,
        "Müdigkeit": 3,
        "Heißhunger": 5
    }

    score -= mapa.get(st.session_state.get("problem"), 0)
    return max(min(score, 85), 55)


def calcular_idade_metabolica(idade, score):
    acrescimo = 2

    if score <= 58:
        acrescimo = 7
    elif score <= 62:
        acrescimo = 5
    elif score <= 66:
        acrescimo = 4
    elif score <= 70:
        acrescimo = 3

    return idade + acrescimo


def definir_perfil():
    prob = st.session_state.get("problem", "")

    if prob == "Bauchfett":
        return "Typ A – Verlangsamter Stoffwechsel"
    elif prob == "Müdigkeit":
        return "Typ B – Energie-Dysbalance"
    else:
        return "Typ C – Hunger-Regulation"


def obter_bullets():
    prob = st.session_state.get("problem", "")

    if prob == "Bauchfett":
        return [
            "Fettverbrennung kann verlangsamt sein",
            "Bauchfett bleibt oft besonders hartnäckig",
            "Veränderungen zeigen sich meist erst spät"
        ]
    elif prob == "Müdigkeit":
        return [
            "Energie fällt im Tagesverlauf spürbar ab",
            "normale Routinen fühlen sich anstrengender an",
            "Belastbarkeit schwankt häufiger"
        ]
    else:
        return [
            "Heißhunger tritt am Nachmittag oder Abend häufiger auf",
            "Sättigungsgefühl bleibt nicht lange stabil",
            "Appetit ist schwerer kontrollierbar"
        ]


def obter_titulo_resultado():
    prob = st.session_state.get("problem", "")

    if prob == "Bauchfett":
        return "Hinweise auf einen verlangsamten Stoffwechsel"
    elif prob == "Müdigkeit":
        return "Hinweise auf eine mögliche Energie-Dysbalance"
    else:
        return "Hinweise auf ein mögliches Hunger-Regulationsmuster"


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "pagina" not in st.session_state:
    utm = st.query_params.get("utm_source", "")
    if isinstance(utm, list):
        utm = utm[0]

    if utm in ["facebook", "instagram", "meta", "taboola", "outbrain"]:
        st.session_state.pagina = "advertorial"
    else:
        st.session_state.pagina = "home"

if "step" not in st.session_state:
    st.session_state.step = 1

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if st.session_state.pagina == "home":
    st.markdown(f"**BioReset Analyse | {datetime.now().strftime('%d.%m.%Y')}**")
    st.title("Kostenloser Stoffwechsel-Test in 30 Sekunden")

    st.write("""
Viele Menschen bemerken mit der Zeit Veränderungen wie:

- **mehr Bauchfett**
- **weniger Energie**
- **häufiger Heißhunger**
""")

    st.write("""
Mit diesem kurzen Test erhalten Sie eine erste Einschätzung,
welches Stoffwechsel-Muster bei Ihnen wahrscheinlicher ist.
""")

    if st.button("👉 JETZT TEST STARTEN", use_container_width=True):
        st.session_state.pagina = "quiz"
        st.session_state.step = 1
        st.rerun()

# ---------------------------------------------------
# ADVERTORIAL
# ---------------------------------------------------

elif st.session_state.pagina == "advertorial":
    st.markdown(f"**Wissenschaft & Gesundheit | {datetime.now().strftime('%d.%m.%Y')}**")
    st.title("Neuer 30-Sekunden-Test zeigt mögliche Stoffwechsel-Blockade ab 40")

    st.write("""
Viele Menschen bemerken plötzlich Veränderungen:

- **mehr Bauchfett** trotz normaler Ernährung
- **weniger Energie im Alltag**
- **Heißhunger am Nachmittag**
""")

    st.write("""
Ein kurzer Test kann Hinweise darauf geben,
welches Stoffwechsel-Muster dahinterstecken könnte.
""")

    st.image(
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=1200&q=80",
        use_container_width=True
    )

    st.write("""
### Dieser Test zeigt Ihnen:

- welches **Stoffwechsel-Profil** wahrscheinlicher ist
- wie Ihr Ergebnis im Vergleich zu Ihrer Altersgruppe aussieht
- welche Maßnahmen häufig empfohlen werden
""")

    if st.button("👉 TEST IN 30 SEKUNDEN STARTEN", use_container_width=True):
        st.session_state.pagina = "quiz"
        st.session_state.step = 1
        st.rerun()

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------

elif st.session_state.pagina == "quiz":
    st.write(f"Frage {st.session_state.step} von 3")
    st.progress(st.session_state.step / 3)

    if st.session_state.step == 1:
        with st.form("q1"):
            prob = st.selectbox(
                "Was ist aktuell Ihre größte Herausforderung?",
                ["Bauchfett", "Müdigkeit", "Heißhunger"]
            )

            if st.form_submit_button("Weiter"):
                st.session_state.problem = prob
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        pergunta = {
            "Bauchfett": "Reagiert Ihr Körper kaum auf Diät oder Sport?",
            "Müdigkeit": "Fühlen Sie sich tagsüber häufig erschöpft?",
            "Heißhunger": "Haben Sie starke Heißhunger-Phasen?"
        }[st.session_state.problem]

        with st.form("q2"):
            res = st.radio(pergunta, ["Ja", "Manchmal", "Nein"])

            if st.form_submit_button("Weiter"):
                st.session_state.res2 = res
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        with st.form("q3"):
            idade = st.slider("Wie alt sind Sie?", 18, 80, 42)
            res3 = st.radio(
                "Fällt es Ihnen schwer Gewicht zu verlieren?",
                ["Ja, sehr häufig", "Manchmal", "Selten"]
            )

            if st.form_submit_button("ANALYSE ANZEIGEN"):
                st.session_state.idade = idade
                st.session_state.res3 = res3
                st.session_state.pagina = "analysing"
                st.rerun()

# ---------------------------------------------------
# ANALYSING
# ---------------------------------------------------

elif st.session_state.pagina == "analysing":
    with st.spinner("Analyse läuft..."):
        time.sleep(1.2)

    st.session_state.pagina = "result"
    st.rerun()

# ---------------------------------------------------
# RESULTADO
# ---------------------------------------------------

elif st.session_state.pagina == "result":
    score = calcular_score()
    perfil = definir_perfil()
    idade_meta = calcular_idade_metabolica(st.session_state.idade, score)
    titulo_resultado = obter_titulo_resultado()
    bullets = obter_bullets()

    st.success("Ihre Analyse ist fertig.")
    st.metric("Metabolischer Index", f"{score}/100")
    st.progress(score / 100)

    st.caption(
        f"Vergleichswert für Alter {st.session_state.idade-2}-{st.session_state.idade+3}: ca. 74/100"
    )

    st.markdown(f"""
    <div class="result-box">
        <h3 style="margin-top:0; color:white;">{titulo_resultado}</h3>
        <p style="color:white;">
            Ihr Ergebnis deutet darauf hin, dass Ihr Körper möglicherweise
            langsamer auf Veränderungen reagiert als üblich.
        </p>
        <p style="color:white;"><strong>Stoffwechsel-Profil:</strong> {perfil}</p>
        <p style="color:white;"><strong>Geschätztes Stoffwechsel-Alter:</strong> {idade_meta} Jahre</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Auffälligkeiten, die häufig zu diesem Ergebnis passen:")
    for item in bullets:
        st.markdown(f"- {item}")

    st.markdown("""
    <div class="warning-box">
        Ihr Ergebnis zeigt Hinweise darauf, dass gezielte Maßnahmen zur Unterstützung
        des Stoffwechsels sinnvoll sein könnten.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="cta-box">
        Im nächsten Schritt sehen Sie eine kurze Erklärung, welche Methode viele
        Menschen in dieser Situation nutzen.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Test wiederholen", use_container_width=True):
            st.session_state.step = 1
            st.session_state.pagina = "quiz"
            st.rerun()

    with col2:
        if st.button("👉 ERKLÄRUNG JETZT ANSEHEN", use_container_width=True):
            st.session_state.pagina = "bridge"
            st.rerun()

# ---------------------------------------------------
# BRIDGE
# ---------------------------------------------------

elif st.session_state.pagina == "bridge":
    st.warning(f"Ihr Stoffwechsel-Index liegt bei {calcular_score()}/100.")

    st.write("""
Viele Menschen mit ähnlichem Ergebnis berichten,
dass ihr Körper erst reagierte, nachdem sie einen
bestimmten Stoffwechsel-Ansatz ausprobiert haben.
""")

    st.write("""
Im folgenden Video wird erklärt,
welche Methode derzeit viel Aufmerksamkeit bekommt.
""")

    st.link_button(
        "🎥 VIDEO ZUR LÖSUNG ANSEHEN",
        LINK_AFILIADO,
        use_container_width=True
    )
