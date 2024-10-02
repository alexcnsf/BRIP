import os
import re
import csv

# Regular expression to find the CIK
cik_pattern = re.compile(r'CENTRAL INDEX KEY:\s*(\d{10})')

# Function to extract CIK from a document
def extract_cik(file_content):
    match = cik_pattern.search(file_content)
    if match:
        return match.group(1)
    return None

# Function to loop through all years, quarters, and files
def scrape_ciks(folder_path):
    cik_data = {}
    
    # Walk through the directory structure
    for year in os.listdir(folder_path):
        year_path = os.path.join(folder_path, year)
        
        # Ensure it's a directory (skip any files)
        if os.path.isdir(year_path):
            for quarter in os.listdir(year_path):
                quarter_path = os.path.join(year_path, quarter)
                
                if os.path.isdir(quarter_path):
                    for filename in os.listdir(quarter_path):
                        file_path = os.path.join(quarter_path, filename)
                        
                        if filename.endswith(".txt"):
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                                    content = file.read()
                                    cik = extract_cik(content)
                                    
                                    if cik:
                                        if cik not in cik_data:
                                            cik_data[cik] = {}
                                        # Mark the CIK as present for that year/quarter
                                        cik_data[cik][f'{year}_{quarter}'] = file_path
                            except Exception as e:
                                print(f"Error reading {file_path}: {e}")
    
    return cik_data

# Function to create CSV with CIK presence information
def create_cik_csv(cik_data, all_years_quarters, csv_filename='cik_presence.csv'):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header (CIK + year/quarter columns)
        header = ['CIK'] + all_years_quarters
        writer.writerow(header)
        
        # Write each row: CIK + presence/null in each year/quarter
        for cik, year_quarters in cik_data.items():
            row = [cik]  # Start with CIK
            
            # Loop through all possible year/quarter combinations
            for yq in all_years_quarters:
                row.append(year_quarters.get(yq, 'NULL'))  # Either file path or 'NULL'
            
            writer.writerow(row)

# Identify all year/quarter combinations (i.e., columns)
def get_all_years_quarters(folder_path):
    all_years_quarters = []
    
    for year in os.listdir(folder_path):
        year_path = os.path.join(folder_path, year)
        
        if os.path.isdir(year_path):
            for quarter in os.listdir(year_path):
                if os.path.isdir(os.path.join(year_path, quarter)):
                    all_years_quarters.append(f'{year}_{quarter}')
    
    return sorted(all_years_quarters)

# Main logic to scrape and store the CIK presence in CSV
def main():
    folder_path = 'data'  # Your root folder containing year/quarter structure
    
    # Get all year/quarter combinations
    all_years_quarters = get_all_years_quarters(folder_path)
    
    # Scrape CIKs from documents
    cik_data = scrape_ciks(folder_path)
    
    # Create the CSV report
    create_cik_csv(cik_data, all_years_quarters)

# Run the main function
main()

