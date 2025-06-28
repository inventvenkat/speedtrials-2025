from sqlalchemy.orm import Session
import models
import schemas

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
