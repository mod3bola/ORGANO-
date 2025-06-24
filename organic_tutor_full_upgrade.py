import streamlit as st
from io import BytesIO
import base64
import sys
import importlib

# First try to import qrcode with error handling
try:
    import qrcode
    from PIL import Image  # Verify Pillow is available
except ImportError as e:
    st.error(f"Missing required package: {e}")
    st.info("Please install with: pip install qrcode[pil]")
    st.stop()

def play_sound(file):
    try:
        with open(file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Couldn't play sound: {e}")

# Rest of your imports
from streamlit_lottie import st_lottie
import requests
import random
import time
import datetime

def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except requests.RequestException:
        return None

# Lottie animations
correct_anim = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jbrw3hcz.json")
wrong_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jv60fnyj.json")

# Initialize session state with proper checks
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
try:
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Chemical_structure.svg/1024px-Chemical_structure.svg.png", 
                   width=100)
except Exception as e:
    st.sidebar.warning(f"Couldn't load sidebar image: {e}")

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
    """)
    
    # QR Code Generation with error handling
    st.subheader("📱 Scan to open this app:")
    try:
        qr = qrcode.make("https://org-chem-tutor-f9xcxbghjkvxkyutiwixwr.streamlit.app/")
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=200)
    except Exception as e:
        st.error(f"Couldn't generate QR code: {e}")
        st.info("Please ensure qrcode and Pillow are properly installed")

# [Rest of your menu sections remain unchanged...]

# Achievements tracking
if "🧠 Quiz" in st.session_state.visited and getattr(st.session_state, "quiz_score", 0) >= 3:
    st.session_state.achievements.add("🧠 Quiz Master")

if len(st.session_state.visited) >= 5:
    st.session_state.achievements.add("🧭 Explorer")

if getattr(st.session_state, "Daily_Challenge_Score", 0) >= 1:
    st.session_state.achievements.add("🔥 Daily Winner")

# 🎁 Daily Streak Badge
today = datetime.date.today()
last_day = st.session_state.get("last_visit")
streak = st.session_state.get("streak", 0)

if last_day != today:
    if last_day and last_day == today - datetime.timedelta(days=1):
        streak += 1
    else:
        streak = 1
    st.session_state.streak = streak
    st.session_state.last_visit = today

if streak >= 3:
    st.session_state.achievements.add("🔥 3-Day Streaker")

with st.sidebar.expander("🏅 Achievements"):
    if st.session_state.achievements:
        for badge in sorted(st.session_state.achievements):
            st.success(f"🏅 {badge}")
    else:
        st.info("No achievements yet. Explore more sections!")
    
    st.markdown(f"📅 **Streak:** {streak} day(s)")

# CSS Styling
st.markdown("""
<style>
button[kind="primary"] {
    background: linear-gradient(90deg, #29b6f6, #42a5f5);
    color: white;
    font-weight: bold;
    transition: 0.3s;
}
button[kind="primary"]:hover {
    background: linear-gradient(90deg, #42a5f5, #1e88e5);
}
div[data-testid="stExpander"] > summary {
    transition: 0.3s ease;
}
div[data-testid="stExpander"] > summary:hover {
    background-color: #e3f2fd;
}
</style>
""", unsafe_allow_html=True)
