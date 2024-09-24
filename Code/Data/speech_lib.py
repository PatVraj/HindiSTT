import yt_dlp
import os
import pandas as pd
from datetime import datetime

# Create the directory for storing the audio files
output_dir = "ElectionConduct_Audio"
os.makedirs(output_dir, exist_ok=True)

# URL of the playlist
playlist_url = 'https://www.youtube.com/playlist?list=PLBG6UuYpOcTsQwd1AGLLhks_aPAWfeJMH'

# Function to sanitize filenames
def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in ' -_.']).rstrip()

# Configuration for yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
}

# Create a list to store video information
video_info = []

# Create a yt-dlp object
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    # Extract playlist information
    playlist = ydl.extract_info(playlist_url, download=False)
    
    if 'entries' in playlist:
        for entry in playlist['entries']:
            title = entry.get('title', 'Untitled')
            sanitized_title = sanitize_filename(title)
            url = entry.get('webpage_url', '')
            upload_date = entry.get('upload_date', '')
            if upload_date:
                upload_date = datetime.strptime(upload_date, '%Y%m%d').strftime('%Y-%m-%d')
            
            # Attempt to download the video
            try:
                ydl.download([url])
                downloaded = True
            except Exception as e:
                print(f"Error downloading {title}: {str(e)}")
                downloaded = False
            
            video_info.append({
                'Title': title,
                'URL': url,
                'Upload Date': upload_date,
                'Downloaded': downloaded
            })

# Create a DataFrame from the video information
df = pd.DataFrame(video_info)

# Function to color the 'Downloaded' column
def color_downloaded(val):
    color = 'green' if val else 'red'
    return f'background-color: {color}'

# Save the DataFrame to an Excel file with colored 'Downloaded' column
excel_file = 'video_info.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Video Info')
    workbook = writer.book
    worksheet = writer.sheets['Video Info']
    
    # Apply conditional formatting to the 'Downloaded' column
    downloaded_col = df.columns.get_loc('Downloaded') + 1  # +1 because Excel columns start at 1
    for row in range(2, len(df) + 2):  # +2 because Excel rows start at 1 and we have a header
        cell = worksheet.cell(row=row, column=downloaded_col)
        cell.fill = openpyxl.styles.PatternFill(start_color='00FF00' if df.iloc[row-2]['Downloaded'] else 'FF0000',
                                                end_color='00FF00' if df.iloc[row-2]['Downloaded'] else 'FF0000',
                                                fill_type='solid')

print(f"Download completed! Video information saved to {excel_file}")