import boto3
import time
import requests
from botocore.exceptions import NoCredentialsError, ClientError

# Constants
bucket_name = 'your-s3-bucket-name'
file_name = 'path/to/your/audiofile.mp3'
s3_file_name = 'audiofile.mp3'
job_name = "your_transcription_job_name"
custom_vocabulary_name = "your_custom_vocabulary_name"
vocabulary_file = "path/to/vocabulary.txt"  # File with custom vocabulary terms

# Upload file to S3
s3 = boto3.client('s3')
try:
    s3.upload_file(file_name, bucket_name, s3_file_name)
    print("Upload Successful")
except FileNotFoundError:
    print("The file was not found")
except NoCredentialsError:
    print("Credentials not available")

# Create Custom Vocabulary (optional)
try:
    s3.upload_file(vocabulary_file, bucket_name, vocabulary_file)
    print("Vocabulary upload successful")
except FileNotFoundError:
    print("The vocabulary file was not found")
except NoCredentialsError:
    print("Credentials not available")

transcribe = boto3.client('transcribe')

try:
    transcribe.create_vocabulary(
        VocabularyName=custom_vocabulary_name,
        LanguageCode='hi-IN',
        VocabularyFileUri=f"s3://{bucket_name}/{vocabulary_file}"
    )
    print("Custom vocabulary created successfully")
except ClientError as e:
    print("Error creating custom vocabulary:", e)

# Transcribe Audio
job_uri = f"s3://{bucket_name}/{s3_file_name}"

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',  # Change this based on your file format
    LanguageCode='hi-IN',  # Hindi language code
    Settings={
        'VocabularyName': custom_vocabulary_name  # Use custom vocabulary if created
    }
)

# Wait for the job to complete
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(10)

if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print("Transcription completed successfully!")
else:
    print("Transcription failed")

# Retrieve and Read Transcription
transcription_text = requests.get(transcript_uri).json()
hindi_text = transcription_text['results']['transcripts'][0]['transcript']
print(hindi_text)

# Translate Hindi Text to English
translate = boto3.client('translate')

response = translate.translate_text(
    Text=hindi_text,
    SourceLanguageCode='hi',
    TargetLanguageCode='en'
)

english_text = response['TranslatedText']
print("Translated Text: ", english_text)
