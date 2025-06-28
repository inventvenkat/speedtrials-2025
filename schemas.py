from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class PublicWaterSystemBase(BaseModel):
    pwsid: str
    pws_name: Optional[str] = None
    population_served_count: Optional[int] = None
    city_name: Optional[str] = None
    state_code: Optional[str] = None
    zip_code: Optional[str] = None
    admin_name: Optional[str] = None
    email_addr: Optional[str] = None
    phone_number: Optional[str] = None
    org_name: Optional[str] = None
    alt_phone_number: Optional[str] = None
    fax_number: Optional[str] = None

class PublicWaterSystemCreate(PublicWaterSystemBase):
    pass

class PublicWaterSystem(PublicWaterSystemBase):
    class Config:
        orm_mode = True

class ViolationBase(BaseModel):
    violation_id: str
    pwsid: str
    violation_code: Optional[str] = None
    is_health_based_ind: Optional[str] = None
    contaminant_code: Optional[str] = None
    non_compl_per_begin_date: Optional[date] = None
    non_compl_per_end_date: Optional[date] = None
    violation_status: Optional[str] = None

class ViolationCreate(ViolationBase):
    pass

class Violation(ViolationBase):
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

from datetime import datetime

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class MapOverview(BaseModel):
    pwsid: str
    pws_name: str
    geom: str
    status: str

class SiteVisit(BaseModel):
    visit_id: str
    visit_date: Optional[date] = None
    agency_type_code: Optional[str] = None
    visit_reason_code: Optional[str] = None

    class Config:
        orm_mode = True

class LcrSample(BaseModel):
    sample_id: str
    sampling_end_date: Optional[date] = None
    result_sign_code: Optional[str] = None
    sample_measure: Optional[float] = None

    class Config:
        orm_mode = True

class EventMilestone(BaseModel):
    event_schedule_id: str
    event_end_date: Optional[date] = None
    event_actual_date: Optional[date] = None
    event_milestone_code: Optional[str] = None

    class Config:
        orm_mode = True

class SystemHistory(BaseModel):
    violations: List[Violation]
    site_visits: List[SiteVisit]
    lcr_samples: List[LcrSample]
    events_milestones: List[EventMilestone]
