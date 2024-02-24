import vosk
import sys
import os
import pyaudio, json
from openai import OpenAI
from datetime import datetime, timedelta

gpt_client = OpenAI()
last_asked_gpt = datetime.now() - timedelta(seconds=10)
CL = '\r'

def askChatGPT(transcript: str):
    global last_asked_gpt
    now = datetime.now()
    if now - last_asked_gpt < timedelta(seconds=5):
        # only check every 10 seconds
        return False
    last_asked_gpt = datetime.now()
    gpt_response = gpt_client.chat.completions.create(
        model="gpt-4-1106-preview",
        temperature=0.1,
        messages=[
            {"role": "system", "content": "Read the following transcript. Check for any instance of pretending to be an old friend, especially attempting to make the other party guess their identity. Strictly answer 'yes' if so, 'no' otherwise"},
            {"role": "user", "content": transcript},
        ]
    )
    ans = gpt_response.choices[0].message.content.lower()
    print('real')
    if ans == 'yes':
        return True
    elif ans == 'no':
        return False
    else:
        print('ChatGPT is not complying\n', ans)
        return False

# Define the path to the Vosk model and set up the Vosk recognizer
MODEL_PATH = "model"
if not os.path.exists(MODEL_PATH):
    print(f"Please download and unzip the Vosk model to {MODEL_PATH}")
    sys.exit(1)
    
vosk.SetLogLevel(-1)  # Disable Vosk log messages

# Initialize the Vosk recognizer
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Set up the PyAudio microphone input
audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

# Main loop to continuously transcribe audio
print("Listening... Press Ctrl+C to exit.")
log = ''
last_partial = ''
try:
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())['text']
            if len(result) == 0: continue
            log += last_partial
            print("\nFull:", log)
        else:
            r = json.loads(recognizer.PartialResult())['partial']
            if len(r) == 0: continue
            last_partial = r
            print(CL + r, end='', flush=True)
            ans = askChatGPT(log + r)
            if ans:
                print(CL + "\nFLAGGED!!!\n\n", log + r)
                break
except KeyboardInterrupt:
    pass
finally:
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    audio.terminate()

