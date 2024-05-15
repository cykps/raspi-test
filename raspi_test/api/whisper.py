from openai import OpenAI
from dotenv import load_dotenv
import time
start_time = time.time()

load_dotenv()
client = OpenAI()

audio_file= open("api/assets/cut.mp3", "rb")

api_start_time = time.time()

transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

end_time = time.time()

print(transcription.text)

print("preparation: %d, run: %d" %(api_start_time - start_time, end_time - api_start_time))
