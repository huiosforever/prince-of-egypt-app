
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

# Initialize Firebase only once, globally safe
if not firebase_admin._apps:
    firebase_secrets = st.secrets["firebase"]
    cred = credentials.Certificate({
        "type": firebase_secrets["type"],
        "project_id": firebase_secrets["project_id"],
        "private_key_id": firebase_secrets["private_key_id"],
        "private_key": firebase_secrets["private_key"].replace("\\n", "\n"),
        "client_email": firebase_secrets["client_email"],
        "client_id": firebase_secrets["client_id"],
        "auth_uri": firebase_secrets["auth_uri"],
        "token_uri": firebase_secrets["token_uri"],
        "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Title with themed emoji
st.markdown("<h1 style='text-align: center;'>🧺 Prince of Egypt – Adventure Game 🌟</h1>", unsafe_allow_html=True)

# Fun image at the top
st.image("https://upload.wikimedia.org/wikipedia/en/d/dc/Prince_of_Egypt_poster.png", caption="What a journey! Let's learn about Moses.", use_column_width=True)

# Play sound effect
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")

# User Info
st.subheader("👋 What's your name?")
name = st.text_input("Type your name below 👇", "")

# Today's date
date = datetime.now().strftime("%Y-%m-%d")

# Questions
st.markdown("### 🔥 What did Moses see in the desert?")
q1 = st.radio("", ["A lion", "A burning bush", "A giant pyramid"])

st.markdown("### 📜 What was the message God gave to Moses?")
q2 = st.text_area("Write it in your own words!")

st.markdown("### 💬 What does 'God said, I will be with you' mean to YOU?")
q3 = st.text_input("Type your answer")

# Optional drawing upload
st.markdown("### 🎨 Draw your favorite scene!")
drawing = st.file_uploader("Upload a picture if you drew something from the movie!", type=["jpg", "png"])

# Save Button
if st.button("✅ Save My Answers"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    else:
        user_ref = db.collection("prince_of_egypt_quiz").document(name)
        user_ref.set({
            "date": date,
            "question_1": q1,
            "question_2": q2,
            "question_3": q3
        })
        st.success("🎉 Great job! Your answers were saved.")

# Load Previous
if name.strip() != "":
    doc = db.collection("prince_of_egypt_quiz").document(name).get()
    if doc.exists:
        st.markdown("### 📖 Your Previous Answers")
        data = doc.to_dict()
        st.write("**📅 Date:**", data.get("date"))
        st.write("**🔥 What did Moses see?**", data.get("question_1"))
        st.write("**📜 God's message:**", data.get("question_2"))
        st.write("**💬 What it means to you:**", data.get("question_3"))
