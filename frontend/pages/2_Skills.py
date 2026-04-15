import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("My Skills")

# --- Load Skills ---
"""
Load and display current user skills from the backend API.

Fetches all skills from the database and displays them as styled tags
in a responsive grid layout. Shows a warning if no skills are found.
"""
skills_res = requests.get(f"{API_URL}/skills")
skills = skills_res.json()

st.subheader("Current Skills")

if len(skills) == 0:
    st.warning("No skills in database yet.")
else:
    # Display as tags
    cols = st.columns(4)
    for i, skill in enumerate(skills):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div style="
                    padding: 8px;
                    background-color: #222;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 8px;
                    font-size: 14px;
                ">
                    {skill['skill']}
                </div>
                """,
                unsafe_allow_html=True
            )

if st.button("🗑️ Delete ALL skills"):
    """
    Delete all user skills from the database.
    
    Sends a DELETE request to clear all skills and refreshes the page
    to reflect changes. Shows success/error feedback.
    """
    r = requests.delete(f"{API_URL}/skills/clear")

    if r.status_code == 200:
        st.success("All skills deleted!")
        st.rerun()
    else:
        st.error("Failed to delete skills.")

st.divider()

# --- Add skill manually ---
"""
Manual skill addition section.

Provides a text input for entering new skills and validates that
the input is not empty before submitting to the API.
"""
st.subheader("➕ Add a new skill")

new_skill = st.text_input("")

if st.button("Add Skill"):
    if new_skill.strip() == "":
        st.error("Skill cannot be empty.")
    else:
        requests.post(f"{API_URL}/skills",json={"skill": new_skill.lower().strip()})
        st.success(f"Added: {new_skill}")
        st.rerun()

st.divider()

# --- Upload Resume ---
"""
Resume upload and skill extraction section.

Allows users to upload a PDF resume and extract skills automatically
using the backend's NLP processing. Displays extraction results.
"""
st.subheader("📄 Upload Resume PDF")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

extract_clicked = st.button("Extract Skills from Resume", disabled=(uploaded_file is None))

if extract_clicked:
    """
    Process uploaded resume PDF for skill extraction.
    
    Sends the PDF file to the backend API for text extraction and skill parsing,
    then displays the number of skills found and inserted.
    """
    response = requests.post(
        f"{API_URL}/skills/from-resume",
        files={"file": uploaded_file} # type: ignore
    )

    if response.status_code == 200:
        data = response.json()
        st.success(f"Found {data['found']} skills, inserted {data['inserted']} new ones.")
        st.write(data.get("skills", []))
        st.rerun()
    else:
        st.error(response.text)