#!/usr/bin/env python3
"""
Patient Data Cleaner

This script standardizes and filters patient records according to specific rules:

Data Cleaning Rules:
1. Names: Capitalize each word (e.g., "john smith" -> "John Smith")
2. Ages: Convert to integers, set invalid ages to 0
3. Filter: Remove patients under 18 years old
4. Remove any duplicate records

Input JSON format:
    [
        {
            "name": "john smith",
            "age": "32",
            "gender": "male",
            "diagnosis": "hypertension"
        },
        ...
    ]

Output:
- Cleaned list of patient dictionaries
- Each patient should have:
  * Properly capitalized name
  * Integer age (≥ 18)
  * Original gender and diagnosis preserved
- No duplicate records
- Prints cleaned records to console

Example:
    Input: {"name": "john smith", "age": "32", "gender": "male", "diagnosis": "flu"}
    Output: {"name": "John Smith", "age": 32, "gender": "male", "diagnosis": "flu"}

Usage:
    python patient_data_cleaner.py
"""

import json
import os
import pandas as pd

def load_patient_data(filepath):
    """
    Load patient data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list: List of patient dictionaries
    """
    # BUG: No error handling for file not found
    try:
        with open(filepath, 'r') as file:
            json_file = json.load(file)
            return pd.DataFrame(json_file)
    except:
        return("No file found")

def clean_patient_data(patients):
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(patients)

    # Standardize and clean
    df['name'] = df['name'].str.title()
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0).astype(int)

    # Filter patients age 18+
    df = df[df['age'] >= 18]

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Convert back to list of dicts
    cleaned_patients = df.to_dict(orient='records')

    return cleaned_patients if cleaned_patients else None

def main():
    """Main function to run the script."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_path = os.path.join(script_dir, 'data', 'raw', 'patients.json')
    print(data_path)
    # BUG: No error handling for load_patient_data failure
    try:
        patients = load_patient_data(data_path)
    except:
        exit("load data failed")
    
    # Clean the patient data
    cleaned_patients = clean_patient_data(patients)
    if cleaned_patients is not None:
        # BUG: No check if cleaned_patients is None
        # Print the cleaned patient data
        print("Cleaned Patient Data:")
        for patient in cleaned_patients:
            # BUG: Using 'name' key but we changed it to 'nage'
            print(f"Name: {patient['name']}, Age: {patient['age']}, Diagnosis: {patient['diagnosis']}")
    else:
        print('No qualified patients')
    # Return the cleaned data (useful for testing)
    return cleaned_patients

if __name__ == "__main__":
    main()