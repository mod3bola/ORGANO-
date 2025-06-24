import streamlit as st
from io import BytesIO
import base64

# ====================== LOTTIE ANIMATION SETUP ======================
# Safe import with error handling
LOTTIE_ENABLED = True
try:
    from streamlit_lottie import st_lottie
except ImportError:
    LOTTIE_ENABLED = False
    st.warning(
        "Lottie animations disabled - 'streamlit-lottie' package not installed.\n"
        "Install with: pip install streamlit-lottie"
    )

def load_lottie(url):
    """Safe Lottie animation loader with fallback"""
    if not LOTTIE_ENABLED:
        return None
        
    try:
        import requests
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        st.warning(f"Couldn't load Lottie animation: {str(e)}")
        return None

# Initialize animations with fallback
correct_anim = load_lottie("https://assets4.lottiefiles.com/packages/lf20_jbrw3hcz.json") if LOTTIE_ENABLED else None
wrong_anim = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jv60fnyj.json") if LOTTIE_ENABLED else None

def show_lottie_animation(animation, height=150):
    """Safe animation display with fallback"""
    if LOTTIE_ENABLED and animation:
        st_lottie(animation, height=height)
    return None
# ====================== END LOTTIE SETUP ======================

# Rest of your imports...
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
        st.warning(f"Couldn't play sound: {str(e)}")

# ... [rest of your existing code] ...

# In your quiz section, replace animation calls with:
if user_answer == q["a"]:
    st.success("✅ Correct!")
    st.session_state["quiz_score"] += 1
    show_lottie_animation(correct_anim)
    play_sound("correct.mp3")
else:
    st.error(f"❌ Wrong. Correct answer: {q['a']}")
    show_lottie_animation(wrong_anim)
    play_sound("wrong.mp3")
