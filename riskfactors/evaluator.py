import os
from riskfactors2 import extract_risk_factors  # Importing the function from riskfactors.py

# Path to the QTR1 directory containing the 200 files
directory_path = "/Users/anasoni/FEI/BRIP/data/2023/QTR1"

# Counters for success and total files
total_files = 0
found_risk_factors = 0

# Loop through all files in the QTR1 folder
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    # Check if the file is a text file
    if filename.endswith(".txt"):
        total_files += 1
        print(f"Extracting from {file_path}:")
        result = extract_risk_factors(file_path)
        print(result[:500])  # Print the first 500 characters to ensure we’re capturing meaningful content
        print("\n" + "="*50 + "\n")

        # Increment counter if something is found
        if "not applicable" not in result.lower() and "content not found" not in result.lower() and "section not found" not in result.lower():
            found_risk_factors += 1

# Calculate and print the success rate
if total_files > 0:
    success_rate = (found_risk_factors / total_files) * 100
    print(f"Successfully found Risk Factors content in {found_risk_factors} out of {total_files} documents.")
    print(f"Success rate: {success_rate:.2f}%")
else:
    print("No files found in the directory.")

