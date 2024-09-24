import os
from pytube import YouTube
from pydub import AudioSegment
from pytube.exceptions import PytubeError
from pydub.exceptions import CouldntDecodeError
import pandas as pd

def initialize_youtube(url):
    try:
        yt = YouTube(url)
        return yt
    except (PytubeError, Exception) as e:
        print(f"Error initializing YouTube: {e}")
        return None

def convert_audio_16khz(in_file, out_file):
    try:
        song = AudioSegment.from_file(in_file)
        if song.frame_rate != 16000:
            song = song.set_frame_rate(16000)
        song.export(out_file, format="wav")
        print(f"Converted {in_file} to {out_file} at 16000 Hz")
    except CouldntDecodeError:
        print(f"Error decoding audio file {in_file}")

def download_audio(yt, audio_folder_path):
    try: 
        audio_stream = yt.streams.filter(only_audio=True).first()  
        if not audio_stream:
            print("No audio stream found")
            return None
            
        video_title = yt.title  
        original_filename = f"{video_title}.wav"
        converted_filename = f"{video_title}_16000hz.wav"
        
        original_full_path = os.path.join(audio_folder_path, original_filename)
        converted_full_path = os.path.join(audio_folder_path, converted_filename)

        if os.path.exists(original_full_path) or os.path.exists(converted_full_path):
            print(f"{original_filename} or {converted_filename} already exists. Checking sample rate...")
            try:
                if os.path.exists(original_full_path):
                    song = AudioSegment.from_file(original_full_path)
                else:
                    song = AudioSegment.from_file(converted_full_path)
                
                if song.frame_rate != 16000:
                    print(f"Warning: {original_filename} or {converted_filename} is not at 16000 Hz")
                return original_filename if os.path.exists(original_full_path) else converted_filename
            except CouldntDecodeError:
                print(f"Error decoding audio file {original_full_path} or {converted_full_path}")
                return None
        else:
            print(f"Downloading audio: {original_filename}")
            audio_stream.download(output_path=audio_folder_path, filename=original_filename)
            print("Download complete")
            
            # Convert audio if not 16k Hz
            try:
                song = AudioSegment.from_file(original_full_path)  
                if song.frame_rate != 16000:
                    song = song.set_frame_rate(16000) 
                    song.export(converted_full_path, format="wav")
                    os.remove(original_full_path)  # Remove the original file
                    print(f"Converted {original_filename} to 16000 Hz")
                    return converted_filename
                else:
                    return original_filename
            except CouldntDecodeError:
                print(f"Error decoding downloaded audio file {original_full_path}")
                return None
            
    except (PytubeError, Exception) as e:
        print(f"Error downloading audio: {e}")
        return None



def update_dataframe(df, index, audio_title, excel_file_path):
    df.at[index, 'Audio_Title'] = audio_title
    print(f"Updated Audio_Title: {audio_title}")
    df.to_excel(excel_file_path, index=False)  # save to the original file

def download_youtube_audio_from_excel(excel_file_path, audio_folder_path):
    df = pd.read_excel(excel_file_path, sheet_name=0)

    for index, row in df.iterrows():
        try:
            youtube_url = row['Video_Link']

            yt = initialize_youtube(youtube_url)

            if yt:
                downloaded_title = download_audio(yt, audio_folder_path)
                if downloaded_title:
                    update_dataframe(df, index, downloaded_title, excel_file_path)

        except Exception as e:
            print(f"Error processing link: {youtube_url}. Error: {e}")

# Paths:
excel_file_path = "../2014 and 2019 elections.xlsx"
audio_folder_path = "../Audio"
download_youtube_audio_from_excel(excel_file_path, audio_folder_path)
