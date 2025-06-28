import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import glob

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host="localhost",
        database="water_data",
        user="user",
        password="password"
    )

def clean_and_prepare_data(df, table_name):
    """Cleans and prepares the DataFrame for insertion."""
    # Convert column names to lowercase to match schema
    df.columns = [col.lower() for col in df.columns]

    # Drop duplicate/unwanted columns before processing
    if table_name == 'sdwa_violations_enforcement' or table_name == 'sdwa_pn_violation_assoc':
        df = df.drop(columns=['compl_per_begin_date', 'compl_per_end_date'], errors='ignore')
    if table_name == 'sdwa_violations_enforcement':
        df = df.drop(columns=['pws_deactivation_date'], errors='ignore')


    # Handle date columns - convert to None if invalid
    date_columns = [
        'pws_deactivation_date', 'first_reported_date', 'last_reported_date',
        'source_protection_begin_date', 'outstanding_perform_begin_date',
        'reduced_monitoring_begin_date', 'reduced_monitoring_end_date',
        'facility_deactivation_date', 'non_compl_per_begin_date',
        'non_compl_per_end_date', 'calculated_rtc_date', 'enforcement_date',
        'viol_first_reported_date', 'viol_last_reported_date',
        'enf_first_reported_date', 'enf_last_reported_date',
        'sampling_end_date', 'sampling_start_date',
        'sample_first_reported_date', 'sample_last_reported_date',
        'sar_first_reported_date', 'sar_last_reported_date',
        'event_end_date', 'event_actual_date', 'visit_date'
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            # Convert NaT to None, then format to date string
            df[col] = df[col].apply(lambda x: x.date() if pd.notnull(x) else None)

    # Replace numpy.nan with None for SQL compatibility
    df = df.where(pd.notnull(df), None)

    if table_name == 'sdwa_violations_enforcement':
        int_cols = ['public_notification_tier', 'calculated_pub_notif_tier']
        for col in int_cols:
            # Coerce to numeric, then fill NA with a placeholder, convert to int, and replace placeholder with None
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype(int).replace(-1, None)

    # Special handling for ref_code_values to prevent null primary keys
    if table_name == 'sdwa_ref_code_values':
        df.dropna(subset=['value_type', 'value_code'], inplace=True)

    # Special handling for pn_violation_assoc to prevent duplicate primary keys
    if table_name == 'sdwa_pn_violation_assoc':
        df.drop_duplicates(subset=['pwsid', 'pn_violation_id'], keep='first', inplace=True)

    if table_name == 'sdwa_violations_enforcement':
        df.dropna(subset=['violation_id'], inplace=True)
        df.drop_duplicates(subset=['violation_id'], keep='first', inplace=True)

    return df


def ingest_csv(conn, file_path, table_name):
    """Ingests a single CSV file into the specified table."""
    print(f"Processing {file_path} for table {table_name}...")
    try:
        df = pd.read_csv(file_path, low_memory=False)
        df = clean_and_prepare_data(df, table_name)
        print(f"Columns for {table_name}: {list(df.columns)}")

        with conn.cursor() as cur:
            # Clear the table before inserting new data
            cur.execute(f"TRUNCATE TABLE {table_name} CASCADE;")

            # Prepare data for insertion
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))

            # Use execute_values for efficient bulk insertion
            query = f"INSERT INTO {table_name} ({cols}) VALUES %s"
            execute_values(cur, query, tuples)

            conn.commit()
            print(f"Successfully ingested {len(df)} rows into {table_name}.")

    except Exception as e:
        print(f"Error ingesting {file_path}: {e}")
        conn.rollback()


def main():
    """Main function to orchestrate the data ingestion process."""
    conn = get_db_connection()

    # Mapping of CSV filenames to table names
    file_to_table_map = {
        'SDWA_PUB_WATER_SYSTEMS.csv': 'sdwa_pub_water_systems',
        'SDWA_GEOGRAPHIC_AREAS.csv': 'sdwa_geographic_areas',
        'SDWA_FACILITIES.csv': 'sdwa_facilities',
        'SDWA_VIOLATIONS_ENFORCEMENT.csv': 'sdwa_violations_enforcement',
        'SDWA_LCR_SAMPLES.csv': 'sdwa_lcr_samples',
        'SDWA_REF_CODE_VALUES.csv': 'sdwa_ref_code_values',
        'SDWA_EVENTS_MILESTONES.csv': 'sdwa_events_milestones',
        'SDWA_PN_VIOLATION_ASSOC.csv': 'sdwa_pn_violation_assoc',
        'SDWA_SERVICE_AREAS.csv': 'sdwa_service_areas',
        'SDWA_SITE_VISITS.csv': 'sdwa_site_visits'
    }

    data_dir = 'data'
    for file_name, table_name in file_to_table_map.items():
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            ingest_csv(conn, file_path, table_name)
        else:
            print(f"Warning: File not found - {file_path}")

    conn.close()
    print("\nData ingestion complete.")

if __name__ == "__main__":
    main()
