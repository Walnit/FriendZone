import audioop
import base64
import json
import os
from flask import Flask, request
from flask_sock import Sock, ConnectionClosed
from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
import vosk
from openai import OpenAI
from datetime import datetime, timedelta
from pyngrok import ngrok

#from twilio.rest.resources import Call

app = Flask(__name__)
sock = Sock(app)
model = vosk.Model('model')

gpt_client = OpenAI()
twilio_client = Client()

CL = '\r'

last_asked_gpt = datetime.now() - timedelta(seconds=10)

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


@app.route('/call', methods=['POST'])
def call():
    """Accept a phone call."""
    try:
        print(f'Incoming call from {request.form["From"]}')
    except:
        print(f'error')
    response = VoiceResponse()
    start = Start()
    start.stream(url=f'wss://{request.host}/stream')
    response.append(start)
    response.say('Please say your name')
    # response.dial('65-8834-3074')
    response.pause(58)
    # response.gather(input='speech', action='/completed')
    print(f'Incoming call from {request.form["From"]}')
    return str(response), 200, {'Content-Type': 'text/xml'}


call_log = last_partial = ''
@sock.route('/stream')
def stream(ws):
    global call_log, last_partial
    """Receive and transcribe audio stream."""
    rec = vosk.KaldiRecognizer(model, 16000)
    while True:
        message = ws.receive()
        packet = json.loads(message)
        if packet['event'] == 'start':
            print('Streaming is starting')
        elif packet['event'] == 'stop':
            print('\nStreaming has stopped')
        elif packet['event'] == 'media':
            audio = base64.b64decode(packet['media']['payload'])
            audio = audioop.ulaw2lin(audio, 2)
            audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
            if rec.AcceptWaveform(audio):
                call_log += last_partial
                last_partial = ''
            else:
                r = json.loads(rec.PartialResult())['partial']
                if len(r) == 0: continue
                last_partial = r
                print(CL + r, end='', flush=True)
                is_scam = askChatGPT(call_log + r)
                if is_scam:
                    print(CL + "\n\nFLAGGED !!!\n\n", call_log+r)
                    try:
                        callList = twilio_client.calls.list(status='in-progress')
                        print('inprog:', callList)
                        for call in callList:
                            call.update(status='completed')
                    except Exception as e:
                        print('error call list in-progress')
                        print(e)


if __name__ == '__main__':
    port = 5000
    public_url = ngrok.connect(port, bind_tls=True).public_url
    number = twilio_client.incoming_phone_numbers.list()[0]
    number.update(voice_url=public_url + '/call')
    print(f'Waiting for calls on {number.phone_number}')

    app.run(port=port)
