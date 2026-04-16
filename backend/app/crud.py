from sqlalchemy import or_
from sqlalchemy.orm import Session
from streamlit import status

from .scraper.scoring import compute_score
from .models import JobApplication
from .models import UserSkills
from .schemas import JobCreate
from .schemas import UserSkill


#JOBS

def create_job(db: Session, job: JobCreate):
    """
    Create a new job application record or retrieve existing one.
    
    Inserts a new job into the database with the provided details. If a job with the same URL
    already exists, returns the existing record instead to prevent duplicates.
    
    Args:
        db (Session): Database session dependency.
        job (JobCreate): Job creation schema containing title, source, company, skills, url, score, and status.
    
    Returns:
        JobApplication: The created or existing job object.
    
    Example:
        >>> job = JobCreate(title="Backend Dev", source="wanted", company="TechCorp", 
        ...                  skills="python,fastapi", url="https://...", score=85.0, status="fit")
        >>> result = create_job(db, job)
    """
    existing = db.query(JobApplication).filter(JobApplication.url == job.url).first() # type: ignore
    if existing:
        return existing, False
    
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
    return new_job, True

def get_jobs(db: Session, status: str = None, company: str = None, score: float = 0.0): # type: ignore
    """
    Retrieve jobs with optional filtering and sorting.
    
    Fetches job records from the database filtered by status, company name, and minimum score.
    Results are ordered by score in descending order (highest scores first).
    
    Args:
        db (Session): Database session dependency.
        status (str, optional): Filter by job status ("fit", "unfit", "applied", etc.). Defaults to None.
        company (str, optional): Filter by company name (case-insensitive substring match). Defaults to None.
        score (float, optional): Minimum match score threshold. Defaults to 0.0.
    
    Returns:
        list[JobApplication]: List of job records matching the criteria, sorted by score descending.
    
    Example:
        >>> jobs = get_jobs(db, status="fit", score=70.0)
        >>> print(len(jobs))
    """
    query = db.query(JobApplication)
    score_filter = JobApplication.score >= score
    status_filter = JobApplication.status == status if status else None

    if status_filter is not None:
        query = query.filter(or_(score_filter, status_filter))
    else:
        query = query.filter(score_filter)
        
    if company:
        query = query.filter(JobApplication.company.ilike(f"%{company}%"))

    return query.order_by(JobApplication.score.desc()).all()

def get_job(db: Session, job_id: int):
    """
    Retrieve a single job by its ID.
    
    Args:
        db (Session): Database session dependency.
        job_id (int): Unique identifier of the job.
    
    Returns:
        JobApplication | None: Job object if found, None otherwise.
    
    Example:
        >>> job = get_job(db, 123)
        >>> if job:
        ...     print(job.title)
    """
    return db.query(JobApplication).filter(JobApplication.id == job_id).first()

def delete_job(db: Session, job_id: int):
    """
    Delete a job record from the database.
    
    Removes the job with the specified ID from the database and commits the change.
    
    Args:
        db (Session): Database session dependency.
        job_id (int): Unique identifier of the job to delete.
    
    Returns:
        JobApplication | None: The deleted job object if found, None otherwise.
    
    Example:
        >>> deleted_job = delete_job(db, 123)
        >>> if deleted_job:
        ...     print(f"Deleted: {deleted_job.title}")
    """
    job = get_job(db, job_id)
    if job is None:
        return None
    db.delete(job)
    db.commit()
    return job

def update_job_status(db: Session, job_id: int, new_status: str):
    """
    Update the status of a job record.
    
    Changes the status field of a job (e.g., "fit" -> "applied", "unfit" -> "fit")
    and persists the change to the database.
    
    Args:
        db (Session): Database session dependency.
        job_id (int): Unique identifier of the job.
        new_status (str): New status value to assign.
    
    Returns:
        JobApplication | None: Updated job object if found, None otherwise.
    
    Example:
        >>> updated_job = update_job_status(db, 123, "applied")
        >>> print(updated_job.status)  # "applied"
    """
    job = get_job(db, job_id)
    if job is None:
        return None
    job.status = new_status # type: ignore
    db.commit()
    db.refresh(job)
    return job

