import pandas as pd
import re
from datetime import datetime, timedelta

# Function to parse the text file
def parse_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        
    entries = re.findall(r'Date: (.*?)\nLink: (.*?)\n', data)
    return [{'Date': datetime.strptime(date, '%B %d, %Y'), 'Link': link} for date, link in entries]

# Function to group data by week and save to Excel files
def save_weekly_excel(entries):
    start_date = entries[0]['Date']
    end_date = entries[-1]['Date']
    
    current_date = start_date
    while current_date <= end_date:
        week_entries = [entry for entry in entries if current_date <= entry['Date'] < current_date + timedelta(days=7)]
        if week_entries:
            df = pd.DataFrame(week_entries)
            week_start_str = current_date.strftime('%Y-%m-%d')
            week_end_str = (current_date + timedelta(days=6)).strftime('%Y-%m-%d')
            filename = f'week_{week_start_str}_to_{week_end_str}.xlsx'
            df.to_excel(filename, index=False)
            print(f'Saved {filename}')
        current_date += timedelta(days=7)

# Parse the text file and save weekly data to Excel files
entries = parse_text_file('speech_links.txt')
entries.sort(key=lambda x: x['Date'])
save_weekly_excel(entries)
