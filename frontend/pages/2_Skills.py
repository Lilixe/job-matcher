import streamlit as st
import requests

from config import API_URL, min_score

st.title("My Skills")

# --- Load Skills ---
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
            c1, c2 = st.columns([4, 1])
            with c1:
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
            with c2:
                if st.button("❌", key=f"del_{skill['id']}", width="stretch"):
                    requests.delete(f"{API_URL}/skills/{skill['id']}",params={"min_score": min_score})
                    st.rerun()

if st.button("🗑️ Delete ALL skills"):
    r = requests.delete(f"{API_URL}/skills/clear", params={"min_score": min_score})

    if r.status_code == 200:
        st.success("All skills deleted!")
        st.rerun()
    else:
        st.error("Failed to delete skills.")

st.divider()

# --- Add skill manually ---
st.subheader("➕ Add a new skill")

new_skill = st.text_input("")

if st.button("Add Skill"):
    if new_skill.strip() == "":
        st.error("Skill cannot be empty.")
    else:
        requests.post(f"{API_URL}/skills",json={"skill": new_skill.lower().strip()}, params={"min_score": min_score})
        st.success(f"Added: {new_skill}")
        st.rerun()

st.divider()

# --- Upload Resume ---
st.subheader("📄 Upload Resume PDF")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

extract_clicked = st.button("Extract Skills from Resume", disabled=(uploaded_file is None))

if extract_clicked:
    response = requests.post(
        f"{API_URL}/skills/from-resume",
        files={"file": uploaded_file}, # type: ignore
        params={"min_score": min_score}
    )

    if response.status_code == 200:
        data = response.json()
        st.success(f"Found {data['found']} skills, inserted {data['inserted']} new ones.")
        st.write(data.get("skills", []))
        st.rerun()
    else:
        st.error(response.text)