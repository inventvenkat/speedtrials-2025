from sqlalchemy import Column, Integer, String, Date, BigInteger, Numeric
from geoalchemy2 import Geometry
import database

class PublicWaterSystem(database.Base):
    __tablename__ = "sdwa_pub_water_systems"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True, index=True)
    pws_name = Column(String(100))
    primacy_agency_code = Column(String(2))
    epa_region = Column(String(2))
    season_begin_date = Column(String(10))
    season_end_date = Column(String(10))
    pws_activity_code = Column(String(1))
    pws_deactivation_date = Column(Date)
    pws_type_code = Column(String(6))
    dbpr_schedule_cat_code = Column(String(6))
    cds_id = Column(String(100))
    gw_sw_code = Column(String(2))
    lt2_schedule_cat_code = Column(String(6))
    owner_type_code = Column(String(1))
    population_served_count = Column(BigInteger)
    pop_cat_2_code = Column(String(2))
    pop_cat_3_code = Column(String(2))
    pop_cat_4_code = Column(String(2))
    pop_cat_5_code = Column(String(2))
    pop_cat_11_code = Column(String(2))
    primacy_type = Column(String(20))
    primary_source_code = Column(String(4))
    is_grant_eligible_ind = Column(String(1))
    is_wholesaler_ind = Column(String(1))
    is_school_or_daycare_ind = Column(String(1))
    service_connections_count = Column(BigInteger)
    submission_status_code = Column(String(1))
    org_name = Column(String(100))
    admin_name = Column(String(100))
    email_addr = Column(String(100))
    phone_number = Column(String(15))
    phone_ext_number = Column(String(10))
    fax_number = Column(String(15))
    alt_phone_number = Column(String(15))
    address_line1 = Column(String(200))
    address_line2 = Column(String(200))
    city_name = Column(String(40))
    zip_code = Column(String(14))
    country_code = Column(String(2))
    first_reported_date = Column(Date)
    last_reported_date = Column(Date)
    state_code = Column(String(2))
    source_water_protection_code = Column(String(2))
    source_protection_begin_date = Column(Date)
    outstanding_performer = Column(String(2))
    outstanding_perform_begin_date = Column(Date)
    reduced_rtcr_monitoring = Column(String(20))
    reduced_monitoring_begin_date = Column(Date)
    reduced_monitoring_end_date = Column(Date)
    seasonal_startup_system = Column(String(40))

class GeographicArea(database.Base):
    __tablename__ = "sdwa_geographic_areas"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    geo_id = Column(String(20), primary_key=True)
    area_type_code = Column(String(10))
    tribal_code = Column(String(10))
    state_served = Column(String(10))
    ansi_entity_code = Column(String(10))
    zip_code_served = Column(String(5))
    city_served = Column(String(40))
    county_served = Column(String(40))
    last_reported_date = Column(Date)
    geom = Column(Geometry('POINT'))

class Facility(database.Base):
    __tablename__ = "sdwa_facilities"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    facility_id = Column(String(12), primary_key=True)
    facility_name = Column(String(100))
    state_facility_id = Column(String(40))
    facility_activity_code = Column(String(1))
    facility_deactivation_date = Column(Date)
    facility_type_code = Column(String(4))
    submission_status_code = Column(String(4))
    is_source_ind = Column(String(1))
    water_type_code = Column(String(4))
    availability_code = Column(String(4))
    seller_treatment_code = Column(String(4))
    seller_pwsid = Column(String(9))
    seller_pws_name = Column(String(100))
    filtration_status_code = Column(String(4))
    is_source_treated_ind = Column(String(1))
    first_reported_date = Column(Date)
    last_reported_date = Column(Date)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Violation(database.Base):
    __tablename__ = "sdwa_violations_enforcement"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), ForeignKey("sdwa_pub_water_systems.pwsid"))
    violation_id = Column(String(20), primary_key=True, index=True)
    facility_id = Column(String(12))
    non_compl_per_begin_date = Column(Date)
    non_compl_per_end_date = Column(Date)
    violation_code = Column(String(10))
    violation_category_code = Column(String(5))
    is_health_based_ind = Column(String(1))
    contaminant_code = Column(String(10))
    viol_measure = Column(String(255))
    unit_of_measure = Column(String(9))
    federal_mcl = Column(String(31))
    state_mcl = Column(String(255))
    is_major_viol_ind = Column(String(1))
    severity_ind_cnt = Column(String(255))
    calculated_rtc_date = Column(Date)
    violation_status = Column(String(11))
    public_notification_tier = Column(Integer)
    calculated_pub_notif_tier = Column(Integer)
    viol_originator_code = Column(String(10))
    sample_result_id = Column(String(40))
    corrective_action_id = Column(String(40))
    rule_code = Column(String(10))
    rule_group_code = Column(String(10))
    rule_family_code = Column(String(10))
    viol_first_reported_date = Column(Date)
    viol_last_reported_date = Column(Date)
    enforcement_id = Column(String(20))
    enforcement_date = Column(Date)
    enforcement_action_type_code = Column(String(4))
    enf_action_category = Column(String(4000))
    enf_originator_code = Column(String(4))
    enf_first_reported_date = Column(Date)
    enf_last_reported_date = Column(Date)

