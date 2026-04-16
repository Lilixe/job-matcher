import streamlit as st
import requests
import pandas as pd

from config import API_URL, min_score

st.set_page_config(page_title="Job Match Dashboard", layout="wide")

st.title("Job Match Dashboard")

# Sidebar controls
min_score = st.sidebar.slider("Minimum match score (%)", 0, 100, 50)

if st.sidebar.button("Scrape Wanted Jobs"):
    r = requests.post(
        f"{API_URL}/scrape/wanted",
        params={"limit": 30, "min_score": min_score}
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

# Show jobs table
st.subheader(f"Recommended Jobs (score >= {min_score}%)")
df_display = df.copy()

df_display["status"] = df_display["status"].astype("category")

edited_df = st.data_editor(
    df_display,
    use_container_width=True,
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

for i in range(len(df)):
    old_status = df.loc[i, "status"]
    new_status = edited_df.loc[i, "status"]

    if old_status != new_status:
        job_id = df.loc[i, "id"]
        requests.patch(
            f"{API_URL}/jobs/{job_id}",
            json={"status": new_status}
        )
        st.success(f"Updated job {job_id} → {new_status}")
        st.rerun()

df_display["delete"] = False

to_delete = edited_df[edited_df["delete"] == True]

if len(to_delete) > 0:
    if st.button("Confirm Delete Selected Jobs"):
        for _, row in to_delete.iterrows():
            requests.delete(f"{API_URL}/jobs/{row['id']}")
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