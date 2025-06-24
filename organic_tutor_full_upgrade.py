import streamlit as st
from io import BytesIO
import qrcode
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
    "📘 SS2 Glossary"       
    "🎮 Name It Fast"
])

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
    st.subheader("📱 Scan to open this app:")
    qr = qrcode.make("https://org-chem-tutor-f9xcxbghjkvxkyutiwixwr.streamlit.app/")
    buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=200)

# 🧬 FUNCTIONAL GROUPS
elif menu == "🧬 Functional Groups":
    st.title("🧬 Functional Groups")

    groups = {
        "Alkane": ["C–C", "Ethane (C2H6)", "https://chem.libretexts.org/@api/deki/files/11080/alkane.png"],
        "Alkene": ["C=C", "Ethene (C2H4)", "https://chem.libretexts.org/@api/deki/files/11081/alkene.png"],
        "Alkyne": ["C≡C", "Ethyne (C2H2)", "https://chem.libretexts.org/@api/deki/files/11082/alkyne.png"],
        "Alcohol": ["-OH", "Ethanol (C2H5OH)", "https://www.chemguide.co.uk/organicprops/alcohols/ethanolmolec.png"],
        "Aldehyde": ["-CHO", "Ethanal (CH3CHO)", "https://chem.libretexts.org/@api/deki/files/11084/aldehyde.png"],
        "Ketone": ["C=O", "Propanone (CH3COCH3)", "https://chem.libretexts.org/@api/deki/files/11085/ketone.png"],
        "Carboxylic Acid": ["-COOH", "Ethanoic acid (CH3COOH)", "https://chem.libretexts.org/@api/deki/files/11086/carboxylicacid.png"],
        "Ester": ["-COO-", "Methyl ethanoate", "https://chem.libretexts.org/@api/deki/files/11087/ester.png"],
        "Amine": ["-NH2", "Methylamine (CH3NH2)", "https://chem.libretexts.org/@api/deki/files/11088/amine.png"]
    }

    for name, (group, example, img_url) in groups.items():
        with st.expander(name):
            st.image(img_url, width=300, caption=f"{example} structure")
            st.markdown(f"**Group:** `{group}`")
            st.markdown(f"**Example:** {example}")

# 🔤 IUPAC NAMING
elif menu == "🔤 IUPAC Naming":
    st.title("🔤 IUPAC Naming of Compounds")
    st.markdown("Enter a common organic compound formula to identify its IUPAC name.")

    examples = {
        "CH3CH2OH": "Ethanol – Alcohol with two carbon atoms.",
        "CH3COOH": "Ethanoic Acid – Carboxylic acid with two carbon atoms.",
        "CH4": "Methane – Simplest alkane.",
        "C2H4": "Ethene – Two-carbon alkene.",
        "C2H2": "Ethyne – Two-carbon alkyne.",
        "CH3CHO": "Ethanal – Aldehyde with two carbon atoms."
    }

    user_input = st.text_input("Enter formula (e.g. CH3COOH):")
    if user_input:
        st.info(examples.get(user_input.strip(), "❌ Not in database. Try a common organic compound."))

# 📈 HOMOLOGOUS SERIES
elif menu == "📈 Homologous Series":
    st.title("📈 Homologous Series")
    st.markdown("Homologous series share the same functional group and follow a pattern.")

    n = st.slider("Select the number of carbon atoms (n):", 1, 10, 1)
    st.markdown(f"- **Alkane** → C{n}H{2*n + 2}")
    st.markdown(f"- **Alkene** → C{n}H{2*n}")
    st.markdown(f"- **Alkyne** → {'Invalid for n < 2' if n < 2 else f'C{n}H{2*n - 2}'}")
    st.markdown(f"- **Alcohol** → C{n}H{2*n + 1}OH")

# 🔀 ISOMERS
elif menu == "🔀 Isomers":
    st.title("🔀 Meet the Twins: Isomers Explained")
    st.markdown("""
**Isomers** have the **same molecular formula** but **different structures or arrangements**.

### 🧱 Structural Isomers:
- **Chain Isomers** – Butane vs Isobutane
- **Position Isomers** – Butan-1-ol vs Butan-2-ol
- **Functional Isomers** – Alcohol vs Ether

![Chain Isomers](https://chem.libretexts.org/@api/deki/files/11070/clipboard_e0d7a06c176445c5ef94eec70d233c259.png)

---

### 🔄 Stereoisomers:
- **Geometric Isomers** – cis-but-2-ene vs trans-but-2-ene
- **Optical Isomers** – Lactic acid mirror images

![Cis-Trans](https://www.chemistrysteps.com/wp-content/uploads/2020/07/Cis-and-Trans-Isomers.png)

| Type       | Description                  | Example                 |
|------------|------------------------------|--------------------------|
| Chain      | Carbon skeleton differences   | Butane vs Isobutane      |
| Position   | Group position changes        | Butan-1-ol vs Butan-2-ol |
| Functional | Functional group differences  | Alcohol vs Ether         |
| Geometric  | Spatial arrangement (double bond) | Cis vs Trans Butene  |
| Optical    | Non-superimposable mirror images | Lactic acid isomers  |
""")

