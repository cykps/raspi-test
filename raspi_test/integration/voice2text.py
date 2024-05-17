import wave
import sys
import time
import io

import pyaudio
import RPi.GPIO as GPIO

### pyaudio ###
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

audio_buffer = io.BytesIO()
audio_buffer.name = "voice.wav"
###

### RPi.GPIO ###
GPIO.setmode(GPIO.BCM)
button_pin = 23

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
###

### OpenAi(Whisper) ###
from openai import OpenAI
from dotenv import load_dotenv
start_time = time.time()

load_dotenv()
openai_client = OpenAI()
###

with wave.open(audio_buffer, 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    print('Ready to record')
    while True:
        if GPIO.input(button_pin) == 1: #wait
            time.sleep(0.2)
        else: #start recording
            print('Recording...')
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
            while GPIO.input(button_pin) == 0:
                wf.writeframes(stream.read(CHUNK))
            print('Done')

            stream.close()
            p.terminate()
            break

audio_buffer.seek(0)

api_start_time = time.time()

transcription = openai_client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_buffer,
  response_format='json',
  language='ja'
)

trans_end_time = time.time()

print(transcription.text)

completion = openai_client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "丁寧な言い方に変換してください"},
    {"role": "user", "content": transcription.text}
  ]
)

end_time = time.time()

print(completion.choices[0].message)



print("preparation: %5.2f, trans: %5.2f, gpt: %5.2f" %(api_start_time - start_time, trans_end_time - api_start_time, end_time - trans_end_time))
