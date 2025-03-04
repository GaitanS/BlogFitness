import pandas as pd
import os

# Path to the Excel file
excel_file = r"C:\Users\Silviu\Downloads\Calculator nutritie website.xlsx"

# Check if the file exists
if not os.path.exists(excel_file):
    print(f"Error: File {excel_file} not found")
    exit(1)

# Load the Excel file
try:
    # Try to read all sheets
    excel_data = pd.ExcelFile(excel_file)
    sheet_names = excel_data.sheet_names
    print(f"Excel file contains {len(sheet_names)} sheets: {', '.join(sheet_names)}")
    
    # Read each sheet
    for sheet_name in sheet_names:
        print(f"\n--- Sheet: {sheet_name} ---")
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Display basic info about the sheet
        print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print("Columns:", df.columns.tolist())
        
        # Try to identify BMI calculation formulas
        if "BMI" in ' '.join(df.columns).upper():
            print("\nFound BMI-related columns:")
            bmi_cols = [col for col in df.columns if "BMI" in str(col).upper()]
            for col in bmi_cols:
                print(f"  - {col}")
        
        # Look for gender-specific calculations
        gender_keywords = ["bărbat", "barbat", "masculin", "femeie", "feminin"]
        for keyword in gender_keywords:
            if any(keyword.lower() in str(col).lower() for col in df.columns):
                print(f"\nFound {keyword}-related columns:")
                gender_cols = [col for col in df.columns if keyword.lower() in str(col).lower()]
                for col in gender_cols:
                    print(f"  - {col}")
        
        # Display first few rows to understand structure
        print("\nSample data:")
        print(df.head(3).to_string())
        
        # Try to extract formulas (note: pandas doesn't directly access Excel formulas)
        print("\nNote: To see actual Excel formulas, manual inspection of the file is required.")
        print("This script can only analyze the calculated values.")

except Exception as e:
    print(f"Error analyzing Excel file: {str(e)}")
