import re

def extract_risk_factors(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Define start and end of the Risk Factors section
    start_pattern = r"ITEM\s*1A[\.\s]*RISK FACTORS"
    end_pattern = r"ITEM\s+1B[\.\s]*|ITEM\s+2[\.\s]*"  # End at Item 1B or Item 2

    # Find all occurrences of Risk Factors section
    matches = re.findall(f'{start_pattern}(.*?){end_pattern}', content, re.S | re.I)

    if matches:
        # Find the longest match
        longest_match = max(matches, key=len).strip()

        # Check if the match contains "Not applicable" or similar phrases
        if "not applicable" in longest_match.lower():
            return "Risk Factors: Not applicable in this document."
        
        # Return the longest match if it has significant content
        return longest_match if len(longest_match) > 100 else "Risk Factors content not found."
    else:
        return "Risk Factors section not found or missing."

# List of file paths
file_paths = [
    "/Users/anasoni/FEI/BRIP/data/2023/QTR1/20230103_10-K_edgar_data_1487931_0001477932-23-000012.txt",
    "/Users/anasoni/FEI/BRIP/data/2023/QTR1/20230103_10-K_edgar_data_1828739_0001477932-23-000002.txt",
    "/Users/anasoni/FEI/BRIP/data/2023/QTR1/20230103_10-K-A_edgar_data_1880151_0001104659-22-131423.txt",
    "/Users/anasoni/FEI/BRIP/data/2023/QTR1/20230103_10-Q_edgar_data_1538217_0001493152-22-037214.txt"
]

# Extract and print Risk Factors for each file
for file_path in file_paths:
    print(f"Extracting from {file_path}:")
    result = extract_risk_factors(file_path)
    print(result[:500])  # Print the first 500 characters to ensure we’re capturing meaningful content
    print("\n" + "="*50 + "\n")

