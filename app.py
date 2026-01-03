import streamlit as st
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(
    page_title="German A2 Grammar Practice | GermanBhashi",
    page_icon="🇩🇪",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
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
    }
    .incorrect-answer {
        background-color: #F8D7DA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #DC3545;
        margin: 10px 0;
    }
    .info-box {
        background-color: #E7F3FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin: 20px 0;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    .contact-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
    }
    h1 {
        color: #2C3E50;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Exercise database with 10 fill-in-the-blank questions
exercises = [
    {
        "id": 1,
        "sentence": "Ich ___ gestern im Kino.",
        "options": ["bin", "war", "habe", "hatte"],
        "correct": "war",
        "explanation": "Correct! 'War' is the simple past (Präteritum) form of 'sein' (to be) for 'ich'. We use simple past for common verbs like 'sein' and 'haben' when talking about the past.",
        "topic": "Simple Past (Präteritum)",
        "translation": "I was at the cinema yesterday."
    },
    {
        "id": 2,
        "sentence": "Wir ___ einen Brief geschrieben.",
        "options": ["sind", "haben", "wurden", "werden"],
        "correct": "haben",
        "explanation": "Excellent! 'Haben' is used as the auxiliary verb with 'geschrieben' to form the perfect tense. Most verbs use 'haben' in the Perfekt.",
        "topic": "Perfect Tense (Perfekt)",
        "translation": "We have written a letter."
    },
    {
        "id": 3,
        "sentence": "Sie ___ nach Berlin gefahren.",
        "options": ["ist", "hat", "war", "wird"],
        "correct": "ist",
        "explanation": "Perfect! 'Ist' is correct because 'fahren' is a verb of movement and uses 'sein' as the auxiliary verb in the perfect tense.",
        "topic": "Perfect Tense with Movement Verbs",
        "translation": "She has driven/traveled to Berlin."
    },
    {
        "id": 4,
        "sentence": "Der Mann, ___ Frau Lehrerin ist, wohnt hier.",
        "options": ["der", "dessen", "dem", "den"],
        "correct": "dessen",
        "explanation": "Great job! 'Dessen' is the genitive form of the relative pronoun for masculine/neuter nouns, meaning 'whose'. It shows possession.",
        "topic": "Relative Pronouns (Genitive)",
        "translation": "The man whose wife is a teacher lives here."
    },
    {
        "id": 5,
        "sentence": "Wenn ich Zeit ___, würde ich dich besuchen.",
        "options": ["habe", "hätte", "hatte", "haben"],
        "correct": "hätte",
        "explanation": "Correct! 'Hätte' is the Konjunktiv II form of 'haben'. We use it for hypothetical or unreal conditions in the present or future.",
        "topic": "Subjunctive II (Konjunktiv II)",
        "translation": "If I had time, I would visit you."
    },
    {
        "id": 6,
        "sentence": "Das Buch liegt ___ dem Tisch.",
        "options": ["auf", "über", "in", "an"],
        "correct": "auf",
        "explanation": "Perfect! 'Auf' (on) is the correct preposition for objects lying on a horizontal surface. With dative case (dem), it indicates position.",
        "topic": "Two-Way Prepositions (Wechselpräpositionen)",
        "translation": "The book is lying on the table."
    },
    {
        "id": 7,
        "sentence": "Ich freue mich ___ die Ferien.",
        "options": ["auf", "über", "für", "an"],
        "correct": "auf",
        "explanation": "Excellent! 'Sich freuen auf' means 'to look forward to' (something in the future). The preposition 'auf' with accusative case is required here.",
        "topic": "Reflexive Verbs with Prepositions",
        "translation": "I'm looking forward to the holidays."
    },
    {
        "id": 8,
        "sentence": "Er arbeitet, ___ Geld zu verdienen.",
        "options": ["um", "zu", "für", "damit"],
        "correct": "um",
        "explanation": "Great! 'Um...zu' is used to express purpose or goal (in order to). This construction is used when the subject is the same in both clauses.",
        "topic": "Infinitive Clauses with 'um...zu'",
        "translation": "He works in order to earn money."
    },
    {
        "id": 9,
        "sentence": "Nachdem ich gegessen ___, ging ich spazieren.",
        "options": ["habe", "hatte", "bin", "war"],
        "correct": "hatte",
        "explanation": "Perfect! 'Hatte' is the past perfect (Plusquamperfekt) auxiliary. We use Plusquamperfekt after 'nachdem' to show an action completed before another past action.",
        "topic": "Past Perfect (Plusquamperfekt)",
        "translation": "After I had eaten, I went for a walk."
    },
    {
        "id": 10,
        "sentence": "Das Auto wird von meinem Vater ___.",
        "options": ["gefahren", "fahren", "fuhr", "gefahrt"],
        "correct": "gefahren",
        "explanation": "Excellent! 'Gefahren' is the past participle of 'fahren'. In passive voice with 'wird...von', we use the past participle. This is the passive voice (Passiv).",
        "topic": "Passive Voice (Passiv)",
        "translation": "The car is driven by my father."
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
    APP_PASSWORD = "ntbdswcaxdmqznvd"      # Your Gmail App Password (16 characters, no spaces)
    RECEIVER_EMAIL = "vishesh@germanbhashi.com"  # Where you want to receive emails
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🎯 New GermanBhashi Contact - {name}"
        
        # Email body
        body = f"""
New Contact Form Submission from GermanBhashi Grammar Practice App

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

This lead came from the A2 Grammar Practice tool.
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

# Header with Logo and QR Code
header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

with header_col1:
    # Logo on the left
    try:
        st.image("resources/logo.jpg", width=150)  # Adjust width as needed
    except:
        st.markdown("**GermanBhashi**")  # Fallback if image not found

with header_col2:
    st.markdown("<h1>🇩🇪 German A2 Grammar Practice</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #666;'>Master German Grammar with Interactive Exercises | Powered by GermanBhashi</p>", unsafe_allow_html=True)

with header_col3:
    # QR Code on the right
    try:
        st.image("resources/GermanBhashi_QRCode.jpg", width=150)  # Adjust width as needed
        st.markdown("<p style='text-align: center; font-size: 12px;'>Scan for more info</p>", unsafe_allow_html=True)
    except:
        pass  # Hide if QR code not found

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
        st.markdown(f"### 📝 Exercise {current_ex['id']}")
        st.markdown(f"**Topic:** {current_ex['topic']}")
        st.markdown(f"#### Fill in the blank:")
        st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #2C3E50;'>{current_ex['sentence']}</p>", unsafe_allow_html=True)
        
        # Answer options
        selected_answer = st.radio(
            "Choose the correct answer:",
            current_ex['options'],
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
                <h4>💡 Quick Tips:</h4>
                <ul>
                    <li>Read each sentence carefully</li>
                    <li>Consider the context</li>
                    <li>Think about grammar rules</li>
                    <li>Learn from explanations</li>
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
            <h2>You've completed all exercises!</h2>
            <h1 style='font-size: 60px; margin: 20px 0;'>{st.session_state.score} / {len(exercises)}</h1>
            <h3>{percentage:.0f}% Correct</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Performance feedback
    if percentage >= 90:
        feedback = "🌟 Outstanding! You have excellent command of A2 German grammar!"
        emoji = "🏆"
    elif percentage >= 70:
        feedback = "👏 Great job! You're well on your way to mastering A2 level!"
        emoji = "⭐"
    elif percentage >= 50:
        feedback = "👍 Good effort! Keep practicing to improve further!"
        emoji = "📚"
    else:
        feedback = "💪 Keep learning! More practice will help you improve!"
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
                # Prepare score text
                score_text = f"{st.session_state.score}/{len(exercises)} ({percentage:.0f}%)"
                
                # Show sending indicator
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
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>© 2025 GermanBhashi | Your Partner in German Language Excellence</p>
        <p style='font-size: 14px;'>Made with ❤️ for German learners worldwide</p>
    </div>
""", unsafe_allow_html=True)