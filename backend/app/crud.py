from sqlalchemy.orm import Session
from .models import JobApplication
from .schemas import JobCreate

def create_job(db: Session, job: JobCreate):
    existing = db.query(JobApplication).filter(JobApplication.url == job.url).first() # type: ignore
    if existing:
        return existing
    
    new_job = JobApplication(
        title=job.title,
        source=job.source,
        company=job.company,
        skills=job.skills,
        url=job.url,
        score=job.score,
        status=job.status
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def get_jobs(db: Session, status: str = None, company: str = None, score: float = 0.0): # type: ignore
    query = db.query(JobApplication)
    query = query.filter(JobApplication.score >= score)

    if status:
        query = query.filter(JobApplication.status == status)

    if company:
        query = query.filter(JobApplication.company.ilike(f"%{company}%"))

    return query.order_by(JobApplication.score.desc()).all()

def get_job(db: Session, job_id: int):
    return db.query(JobApplication).filter(JobApplication.id == job_id).first()

def delete_job(db: Session, job_id: int):
    job = get_job(db, job_id)
    if job is None:
        return None
    db.delete(job)
    db.commit()
    return job

def update_job_status(db: Session, job_id: int, new_status: str):
    job = get_job(db, job_id)
    if job is None:
        return None
    job.status = new_status # type: ignore
    db.commit()
    db.refresh(job)
    return job