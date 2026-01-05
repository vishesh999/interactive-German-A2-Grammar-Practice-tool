import streamlit as st
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration with light mode
st.set_page_config(
    page_title="German Partizip Perfekt Practice | GermanBhashi",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force light mode
st.markdown("""
    <style>
    /* Force light theme */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }
    [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }
    .main {
        padding: 2rem;
        background-color: #FFFFFF !important;
    }
    
    /* Force all text colors */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #333333 !important;
    }
    
    /* Radio button labels */
    .stRadio label, .stRadio div {
        color: #333333 !important;
    }
    
    /* Form labels */
    label, .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #333333 !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader, .streamlit-expanderContent {
        color: #333333 !important;
    }
    
    /* Headers remain dark */
    h1, h2, h3, h4, h5, h6 {
        color: #2C3E50 !important;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
    .correct-answer {
        background-color: #D4EDDA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28A745;
        margin: 10px 0;
        color: #155724 !important;
    }
    .correct-answer * {
        color: #155724 !important;
    }
    .incorrect-answer {
        background-color: #F8D7DA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #DC3545;
        margin: 10px 0;
        color: #721C24 !important;
    }
    .incorrect-answer * {
        color: #721C24 !important;
    }
    .info-box {
        background-color: #E7F3FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 20px 0;
        color: #004085 !important;
    }
    .info-box * {
        color: #004085 !important;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .score-card * {
        color: white !important;
    }
    .contact-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
    }
    .contact-section * {
        color: white !important;
    }
    
    /* Progress bar text */
    .stProgress + div {
        color: #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)
# Exercise database - ALL Partizip Perfekt questions
exercises = [
    {
        "id": 1,
        "sentence": "Ich habe gestern einen Brief ___. (schreiben)",
        "options": ["geschrieben", "geschreibt", "geskribben", "schreibt"],
        "correct": "geschrieben",
        "explanation": "Correct! 'Geschrieben' is the Partizip Perfekt of the irregular verb 'schreiben'. Irregular verbs typically form the past participle with ge- + stem change + -en.",
        "topic": "Partizip Perfekt - Irregular Verbs",
        "translation": "I wrote a letter yesterday.",
        "verb_type": "Irregular verb"
    },
    {
        "id": 2,
        "sentence": "Wir haben das Haus ___. (kaufen)",
        "options": ["gekauft", "gekafen", "kauft", "gekaufen"],
        "correct": "gekauft",
        "explanation": "Perfect! 'Gekauft' is the Partizip Perfekt of the regular verb 'kaufen'. Regular verbs form the past participle with ge- + stem + -t.",
        "topic": "Partizip Perfekt - Regular Verbs",
        "translation": "We bought the house.",
        "verb_type": "Regular verb"
    },
    {
        "id": 3,
        "sentence": "Sie ist nach Berlin ___. (fahren)",
        "options": ["gefahren", "gefahrt", "gefahrt", "fahrt"],
        "correct": "gefahren",
        "explanation": "Excellent! 'Gefahren' is the Partizip Perfekt of 'fahren'. This verb uses 'sein' as auxiliary because it indicates movement from one place to another.",
        "topic": "Partizip Perfekt - Movement Verbs with 'sein'",
        "translation": "She traveled to Berlin.",
        "verb_type": "Irregular verb (movement)"
    },
    {
        "id": 4,
        "sentence": "Er hat das Problem ___. (verstehen)",
        "options": ["verstanden", "geverstanden", "versteht", "gestanden"],
        "correct": "verstanden",
        "explanation": "Great! 'Verstanden' is correct. Verbs with inseparable prefixes (ver-, be-, er-, ent-, emp-, ge-, miss-, zer-) do NOT add 'ge-' in the Partizip Perfekt.",
        "topic": "Partizip Perfekt - Inseparable Prefix Verbs",
        "translation": "He understood the problem.",
        "verb_type": "Irregular verb with inseparable prefix"
    },
    {
        "id": 5,
        "sentence": "Ich habe die Tür ___. (aufmachen)",
        "options": ["aufgemacht", "geaufmacht", "aufmacht", "aufgmacht"],
        "correct": "aufgemacht",
        "explanation": "Perfect! 'Aufgemacht' is the Partizip Perfekt of the separable verb 'aufmachen'. With separable verbs, 'ge-' goes between the prefix and the stem: auf-ge-macht.",
        "topic": "Partizip Perfekt - Separable Verbs",
        "translation": "I opened the door.",
        "verb_type": "Separable verb"
    },
    {
        "id": 6,
        "sentence": "Wir haben den Film ___. (sehen)",
        "options": ["gesehen", "geseht", "sehen", "gesieht"],
        "correct": "gesehen",
        "explanation": "Correct! 'Gesehen' is the Partizip Perfekt of the irregular verb 'sehen'. The stem vowel changes from 'e' to 'e' in this case.",
        "topic": "Partizip Perfekt - Irregular Verbs",
        "translation": "We saw the film.",
        "verb_type": "Irregular verb"
    },
    {
        "id": 7,
        "sentence": "Sie hat ihr Zimmer ___. (aufräumen)",
        "options": ["aufgeräumt", "geaufräumt", "aufräumt", "aufgeräumen"],
        "correct": "aufgeräumt",
        "explanation": "Excellent! 'Aufgeräumt' is correct. This separable verb places 'ge-' between the prefix 'auf' and the stem 'räum' + regular ending '-t'.",
        "topic": "Partizip Perfekt - Separable Regular Verbs",
        "translation": "She cleaned up her room.",
        "verb_type": "Separable regular verb"
    },
    {
        "id": 8,
        "sentence": "Er hat den Text ___. (übersetzen)",
        "options": ["übersetzt", "geübersetzt", "übergesetzt", "übersetzet"],
        "correct": "übersetzt",
        "explanation": "Great! 'Übersetzt' is correct. 'Übersetzen' (to translate) has an inseparable prefix 'über-', so no 'ge-' is added. Note: 'über-' can be separable or inseparable depending on meaning!",
        "topic": "Partizip Perfekt - Inseparable Prefix Verbs",
        "translation": "He translated the text.",
        "verb_type": "Inseparable prefix verb"
    },
    {
        "id": 9,
        "sentence": "Ich habe das Buch ___. (lesen)",
        "options": ["gelesen", "gelest", "lesen", "gelist"],
        "correct": "gelesen",
        "explanation": "Perfect! 'Gelesen' is the Partizip Perfekt of 'lesen'. The stem vowel changes from 'e' to 'e', and it takes the irregular ending '-en'.",
        "topic": "Partizip Perfekt - Irregular Verbs",
        "translation": "I read the book.",
        "verb_type": "Irregular verb"
    },
    {
        "id": 10,
        "sentence": "Sie sind nach Hause ___. (gehen)",
        "options": ["gegangen", "gegeht", "gangen", "gegehn"],
        "correct": "gegangen",
        "explanation": "Excellent! 'Gegangen' is the Partizip Perfekt of 'gehen'. This verb uses 'sein' as auxiliary because it indicates movement, and the past participle is formed irregularly.",
        "topic": "Partizip Perfekt - Movement Verbs",
        "translation": "They went home.",
        "verb_type": "Irregular verb (movement)"
    }
]

# Email configuration function
def send_email(name, email, phone, level, interest, message, score):
    """
    Send email using Gmail SMTP
    
    SETUP REQUIRED:
    1. Use Gmail account
    2. Enable 2-Factor Authentication in your Google Account
    3. Generate App Password: https://myaccount.google.com/apppasswords
    4. Replace SENDER_EMAIL and APP_PASSWORD below
    """
    
    # ⚠️ IMPORTANT: Replace these with your actual credentials
    SENDER_EMAIL = "germanbhashi@gmail.com"  # Your Gmail address
    APP_PASSWORD = ""      # Your Gmail App Password (16 characters, no spaces)
    RECEIVER_EMAIL = "vishesh@germanbhashi.com"  # Where you want to receive emails
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🎯 New GermanBhashi Contact - {name}"
        
        # Email body
        body = f"""
New Contact Form Submission from GermanBhashi Partizip Perfekt Practice App

═══════════════════════════════════════════════════════
📋 CONTACT DETAILS
═══════════════════════════════════════════════════════

👤 Name:              {name}
📧 Email:             {email}
📱 Phone:             {phone if phone else 'Not provided'}

═══════════════════════════════════════════════════════
📊 LEARNING INFORMATION
═══════════════════════════════════════════════════════

📚 Current Level:     {level}
🎯 Interest:          {interest}
🏆 Quiz Score:        {score}

═══════════════════════════════════════════════════════
💬 MESSAGE
═══════════════════════════════════════════════════════

{message if message else 'No message provided'}

═══════════════════════════════════════════════════════
⏰ Submitted on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
═══════════════════════════════════════════════════════

This lead came from the Partizip Perfekt Practice tool.
Follow up within 24 hours for best results! 🚀
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        
        return True, "Email sent successfully!"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

# Initialize session state
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = [False] * len(exercises)
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [None] * len(exercises)
if 'completed' not in st.session_state:
    st.session_state.completed = False
if 'shuffled_options' not in st.session_state:
    # Shuffle options for each exercise once at the start
    st.session_state.shuffled_options = []
    for ex in exercises:
        shuffled = ex['options'].copy()
        random.shuffle(shuffled)
        st.session_state.shuffled_options.append(shuffled)

# Header with Logo and QR Code
header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

with header_col1:
    # Logo on the left
    try:
        st.image("resources/logo.jpg", width=150)
    except:
        st.markdown("**GermanBhashi**")

with header_col2:
    st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100%;
            margin-top: -8px;
        ">
            <h1 style="
                margin-bottom: 6px;
            ">
                🇩🇪 German Partizip Perfekt Practice
            </h1>
            <p style="
                font-size: 18px;
                color: #666;
                margin: 0;
            ">
                Master Past Participles with Interactive Exercises | Powered by GermanBhashi
            </p>
        </div>
    """, unsafe_allow_html=True)

with header_col3:
    try:
        st.image("resources/GermanBhashi_QRCode.jpg", width=150, caption="Scan for more info")
    except:
        pass


# Mobile notice
st.markdown("""
    <div class='mobile-notice'>
        💻 For the best experience, please use a laptop or desktop computer
    </div>
""", unsafe_allow_html=True)

# Progress bar
progress = (st.session_state.current_exercise) / len(exercises)
st.progress(progress)
st.markdown(f"**Question {st.session_state.current_exercise + 1} of {len(exercises)}**")

# Main content
if not st.session_state.completed:
    current_ex = exercises[st.session_state.current_exercise]
    
    # Display exercise
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Topic:** {current_ex['topic']}")
        st.markdown(f"**Verb Type:** {current_ex['verb_type']}")
        st.markdown(f"#### Fill in the correct Partizip Perfekt:")
        st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #2C3E50;'>{current_ex['sentence']}</p>", unsafe_allow_html=True)
        
        # Answer options
        selected_answer = st.radio(
            "Choose the correct past participle:",
            st.session_state.shuffled_options[st.session_state.current_exercise],
            key=f"q_{current_ex['id']}",
            disabled=st.session_state.answered[st.session_state.current_exercise]
        )
        
        # Check answer button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            if not st.session_state.answered[st.session_state.current_exercise]:
                if st.button("✓ Check Answer", key=f"check_{current_ex['id']}"):
                    st.session_state.answered[st.session_state.current_exercise] = True
                    st.session_state.user_answers[st.session_state.current_exercise] = selected_answer
                    if selected_answer == current_ex['correct']:
                        st.session_state.score += 1
                    st.rerun()
        
        # Show feedback if answered
        if st.session_state.answered[st.session_state.current_exercise]:
            user_ans = st.session_state.user_answers[st.session_state.current_exercise]
            
            if user_ans == current_ex['correct']:
                st.markdown(f"""
                    <div class='correct-answer'>
                        <h3>✅ Correct!</h3>
                        <p><strong>Your answer:</strong> {user_ans}</p>
                        <p><strong>Translation:</strong> {current_ex['translation']}</p>
                        <p><strong>Explanation:</strong> {current_ex['explanation']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='incorrect-answer'>
                        <h3>❌ Not quite right</h3>
                        <p><strong>Your answer:</strong> {user_ans}</p>
                        <p><strong>Correct answer:</strong> {current_ex['correct']}</p>
                        <p><strong>Translation:</strong> {current_ex['translation']}</p>
                        <p><strong>Explanation:</strong> {current_ex['explanation']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Navigation buttons
        col_nav1, col_nav2 = st.columns(2)
        
        with col_nav1:
            if st.session_state.current_exercise > 0:
                if st.button("⬅️ Previous", key="prev"):
                    st.session_state.current_exercise -= 1
                    st.rerun()
        
        with col_nav2:
            if st.session_state.answered[st.session_state.current_exercise]:
                if st.session_state.current_exercise < len(exercises) - 1:
                    if st.button("Next ➡️", key="next"):
                        st.session_state.current_exercise += 1
                        st.rerun()
                else:
                    if st.button("🎯 Finish & See Results", key="finish"):
                        st.session_state.completed = True
                        st.rerun()
    
    with col2:
        # Score card
        st.markdown(f"""
            <div class='score-card'>
                <h2>📊 Your Progress</h2>
                <h1>{st.session_state.score} / {st.session_state.current_exercise + 1}</h1>
                <p style='font-size: 16px;'>Questions Answered</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick tips
        st.markdown("""
            <div class='info-box'>
                <h4>💡 Partizip Perfekt Tips:</h4>
                <ul>
                    <li><strong>Regular verbs:</strong> ge- + stem + -t</li>
                    <li><strong>Irregular verbs:</strong> ge- + stem + -en</li>
                    <li><strong>Separable verbs:</strong> prefix + ge- + stem</li>
                    <li><strong>Inseparable prefixes:</strong> no "ge-" added</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

else:
    # Results page
    percentage = (st.session_state.score / len(exercises)) * 100
    
    st.balloons()
    
    st.markdown(f"""
        <div class='score-card'>
            <h1>🎉 Congratulations!</h1>
            <h2>You've completed all Partizip Perfekt exercises!</h2>
            <h1 style='font-size: 60px; margin: 20px 0;'>{st.session_state.score} / {len(exercises)}</h1>
            <h3>{percentage:.0f}% Correct</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Performance feedback
    if percentage >= 90:
        feedback = "🌟 Outstanding! You've mastered Partizip Perfekt formation!"
        emoji = "🏆"
    elif percentage >= 70:
        feedback = "👏 Great job! You have a solid understanding of past participles!"
        emoji = "⭐"
    elif percentage >= 50:
        feedback = "👍 Good effort! Keep practicing different verb types!"
        emoji = "📚"
    else:
        feedback = "💪 Keep learning! Focus on the different formation rules!"
        emoji = "🎯"
    
    st.markdown(f"### {emoji} {feedback}")
    
    # Detailed results
    st.markdown("### 📋 Detailed Results")
    
    for i, ex in enumerate(exercises):
        user_ans = st.session_state.user_answers[i]
        is_correct = user_ans == ex['correct']
        
        with st.expander(f"Question {i+1}: {ex['topic']} {'✅' if is_correct else '❌'}"):
            st.markdown(f"**Sentence:** {ex['sentence']}")
            st.markdown(f"**Your Answer:** {user_ans}")
            st.markdown(f"**Correct Answer:** {ex['correct']}")
            st.markdown(f"**Verb Type:** {ex['verb_type']}")
            st.markdown(f"**Explanation:** {ex['explanation']}")
            st.markdown(f"**Translation:** {ex['translation']}")
    
    # Contact section
    st.markdown("""
        <div class='contact-section'>
            <h2>🚀 Want to Master German?</h2>
            <p style='font-size: 18px; margin: 20px 0;'>
                This is just the beginning! Join GermanBhashi for comprehensive German language courses 
                designed specifically for IB students and German learners.
            </p>
            <h3>✨ What We Offer:</h3>
            <ul style='list-style: none; padding: 0; font-size: 16px;'>
                <li>✓ Expert IB German coaching (ab initio & B)</li>
                <li>✓ Personalized learning paths</li>
                <li>✓ Native speaker practice sessions</li>
                <li>✓ Exam-focused preparation</li>
                <li>✓ Interactive learning materials</li>
                <li>✓ CV optimization as per German Job market</li>
                <li>✓ Interview preparation as per job's description</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    col_contact1, col_contact2, col_contact3 = st.columns(3)
    
    with col_contact1:
        st.markdown("### 📧 Email Us")
        st.markdown("[vishesh@germanbhashi.com](mailto:vishesh@germanbhashi.com)")
    
    with col_contact2:
        st.markdown("### 🌐 Visit Website")
        st.markdown("[www.germanbhashi.com](https://germanbhashi.com)")
    
    with col_contact3:
        st.markdown("### 📱 Follow Us")
        st.markdown("[@germanbhashi](https://instagram.com/germanbhashi)")
    
    # Contact form
    st.markdown("### 💬 Get in Touch")
    st.markdown("Interested in learning more? Fill out this quick form:")
    
    with st.form("contact_form"):
        name = st.text_input("Your Name*")
        email = st.text_input("Your Email*")
        phone = st.text_input("Phone Number")
        level = st.selectbox("Current German Level", 
                            ["Beginner (A1)", "Elementary (A2)", "Intermediate (B1)", 
                             "Upper Intermediate (B2)", "Not sure"])
        interest = st.selectbox("I'm interested in:",
                               ["IB German Coaching", "General German Course", 
                                "Exam Preparation", "Conversation Practice", 
                                "CV optimization", "Interview preparation"])
        message = st.text_area("Message (Optional)")
        
        submitted = st.form_submit_button("📨 Send Message")
        
        if submitted:
            if name and email:
                score_text = f"{st.session_state.score}/{len(exercises)} ({percentage:.0f}%)"
                
                with st.spinner('Sending your message...'):
                    success, msg = send_email(name, email, phone, level, interest, message, score_text)
                
                if success:
                    st.success(f"✅ Thank you, {name}! We've received your message and will contact you at {email} within 24 hours! 🎉")
                    st.markdown("In the meantime, check out our website at [germanbhashi.com](https://germanbhashi.com)")
                else:
                    st.error(f"❌ {msg}")
                    st.info("💡 Please check your email configuration in the code or contact us directly at vishesh@germanbhashi.com")
            else:
                st.error("Please fill in your name and email.")
    
    # Restart button
    st.markdown("---")
    if st.button("🔄 Practice Again", key="restart"):
        st.session_state.current_exercise = 0
        st.session_state.score = 0
        st.session_state.answered = [False] * len(exercises)
        st.session_state.user_answers = [None] * len(exercises)
        st.session_state.completed = False
        # Re-shuffle options for new practice session
        st.session_state.shuffled_options = []
        for ex in exercises:
            shuffled = ex['options'].copy()
            random.shuffle(shuffled)
            st.session_state.shuffled_options.append(shuffled)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>© 2025 GermanBhashi | Your Partner in German Language Excellence</p>
        <p style='font-size: 14px;'>Made with ❤️ for German learners worldwide</p>
    </div>
""", unsafe_allow_html=True)