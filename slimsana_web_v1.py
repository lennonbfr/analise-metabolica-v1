import streamlit as st
import time
from datetime import datetime

# ---------------------------------------------------
# CONFIGURAÇÃO INICIAL
# ---------------------------------------------------

LINK_AFILIADO = "https://myslimsana.com/slimsana-pdp-fe?aff=lennonbfr"

st.set_page_config(
    page_title="BioReset Analysis",
    page_icon="🔬",
    layout="centered"
)

# ---------------------------------------------------
# FUNÇÕES DE CÁLCULO
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

    p_map = {
        "Bauchfett": 4,
        "Müdigkeit": 3,
        "Heißhunger": 5
    }

    score -= p_map.get(st.session_state.get("problem"), 0)

    return max(min(score, 85), 55)


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
            "titulo": "Hinweise auf einen verlangsamten Stoffwechsel",
            "desc": (
                "Ihr Ergebnis deutet darauf hin, dass Ihr Körper möglicherweise "
                "langsamer auf Gewichtsveränderungen reagiert als üblich."
            ),
            "bullets": [
                "Fettverbrennung kann verlangsamt sein",
                "Bauchfett bleibt oft besonders hartnäckig",
                "Veränderungen zeigen sich meist erst spät"
            ]
        }

    elif "Typ B" in label:
        return {
            "titulo": "Hinweise auf eine Energie-Dysbalance",
            "desc": (
                "Ihr Ergebnis zeigt mögliche Anzeichen dafür, dass Ihr Energiehaushalt "
                "im Alltag nicht optimal reguliert ist."
            ),
            "bullets": [
                "stärkere Erschöpfung im Tagesverlauf",
                "niedriges Energiegefühl trotz normalem Alltag",
                "Belastbarkeit schwankt häufiger"
            ]
        }

    else:
        return {
            "titulo": "Hinweise auf ein Hunger-Regulationsmuster",
            "desc": (
                "Ihr Ergebnis deutet auf mögliche Auffälligkeiten bei Sättigung und "
                "Heißhunger hin."
            ),
            "bullets": [
                "wiederkehrende Heißhungerphasen",
                "instabiles Sättigungsgefühl",
                "mehr Appetit am Nachmittag oder Abend"
            ]
        }


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "pagina" not in st.session_state:
    utm_source = st.query_params.get("utm_source", "")
    if isinstance(utm_source, list):
        utm_source = utm_source[0]

    st.session_state.pagina = (
        "advertorial"
        if utm_source in ["facebook", "instagram", "meta", "taboola", "outbrain"]
        else "home"
    )

# ---------------------------------------------------
# ESTILO
# ---------------------------------------------------

