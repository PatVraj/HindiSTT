

### For Weeks excel files


# import pandas as pd
# import re
# import glob
# import os

# # Define a function to extract location from URL
# def extract_location(url):
#     match = re.search(r'-in-([a-zA-Z0-9\-]+)', url)
#     if match:
#         # Replace dashes with spaces
#         location = match.group(1).replace('-', ' ')
#         print(f"URL: {url}\nExtracted location: {location}")
#         return location
#     print(f"URL: {url}\nExtracted location: None")
#     return None

# # Directory containing the Excel files
# directory_path = '/Users/vrajpatel/Desktop/work/IBS/Komal_Kaur/HindiSTT/Code/ECOC/Weeks/'

# # Find all Excel files in the directory
# excel_files = glob.glob(directory_path + '*.xlsx')

# # Process each Excel file
# for file_path in excel_files:
#     # Skip temporary and hidden files
#     if os.path.basename(file_path).startswith('~$'):
#         print(f"Skipping file: {file_path}")
#         continue
    
#     print(f"Processing file: {file_path}")
    
#     try:
#         # Load the Excel file
#         df = pd.read_excel(file_path)

#         # Apply the function to the 'Speech' column to extract locations
#         df['Location'] = df['Speech'].apply(extract_location)

#         # Save the DataFrame with the new 'Location' column to the same Excel file
#         df.to_excel(file_path, index=False)

#         print(f"Updated file saved: {file_path}")
#     except Exception as e:
#         print(f"Failed to process file {file_path}: {e}")

# print("All files have been processed and updated.")



### For video_info.xlsx


import pandas as pd
import re

# Define a function to extract location from title
def extract_location_from_title(title):
    match = re.search(r'in ([a-zA-Z\s]+,[a-zA-Z\s]+)', title)
    if match:
        location = match.group(1).strip()
        print(f"Title: {title}\nExtracted location: {location}")
        return location
    print(f"Title: {title}\nExtracted location: None")
    return None

# Load the Excel file
file_path = '/Users/vrajpatel/Desktop/work/IBS/Komal_Kaur/HindiSTT/Code/ECOC/video_info.xlsx'  # Change this to your file path
df = pd.read_excel(file_path)

# Apply the function to the 'Title' column to extract locations
df['Location'] = df['Title'].apply(extract_location_from_title)

# Save the DataFrame with the new 'Location' column to the same Excel file
df.to_excel(file_path, index=False)

print(f"Updated file saved: {file_path}")
