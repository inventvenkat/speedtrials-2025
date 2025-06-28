-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Drop tables if they exist to ensure a clean slate
DROP TABLE IF EXISTS sdwa_violations_enforcement CASCADE;
DROP TABLE IF EXISTS sdwa_site_visits CASCADE;
DROP TABLE IF EXISTS sdwa_service_areas CASCADE;
DROP TABLE IF EXISTS sdwa_ref_code_values CASCADE;
DROP TABLE IF EXISTS sdwa_pub_water_systems CASCADE;
DROP TABLE IF EXISTS sdwa_pn_violation_assoc CASCADE;
DROP TABLE IF EXISTS sdwa_lcr_samples CASCADE;
DROP TABLE IF EXISTS sdwa_geographic_areas CASCADE;
DROP TABLE IF EXISTS sdwa_facilities CASCADE;
DROP TABLE IF EXISTS sdwa_events_milestones CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Table for Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Operator', 'Regulator')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for Public Water Systems
CREATE TABLE sdwa_pub_water_systems (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) PRIMARY KEY,
    pws_name VARCHAR(100),
    primacy_agency_code VARCHAR(2),
    epa_region VARCHAR(2),
    season_begin_date VARCHAR(10),
    season_end_date VARCHAR(10),
    pws_activity_code VARCHAR(1),
    pws_deactivation_date DATE,
    pws_type_code VARCHAR(6),
    dbpr_schedule_cat_code VARCHAR(6),
    cds_id VARCHAR(100),
    gw_sw_code VARCHAR(2),
    lt2_schedule_cat_code VARCHAR(6),
    owner_type_code VARCHAR(1),
    population_served_count BIGINT,
    pop_cat_2_code VARCHAR(2),
    pop_cat_3_code VARCHAR(2),
    pop_cat_4_code VARCHAR(2),
    pop_cat_5_code VARCHAR(2),
    pop_cat_11_code VARCHAR(2),
    primacy_type VARCHAR(20),
    primary_source_code VARCHAR(4),
    is_grant_eligible_ind VARCHAR(1),
    is_wholesaler_ind VARCHAR(1),
    is_school_or_daycare_ind VARCHAR(1),
    service_connections_count BIGINT,
    submission_status_code VARCHAR(1),
    org_name VARCHAR(100),
    admin_name VARCHAR(100),
    email_addr VARCHAR(100),
    phone_number VARCHAR(15),
    phone_ext_number VARCHAR(10),
    fax_number VARCHAR(15),
    alt_phone_number VARCHAR(15),
    address_line1 VARCHAR(200),
    address_line2 VARCHAR(200),
    city_name VARCHAR(40),
    zip_code VARCHAR(14),
    country_code VARCHAR(2),
    first_reported_date DATE,
    last_reported_date DATE,
    state_code VARCHAR(2),
    source_water_protection_code VARCHAR(2),
    source_protection_begin_date DATE,
    outstanding_performer VARCHAR(2),
    outstanding_perform_begin_date DATE,
    reduced_rtcr_monitoring VARCHAR(20),
    reduced_monitoring_begin_date DATE,
    reduced_monitoring_end_date DATE,
    seasonal_startup_system VARCHAR(40)
);

-- Table for Geographic Areas
CREATE TABLE sdwa_geographic_areas (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    geo_id VARCHAR(20),
    area_type_code VARCHAR(10),
    tribal_code VARCHAR(10),
    state_served VARCHAR(10),
    ansi_entity_code VARCHAR(10),
    zip_code_served VARCHAR(5),
    city_served VARCHAR(40),
    county_served VARCHAR(40),
    last_reported_date DATE,
    geom GEOMETRY(Point, 4326), -- For storing geocoded coordinates
    PRIMARY KEY (pwsid, geo_id)
);

-- Table for Facilities
CREATE TABLE sdwa_facilities (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    facility_id VARCHAR(12),
    facility_name VARCHAR(100),
    state_facility_id VARCHAR(40),
    facility_activity_code VARCHAR(1),
    facility_deactivation_date DATE,
    facility_type_code VARCHAR(4),
    submission_status_code VARCHAR(4),
    is_source_ind VARCHAR(1),
    water_type_code VARCHAR(4),
    availability_code VARCHAR(4),
    seller_treatment_code VARCHAR(4),
    seller_pwsid VARCHAR(9),
    seller_pws_name VARCHAR(100),
    filtration_status_code VARCHAR(4),
    is_source_treated_ind VARCHAR(1),
    first_reported_date DATE,
    last_reported_date DATE,
    PRIMARY KEY (pwsid, facility_id)
);

