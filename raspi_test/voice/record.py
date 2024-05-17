import wave
import sys
import time

import pyaudio
import RPi.GPIO as GPIO

### pyaudio ###
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5
###

### RPi.GPIO ###
GPIO.setmode(GPIO.BCM)
button_pin = 23

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
###

with wave.open('output.wav', 'wb') as wf:
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