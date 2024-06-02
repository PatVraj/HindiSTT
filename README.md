# Audio Translation and Transcription Tools

This repository contains Python scripts and Jupyter notebooks for translating and transcribing audio content. Whether you're working with Hindi audio files or extracting text from YouTube videos, these tools streamline the process. Below, each script and its functionality are described.

## Scripts Overview (Code)

1. **(Transcribe)Amazon.ipynb**
   - This Python script transcribes Hindi audio files stored in Amazon S3 using the AWS Transcribe service.
   - Key features:
     - Utilizes the boto3 library to interact with AWS Transcribe.
     - Starts a transcription job for the provided S3 URI of the audio file.
     - Specifies the language code for Hindi and the output S3 bucket for the transcription result.
     - Prints a message indicating the start of the transcription job.

2. **(Transcribe)Azure.ipynb**
   - This Jupyter notebook demonstrates how to transcribe Hindi audio files using Azure Cognitive Services Speech SDK.
   - Key features:
     - Imports the necessary library and sets up the Azure Speech configuration.
     - Defines a function to transcribe Hindi audio files.
     - Performs speech recognition using the Azure Speech SDK.
     - Prints the transcribed text or error details.

3. **(Transcribe)Deepgram.ipynb**
   - This Jupyter notebook showcases how to transcribe Hindi audio files using Deepgram's API.
   - Key features:
     - Imports the necessary libraries and sets up the Deepgram client.
     - Defines a function to transcribe Hindi audio files.
     - Sends the audio file to Deepgram for transcription, specifying language and model options.
     - Prints the JSON response containing the transcribed text.

4. **(Transcribe)Google.ipynb**
   - This Jupyter notebook transcribes Hindi audio stored in Google Cloud Storage to text using Google Speech-to-Text.
   - Key features:
     - Authenticates and configures the API.
     - Sends an asynchronous recognition request for the audio file.
     - Processes the response to extract transcripts, timestamps, and confidence scores for each spoken segment.

5. **(Transcribe)NeuralSpace.ipynb**
   - This Jupyter notebook demonstrates how to transcribe and translate Hindi audio files using the NeuralSpace API.
   - Key features:
     - Installs the NeuralSpace Python library.
     - Initializes the VoiceAI object with the API key.
     - Configures job settings for file transcription and translation.
     - Submits a transcription job for a Hindi audio file and prints the job ID.
     - Retrieves and prints the status of the transcription job.

6. **(Transcribe)Whisper.ipynb**
   - This Jupyter notebook handles transcription or translation of audio files.
   - Key features:
     - Checks for ffmpeg and installs it if needed.
     - Iterates through audio files, checking formats and selecting languages.
     - Loads Whisper models, sets options, and transcribes or translates the audio.
     - Uses the OpenAI API if a key is provided; otherwise, it uses a local model.
     - Formats and saves results in various formats to a user-specified folder.

7. **(Translate)Azure.ipynb**
   - This Jupyter notebook illustrates how to translate Hindi text to English using the Azure Translator Text API.
   - Key features:
     - Defines a function to translate Hindi text to English using the Azure Translator Text API.
     - Sends a POST request to the API endpoint with the Hindi text to be translated.
     - Parses the response to extract the translated English text.
     - Saves the translated text to a specified output file.
     - Prints a message upon completion, indicating the path to the translated text file.

8. **(Translate)Google.ipynb**
   - This Jupyter notebook utilizes the Google Cloud Translation API to translate a Hindi text file into English.
   - Key features:
     - Installs the necessary library and sets up authentication.
     - Defines functions to read the Hindi text, translate it into English, and write the result to a new file.

9. **Compare.ipynb**
   - This function compares two text files line by line (sentence by sentence).
   - Key features:
     - Defines a function `read_file` to read a file and return its content as a list of sentences.
     - Defines a function `compare_files` to compare two files line by line.
     - Reads the content of both files and splits them into sentences.
     - Compares the sentences from both files and prints any differences.
     - Usage example provided to demonstrate how to compare two translated text files.

10. **WER.ipynb - Word Error Rate (WER) Statistics and Visualization**
   - This function computes various statistics to evaluate the performance of an Automatic Speech Recognition (ASR) system based on the Word Error Rate (WER).
   - Key features:
     - Defines a function `load_text` to read the content of a text file.
     - Defines a function `preprocess_text` to preprocess the text by converting it to lowercase, removing punctuation, and extra whitespaces.
     - Defines a function `compute_wer_stats` to compute WER and additional statistics such as insertion rate, deletion rate, substitution rate, and accuracy.
     - Usage example provided to demonstrate how to compute statistics for comparing ASR output with a master text.
     - Explanation provided for each statistic to clarify its meaning and significance in evaluating ASR performance.
   - Additionally, a function `plot_statistics` is defined to visualize the computed statistics.
     - The function takes a list of dictionaries containing statistics and their titles as input.
     - It generates horizontal bar plots for each set of statistics, displaying the percentage values and titles.
     - Usage example provided to demonstrate how to plot statistics for multiple ASR comparisons.

11. **YoutubeToAudio16Hz.py**
   - This Python script automates downloading audio from YouTube videos listed in an Excel file.
   - Key features:
     - Utilizes the pytube library to interact with YouTube.
     - Reads YouTube URLs from an Excel sheet.
     - Downloads in 16Hz as most ASR models work best with this sampling rate
     - Initializes YouTube objects, extracts audio streams, and saves them as WAV files.
     - Ensures filenames are created using video titles and avoids duplicates.

## Output Overview (Text)

1. **Transcriptions**
   - Contains format(s) of Hindi text: .txt
   - If any results from ASR API request is recvieved, it is saved here

2. **Translations**
   - Contains format(s) of Hindi text: .txt
   - Based on Transcription result, each translation API is used one text to find best overall accuracy

## Getting Started

1. **Prerequisites**
   - Ensure you have Python installed (version 3.10 or higher).
   - Set up a Google Cloud project and obtain the necessary credentials (service account key) for the Translation and Speech-to-Text APIs.
   - Install required Python libraries (`pip install -r requirements.txt`).
      - google-auth: Required for authentication with Google Cloud services (used in the speech-to-text script)
      - google-cloud-speech: Used for the Google Speech-to-Text functionality
      - gtts: Used for text-to-speech functionality (not explicitly shown in provided snippets)
      - openai: Required for the OpenAI API usage in the Whisper script
      - pydub: Used for audio manipulation in the Whisper script
      - pytube: As mentioned before, used for YouTube interaction and audio download
      - requests: A common HTTP library for making requests
      - scipy: A scientific computing library
      - tensorflow: A machine learning framework
      - torch: Another popular machine learning framework
      - whisper: The core library for speech processing and translation using the Whisper model
      - boto3: interacting with AWS services, used in the Amazon S3 transcription script
      - jiwer: computing Word Error Rate (WER) for ASR evaluation.

2. **Usage**
   - Customize the scripts by replacing placeholders (e.g., `YOUR_SERVICE_ACCOUNT_KEY.json`, input/output file paths).
   - Step 1. Clone this repository: `git clone https://github.com/<username>/<project>`
   - Step 2. Using a Virtual Enviroment is recommened: `python -m venv env`
      - Activate Virtual Enviroments:

         `source env/bin/activate`  # Linux/macOS

         `env\Scripts\activate.bat`   # Windows

   - Step 3. Install dependencies: `pip install -r requirements.txt`