def recalculate_all_jobs(db: Session, score_threshold: float):
    """
    Recalculate match scores and statuses for all job applications.

    Retrieves the current user skills from the database, then iterates through all job
    applications to recompute their match scores based on the intersection of job skills
    and user skills. Updates the score and status ("fit" if score >= 50, "unfit" otherwise)
    for each job. Jobs with no skills are assigned a score of 0.0 and status "unfit".

    Args:
        db (Session): Database session dependency.

    Returns:
        None: Modifies job records in place and commits changes to the database.

    Example:
        >>> recalculate_all_jobs(db)
        # All job scores and statuses are updated based on current user skills.
    """
    skills_db = get_skills(db)
    user_skills = [s.skill.lower() for s in skills_db]

    jobs = db.query(JobApplication).all()

    for job in jobs:
        if not job.skills: # type: ignore
            job.score = 0.0 # type: ignore
            job.status = "unfit" # type: ignore
            continue

        job_skills = [s.strip().lower() for s in job.skills.split(",") if s.strip()]
        score = compute_score(job_skills, user_skills)

        job.score = score # type: ignore
        job.status = "fit" if score >= score_threshold else "unfit" # type: ignore

    db.commit()

# SKILLS

def add_skill(db: Session, skill: str):
    """
    Add a single skill to the user's skill set.
    
    Normalizes the skill name (strips whitespace and converts to lowercase), checks for duplicates,
    and inserts into the database if not already present.
    
    Args:
        db (Session): Database session dependency.
        skill (str): Skill name to add.
    
    Returns:
        UserSkills | None: Created or existing skill object, None if skill is empty after normalization.
    
    Example:
        >>> skill = add_skill(db, "  Python  ")
        >>> print(skill.skill)  # "python"
    """
    skill = skill.strip().lower()
    if not skill:
        return None

    existing = db.query(UserSkills).filter(UserSkills.skill == skill).first()
    if existing:
        return existing

    new_skill = UserSkills(skill=skill)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

def add_skills_bulk(db: Session, skills: list[str]) -> int:
    """
    Add multiple skills to the user's skill set in batch.
    
    Normalizes each skill name (strips whitespace and converts to lowercase), filters out
    duplicates and empty strings, and inserts new skills into the database in a single commit.
    
    Args:
        db (Session): Database session dependency.
        skills (list[str]): List of skill names to add.
    
    Returns:
        int: Number of new skills successfully inserted (excludes duplicates).
    
    Example:
        >>> count = add_skills_bulk(db, ["Python", "FastAPI", "SQL", "python"])
        >>> print(count)  # 3 (python not duplicated)
    """
    inserted = 0

    for skill in skills:
        skill = skill.strip().lower()
        if not skill:
            continue

        existing = db.query(UserSkills).filter(UserSkills.skill == skill).first()
        if not existing:
            db.add(UserSkills(skill=skill))
            inserted += 1
    db.commit()
    return inserted

def get_skills(db: Session): # type: ignore
    """
    Retrieve all user skills from the database.
    
    Fetches all skills ordered by creation date in descending order (most recent first).
    
    Args:
        db (Session): Database session dependency.
    
    Returns:
        list[UserSkills]: List of all user skill records.
    
    Example:
        >>> all_skills = get_skills(db)
        >>> for skill in all_skills:
        ...     print(skill.skill)
    """
    query = db.query(UserSkills)
    return query.order_by(UserSkills.created_at.desc()).all()

def delete_all_skills(db: Session):
    """
    Delete all user skills from the database.
    
    WARNING: This operation is irreversible and removes all stored skills at once.
    
    Args:
        db (Session): Database session dependency.
    
    Returns:
        None
    
    Example:
        >>> delete_all_skills(db)  # All skills permanently removed
    """
    db.query(UserSkills).delete()
    db.commit()

def delete_skill(db: Session, skill_id: int):
    """
    Delete a specific skill by its ID.
    
    Removes a single skill record from the database.
    
    Args:
        db (Session): Database session dependency.
        skill_id (int): Unique identifier of the skill to delete.
    
    Returns:
        UserSkills | None: Deleted skill object if found, None otherwise.
    
    Example:
        >>> deleted_skill = delete_skill(db, 5)
        >>> if deleted_skill:
        ...     print(f"Deleted: {deleted_skill.skill}")
    """
    skill = db.query(UserSkills).filter(UserSkills.id == skill_id).first()
    if skill is None:
        return None
    db.delete(skill)
    db.commit()
    return skill

