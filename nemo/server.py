from flask import *  # Flask modules for server side services
from flask_cors import CORS  # CORS required
import requests  # to make some request to rasa
from asr.ASR_Model import *  # ASR modules
from tts.TTS_Model import *  # TTS modules
# default packages
import numpy as np
import itertools, spacy, smtplib, wikipedia
from nemo.collections.nlp.models import QAModel
from nlp.QAModel import _QAModel
from pymongo import MongoClient
from bson.objectid import ObjectId
from time import strftime
from email.message import EmailMessage


# instance the app
app = Flask(__name__)
CORS(app)

# ASR modules setup
asr = ASR_Model()


# QAModel
qaModel = _QAModel().getModel()

# Spacy
nlp = spacy.load('en_core_web_sm')

# utils
global counter
counter = 0

global mailReceiver
global contentBody
mailReceiver = ""
contentBody = ""

# MongoDB setup
client = MongoClient(
    "mongodb+srv://Jarvis:JarvisNLP@cluster0.zbc0n.mongodb.net/todo_db?retryWrites=true&w=majority")
db = client['todo_db']  # name of the database
actions = db['actions']  # name of collection


# main index page which return the index.html
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# main function to get back the rasa response given a question in input


@app.route('/intent', methods=["POST"])
def sendIntent():
    global mailReceiver
    global contentBody
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
    
    # ------------ Ask Wiki --------------
    if(intent_name == "ask_wiki"):
        # ask_wiki intent
        print('Ask Wiki invocation')
        # define returnValue
        returnValue = dispatchingQAModel(question)
    
    # ------------ Give Time --------------
    elif intent_name == "give_time":
        returnValue = f'It\'s {dispatchingTime()}'
        print(f'Output sent: {returnValue}')
    
    # ------------ Weather Service --------------
    elif intent_name == "inform_weather":
        entities = prediction.get('entities')
        city = ""
        for element in entities:
            city = element.get('value')
        print('The weather city found is:', city)
        if city == "" or city == None:
            returnValue = "I'm sorry, this city doesn't exist"
        else:
            returnValue = dispatchingWeather(city)
    
    # ------------ Add To-Do List --------------
    elif intent_name == "add_todo":
        entities = prediction.get('entities')
        for element in entities:
            todo_task = element.get('value')
            print(f'Possible entity: {todo_task}')
        print(f'Final entity chosen is: {todo_task}')
        dispatchingAddToDo(todo_task)
        returnValue = f'Task {todo_task} added to the list'
    
    # ------------ Ask To-Do List --------------
    elif intent_name == "ask_todo":
        returnValue = dispatchingAskToDo()
    
    # ------------ Complete To-Do List --------------
    elif intent_name == "complete_todo":
        entities = prediction.get('entities')
        if(not entities or entities == []):
            returnValue = "Sorry, I can't understand the task"
        else:
            for element in entities:
                todo_task = element.get('value')
                print(f'Possible entity: {todo_task}')
            print(f'Final entity chosen is: {todo_task}')
            returnValue = dispatchingCompleteToDo(todo_task)
   
    # ------------ Mood Unhappy --------------
    elif intent_name == "mood_unhappy":
        returnValue = f"So, let's me give you a joke; {dispatchingUnhappyJoke()}"
    
    # ------------ Mail Registration --------------
    elif intent_name == "mail_recipient":
        entities = prediction.get('entities')
        for element in entities:
            mail = element.get('value')
            print(f'Possible entity: {mail}')
        print(f'Final entity chosen is: {mail}')
        mailReceiver = mail
        returnValue = 'Ok, tell me the content of the mail. Say \'write\' and the content of the mail to send it correctly'
    
    # ------------ Mail Content Registration --------------
    elif intent_name == "mail_content":
        print('Enter in the mail content intent...')
        contentBody = question
        returnValue = dispatchingMail(mailReceiver, contentBody)
    
    elif intent_name == "bot_funcionalities":
        returnValue = "You can ask me the weather, time, todo list management, send a mail, greeting and search on Wikipedia"
    # ------------ Others Default Functions --------------
    else:
        # Other intent different from ask_wiki
        trigger_json = {
            "name": str(intent_name),
            "entities": {},
        }
        entities = prediction.get('entities')
        for element in entities:
            trigger_json.get('entities')[element.get(
                'entity')] = element.get('value')
        print('Trigger JSON to submit to the trigger_intent API:')
        print(trigger_json)
        url = 'http://localhost:5005/conversations/default/trigger_intent'
        jarvis_response = requests.post(
            url, json=trigger_json, headers=headers)
        jarvis_response = jarvis_response.json()
        print(jarvis_response)
        try:
            client_response = [jarvis_response.get('messages')[0].get('text')]
            print(f"Bot says: {client_response}")
            returnValue = client_response[0]
        except TypeError:
            returnValue = "I am sorry, I didn\'t understand"

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
    print('Current path', os.getcwd())
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


# Internal function

# Action to do for the wikipedia function


def dispatchingQAModel(text):
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
    except:
        return "I can't find an answer, I am sorry"

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
        text = f"The answer is " + str(value[1][1])
    return text

# utility for wikipedia function


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


# Time function
def dispatchingTime():
    return strftime("%H:%M")

# Weather function
def dispatchingWeather(city: str):
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        city + "&APPID=dbd3b02d8958d62185d02e944cd5f522"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    if(api_data['cod'] == '404'):
        return "I'm sorry, this city doesn't exist"
    else:
        temp_city = ((api_data['main']['temp'])-273.15)
        weather_desc = api_data['weather'][0]['description']
        return f"{'The weather in ' + city + ' is '+ weather_desc + ' and the temperature is '+ str(round(temp_city,1)) +'°'}"


