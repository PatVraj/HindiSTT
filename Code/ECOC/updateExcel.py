import os
import boto3
import hashlib
import logging
import pandas as pd
import json
from urllib.parse import urlparse


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the S3 client
s3 = boto3.client('s3')

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def download_files(bucket_name, folder_name, download_path):
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    downloaded = []
    if 'Contents' in objects:
        for obj in objects['Contents']:
            file_name = obj['Key']
            local_path = os.path.join(download_path, file_name)
            try:
                ensure_dir(local_path)
                if not os.path.exists(local_path):
                    logging.info(f"Downloading new file: {file_name}")
                    s3.download_file(bucket_name, file_name, local_path)
                    downloaded.append(file_name)
                else:
                    # Check if the file has changed
                    s3_etag = obj['ETag'].strip('"')
                    local_hash = get_file_hash(local_path)
                    if s3_etag != local_hash:
                        logging.info(f"Updating changed file: {file_name}")
                        s3.download_file(bucket_name, file_name, local_path)
                        downloaded.append(file_name)
                    else:
                        logging.info(f"File already up to date: {file_name}")
            except Exception as e:
                logging.error(f"Error downloading {file_name}: {str(e)}")
    else:
        logging.warning(f"No objects found in bucket {bucket_name} with prefix {folder_name}")
    return downloaded

def update_dataframe_with_transcripts(df, download_path, link_column, remove_words, new_files):
    # Get the speech title from the provided link
    parsed_url = urlparse(link_column)
    speech_title = os.path.basename(parsed_url.path).rsplit("-", 1)[0]  # Extract title from URL path

    for file_name in new_files:
        local_path = os.path.join(download_path, file_name)
        # Clean downloaded file name (assuming it follows a pattern)
        audio_file_name = file_name.replace('transcriptions/', '').replace('.json', '').lower()

        # Match based on cleaned file name and speech title (after cleaning)
        if speech_title.lower() in audio_file_name:
            # Perform additional cleaning on speech title if needed (remove extra stop words)
            clean_speech_title = speech_title.lower()
            for word in remove_words:
                clean_speech_title = clean_speech_title.replace(word.lower(), '')

            with open(local_path, 'r') as f:
                transcription_data = json.load(f)
            
            # Assuming the transcription text is in the 'results' -> 'transcripts' -> first 'transcript' key
            transcription_text = transcription_data.get('results', {}).get('transcripts', [{}])[0].get('transcript', '')
            
            # Update DataFrame only if there's a match (considering duplicates)
            if not df[clean_speech_title].any():  # Check for existing row with same title (avoid duplicates)
                df = df.append({'Audio_Title': clean_speech_title, 'ASR_AWS': transcription_text}, ignore_index=True)
            
    return df

# Main execution
bucket_name = 'totalhindiaudio'
folder_name = 'transcriptions/'
download_path = './downloads'
excel_file_path = '../../speech_data(AutoRecovered).xlsx'
link_column = 'Speech_Text'

remove_words = ['text-of', 'prime-minister', 'narendra-modis-speech-at', 'in']

try:
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    new_files = download_files(bucket_name, folder_name, download_path)
    logging.info(f"Downloaded {len(new_files)} new or updated files.")

    df = pd.read_excel(excel_file_path)

    df = update_dataframe_with_transcripts(df, download_path, link_column, remove_words, new_files)

    df.to_excel(excel_file_path, index=False)
    logging.info("Transcriptions added successfully.")
except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
