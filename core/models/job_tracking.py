# core/models/job_tracking.py
from sqlalchemy.orm import Session
from core.models.job import Job, JobStatus
from core.memory.postgres_client import SessionLocal
from typing import Optional

# Create a new job
def create_job(job_type: str, payload: str = None) -> Job:
    db: Session = SessionLocal()
    job = Job(type=job_type, payload=payload)
    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()
    return job

# Update job status and result
def update_job_status(job_id: int, status: JobStatus, result: Optional[str] = None) -> Job:
    db: Session = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = status
        if result is not None:
            job.result = result
        db.commit()
        db.refresh(job)
    db.close()
    return job

# Get job by id
def get_job(job_id: int) -> Optional[Job]:
    db: Session = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()
    return job

# List jobs (optionally by status)
def list_jobs(status: Optional[JobStatus] = None):
    db: Session = SessionLocal()
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    jobs = query.order_by(Job.created_at.desc()).all()
    db.close()
    return jobs