# 🧠 QUIZ
elif menu == "🧠 Quiz":
    st.title("🧠 Organic Chemistry Quiz")

    questions = [
        {"q":"General formula for alkanes?", "a":"CₙH₂ₙ₊₂", "opts":["CₙH₂ₙ", "CₙH₂ₙ₊₂", "CₙH₂ₙ₋₂"]},
        {"q":"Functional group in ethanol?", "a":"Alcohol", "opts":["Alkane", "Alcohol", "Ester"]},
        {"q":"Triple bond compound?", "a":"Alkyne", "opts":["Alkane", "Alkene", "Alkyne"]},
        {"q":"Suffix for aldehyde?", "a":"-al", "opts":["-ol", "-al", "-one"]},
        {"q":"Which is a carboxylic acid?", "a":"CH3COOH", "opts":["CH3OH", "CH3CH3", "CH3COOH"]},
    ]


    import time
    if "quiz_start_time" not in st.session_state:
        if st.button("🚀 Start Timed Quiz"):
            st.session_state["quiz_start_time"] = time.time()
            st.experimental_rerun()

    if "quiz_start_time" in st.session_state:
        elapsed = int(time.time() - st.session_state["quiz_start_time"])
        remaining = 60 - elapsed
        if remaining > 0:
            st.info(f"⏱ Time remaining: {remaining} seconds")

    score = 0
    for i, q in enumerate(questions):
        st.subheader(f"{i+1}. {q['q']}")
        user_answer = st.radio("Choose one:", q["opts"], key=i, index=None)
        if user_answer:
            
                if user_answer == q["a"]:
                    st.success("✅ Correct!")
                    st.session_state["score"] += 1
                    st_lottie(correct_anim, height=150)
                    play_sound("correct.mp3")
                else:
                    st.error(f"❌ Wrong. Correct answer: {q['a']}")
                    st_lottie(wrong_anim, height=150)
                    play_sound("wrong.mp3")


    st.markdown(f"### 🏁 Final Score: **{score}/{len(questions)}**")

# 📩 FEEDBACK
elif menu == "📩 Feedback":
    st.title("📩 Feedback & Suggestions")
    st.markdown("We’d love to hear from you. Please fill out this short form:")
    st.components.v1.iframe(
        "https://docs.google.com/forms/d/e/1FAIpQLSdZrs0rEmICl64s8OebmvbB4T-6qf4V8O4T2vKo2CFqFi6sjw/viewform?embedded=true",
        height=700
    )

