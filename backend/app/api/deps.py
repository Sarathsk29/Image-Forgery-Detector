from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.cases import get_job_by_id, require_case_access


def db_session() -> Session:
    return next(get_db())


def require_case(
    case_id: str,
    access_key: str = Query(...),
    db: Session = Depends(get_db),
):
    return require_case_access(db, case_id, access_key)


def require_job(job_id: int, access_key: str, db: Session):
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis job not found.")
    require_case_access(db, job.case.case_id, access_key)
    return job

