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

    # Initialize quiz state
    if "quiz_start_time" not in st.session_state:
        st.session_state.quiz_start_time = None
        st.session_state.quiz_score = 0
        st.session_state.user_answers = {}

    # Start quiz button
    if not st.session_state.quiz_start_time:
        if st.button("🚀 Start Timed Quiz"):
            st.session_state.quiz_start_time = time.time()
            st.session_state.quiz_score = 0
            st.session_state.user_answers = {}
            st.experimental_rerun()
    else:
        elapsed = time.time() - st.session_state.quiz_start_time
        remaining = max(60 - int(elapsed), 0)
        st.info(f"⏱ Time remaining: {remaining} seconds")

        if remaining <= 0:
            st.warning("⏰ Time's up!")
            st.session_state.quiz_start_time = None

    # Display questions
    for i, q in enumerate(questions):
        st.subheader(f"{i+1}. {q['q']}")
        
        # Use session state to preserve answers
        if i not in st.session_state.user_answers:
            st.session_state.user_answers[i] = None
            
        user_answer = st.radio(
            "Choose one:", 
            q["opts"], 
            key=f"quiz_{i}",
            index=None if i not in st.session_state.user_answers else q["opts"].index(st.session_state.user_answers[i]) if st.session_state.user_answers[i] else None
        )
        
        if user_answer:
            st.session_state.user_answers[i] = user_answer
            
            if user_answer == q["a"]:
                st.success("✅ Correct!")
                if LOTTIE_ENABLED and correct_anim:
                    st_lottie(correct_anim, height=150)
                play_sound("correct.mp3")
            else:
                st.error(f"❌ Wrong. Correct answer: {q['a']}")
                if LOTTIE_ENABLED and wrong_anim:
                    st_lottie(wrong_anim, height=150)
                play_sound("wrong.mp3")

    # Calculate and display score
    if st.session_state.quiz_start_time and remaining > 0:
        current_score = sum(
            1 for i, q in enumerate(questions) 
            if st.session_state.user_answers.get(i) == q["a"]
        )
        st.session_state.quiz_score = current_score
        st.markdown(f"### 🏁 Current Score: **{current_score}/{len(questions)}**")
    else:
        st.markdown(f"### 🏁 Final Score: **{st.session_state.quiz_score}/{len(questions)}**")
