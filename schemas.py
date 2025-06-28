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
