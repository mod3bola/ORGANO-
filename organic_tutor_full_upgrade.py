import streamlit as st
from io import BytesIO
import base64

# Import streamlit_lottie with error handling
try:
    from streamlit_lottie import st_lottie
    LOTTIE_ENABLED = True
except ImportError:
    LOTTIE_ENABLED = False
    st.warning("Lottie animations disabled - 'streamlit-lottie' package not installed. "
              "Install with: pip install streamlit-lottie")

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

# Lottie animations with fallback
def load_lottie(url):
    if not LOTTIE_ENABLED:
        return None
        
    try:
        import requests
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        st.warning(f"Couldn't load Lottie animation: {e}")
        return None

# Initialize animations with fallback
correct_anim = None
wrong_anim = None
if LOTTIE_ENABLED:
    correct_anim = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jbrw3hcz.json")
    wrong_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jv60fnyj.json")
