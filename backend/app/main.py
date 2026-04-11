from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine
from .schemas import JobCreate, JobResponse, JobUpdateStatus
from .deps import get_db
from . import crud
from typing import Optional

from .scraper.wanted import scrape_wanted_jobs
from .scraper.skill_extract import extract_skills
from .scraper.scoring import compute_score
from .scraper.wanted import fetch_wanted_details

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")

@app.get("/")
def root():
    return {"message": "Job Tracker API running"}


#@app.post("/jobs", response_model=JobResponse)
#def create_job(job: JobCreate, db: Session = Depends(get_db)):
#    return crud.create_job(db, job)

@app.post("/scrape/wanted")
def scrape_wanted(limit: int = 30, min_score: float = 50.0, db: Session = Depends(get_db)):
    jobs = scrape_wanted_jobs(limit=limit)

    inserted = 0

    for job in jobs:
        # For MVP, we use title only as "text"
        desc, wanted_tags = fetch_wanted_details(job["id"])

        text = job["title"] + " " + desc
        parsed_skills = extract_skills(text)

        merged_skills = sorted(set(parsed_skills) | set(wanted_tags))

        score = compute_score(merged_skills)

        status = "fit" if score >= min_score else "unfit" 
        
        offer = JobCreate(source="wanted",title=job["title"],company=job["company"],url=job["url"],skills=", ".join(merged_skills),score=score,status=status)
        crud.create_job(db, offer)

        inserted += 1

    return {"scraped": len(jobs), "inserted": inserted}

@app.get("/jobs", response_model=list[JobResponse])
def list_jobs(
    status: Optional[str] = None,
    company: Optional[str] = None,
    score: float = 0.0,
    db: Session = Depends(get_db)
):
    return crud.get_jobs(db, status=status, company=company, score=score) # type: ignore

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.delete("/jobs/{job_id}", response_model=JobResponse)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.delete_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.patch("/jobs/{job_id}", response_model=JobResponse)
def update_status(job_id: int, data: JobUpdateStatus, db: Session = Depends(get_db)):
    job = crud.update_job_status(db, job_id, data.status)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job