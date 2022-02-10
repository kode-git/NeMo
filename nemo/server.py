from flask import * # Flask modules for server side services
from flask_cors import CORS # CORS required
import requests # to make some request to rasa
from asr.ASR_Model import * # ASR modules
from tts.TTS_Model import * # TTS modules
# default packages 
import numpy as np
import os

# instance the app
app = Flask(__name__)
CORS(app)

# ASR modules setup
asr = ASR_Model()

# TTS modules setup
tts = TTS_Model()
tts.downloadSpectogramGenerator()
tts.downloadVocoder() 


#utils 
global counter
counter = 0

# main index page which return the index.html
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# main function to get back the rasa response given a question in input
@app.route('/intent', methods=["POST"])
def sendIntent(): 
    content = request.get_json()
    question = content['text']
    print('----------------------- Intent API ------------------------------')
    print(f"Sending '{question}' to the Rasa server")
    
    # request Rasa Server for the intent with highest level of confidence
    payload = {'text': str(question)}
    headers = {'content-type': 'application/json'}
    url = 'http://localhost:5005/model/parse'
    prediction = requests.post(url, json=payload, headers=headers)
    print(f"Status code: {prediction.status_code} for url response on {url}")
    prediction = prediction.json()
    intent_name = prediction.get('intent').get('name')
    print(f"Intent found: {intent_name} with a confidence level of {prediction.get('intent').get('confidence')}")
    
    # gives the text associated to the intent in the Rasa Server response and forward it to client
    trigger_json = {
        "name" : str(intent_name),
        "entities": {
            "temperature": "high"
        },
    }
    url = 'http://localhost:5005/conversations/default/trigger_intent'
    jarvis_response = requests.post(url, json=trigger_json, headers=headers)
    jarvis_response = jarvis_response.json()
    client_response = [jarvis_response.get('messages')[0].get('text')]
    print(f"Bot says: {client_response}")
    # return the response to the client in Json format
    print('---------------------------------------------------------------')
    return client_response[0]

@app.route('/asr', methods=["POST"])
def transcribeAudio():
    print("-------------------------- ASR API ----------------------------")
    print('Getting the blob file from the formData')
    file = request.files.get('file')
    print('Getting the name of thefile')
    filename = request.form['name']
    path = "./static/audio/"
    print(f'Saving file...')
    file.save(path + filename)
    print(f'File saved on {path}{filename}')
    print('Starting ASR...')
    _transcript = asr.model.transcribe(paths2audio_files=[path + filename + ''], logprobs=True)[0]
    probs = asr.softmax(_transcript)
    _text = asr.beam.forward(log_probs = np.expand_dims(probs, axis=0), log_probs_length=None)
    if _text[0][0][1] != None:
        data =  _text[0][0][1]
    else:
        data = _transcript
    print(f"Prediction text: {data}")
    print('---------------------------------------------------------------')
    return jsonify(transcript=data)

@app.route('/tts', methods=["POST"])
def encodeText():
    print("-------------------------- TTS API ----------------------------")
    print('Getting context')
    content = request.get_json()
    message = content['text']
    filename = content['filename']
    print('Filename taken from the request is: ', filename, ' and message to write is: ', message)
    print(f'Starting encoding...')
    audio = tts.textToSpeech(message, './static/speech/' + filename + ".wav" )
    print('Play the audio file...')
    os.system(f"play {audio}")
    print('Return the message\" ', message, ' \"to the client')
    print('---------------------------------------------------------------')
    return message


app.run(host='0.0.0.0', port=4000)