class LcrSample(database.Base):
    __tablename__ = "sdwa_lcr_samples"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    sample_id = Column(String(20), primary_key=True)
    sampling_end_date = Column(Date)
    sampling_start_date = Column(Date)
    reconciliation_id = Column(String(40))
    sample_first_reported_date = Column(Date)
    sample_last_reported_date = Column(Date)
    sar_id = Column(Numeric, primary_key=True)
    contaminant_code = Column(String(4))
    result_sign_code = Column(String(5))
    sample_measure = Column(Numeric)
    unit_of_measure = Column(String(4))
    sar_first_reported_date = Column(Date)
    sar_last_reported_date = Column(Date)

class RefCodeValue(database.Base):
    __tablename__ = "sdwa_ref_code_values"

    value_type = Column(String(40), primary_key=True)
    value_code = Column(String(40), primary_key=True)
    value_description = Column(String(250))

class EventMilestone(database.Base):
    __tablename__ = "sdwa_events_milestones"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    event_schedule_id = Column(String(20), primary_key=True)
    event_end_date = Column(Date)
    event_actual_date = Column(Date)
    event_comments_text = Column(String(2000))
    event_milestone_code = Column(String(4))
    event_reason_code = Column(String(4))
    first_reported_date = Column(Date)
    last_reported_date = Column(Date)

class PnViolationAssoc(database.Base):
    __tablename__ = "sdwa_pn_violation_assoc"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    pn_violation_id = Column(String(20), primary_key=True)
    related_violation_id = Column(String(20))
    non_compl_per_begin_date = Column(Date)
    non_compl_per_end_date = Column(Date)
    violation_code = Column(String(10))
    contaminant_code = Column(String(10))
    first_reported_date = Column(Date)
    last_reported_date = Column(Date)

class ServiceArea(database.Base):
    __tablename__ = "sdwa_service_areas"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    service_area_type_code = Column(String(4), primary_key=True)
    is_primary_service_area_code = Column(String(1))
    first_reported_date = Column(Date)
    last_reported_date = Column(Date)

class SiteVisit(database.Base):
    __tablename__ = "sdwa_site_visits"

    submissionyearquarter = Column(String(7))
    pwsid = Column(String(9), primary_key=True)
    visit_id = Column(String(20), primary_key=True)
    visit_date = Column(Date)
    agency_type_code = Column(String(2))
    visit_reason_code = Column(String(4))
    management_ops_eval_code = Column(String(1))
    source_water_eval_code = Column(String(1))
    security_eval_code = Column(String(1))
    pumps_eval_code = Column(String(1))
    other_eval_code = Column(String(1))
    compliance_eval_code = Column(String(1))
    data_verification_eval_code = Column(String(1))
    treatment_eval_code = Column(String(1))
    finished_water_stor_eval_code = Column(String(1))
    distribution_eval_code = Column(String(1))
    financial_eval_code = Column(String(1))
    visit_comments = Column(String(2000))
    first_reported_date = Column(Date)
    last_reported_date = Column(Date)
