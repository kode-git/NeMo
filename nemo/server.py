from flask import *  # Flask modules for server side services
from flask_cors import CORS  # CORS required
import requests  # to make some request to rasa
from asr.ASR_Model import *  # ASR modules
from tts.TTS_Model import *  # TTS modules
# default packages
import numpy as np
import os
import spacy
import wikipedia
from nemo.collections.nlp.models import QAModel
from nlp.QAModel import _QAModel

# instance the app
app = Flask(__name__)
CORS(app)

# ASR modules setup
asr = ASR_Model()

# TTS modules setup
# tts = TTS_Model()
# tts.downloadSpectogramGenerator()
# tts.downloadVocoder()

# QAModel 
qaModel = _QAModel().getModel()

# Spacy
nlp = spacy.load('en_core_web_sm')

# utils
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
    print(
        f"Intent found: {intent_name} with a confidence level of {prediction.get('intent').get('confidence')}")

    trigger_json = {}
    returnValue = "I didn't understand, can you repeat?"
    if(intent_name == "ask_wiki"):
        # ask_wiki intent
        print('Ask Wiki invocation')
        # define returnValue
        returnValue = dispatchingQAModel(question)
    else:
        # Other intent different from ask_wiki
        trigger_json = {
        "name": str(intent_name),
        "entities": {},
        }
        entities = prediction.get('entities')
        for element in entities:
            trigger_json.get('entities')[element.get('entity')] = element.get('value')
        print('Trigger JSON to submit to the trigger_intent API:')
        print(trigger_json)
        url = 'http://localhost:5005/conversations/default/trigger_intent'
        jarvis_response = requests.post(url, json=trigger_json, headers=headers)
        jarvis_response = jarvis_response.json()
        client_response = [jarvis_response.get('messages')[0].get('text')]
        print(f"Bot says: {client_response}")
        returnValue = client_response[0]
    
    # return the response to the client in Json format
    print('---------------------------------------------------------------')
    return returnValue


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
    _transcript = asr.model.transcribe(
        paths2audio_files=[path + filename + ''], logprobs=True)[0]
    probs = asr.softmax(_transcript)
    _text = asr.beam.forward(log_probs=np.expand_dims(
        probs, axis=0), log_probs_length=None)
    if _text[0][0][1] != None:
        data = _text[0][0][1]
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
    print('Filename taken from the request is: ',
          filename, ' and message to write is: ', message)
    print(f'Starting encoding...')
    tts.downloadVocoder()
    audio = tts.textToSpeech(message, './static/speech/' + filename + ".wav")
    print('Play the audio file...')
    os.system(f"play {audio}")
    print('Return the message\" ', message, ' \"to the client')
    print('---------------------------------------------------------------')
    return message

# Internal function


def dispatchingQAModel(text):
    print('----------------------------- Wikipedia Dispatcher -----------------------------------')
    sentence = text.replace('search', '')
    print('Text input is: ' + sentence)
    try:
        doc = nlp(sentence)
        print("Part-of-Speech extrapolation")
        oblique_phrase = get_info_phrase(doc)
        print("Result: " + str(oblique_phrase))
        print("Keys words: ", oblique_phrase)
        print(wikipedia.search(oblique_phrase))
        result = wikipedia.summary(oblique_phrase, auto_suggest=False)
    except wikipedia.exceptions.PageError:
        # Page Error on Wikipedia scraping
        new_search = wikipedia.search(oblique_phrase)[0]
        result = wikipedia.summary(new_search)
    except wikipedia.DisambiguationError as e:
        # Page Semantic Error on the Disambiguation
        result = wikipedia.summary(e.options[0])

    title = oblique_phrase
    context = result
    question = sentence
    # Input of the QaModel with the Squad_v1 formatting
    myInput = {
        "data": [
            {
                    "title": title,
                    "paragraphs": [
                        {
                            "context": context,
                            "qas": [
                                {
                                    "question": question,
                                    "id": "56be4db0acb8001400a502ee"
                                }
                            ]
                        }
                    ]
                }
        ]
    }
    # Transform it in JSON
    inputFile = json.dumps(myInput)
    # Writing the bert_input to submit to QA_Model
    with open('bert_input.json', 'w') as outfile:
        outfile.write(inputFile)

    print('Inference on the QA_Model...')
    output = qaModel.inference('bert_input.json')
    for value in output[0].items():
        text = f"The answer is: " + str(value[1][1])
    print('-------------------------------------------------------------------------------------------')
    return text


def get_info_phrase(doc):
    phrase = " "
    for token in doc:
        print(str(token)+" => " + str(token.pos_))
        print(str(token)+" => " + str(token.dep_))
        if (
            "PRON" in token.pos_ or
            "ADJ" in token.pos_ or
            "PROPN" in token.pos_ or
            "NOUN" in token.pos_ or
            "NUM" in token.pos_ or
            "ADV" in token.pos_
        ):
            if(str(token) != 'who' and
                str(token) != 'where' and
                str(token) != 'when' and
                str(token) != 'why' and
                str(token) != 'which' and
                    str(token) != 'what'):
                phrase = phrase + str(token) + " "

    return phrase


app.run(host='0.0.0.0', port=4000)
