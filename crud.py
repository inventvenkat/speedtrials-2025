from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_pws_by_id(db: Session, pwsid: str):
    return db.query(models.PublicWaterSystem).filter(models.PublicWaterSystem.pwsid == pwsid).first()

def get_pws_by_name(db: Session, name: str):
    return db.query(models.PublicWaterSystem).filter(models.PublicWaterSystem.pws_name.ilike(f"%{name}%")).all()

def get_pws_by_zip(db: Session, zip_code: str):
    return db.query(models.PublicWaterSystem).filter(models.PublicWaterSystem.zip_code == zip_code).all()

from sqlalchemy import or_
from geoalchemy2.functions import ST_Distance
from geoalchemy2.types import Geography

def get_violations_by_pwsid(db: Session, pwsid: str):
    return db.query(models.Violation).filter(models.Violation.pwsid == pwsid).all()

def search_systems(db: Session, query: str):
    if query.isdigit() and len(query) == 5:
        return db.query(models.PublicWaterSystem).filter(models.PublicWaterSystem.zip_code == query).all()
    return db.query(models.PublicWaterSystem).filter(
        or_(
            models.PublicWaterSystem.pwsid.ilike(f"%{query}%"),
            models.PublicWaterSystem.pws_name.ilike(f"%{query}%")
        )
    ).all()

def get_water_system_status(db: Session, pwsid: str):
    health_based_violations = db.query(models.Violation).filter(
        models.Violation.pwsid == pwsid,
        models.Violation.is_health_based_ind == 'Y',
        models.Violation.non_compl_per_end_date == None
    ).count()
    return "safe" if health_based_violations == 0 else "not safe"

def get_system_statistics(db: Session):
    total_systems = db.query(models.PublicWaterSystem).count()

    # All-time health-based violations
    total_systems_with_violations = db.query(models.PublicWaterSystem.pwsid).join(models.Violation).filter(
        models.Violation.is_health_based_ind == 'Y'
    ).distinct().count()

    # Active health-based violations
    active_systems_with_violations = db.query(models.PublicWaterSystem.pwsid).join(models.Violation).filter(
        models.Violation.is_health_based_ind == 'Y',
        models.Violation.non_compl_per_end_date == None
    ).distinct().count()

    return {
        "total_systems": total_systems,
        "total_systems_with_violations": total_systems_with_violations,
        "active_systems_with_violations": active_systems_with_violations
    }

def get_nearest_system(db: Session, lat: float, lon: float):
    return db.query(models.GeographicArea).order_by(
        ST_Distance(
            models.GeographicArea.geom,
            f'POINT({lon} {lat})'
        )
    ).first()

def is_in_georgia(lat: float, lon: float):
    """Checks if a given latitude and longitude are within the state of Georgia."""
    return 30.3 <= lat <= 35.0 and -85.6 <= lon <= -81.0

def get_map_overview(db: Session):
    systems = db.query(
        models.PublicWaterSystem.pwsid,
        models.PublicWaterSystem.pws_name,
        models.GeographicArea.geom
    ).join(models.GeographicArea, models.PublicWaterSystem.pwsid == models.GeographicArea.pwsid).all()

    systems_with_status = []
    for system in systems:
        status = get_water_system_status(db, system.pwsid)
        systems_with_status.append({
            "pwsid": system.pwsid,
            "pws_name": system.pws_name,
            "geom": system.geom,
            "status": status
        })
    return systems_with_status

def get_system_history(db: Session, pwsid: str):
    violations = db.query(models.Violation).filter(models.Violation.pwsid == pwsid).all()
    site_visits = db.query(models.SiteVisit).filter(models.SiteVisit.pwsid == pwsid).all()
    lcr_samples = db.query(models.LcrSample).filter(models.LcrSample.pwsid == pwsid).all()
    events_milestones = db.query(models.EventMilestone).filter(models.EventMilestone.pwsid == pwsid).all()

    return {
        "violations": violations,
        "site_visits": site_visits,
        "lcr_samples": lcr_samples,
        "events_milestones": events_milestones,
    }

def acknowledge_violation(db: Session, violation_id: str):
    db_violation = db.query(models.Violation).filter(models.Violation.violation_id == violation_id).first()
    if not db_violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    db_violation.violation_status = "Acknowledged"
    db.commit()
    db.refresh(db_violation)
    return db_violation
