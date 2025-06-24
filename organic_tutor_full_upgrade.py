import streamlit as st
from io import BytesIO
import base64
import time
import datetime
import random
import requests

# Safe Lottie import with error handling
LOTTIE_ENABLED = True
try:
    from streamlit_lottie import st_lottie
except ImportError:
    LOTTIE_ENABLED = False
    st.warning("Lottie animations disabled - install with: pip install streamlit-lottie")

def load_lottie(url):
    if not LOTTIE_ENABLED:
        return None
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

correct_anim = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jbrw3hcz.json")
wrong_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jv60fnyj.json")

# Initialize session state
if "visited" not in st.session_state:
    st.session_state.visited = set()
if "achievements" not in st.session_state:
    st.session_state.achievements = set()
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "game_score" not in st.session_state:
    st.session_state.game_score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_visit" not in st.session_state:
    st.session_state.last_visit = None

# App setup
st.set_page_config(page_title="Organic Chemistry Tutor", page_icon="🧪", layout="wide")

# Sidebar setup
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Chemical_structure.svg/1024px-Chemical_structure.svg.png", width=100)
st.sidebar.title("🧪 Chemistry Tutor")

# Theme Switcher
theme_choice = st.sidebar.selectbox("🎨 Theme", ["Light", "Dark", "Neon"])
themes = {
    "Light": {"bg": "#ffffff", "fg": "#000000"},
    "Dark": {"bg": "#0e1117", "fg": "#f0f0f0"},
    "Neon": {"bg": "#141414", "fg": "#39ff14"}
}
bg, fg = themes[theme_choice]["bg"], themes[theme_choice]["fg"]
st.markdown(f"""
<style>
body, .stApp {{
    background-color: {bg} !important;
    color: {fg} !important;
}}
</style>
""", unsafe_allow_html=True)

# Fun Fact
fun_facts = [
    "💧 Water expands when it freezes.",
    "🧪 Diamond and graphite are both carbon.",
    "📜 The letter 'J' isn't in the periodic table.",
    "🌡️ Mercury is a liquid metal at room temp!",
    "🌍 Astatine is Earth's rarest element."
]
st.sidebar.markdown(f"💡 **Fun Fact:** {random.choice(fun_facts)}")

menu = st.sidebar.selectbox("Choose a topic", [
    "🏠 Home",
    "🧬 Functional Groups",
    "🔤 IUPAC Naming",
    "📈 Homologous Series",
    "🔀 Isomers",
    "🧠 Quiz",
    "📩 Feedback", 
    "📅 Daily Challenge",   
    "📘 SS2 Glossary",
    "🎮 Name It Fast"
])

# Track visited sections
st.session_state.visited.add(menu)

# Home Page
if menu == "🏠 Home":
    st.title("🏠 Welcome to Organic Chemistry Tutor")
    st.markdown("""
    This app helps SS2 students master key concepts in organic chemistry:
    - 🧬 Functional Groups  
    - 🔤 IUPAC Naming  
    - 📈 Homologous Series  
    - 🔀 Isomers  
    - 🧠 Quiz  
    - 📩 Feedback
    - 📅 Daily Challenge
    - 📘 SS2 Glossary    
    - 🎮 Name It Fast
    """)

# Quiz Section
elif menu == "🧠 Quiz":
    st.title("🧠 Organic Chemistry Quiz")
    
    questions = [
        {"q":"General formula for alkanes?", "a":"CₙH₂ₙ₊₂", "opts":["CₙH₂ₙ", "CₙH₂ₙ₊₂", "CₙH₂ₙ₋₂"]},
        {"q":"Functional group in ethanol?", "a":"Alcohol", "opts":["Alkane", "Alcohol", "Ester"]},
        {"q":"Triple bond compound?", "a":"Alkyne", "opts":["Alkane", "Alkene", "Alkyne"]},
        {"q":"Suffix for aldehyde?", "a":"-al", "opts":["-ol", "-al", "-one"]},
        {"q":"Which is a carboxylic acid?", "a":"CH3COOH", "opts":["CH3OH", "CH3CH3", "CH3COOH"]},
    ]

    # Initialize quiz state
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {
            "start_time": None,
            "score": 0,
            "answers": {},
            "submitted": [False] * len(questions)
        }

    # Start quiz
    if st.button("🚀 Start Quiz") and not st.session_state.quiz_data["start_time"]:
        st.session_state.quiz_data = {
            "start_time": time.time(),
            "score": 0,
            "answers": {},
            "submitted": [False] * len(questions)
        }

    # Quiz timer
    if st.session_state.quiz_data["start_time"]:
        elapsed = time.time() - st.session_state.quiz_data["start_time"]
        remaining = max(60 - int(elapsed), 0)
        st.info(f"⏱ Time remaining: {remaining} seconds")

    # Display questions
    for i, q in enumerate(questions):
        st.subheader(f"{i+1}. {q['q']}")
        
        if not st.session_state.quiz_data["submitted"][i]:
            user_answer = st.radio("Choose one:", q["opts"], key=f"quiz_{i}")
            
            if st.button(f"Submit Answer {i+1}"):
                st.session_state.quiz_data["answers"][i] = user_answer
                st.session_state.quiz_data["submitted"][i] = True
                
                if user_answer == q["a"]:
                    st.success("✅ Correct!")
                    st.session_state.quiz_data["score"] += 1
                    if LOTTIE_ENABLED and correct_anim:
                        st_lottie(correct_anim, height=150)
                else:
                    st.error(f"❌ Incorrect. The correct answer is: {q['a']}")
                    if LOTTIE_ENABLED and wrong_anim:
                        st_lottie(wrong_anim, height=150)

    # Display score
    st.markdown(f"### 🏁 Score: {st.session_state.quiz_data['score']}/{len(questions)}")

# [Rest of your menu options (Functional Groups, IUPAC Naming, etc.) go here...]

# Achievements and footer
with st.sidebar.expander("🏅 Achievements"):
    if st.session_state.achievements:
        for badge in st.session_state.achievements:
            st.success(f"🏅 {badge}")
    else:
        st.info("No achievements yet. Explore more sections!")
    st.markdown(f"📅 Streak: {st.session_state.streak} days")

st.markdown("""
<style>
button { margin-top: 10px; }
div[data-testid="stExpander"] > div { padding: 10px; }
</style>
""", unsafe_allow_html=True)