# Ask To-Do function
def dispatchingAskToDo():
    composition = ""
    num_task = len(list(actions.find()))
    task = actions.find()
    print(f'Number of actual tasks:{num_task}')
    i = 0
    if(num_task == 0):
        return 'There are not task in the To-Do list, please add one saying \'add X to the list\''
    for x in task:
        i = i+1
        if(i == num_task):
            single_task = str(i) + ': ' + x['name'] + '.'
            composition = composition + single_task
        else:
            single_task = str(i) + ': ' + x['name'] + ', '
            composition = composition + single_task

    return f"{'TODO list is: ' + composition }"


def dispatchingAddToDo(todo_task):
    data = {'name': todo_task}
    print(f'Task to add: {todo_task}')
    if db.actions.count_documents(data):
        return f"I have already added this task to your list"
    else:
        actions.insert_one(data)
        return f"I added {todo_task} to your list"


def dispatchingCompleteToDo(task):
    # get the task from the latest message on the tracker

    # initiation of id and list element
    new_list = []
    id_list = []

    # initiation of the data json with the task name
    data = {'name': task}

    # query to find the task name in the list
    query = actions.find({'name': task})

    # return the elements from the query
    check = format(query.retrieved)
    print(f"Check elements retrieved from the query: {check}")

    if int(check) == 1:
        # if it is equal to 1 element
        query = actions.delete_one(data)
        return f"You have completed your task: {task}"
    else:
        # if there is 0 or more than 1 element in the list
        # combination between words of the task, splitting the words, defines the most confidence task and select it
        li = list(task.split(" "))
        for L in range(1, len(li)+1):
            for subset in itertools.combinations(li, L):
                cont = L
                string = ' { "$and" : [ { "name": { "$regex" : ".*' + subset[0] + '.*" } } ] }'
                for X in range(1, L):
                    string = string.replace(
                        '] }', ', { "name": { "$regex" : ".*' + subset[X] + '.*" } } ] }')

        data = json.loads(string)

        result = actions.find(data)
        for x in result:
            id = x['_id']
            id_list = []
            id_list.append(str(L))
            id_list.append(str(id))
            new_list.append(id_list)

        res = list(set(tuple(sorted(sub)) for sub in new_list))
        if len(res) != 0:
            max_value = max(res)
        else:
            max_value = 0

        for i in res:
            for j in res:
                if i[1] == j[1] and i[0] !=j[0] and i[0]<j[0]:
                    try:
                        res.remove(i)
                    except:
                        print('Resource removing failed')

        new_res = []
        for el in res:
            if int(el[0]) >= int(max_value[0]):
                new_res.append(el)

        if len(new_res) == 0:
            return f"I am sorry, no task found"
        elif len(new_res) == 1:
            query = actions.delete_one(data)
            return f"I have completed your task named {task}"
        else:
            similar_task = []
            for i in range(0, len(new_res)):
                temporal_task = ""
                for j in actions.find({"_id": ObjectId(new_res[i][1])}):
                    temporal_task = temporal_task + f"{ j['name'] }"
                print(f'Task {i} found is: {temporal_task}')
                similar_task.append(temporal_task)
            
            composition_str = ""
            if(len(similar_task) > 0):
                for i in range(0, len(similar_task)- 1):
                    if(i > 1):
                        composition_str += f', {similar_task[i]} '
                    else:
                        composition_str += f'{similar_task[i]}'
                composition_str += f' and {similar_task[i + 1]}'

            
            return f"I found {composition_str} in the list, which one do you want to complete?"

# Greeting function
def dispatchingUnhappyJoke():
    length = 101
    while length > 100: 
        # API of jokes from the link below
        joke_api_link = "https://jokes.guyliangilsing.me/retrieveJokes.php?type=dadjoke"
        joke_link = requests.get(joke_api_link) # request to the API
        joke = joke_link.json() # retrieve the json of response
        length=len(joke['joke']) # retrieve the length of the response
        print(f'Joke is {str(joke["joke"])}')
        # end of while
    return f"{str(joke['joke'])}" # returned message on the joke retrieved from the API


def dispatchingMail(mail, content):
    global mailReceiver
    global contentBody
    if mail == None:
        return f'I am sorry, I forgot the receiver mail, can you rewrite it?'
    if content == None:
        return f'I did not register the content of the mail, can you please say the content and start with \'write \' word?'
    replacement = ''
    content = content.split()
    content[0] = replacement
    content = ' '.join(content)
    content = f"Alysia Assistant is an automatic system, the email sent to the owner is:\n {content}"
    print(f'Email of receiver: {mail}')
    print(f'Content to send: {content}')
    
    # Data of the email
    sender = "alysia.mail.assistant@gmail.com"
    password = "blockchain"
    subject = "Alysia Mailing System: Virtual Assistant Message"

    msg = EmailMessage()
    msg.set_content(content)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = mail

    try:
        # Send the message via our own SMTP server.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("Mail has been sent!")
        mailReceiver = ""
        contentBody = ""
        return f'Email sent to {mail} correctly'
    except smtplib.SMTPAuthenticationError:
        print("Unable to sign in")
        mailReceiver = ""
        contentBody = ""
        return f'Unable to send an email to {mail}'   


app.run(host='0.0.0.0', port=4000)
