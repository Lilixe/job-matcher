# Job Match Dashboard 🚀

A full-stack job scraping + matching web app that automatically scrapes job postings, extracts required skills, compares them with your personal skills, ranks jobs by match score, and lets you track applications.

Built with **FastAPI + SQLite + Streamlit**.

---

## ✨ Features

### Job Scraping
- Scrapes job postings from **Wanted Korea**
- Extracts:
  - job title
  - company name
  - job URL
  - job description (tasks + requirements)

### Skill Extraction / Matching
- Parses job descriptions to detect skills using keyword patterns
- Calculates a match score (%) between job requirements and your saved skill set
- Filters jobs based on a minimum match score

### Job Tracking
- Stores jobs in SQLite database
- Tracks job status:
  - `new`
  - `unfit`
  - `applied`

### Skill Management
- Add skills manually
- Delete skills
- Clear all skills
- Upload a resume PDF and automatically extract skills

### ✅ Frontend Dashboard
- Built using Streamlit (no HTML/CSS required)
- Job list filtering with a slider (minimum score)
- Open job URL directly
- Mark jobs as applied

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Requests
- BeautifulSoup

### Frontend
- Streamlit

---

## 📂 Project Structure

```text
job-match-dashboard/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── scoring.py
│   │   ├── skills_parser.py
│   │   └── scraper/
│   │       └── wanted.py
│   └── jobs.db
│
├── frontend/
│   ├── Home.py
│   └── pages/
│       └── 2_Skills.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

1. Clone the repository
     
git clone https://github.com/YOUR_USERNAME/job-matcher.git

cd job-matcher

2. Create virtual environment

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

3. Install dependencies
   
pip install -r requirements.txt

### ▶️ Running the App

1. Start the FastAPI backend
   
cd backend

uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000

Docs available at:

http://127.0.0.1:8000/docs

2. Start the Streamlit frontend

In a second terminal:

cd frontend

streamlit run Home.py

Frontend runs at:

http://localhost:8501

### 🔥 How It Works
Step 1: Add your skills

Go to the Skills page and add skills manually OR upload your resume PDF.

Step 2: Scrape Wanted jobs

Click Scrape Wanted Jobs in the dashboard sidebar.

Step 3: Filter by match score

Use the slider to filter jobs by minimum match score.

Step 4: Apply & Track

Open job posting using the Open Job button

Click Mark Applied to update the job status in the database

### 📌 Planned Improvements
- Add more Korean job-posting website scraper
- Better NLP-based skill extraction
- Job specialty based scrapping
- Auto-discover new skills from job descriptions

### ⚠️ Disclaimer

This project is for educational and personal use only.
Some job websites may block scraping depending on rate limits or bot detection.

## 👤 Author

Built by Patrick Bastard
