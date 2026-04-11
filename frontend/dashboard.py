import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Job Match Dashboard", layout="wide")

st.title("Job Match Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
min_score = st.sidebar.slider("Minimum match score (%)", 0, 100, 50)

if st.sidebar.button("Scrape Wanted Jobs"):
    r = requests.post(f"{API_URL}/scrape/wanted", params={
                      "limit":30,
                      "min_score": min_score})
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
st.dataframe(df, use_container_width=True)

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

        if st.button(f"Mark Applied #{job['id']}"):
            patch = requests.patch(
                f"{API_URL}/jobs/{job['id']}",
                json={"status": "applied"}
            )

            if patch.status_code == 200:
                st.success(f"Marked {job['id']} as applied")
            else:
                st.error("Failed to update job status")