import pandas as pd

file_path = 'data/SDWA_VIOLATIONS_ENFORCEMENT.csv'
df = pd.read_csv(file_path, low_memory=False)
df.columns = [col.lower() for col in df.columns]

# These are the columns that should be integers/bigints
int_columns = [
    'public_notification_tier',
    'calculated_pub_notif_tier'
]

for col in int_columns:
    for i, val in enumerate(df[col]):
        try:
            # Try to convert to a float first to handle decimals, then to int
            if pd.notna(val):
                int(float(val))
        except (ValueError, TypeError):
            print(f"Row {i}, Column '{col}': Cannot convert '{val}' to int.")

print("\nDebug script finished.")