-- Table for Violations and Enforcement
CREATE TABLE sdwa_violations_enforcement (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    violation_id VARCHAR(20) PRIMARY KEY,
    facility_id VARCHAR(12),
    non_compl_per_begin_date DATE,
    non_compl_per_end_date DATE,
    violation_code VARCHAR(10),
    violation_category_code VARCHAR(5),
    is_health_based_ind VARCHAR(1),
    contaminant_code VARCHAR(10),
    viol_measure VARCHAR(255),
    unit_of_measure VARCHAR(9),
    federal_mcl VARCHAR(31),
    state_mcl VARCHAR(255),
    is_major_viol_ind VARCHAR(1),
    severity_ind_cnt VARCHAR(255),
    calculated_rtc_date DATE,
    violation_status VARCHAR(11),
    public_notification_tier INTEGER,
    calculated_pub_notif_tier INTEGER,
    viol_originator_code VARCHAR(10),
    sample_result_id VARCHAR(40),
    corrective_action_id VARCHAR(40),
    rule_code VARCHAR(10),
    rule_group_code VARCHAR(10),
    rule_family_code VARCHAR(10),
    viol_first_reported_date DATE,
    viol_last_reported_date DATE,
    enforcement_id VARCHAR(20),
    enforcement_date DATE,
    enforcement_action_type_code VARCHAR(4),
    enf_action_category VARCHAR(4000),
    enf_originator_code VARCHAR(4),
    enf_first_reported_date DATE,
    enf_last_reported_date DATE
);

-- Table for Lead and Copper Rule Samples
CREATE TABLE sdwa_lcr_samples (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    sample_id VARCHAR(20),
    sampling_end_date DATE,
    sampling_start_date DATE,
    reconciliation_id VARCHAR(40),
    sample_first_reported_date DATE,
    sample_last_reported_date DATE,
    sar_id NUMERIC,
    contaminant_code VARCHAR(4),
    result_sign_code VARCHAR(5),
    sample_measure NUMERIC,
    unit_of_measure VARCHAR(4),
    sar_first_reported_date DATE,
    sar_last_reported_date DATE,
    PRIMARY KEY (pwsid, sample_id, sar_id)
);

-- Table for Reference Codes
CREATE TABLE sdwa_ref_code_values (
    value_type VARCHAR(40),
    value_code VARCHAR(40),
    value_description VARCHAR(250),
    PRIMARY KEY (value_type, value_code)
);

-- Table for Events and Milestones
CREATE TABLE sdwa_events_milestones (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    event_schedule_id VARCHAR(20),
    event_end_date DATE,
    event_actual_date DATE,
    event_comments_text VARCHAR(2000),
    event_milestone_code VARCHAR(4),
    event_reason_code VARCHAR(4),
    first_reported_date DATE,
    last_reported_date DATE,
    PRIMARY KEY (pwsid, event_schedule_id)
);

-- Table for Public Notice Violation Associations
CREATE TABLE sdwa_pn_violation_assoc (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    pn_violation_id VARCHAR(20),
    related_violation_id VARCHAR(20),
    non_compl_per_begin_date DATE,
    non_compl_per_end_date DATE,
    violation_code VARCHAR(10),
    contaminant_code VARCHAR(10),
    first_reported_date DATE,
    last_reported_date DATE,
    PRIMARY KEY (pwsid, pn_violation_id)
);

-- Table for Service Areas
CREATE TABLE sdwa_service_areas (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    service_area_type_code VARCHAR(4),
    is_primary_service_area_code VARCHAR(1),
    first_reported_date DATE,
    last_reported_date DATE
);

-- Table for Site Visits
CREATE TABLE sdwa_site_visits (
    submissionyearquarter VARCHAR(7),
    pwsid VARCHAR(9) REFERENCES sdwa_pub_water_systems(pwsid),
    visit_id VARCHAR(20),
    visit_date DATE,
    agency_type_code VARCHAR(2),
    visit_reason_code VARCHAR(4),
    management_ops_eval_code VARCHAR(1),
    source_water_eval_code VARCHAR(1),
    security_eval_code VARCHAR(1),
    pumps_eval_code VARCHAR(1),
    other_eval_code VARCHAR(1),
    compliance_eval_code VARCHAR(1),
    data_verification_eval_code VARCHAR(1),
    treatment_eval_code VARCHAR(1),
    finished_water_stor_eval_code VARCHAR(1),
    distribution_eval_code VARCHAR(1),
    financial_eval_code VARCHAR(1),
    visit_comments VARCHAR(2000),
    first_reported_date DATE,
    last_reported_date DATE,
    PRIMARY KEY (pwsid, visit_id)
);
