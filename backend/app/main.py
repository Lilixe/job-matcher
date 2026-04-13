from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from .database import Base, engine
from .schemas import JobCreate, JobResponse, JobUpdateStatus, UserSkill, SkillResponse
from .deps import get_db
from . import crud
from typing import Optional

from .utils.resume_parser import extract_text_from_pdf
from .scraper.wanted import scrape_wanted_jobs
from .scraper.skill_extract import extract_skills
from .scraper.scoring import compute_score
from .scraper.wanted import fetch_wanted_details

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")

###### JOBS API ######

@app.get("/")
def root():
    return {"message": "API running"}

#@app.post("/jobs", response_model=JobResponse)
#def create_job(job: JobCreate, db: Session = Depends(get_db)):
#    return crud.create_job(db, job)

@app.post("/scrape/wanted")
def scrape_wanted(limit: int = 30, min_score: float = 50.0, db: Session = Depends(get_db)):
    jobs = scrape_wanted_jobs(limit=limit)

    skills_db = crud.get_skills(db)
    my_skills = [s.skill for s in skills_db]

    inserted = 0

    for job in jobs:
        desc, wanted_tags = fetch_wanted_details(job["id"])

        combined_text = f"{job['title']} {desc} {' '.join(wanted_tags)}"
        merged_skills = extract_skills(combined_text)

        score = compute_score(merged_skills, my_skills) # type: ignore

        status = "fit" if score >= min_score else "unfit"

        offer = JobCreate(
            source="wanted",
            title=job["title"],
            company=job["company"],
            url=job["url"],
            skills=", ".join(merged_skills),
            score=score,
            status=status
        )

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


###### SKILLS API ######

@app.get("/skills", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)):
    return crud.get_skills(db) # type: ignore

@app.post("/skills/from-resume")
async def skills_from_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):

    if not file.filename.endswith(".pdf"): # type: ignore
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    found_skills = extract_skills(text)

    inserted = crud.add_skills_bulk(db, found_skills)

    return {
    "found": len(found_skills),
    "inserted": inserted,
    "skills": found_skills
    }

@app.post("/skills")
def add_skill(payload : UserSkill, db: Session = Depends(get_db)): # type: ignore
    return crud.add_skill(db, payload.skill)

@app.delete("/skills/clear")
def delete_all_skill(db: Session = Depends(get_db)):
    crud.delete_all_skills(db)
    return {"message": "All skills deleted"}

@app.delete("/skills/{skill_id}", response_model=SkillResponse)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = crud.delete_skill(db, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill



