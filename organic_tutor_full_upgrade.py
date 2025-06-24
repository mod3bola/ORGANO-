import streamlit as st
from io import BytesIO
import base64

def play_sound(file):
    try:
        with open(file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
    except:
        pass

from streamlit_lottie import st_lottie
import requests

def load_lottie(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Lottie animations
correct_anim = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jbrw3hcz.json")
wrong_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jv60fnyj.json")

# Initialize session state
if "visited" not in st.session_state:
    st.session_state["visited"] = set()
if "achievements" not in st.session_state:
    st.session_state["achievements"] = set()
if "quiz_score" not in st.session_state:
    st.session_state["quiz_score"] = 0

# App setup
st.set_page_config(page_title="Organic Chemistry Tutor", page_icon="🧪", layout="wide")

# Sidebar setup
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Chemical_structure.svg/1024px-Chemical_structure.svg.png", width=100)
st.sidebar.title("🧪 Chemistry Tutor")

# 🌈 Theme Switcher
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

# 💬 Fun Fact
import random
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
st.session_state["visited"].add(menu)

# 🏠 HOME PAGE
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
    
Use it to study, revise, or explore chemical structures interactively!
""")

# [Rest of your menu sections remain exactly the same...]
# All other menu options (Functional Groups, IUPAC Naming, etc.) remain unchanged
# Only the QR code generation in the Home section has been removed

# [Rest of your file remains exactly the same...]
