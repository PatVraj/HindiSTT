# import os
# import json
# import asyncio
# import pandas as pd
# from dotenv import load_dotenv
# from deepgram import DeepgramClient, PrerecordedOptions, FileSource

# load_dotenv()

# # Load API key from environment variable
# API_KEY = os.getenv("DEEPGRAM_API_TEST")

# # Path to the folder containing audio files
# AUDIO_FOLDER = "../Audio"

# # Path to the folder where transcription results will be saved
# OUTPUT_FOLDER = "TT"



# # Read the Excel file to get the row number for each audio file
# df = pd.read_excel("../2014 and 2019 elections.xlsx")

# async def transcribe_audio_file(file_path, deepgram, row_index):
#     try:
#         with open(file_path, "rb") as file:
#             buffer_data = file.read()

#         payload = {
#             "buffer": buffer_data,
#         }

#         options = PrerecordedOptions(
#             smart_format=True, model="nova-2", language="hi"
#         )


#         response = await deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

#         # Get the corresponding row from the Excel file
#         row = df.iloc[row_index]

#         # Create an ID based on the row number
#         id_number = row_index + 1

#         # Use the audio title and ID to name the output JSON file
#         output_file_name = f"{id_number}_{row['Audio_Title'].replace('.wav', '.json')}"

#         # Save the response to a JSON file in the output folder
#         output_file_path = os.path.join(OUTPUT_FOLDER, output_file_name)
#         with open(output_file_path, "w") as output_file:
#             json.dump(response.to_dict(), output_file, indent=4)

#         print(f"Transcription saved to {output_file_path}")
#         print("-------------------------------------------------------")

#     except Exception as e:
#         print(f"Error processing {file_path}: {e}")





# async def process_audio_files():
#     try:
#         # Create a Deepgram client using the API key
#         deepgram = DeepgramClient(API_KEY)

#         # Create the output folder if it doesn't exist
#         if not os.path.exists(OUTPUT_FOLDER):
#             os.makedirs(OUTPUT_FOLDER)

#         # Loop through all files in the audio folder and transcribe each one asynchronously
#         audio_files = [os.path.join(AUDIO_FOLDER, filename) for filename in os.listdir(AUDIO_FOLDER) if filename.endswith(".wav")]
        
#         for index, audio_file in enumerate(audio_files):
#             await transcribe_audio_file(audio_file, deepgram, index)

#     except Exception as e:
#         print(f"Exception: {e}")


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(process_audio_files())
#     loop.close()

# Non Async with buffer file
import os
import io
import json
import tempfile
import shutil
import pandas as pd
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource

load_dotenv()

# Load API key from environment variable
API_KEY = os.getenv("DEEPGRAM_API_TEST")

# Path to the folder containing audio files
AUDIO_FOLDER = "../Audio"

# Path to the folder where transcription results will be saved
OUTPUT_FOLDER = "TT"

# Read the Excel file to get the row number for each audio file
df = pd.read_excel("../2014 and 2019 elections.xlsx")

def transcribe_audio_file(file_path, deepgram, row_index):
    try:
        with open(file_path, "rb") as file:
            buffer_data = file.read()

        payload = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            smart_format=True, model="nova-2", language="hi"
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # Get the corresponding row from the Excel file
        row = df.iloc[row_index]

        # Create an ID based on the row number
        id_number = row_index + 1

        # Use the audio title and ID to name the output JSON file
        output_file_name = f"{id_number}_{row['Audio_Title'].replace('.wav', '.json')}"

        # Create a temporary directory for writing the output file
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file_path = os.path.join(temp_dir, output_file_name)
            with open(output_file_path, "w") as output_file:
                json.dump(response.to_dict(), output_file, indent=4)

            # Move the file from the temporary directory to the output folder
            final_output_path = os.path.join(OUTPUT_FOLDER, output_file_name)
            shutil.move(output_file_path, final_output_path)

        print(f"Transcription saved to {final_output_path}")
        print("-------------------------------------------------------")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_audio_files():
    try:
        # Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        # Create the output folder if it doesn't exist
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Loop through all files in the audio folder and transcribe each one synchronously
        audio_files = [os.path.join(AUDIO_FOLDER, filename) for filename in os.listdir(AUDIO_FOLDER) if filename.endswith(".wav")]
        for index, audio_file in enumerate(audio_files):
            transcribe_audio_file(audio_file, deepgram, index)

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    process_audio_files()