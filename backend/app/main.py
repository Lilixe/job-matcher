import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Header
from sqlalchemy.orm import Session

from .database import Base, engine
from .schemas import JobCreate, JobResponse, JobUpdateStatus, UserSkill, SkillResponse
from .deps import get_db
from . import crud
from typing import Optional

from .config import MIN_SCORE_ALLOWED
from .utils.resume_parser import extract_text_from_pdf
from .scraper.wanted import scrape_wanted_jobs
from .scraper.skill_extract import extract_skills
from .scraper.scoring import compute_score
from .scraper.wanted import fetch_wanted_details

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API")

# ── Jobs API ─────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    """
    Health check endpoint.
    
    Returns:
        dict: Status message indicating the API is running.
    
    Example:
        GET / -> {"message": "API running"}
    """
    return {"message": "API running"}

@app.post("/scrape/wanted")
def scrape_wanted(limit: int = 100, min_score: float = 50.0, db: Session = Depends(get_db), x_scrape_secret: str = Header(None)):
    """
    Scrape job listings from Wanted.co.kr and store matching jobs in the database.
    
    Fetches job postings, extracts skills from job descriptions, calculates match scores
    against user skills, and stores jobs with "fit" or "unfit" status based on the minimum score threshold.
    
    Args:
        limit (int, optional): Maximum number of jobs to scrape. Defaults to 30.
        min_score (float, optional): Minimum match score threshold. Jobs with score >= min_score are marked as "fit". Defaults to 50.0.
        db (Session): Database session dependency.
        x_scrape_secret (str, optional): Secret header for scraping authorization.
    
    Returns:
        dict: Scraping summary with keys:
            - scraped (int): Total jobs retrieved from Wanted
            - inserted (int): Jobs successfully stored in database
    
    Example:
        POST /scrape/wanted?limit=20&min_score=60 -> {"scraped": 20, "inserted": 15}
    """
    secret = os.getenv("SCRAPE_SECRET")
    if not secret or x_scrape_secret != secret:
        raise HTTPException(status_code=403, detail="Forbidden")   
    
    jobs = scrape_wanted_jobs(limit=limit)

    skills_db = crud.get_skills(db)
    my_skills = [s.skill for s in skills_db]

    inserted = 0

    for job in jobs:
        desc, wanted_tags = fetch_wanted_details(job["id"])

        combined_text = f"{job['title']} {desc} {' '.join(wanted_tags)}"
        merged_skills = extract_skills(combined_text)

        score = compute_score(merged_skills, my_skills) # type: ignore
        
        if score < MIN_SCORE_ALLOWED:
            continue
        
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

        _, created = crud.create_job(db, offer)
        if created:
            inserted += 1

    return {"scraped": len(jobs), "inserted": inserted, "min_score": min_score}

@app.get("/jobs", response_model=list[JobResponse])
def list_jobs(
    status: Optional[str] = None,
    company: Optional[str] = None,
    score: float = 0.0,
    db: Session = Depends(get_db)
):
    """
    Retrieve job listings with optional filtering.
    
    Fetches all stored jobs filtered by status, company name, and minimum match score.
    
    Args:
        status (str, optional): Filter by job status ("fit", "unfit", "applied", etc.). Defaults to None (no filter).
        company (str, optional): Filter by company name (case-insensitive substring match). Defaults to None.
        score (float, optional): Minimum match score threshold. Defaults to 0.0.
        db (Session): Database session dependency.
    
    Returns:
        list[JobResponse]: List of job objects matching the criteria.
    
    Example:
        GET /jobs?status=fit&score=60 -> [{"id": 1, "title": "...", "score": 75.0, ...}, ...]
    """
    return crud.get_jobs(db, status=status, company=company, score=score) # type: ignore

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve detailed information for a specific job.
    
    Args:
        job_id (int): Unique identifier of the job.
        db (Session): Database session dependency.
    
    Returns:
        JobResponse: Detailed job object.
    
    Raises:
        HTTPException: 404 if job not found.
    
    Example:
        GET /jobs/123 -> {"id": 123, "title": "...", "company": "...", ...}
    """
    job = crud.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.delete("/jobs/{job_id}", response_model=JobResponse)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job listing from the database.
    
    Args:
        job_id (int): Unique identifier of the job to delete.
        db (Session): Database session dependency.
    
    Returns:
        JobResponse: The deleted job object.
    
    Raises:
        HTTPException: 404 if job not found.
    
    Example:
        DELETE /jobs/123 -> {"id": 123, "title": "...", ...}
    """
    job = crud.delete_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.patch("/jobs/{job_id}", response_model=JobResponse)
def update_status(job_id: int, data: JobUpdateStatus, db: Session = Depends(get_db)):
    """
    Update the status of a job listing.
    
    Changes the job status (e.g., "fit" to "applied", "unfit" to "fit").
    
    Args:
        job_id (int): Unique identifier of the job.
        data (JobUpdateStatus): Request body containing the new status.
        db (Session): Database session dependency.
    
    Returns:
        JobResponse: Updated job object.
    
    Raises:
        HTTPException: 404 if job not found.
    
    Example:
        PATCH /jobs/123 with {"status": "applied"} -> {"id": 123, "status": "applied", ...}
    """
    job = crud.update_job_status(db, job_id, data.status)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# ── Skills API ─────────────────────────────────────────────────────────────────────
@app.get("/skills", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)):
    """
    Retrieve all user skills from the database.
    
    Args:
        db (Session): Database session dependency.
    
    Returns:
        list[SkillResponse]: List of all stored user skills.
    
    Example:
        GET /skills -> [{"id": 1, "skill": "python"}, {"id": 2, "skill": "fastapi"}, ...]
    """
    return crud.get_skills(db)

@app.post("/skills/from-resume")
async def skills_from_resume(file: UploadFile = File(...), db: Session = Depends(get_db), min_score: float = 50.0):
    """
    Extract and save skills from an uploaded PDF resume.
    
    Parses the PDF file, extracts skills using NLP, and adds new skills to the database.
    
    Args:
        file (UploadFile): PDF file uploaded by the user.
        db (Session): Database session dependency.
        min_score (float): Minimum score threshold for job matching.
    
    Returns:
        dict: Upload summary with keys:
            - found (int): Total skills extracted from resume
            - inserted (int): New skills added to database
            - skills (list[str]): List of extracted skills
    
    Raises:
        HTTPException: 400 if file is not a PDF.
    
    Example:
        POST /skills/from-resume (multipart/form-data with resume.pdf) -> 
        {"found": 12, "inserted": 8, "skills": ["python", "fastapi", ...]}
    """
    if not file.filename.endswith(".pdf"): # type: ignore
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    found_skills = extract_skills(text)

    inserted = crud.add_skills_bulk(db, found_skills)
    crud.recalculate_all_jobs(db, score_threshold=min_score) 
    return {
    "found": len(found_skills),
    "inserted": inserted,
    "skills": found_skills
    }

@app.post("/skills")
def add_skill(payload : UserSkill, db: Session = Depends(get_db), min_score: float = 50.0): # type: ignore
    """
    Add a single skill to the user's skill set.
    
    Args:
        payload (UserSkill): Request body containing the skill name.
        db (Session): Database session dependency.
        min_score (float): Minimum score threshold for job matching.
    
    Returns:
        SkillResponse: Created skill object.
    
    Example:
        POST /skills with {"skill": "kubernetes"} -> {"id": 10, "skill": "kubernetes"}
    """
    result = crud.add_skill(db, payload.skill)
    crud.recalculate_all_jobs(db, score_threshold=min_score) 
    return result

@app.delete("/skills/clear")
def delete_all_skill(db: Session = Depends(get_db), min_score: float = 50.0):
    """
    Delete all user skills from the database.
    
    WARNING: This operation is irreversible and removes all stored skills.
    
    Args:
        db (Session): Database session dependency.
        min_score (float): Minimum score threshold for job matching.
    
    Returns:
        dict: Confirmation message.
    
    Example:
        DELETE /skills/clear -> {"message": "All skills deleted"}
    """
    crud.delete_all_skills(db)
    crud.recalculate_all_jobs(db, score_threshold=min_score)
    return {"message": "All skills deleted"}

@app.delete("/skills/{skill_id}", response_model=SkillResponse)
def delete_skill(skill_id: int, db: Session = Depends(get_db), min_score: float = 50.0):
    """
    Delete a specific skill from the user's skill set.
    
    Args:
        skill_id (int): Unique identifier of the skill to delete.
        db (Session): Database session dependency.
        min_score (float): Minimum score threshold for job matching.
    Returns:
        SkillResponse: The deleted skill object.
    
    Raises:
        HTTPException: 404 if skill not found.
    
    Example:
        DELETE /skills/5 -> {"id": 5, "skill": "deprecated_tool"}
    """
    skill = crud.delete_skill(db, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    crud.recalculate_all_jobs(db, score_threshold=min_score)
    return skill



