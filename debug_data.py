from app import load_data
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("Loading data...")
try:
    df_appt, df_inv = load_data()
    
    print("\n--- APPOINTMENTS (Head) ---")
    print(df_appt.head())
    print("\n--- APPOINTMENTS (Info) ---")
    print(df_appt.info())
    print("\n--- APPOINTMENTS (Describe) ---")
    print(df_appt.describe())
    
    print("\n" + "="*50 + "\n")

    print("\n--- INVOICES (Head) ---")
    print(df_inv.head())
    print("\n--- INVOICES (Info) ---")
    print(df_inv.info())
    print("\n--- INVOICES (Describe) ---")
    print(df_inv.describe())

except Exception as e:
    print(f"Error loading data: {e}")
