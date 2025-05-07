# scripts/clean_data.py

import pandas as pd
import os

def load_data(file_path):
    """Load the original dataset."""
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    """Clean and prepare the dataset."""
    print("Starting data cleaning...")

    # 1. Convert Intake Date to datetime
    df['Intake Date'] = pd.to_datetime(df['Intake Date'], errors='coerce')

    # 2. Drop rows where Intake Date is missing after conversion
    df = df.dropna(subset=['Intake Date'])

    # 3. Filter: Keep only data from 2022-01-01 to 2023-12-31
    mask = (df['Intake Date'] >= '2022-01-01') & (df['Intake Date'] <= '2023-12-31')
    df = df.loc[mask]

    # 4. Create "Month" column (for trend charts)
    df['Month'] = df['Intake Date'].dt.to_period('M').astype(str)

    # 5. Create "Total Compensation" column (Refund Amount + Contract Cancelled Amount)
    df['Refund Amount'] = pd.to_numeric(df['Refund Amount'], errors='coerce').fillna(0)
    df['Contract Cancelled Amount'] = pd.to_numeric(df['Contract Cancelled Amount'], errors='coerce').fillna(0)
    df['Total Compensation'] = df['Refund Amount'] + df['Contract Cancelled Amount']

    # 6. Create "Satisfaction" flag (simple rule: if Result contains "Satisfied")
    df['Satisfaction'] = df['Result'].str.contains('Satisfied', case=False, na=False).astype(int)

    # 7. Fill missing important fields with "Unknown" if necessary
    important_cols = ['Business Category', 'Complaint Code', 'Result', 'City', 'State', 'Postcode', 'Borough']
    df[important_cols] = df[important_cols].fillna('Unknown')

    print("Data cleaning finished.")
    return df

def save_data(df, output_path):
    """Save cleaned dataset."""
    print(f"Saving cleaned data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("File saved successfully.")

def main():
    input_file = os.path.join('data', 'DCWP_Consumer_Complaints_20250428.csv')
    output_file = os.path.join('data', 'cleaned_consumer_complaints.csv')

    df = load_data(input_file)
    df_cleaned = clean_data(df)
    save_data(df_cleaned, output_file)

if __name__ == "__main__":
    main()
