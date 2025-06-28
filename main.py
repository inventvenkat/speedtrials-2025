from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Water Quality Data API",
    description="An API to access and query the Georgia water quality dataset.",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is running."""
    return {"message": "Welcome to the Water Quality Data API!"}

@app.get("/systems/by-id/{pwsid}", response_model=schemas.PublicWaterSystem)
def read_pws_by_id(pwsid: str, db: Session = Depends(get_db)):
    db_pws = crud.get_pws_by_id(db, pwsid=pwsid)
    if db_pws is None:
        raise HTTPException(status_code=404, detail="Public Water System not found")
    return db_pws

@app.get("/systems/by-name/{name}", response_model=List[schemas.PublicWaterSystem])
def read_pws_by_name(name: str, db: Session = Depends(get_db)):
    db_pws = crud.get_pws_by_name(db, name=name)
    return db_pws

@app.get("/systems/by-zip/{zip_code}", response_model=List[schemas.PublicWaterSystem])
def read_pws_by_zip(zip_code: str, db: Session = Depends(get_db)):
    db_pws = crud.get_pws_by_zip(db, zip_code=zip_code)
    return db_pws

@app.get("/violations/{pwsid}", response_model=List[schemas.Violation])
def read_violations_by_pwsid(pwsid: str, db: Session = Depends(get_db)):
    db_violations = crud.get_violations_by_pwsid(db, pwsid=pwsid)
    return db_violations

@app.get("/systems/search", response_model=List[schemas.PublicWaterSystem])
def search_systems(query: str, db: Session = Depends(get_db)):
    return crud.search_systems(db, query=query)

@app.get("/systems/{pwsid}/status", response_model=str)
def read_system_status(pwsid: str, db: Session = Depends(get_db)):
    return crud.get_water_system_status(db, pwsid=pwsid)

@app.get("/statistics", response_model=dict)
def read_statistics(db: Session = Depends(get_db)):
    return crud.get_system_statistics(db)

@app.get("/systems/by-location", response_model=schemas.PublicWaterSystem)
def read_system_by_location(lat: float, lon: float, db: Session = Depends(get_db)):
    if not crud.is_in_georgia(lat, lon):
        raise HTTPException(status_code=404, detail="Location is outside of Georgia.")
    nearest_system = crud.get_nearest_system(db, lat=lat, lon=lon)
    if not nearest_system:
        raise HTTPException(status_code=404, detail="No water system found near this location.")
    return crud.get_pws_by_id(db, pwsid=nearest_system.pwsid)
