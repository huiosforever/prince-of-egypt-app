import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

# Initialize Firebase only once
if "firebase_initialized" not in st.session_state:
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
    st.session_state.firebase_initialized = True

# Connect to Firestore
db = firestore.client()

# Title
st.title("Prince of Egypt – Interactive Adventure")

# User Info
name = st.text_input("Enter your name", "")
date = datetime.now().strftime("%Y-%m-%d")

# Questions
q1 = st.radio("1. What did Moses see in the desert?",
              ["A lion", "A burning bush", "A giant pyramid"])

q2 = st.text_area("2. What was the message God gave to Moses?")

q3 = st.text_input("3. What does 'God said, I will be with you' mean to you?")

drawing = st.file_uploader("Upload your drawing of your favorite scene", type=["jpg", "png"])

# Save Button
if st.button("Save My Answers"):
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
        st.success("Your answers have been saved!")

# Load Previous
if name.strip() != "":
    doc = db.collection("prince_of_egypt_quiz").document(name).get()
    if doc.exists:
        st.subheader("Your Previous Answers")
        data = doc.to_dict()
        st.write("**Date:**", data.get("date"))
        st.write("**1. Desert Vision:**", data.get("question_1"))
        st.write("**2. God's Message:**", data.get("question_2"))
        st.write("**3. Verse Meaning:**", data.get("question_3"))
