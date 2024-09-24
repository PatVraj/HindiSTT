import boto3
import time
import json
import re

# Initialize AWS clients
s3 = boto3.client('s3')
transcribe = boto3.client('transcribe', 'us-east-2')  # Specify your region here

# Configuration
bucket_name = 'ecocaudio'
prefix = '16HzAudio/'
output_bucket = 'ecocaudio'
output_key = 'transcriptions/'  # Folder in the output bucket for transcriptions
language_code = 'hi-IN'
custom_language_model = 'jun24CLM2'  # Name of your Custom Language Model

def list_s3_files(bucket):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj['Key'] for obj in response.get('Contents', [])]

def get_transcribed_files():
    try:
        response = s3.get_object(Bucket=output_bucket, Key='transcribed_files.json')
        return json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        return []

def update_transcribed_files(transcribed_files):
    s3.put_object(
        Bucket=output_bucket,
        Key='transcribed_files.json',
        Body=json.dumps(transcribed_files).encode('utf-8')
    )

def sanitize_job_name(name):
    # Replace invalid characters with underscores
    return re.sub(r'[^0-9a-zA-Z._-]', '_', name)

def start_transcription_job(job_name, file_uri):
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        OutputBucketName=output_bucket,
        OutputKey=output_key,
        LanguageCode=language_code,
        ModelSettings={'LanguageModelName': custom_language_model}
    )

def main():
    s3_files = list_s3_files(bucket_name)
    transcribed_files = get_transcribed_files()
    total_transcribed = len(transcribed_files)
    current_run_transcribed = 0
    
    for file_name in s3_files:
        if file_name not in transcribed_files:
            sanitized_file_name = sanitize_job_name(file_name)
            job_name = f"transcribe_{sanitized_file_name.replace('.', '_')}"
            file_uri = f"s3://{bucket_name}/{file_name}"
            
            try:
                start_transcription_job(job_name, file_uri)
                print(f"Started transcription job for {file_name}")
                
                # Wait for job to complete
                while True:
                    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
                    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                        break
                    print("Not ready yet...")
                    time.sleep(30)

                if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                    current_run_transcribed += 1
                    transcribed_files.append(file_name)
                    update_transcribed_files(transcribed_files)
                    print(f"Transcription completed for {file_name}")
                else:
                    print(f"Transcription failed for {file_name}")
            
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
        
        else:
            print(f"Skipping {file_name} - already transcribed")

    print(f"Files transcribed on this run: {current_run_transcribed}")   
    print(f"Total files transcribed: {total_transcribed}")

if __name__ == "__main__":
    main()