elif menu == "📅 Daily Challenge":
    st.title("📅 Daily Challenge")
    import datetime
    today = datetime.date.today()
    seed = today.toordinal()
    import random
    random.seed(seed)

    daily_questions = [
        {"q": "Which functional group is present in propanoic acid?", "a": "Carboxylic Acid", "opts": ["Alcohol", "Carboxylic Acid", "Ketone"]},
        {"q": "What is the suffix for an alcohol?", "a": "-ol", "opts": ["-one", "-al", "-ol"]},
        {"q": "What is the IUPAC name for CH3CH=CH2?", "a": "Propene", "opts": ["Propane", "Propene", "Propyne"]},
        {"q": "Which group is represented by -COOH?", "a": "Carboxylic Acid", "opts": ["Alcohol", "Carboxylic Acid", "Amine"]},
        {"q": "What type of isomerism involves spatial arrangement around double bonds?", "a": "Geometric", "opts": ["Chain", "Geometric", "Optical"]},
    ]
    challenge = random.choice(daily_questions)
    st.subheader(challenge["q"])
    choice = st.radio("Choose your answer:", challenge["opts"])
    if st.button("Submit Answer"):
        if choice == challenge["a"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. The correct answer is: {challenge['a']}")

elif menu == "📘 SS2 Glossary":
    st.title("📘 SS2 Chemistry Glossary")
    terms = {
        "Homologous Series": "A series of organic compounds with the same functional group and similar chemical properties.",
        "Isomers": "Compounds with the same molecular formula but different structural formulas.",
        "Functional Group": "A specific group of atoms that determines the characteristic reactions of a compound.",
        "Alkane": "A saturated hydrocarbon with single bonds only.",
        "Alkene": "An unsaturated hydrocarbon containing at least one double bond.",
        "Alkyne": "An unsaturated hydrocarbon containing at least one triple bond.",
        "IUPAC": "International Union of Pure and Applied Chemistry – provides naming rules.",
        "Esterification": "A reaction between a carboxylic acid and alcohol to form an ester.",
        "Addition Reaction": "Reaction where atoms are added to a double or triple bond.",
        "Substitution Reaction": "Reaction where one atom or group replaces another in a compound."
    }

    search = st.text_input("Search glossary:")
    for term, definition in terms.items():
        if search.lower() in term.lower():
            with st.expander(term):
                st.write(definition)

# ------------------ ACHIEVEMENT BADGES ------------------
if "achievements" not in st.session_state:
    st.session_state["achievements"] = set()

if "🧠 Quiz" in st.session_state["visited"]:
    st.session_state["achievements"].add("🧠 Quiz Master")

if len(st.session_state["visited"]) >= 7:
    st.session_state["achievements"].add("🧭 Explorer")

if menu == "🏠 Home" and "Daily_Challenge_Score" in st.session_state and st.session_state["Daily_Challenge_Score"]:
    st.session_state["achievements"].add("🔥 Daily Winner")

with st.sidebar.expander("🏅 Achievements"):
    if st.session_state["achievements"]:
        for badge in st.session_state["achievements"]:
            st.success(f"🏅 {badge}")
    else:
        st.info("No achievements yet. Explore more sections!")

# ------------------ ANIMATED STYLES ------------------
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
elif menu == "🎮 Name It Fast":
    st.title("🎮 Name It Fast Challenge!")
    st.markdown("You have 60 seconds to name as many compounds as possible. Ready?")

    import time
    import random

    compounds = {
        "CH4": "Methane",
        "CH3CH3": "Ethane",
        "CH3CH2OH": "Ethanol",
        "CH2=CH2": "Ethene",
        "CH3COOH": "Ethanoic Acid",
        "CH3CHO": "Ethanal",
        "CH3CH=CH2": "Propene",
        "CH≡CH": "Ethyne",
        "CH3COCH3": "Propanone"
    }

    if "game_started" not in st.session_state:
        st.session_state["game_started"] = False
        st.session_state["start_time"] = 0
        st.session_state["score"] = 0
        st.session_state["current_formula"] = ""

    def reset_game():
        st.session_state["game_started"] = True
        st.session_state["start_time"] = time.time()
        st.session_state["score"] = 0
        st.session_state["current_formula"] = random.choice(list(compounds.keys()))

    if not st.session_state["game_started"]:
        if st.button("🚀 Start Game"):
            reset_game()
    else:
        elapsed = time.time() - st.session_state["start_time"]
        remaining = 60 - int(elapsed)

        if remaining > 0:
            st.markdown(f"⏱️ Time left: **{remaining}s**")
            st.markdown(f"🧪 Name this: `{st.session_state['current_formula']}`")

            answer = st.text_input("Enter name:", key=f"name_{elapsed}")

            if answer:
                correct_name = compounds[st.session_state["current_formula"]].lower()
                if answer.strip().lower() == correct_name:
                    st.success("✅ Correct!")
                    st.session_state["score"] += 1
                else:
                    st.error(f"❌ Wrong. Answer: {correct_name}")
                st.session_state["current_formula"] = random.choice(list(compounds.keys()))
        else:
            st.markdown("⏰ **Time's up!**")
            st.success(f"🎉 Final Score: **{st.session_state['score']}**")
            st.session_state["game_started"] = False

# 🎁 Daily Streak Badge
import datetime
today = datetime.date.today()
last_day = st.session_state.get("last_visit")
streak = st.session_state.get("streak", 0)

if last_day != today:
    if last_day == today - datetime.timedelta(days=1):
        streak += 1
    else:
        streak = 1
    st.session_state["streak"] = streak
    st.session_state["last_visit"] = today

if streak >= 3:
    st.session_state["achievements"].add("🔥 3-Day Streaker")

st.sidebar.markdown(f"📅 **Streak:** {streak} day(s)")
