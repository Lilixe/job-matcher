from wsgiref import headers

import streamlit as st
import requests
import pandas as pd

from config import API_URL, MIN_SCORE

st.set_page_config(page_title="Job Match Dashboard", layout="wide")

st.title("Job Match Dashboard")

headers = {"X-Scrape-Secret": st.secrets["SCRAPE_SECRET"]}
if "min_score" not in st.session_state:
    st.session_state.min_score = MIN_SCORE

# Sidebar controls
min_score = st.sidebar.slider("Minimum match score (%)", 0, 100, st.session_state.min_score)
st.session_state.min_score = min_score

if st.sidebar.button("Scrape Wanted Jobs"):
    r = requests.post(
        f"{API_URL}/scrape/wanted",
        params={"limit": 30, "min_score": min_score},
        headers=headers
    )

    if r.status_code == 200:
        st.sidebar.success("Wanted scraping done!")
    else:
        st.sidebar.error("Scraping failed")


# Fetch jobs
r = requests.get(f"{API_URL}/jobs", params={"score": min_score})

if r.status_code != 200:
    st.error("Could not fetch jobs from API.")
    st.stop()

jobs = r.json()

if not jobs:
    st.warning("No jobs found. Try scraping first.")
    st.stop()
df = pd.DataFrame(jobs)

st.subheader(f"Recommended Jobs (score >= {min_score}%)")

search_query = st.text_input("🔍 Search jobs (title, company, skills)", "")

if search_query.strip():
    q = search_query.lower()

    df = df[
        df["title"].str.lower().str.contains(q, na=False)
        | df["company"].str.lower().str.contains(q, na=False)
        | df["skills"].str.lower().str.contains(q, na=False)
    ]

df_display = df.copy()
df_display["delete"] = False

edited_df = st.data_editor(
    df_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "status": st.column_config.SelectboxColumn(
            "Status",
            options=["fit", "unfit", "applied", "rejected"],
            required=True
        ),
        "delete": st.column_config.CheckboxColumn("Delete?")
    },
    disabled=["id", "title", "company", "url", "score", "skills", "source", "created_at"]
)

if st.button("💾 Apply Changes"):
    updates = 0
    deletes = 0

    for i in range(len(df)):
        job_id = df.loc[i, "id"]

        # Delete job
        if edited_df.loc[i, "delete"] is True:
            requests.delete(f"{API_URL}/jobs/{job_id}")
            deletes += 1
            continue

        # Update status
        old_status = df.loc[i, "status"]
        new_status = edited_df.loc[i, "status"]

        if old_status != new_status:
            requests.patch(
                f"{API_URL}/jobs/{job_id}",
                json={"status": new_status}
            )
            updates += 1

    st.success(f"Updated {updates} jobs, deleted {deletes} jobs.")
    st.rerun()
    
    
# Show apply buttons
st.subheader("Apply / Track Jobs")

for job in jobs:
    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])

    with col1:
        st.write(f"**{job['company']}**")
        st.write(job["title"])

    with col2:
        st.write(job["skills"])

    with col3:
        st.write(f"Score: {job['score']:.1f}%")

    with col4:
        st.link_button("Open Job", job["url"])

        if st.button(f"Mark Applied #{job['id']}", key=f"apply_{job['id']}"):
            patch = requests.patch(
                f"{API_URL}/jobs/{job['id']}",
                json={"status": "applied"}
            )

            if patch.status_code == 200:
                st.success(f"Marked {job['id']} as applied")
            else:
                st.error("Failed to update job status")