st.markdown("""
    <style>
        .main > div {
            padding-top: 1.2rem;
        }
        .block-container {
            max-width: 760px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        .result-box {
            background: #f5f7fb;
            padding: 18px;
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            margin-bottom: 18px;
        }
        .warning-box {
            background: #fff7ed;
            padding: 16px;
            border-radius: 14px;
            border: 1px solid #fed7aa;
            margin: 16px 0;
        }
        .cta-box {
            background: #eff6ff;
            padding: 16px;
            border-radius: 14px;
            border: 1px solid #bfdbfe;
            margin-top: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TELA: ADVERTORIAL
# ---------------------------------------------------

if st.session_state.pagina == "advertorial":
    st.markdown(f"**Wissenschaft & Gesundheit | {datetime.now().strftime('%d.%m.%Y')}**")
    st.markdown("# Neuer 30-Sekunden-Test zeigt mögliche Stoffwechsel-Anzeichen ab 40")

    st.markdown("""
Viele Erwachsene bemerken mit der Zeit Veränderungen, die sie sich nicht richtig erklären können:

- **mehr Bauchfett** trotz normaler Ernährung  
- **weniger Energie** im Alltag  
- **Heißhunger am Nachmittag oder Abend**

Ein kurzer Test kann erste Hinweise darauf geben, welches Muster dahinterstecken könnte.
""")

    st.image(
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=1200&q=80",
        use_container_width=True
    )

    st.markdown("""
### Was Sie in diesem Test erfahren:
- welcher **Stoffwechsel-Typ** bei Ihnen wahrscheinlicher ist
- wie Ihr Ergebnis im Vergleich zu Ihrer Altersgruppe aussieht
- welche nächsten Schritte häufig empfohlen werden
""")

    if st.button("👉 TEST IN 30 SEKUNDEN STARTEN", use_container_width=True):
        st.session_state.step = 1
        st.session_state.pagina = "quiz"
        st.rerun()

# ---------------------------------------------------
# TELA: HOME
# ---------------------------------------------------

elif st.session_state.pagina == "home":
    st.markdown("# 🔬 BioReset Stoffwechsel-Analyse")
    st.image(
        "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=1200&q=80",
        use_container_width=True
    )

    st.markdown("""
Finden Sie in weniger als einer Minute heraus, welche Hinweise Ihr Körper aktuell zeigt.

Der Test ist kostenlos und liefert eine kurze persönliche Auswertung.
""")

    if st.button("JETZT ANALYSE STARTEN", use_container_width=True):
        st.session_state.step = 1
        st.session_state.pagina = "quiz"
        st.rerun()

# ---------------------------------------------------
# TELA: QUIZ
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
            submitted = st.form_submit_button("Weiter")
            if submitted:
                st.session_state.problem = prob
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        if st.session_state.problem == "Bauchfett":
            pergunta = "Haben Sie das Gefühl, dass Ihr Körper trotz Bemühungen kaum reagiert?"
        elif st.session_state.problem == "Müdigkeit":
            pergunta = "Fühlen Sie sich tagsüber oft erschöpft, obwohl Sie ausreichend schlafen?"
        else:
            pergunta = "Haben Sie besonders am Nachmittag oder Abend starke Heißhungerphasen?"

        with st.form("q2"):
            res2 = st.radio(pergunta, ["Ja", "Manchmal", "Nein"])
            submitted = st.form_submit_button("Weiter")
            if submitted:
                st.session_state.res2 = res2
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        with st.form("q3"):
            idade = st.slider("Wie alt sind Sie?", 18, 80, 42)
            res3 = st.radio(
                "Fällt es Ihnen schwer, Gewicht zu verlieren?",
                ["Ja, sehr häufig", "Manchmal", "Selten"]
            )

            submitted = st.form_submit_button("ANALYSE ANZEIGEN")
            if submitted:
                st.session_state.idade = idade
                st.session_state.res3 = res3
                st.session_state.pagina = "analyzing"
                st.rerun()

# ---------------------------------------------------
# TELA: ANALYZING
# ---------------------------------------------------

elif st.session_state.pagina == "analyzing":
    with st.status("🧬 Analyse wird vorbereitet...", expanded=True) as s:
        time.sleep(0.8)
        s.update(label="🧬 Ergebnisse werden abgeglichen...", state="running")
        time.sleep(0.8)
        s.update(label="✅ Analyse abgeschlossen", state="complete")

    st.session_state.pagina = "result"
    st.rerun()

# ---------------------------------------------------
# TELA: RESULTADO
# ---------------------------------------------------

elif st.session_state.pagina == "result":
    score = calcular_score()
    label = definir_label_metabolico()
    idade_meta = calcular_idade_metabolica(st.session_state.idade, score)
    detalhes = obter_detalhes_perfil(label)

    st.session_state.score = score
    st.session_state.m_label = label

    st.success("Ihre Auswertung ist fertig.")

    st.metric("Metabolischer Index", f"{score}/100")
    st.progress(score / 100)

    st.caption(
        f"Vergleichswert für Alter {st.session_state.idade-2}-{st.session_state.idade+3}: ca. 74/100"
    )

    st.markdown(
        f"""
        <div class="result-box">
            <h4 style="margin-top:0;">{detalhes["titulo"]}</h4>
            <p>{detalhes["desc"]}</p>
            <p><strong>Stoffwechsel-Profil:</strong> {label}</p>
            <p><strong>Geschätztes Stoffwechsel-Alter:</strong> {idade_meta} Jahre</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### Auffälligkeiten, die häufig zu diesem Ergebnis passen:")
    for bullet in detalhes["bullets"]:
        st.markdown(f"- {bullet}")

    st.markdown(
        f"""
        <div class="warning-box">
            <strong>Hinweis:</strong> Ihr Ergebnis zeigt, dass es sinnvoll sein kann,
            gezielte Maßnahmen zur Unterstützung des Stoffwechsels anzusehen.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="cta-box">
            Im nächsten Schritt sehen Sie eine kurze Erklärung dazu,
            welche Vorgehensweise in solchen Fällen häufig empfohlen wird.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Test wiederholen", use_container_width=True):
            st.session_state.step = 1
            st.session_state.pagina = "quiz"
            st.rerun()

    with col2:
        if st.button("👉 EMPFEHLUNG ANSEHEN", use_container_width=True):
            st.session_state.pagina = "bridge"
            st.rerun()

# ---------------------------------------------------
# TELA: BRIDGE
# ---------------------------------------------------

elif st.session_state.pagina == "bridge":
    st.markdown(
        """<link rel="preconnect" href="https://myslimsana.com">
           <link rel="dns-prefetch" href="https://myslimsana.com">""",
        unsafe_allow_html=True
    )

    st.warning(
        f"Ihr Ergebnis von {st.session_state.score}/100 deutet darauf hin, "
        f"dass Ihr Stoffwechsel aktuell möglicherweise nicht optimal arbeitet."
    )

    st.markdown("""
Viele Menschen mit einem ähnlichen Ergebnis suchen im nächsten Schritt nach einer einfachen Möglichkeit,
ihren Stoffwechsel gezielt zu unterstützen.

Im folgenden Video wird erklärt, welcher Ansatz dafür häufig genutzt wird.
""")

    st.link_button(
        "🎥 VIDEO JETZT ANSEHEN",
        LINK_AFILIADO,
        use_container_width=True
    )
