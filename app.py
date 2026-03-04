

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from resume_parser import extract_text_from_pdf, chunk_text
from embedding import embed_texts, create_faiss_index, search_similar, cosine_similarity
from rag_engine import analyze_with_llm
from ats_engine import keyword_match_score, extract_skills
from auth import create_user_table, signup_user, login_user


# ==============================
# INITIAL SETUP
# ==============================

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
create_user_table()

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ==============================
# AUTHENTICATION SYSTEM
# ==============================

if not st.session_state.logged_in:

    st.title("🔐 AI Resume Analyzer - Login System")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            if signup_user(new_user, new_password):
                st.success("Account Created Successfully! Please Login.")
            else:
                st.error("Username already exists.")

    st.stop()


# ==============================
# MAIN APPLICATION (After Login)
# ==============================

st.title("🚀 AI Resume Analyzer & Job Matcher (RAG System)")
st.markdown("Upload a resume and compare it with a job description using Semantic AI + ATS scoring.")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
job_description = st.text_area("📝 Paste Job Description")

analyze_button = st.button("🚀 Start Analysis")

if analyze_button:

    if not uploaded_file or not job_description:
        st.warning("Please upload resume and paste job description first.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        # Extract resume text
        resume_text = extract_text_from_pdf("temp.pdf")

        # Chunk resume
        chunks = chunk_text(resume_text)

        # Generate embeddings for resume chunks
        resume_embeddings = embed_texts(chunks)

        # Create FAISS index
        index = create_faiss_index(resume_embeddings)

        # Embed job description
        job_embedding = embed_texts([job_description])

        # Retrieve top relevant chunk
        indices, distances = search_similar(index, job_embedding, k=1)
        relevant_chunks = [chunks[i] for i in indices]

        # Compute semantic similarity
        similarity_score = cosine_similarity(
            resume_embeddings[indices[0]],
            job_embedding[0]
        ) * 100

        # ATS keyword score
        keyword_score = keyword_match_score(resume_text, job_description)

        # Skills extraction
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matched_skills = list(set(resume_skills).intersection(set(job_skills)))
        missing_skills = list(set(job_skills) - set(resume_skills))

        # Skill match %
        skill_match_percent = 0
        if len(job_skills) > 0:
            skill_match_percent = (len(matched_skills) / len(job_skills)) * 100

        # Weighted score
        final_score = (0.6 * similarity_score) + (0.4 * keyword_score)

    # ==============================
    # DASHBOARD
    # ==============================

    st.divider()
    st.header("📊 Match Score Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Semantic Score", f"{round(similarity_score, 2)}%")
    col2.metric("ATS Keyword Score", f"{round(keyword_score, 2)}%")
    col3.metric("Final Weighted Score", f"{round(final_score, 2)}%")

    # Chart
    fig, ax = plt.subplots(figsize=(6, 4))
    scores = [similarity_score, keyword_score, final_score]
    labels = ["Semantic", "Keyword", "Final"]

    ax.bar(labels, scores)
    ax.set_ylabel("Score (%)")
    ax.set_title("Resume Match Analysis")
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)



    # ==============================
    # SKILLS REPORT
    # ==============================

    st.divider()
    st.header("🧠 Skills Intelligence Report")

    st.subheader("📈 Skill Match Strength")
    st.progress(skill_match_percent / 100)
    st.write(f"Skill Match Percentage: {round(skill_match_percent, 2)}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.success(skill.upper())
        else:
            st.info("No matched skills found.")

    with col2:
        st.subheader("⚠ Missing Skills (Priority Areas)")
        if missing_skills:
            for skill in missing_skills:
                st.error(skill.upper())
        else:
            st.success("No major skill gaps detected 🎉")

    # ==============================
    # AI ANALYSIS
    # ==============================

    st.divider()
    st.header("🤖 AI Detailed Analysis")

    result = analyze_with_llm(
        relevant_chunks,
        job_description,
        similarity_score / 100
    )

    st.write(result)

    st.success("Analysis Complete ✅")


