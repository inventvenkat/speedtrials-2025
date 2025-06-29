from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "a_very_secret_key"  # In a real app, use a more secure key and load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    return current_user

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

@app.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.get("/api/systems/map_overview", response_model=List[schemas.MapOverview])
def get_map_overview(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_map_overview(db)

@app.get("/api/systems/{pwsid}/history", response_model=schemas.SystemHistory)
def get_system_history(pwsid: str, db: Session = Depends(get_db)):
    return crud.get_system_history(db, pwsid=pwsid)

@app.put("/api/violations/{violation_id}/acknowledge", response_model=schemas.Violation)
def acknowledge_violation(violation_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Operator":
        raise HTTPException(status_code=403, detail="Only operators can acknowledge violations.")
    return crud.acknowledge_violation(db, violation_id=violation_id)
