# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import json, requests, wikipedia, spacy, json, itertools, smtplib
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text
from pymongo import MongoClient
from bson.objectid import ObjectId     
from pymongo import MongoClient
from time import strftime
from search_wiki import get_info_phrase
from sqlalchemy import false
from nemo.collections.nlp.models import QAModel
from QAModel import _QAModel

# Download and load the pre-trained BERT-based model
# model = QAModel.from_pretrained("qa_squadv1.1_bertbase")

model = _QAModel().getModel()

# Global variables for entities
global email
global mailBody
global city
global task
email = "" # send email 
mailBody = "" # mail content 
city = "" # city of weather
task = "" # task for the To-Do list

# MongoDB setup for actions elements
client = MongoClient("mongodb+srv://Jarvis:JarvisNLP@cluster0.zbc0n.mongodb.net/todo_db?retryWrites=true&w=majority")    
db = client['todo_db'] # name of the database
actions= db['actions'] # name of collection
        

# ActionShowTime defines the action to show the time
class ActionShowTime(Action):

    def name(self) -> Text:
        return "action_give_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("----------  Weather Action --------------")
        time = strftime("%H:%M")
        print(f'ActionShowTime invoked, the current time is {time}')
        dispatcher.utter_message(text=f"{'It is '+ time }")
        print('------------------------------------------')
        return [] # Actions run didn't return anything


# ActionShowWeather defines the action of the weather API
class ActionShowWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher,tracker,domain):
        print("----------  Weather Action --------------")
         
        entities = tracker.latest_message['entities']
        for e in entities:
            city=e['value']
              
        print(city)
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=dbd3b02d8958d62185d02e944cd5f522"
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
        
        if(api_data['cod']=='404'):
            dispatcher.utter_message(text=f"I'm sorry, this city doesn't exist")
        else:
            temp_city = ((api_data['main']['temp'])-273.15)
            weather_desc = api_data['weather'][0]['description']
            print(tracker.slots['city'])
            dispatcher.utter_message(text=f"{'The weather in ' + city + ' is '+ weather_desc + ' and the temperature is '+ str(round(temp_city,1)) +'°'}")
        print('------------------------------------------')
        return []
        

# Actions to confirm the adding of the element in the To-Do list
class ActionConfirmAdd(Action):

    def name(self) -> Text:
        return "action_confirm_add"

    def run(self, dispatcher, tracker, domain):
        print("----------  Confirm To-Do List Message --------------")
        entities = tracker.latest_message['entities'] 
        print(f'Last entity:  {entities}')
        print(f'Type of entities: {type(entities)}')
        task = entities[0]['value']
        print(f'Task detected is {task}')
        dispatcher.utter_message(text=f"{'Do you want to add ' + task + ' to your list'}")
        print('-----------------------------------------------------')


# Actions to add the To-Do after the ActionConfirmaAdd invocation
class ActionAddTodo(Action):

    def name(self) -> Text:
        return "action_add_todo"

    def run(self, dispatcher, tracker, domain):
        print('--------- Adding Element in the To-Do List -------------')
        data = {'name' : task}
        print(f'Task to add: {task}')
        if db.actions.count_documents(data):
            dispatcher.utter_message(text=f"{'I have already added this task to your list'}")
            print('Element already exists')
        else:
            actions.insert_one(data)
            dispatcher.utter_message(text=f"{'I added ' + task + ' to your list'}")
            print('Added element in the To-Do list')
        print('-----------------------------------------------------')


                
# Actions to complete the task in the To-Do list
class ActionCompleteTodo(Action):

    def name(self) -> Text:
        return "action_complete_todo"

    def run(self, dispatcher,tracker,domain):
        print('--------- Complete Element in the To-Do List -------------')
         
        # get the task from the latest message on the tracker
        entities = tracker.latest_message['entities']
        task= entities[0]['value']

        # initiation of id and list element
        new_list=[]
        id_list=[]
        
        # initiation of the data json with the task name
        data = {'name' : task}

        # query to find the task name in the list
        query = actions.find({ 'name': task })

        # return the elements from the query 
        check = format(query.retrieved)
        print(f"Check elements retrieved from the query: {check}")
        
        if int(check) == 1:  
            # if it is equal to 1 element
            query = actions.delete_one(data)
            dispatcher.utter_message(text=f"{'You have completed your task: ' + task }")
            print(f'Complete the task: {task}')
        else:
            # if there is 0 or more than 1 element in the list

            # combination between words of the task, splitting the words, defines the most confidence task and select it
            li = list(task.split(" "))
            for L in range(1, len(li)+1):
                for subset in itertools.combinations(li, L):
                    cont = L
                    string = ' { "$and" : [ { "name": { "$regex" : ".*'+ subset[0] +'.*" } } ] }'
                    for X in range(1, L):
                        string = string.replace('] }',', { "name": { "$regex" : ".*'+ subset[X] +'.*" } } ] }')

            data = json.loads(string) #

            result= actions.find( data )
            for x in result:
                id=x['_id']
                id_list=[]
                
                id_list.append(str(L))
                id_list.append(str(id))
                new_list.append(id_list)

            res = list(set(tuple(sorted(sub)) for sub in new_list))
            if len(res) != 0:
                max_value = max(res)
            else: max_value=0

            for i in res:
                for j in res:
                    if i[1]==j[1] and i[0]!=j[0] and i[0]<j[0]:
                        try:
                            res.remove(i)
                        except:
                            pass
            
            new_res=[]
            for el in res:
                if int(el[0]) >= int(max_value[0]): 
                    new_res.append(el)
            
            if len(new_res)==0:
                dispatcher.utter_message(text=f"{'I am sorry, no task found :( ' }")
            elif len(new_res)==1:
                query = actions.delete_one(data)
                dispatcher.utter_message(text=f"{'I have completed your task: ' + task }")
            else: 
                mess=""
                for i in range(0,len(new_res)):
                    for j in actions.find({"_id": ObjectId(new_res[i][1])}):
                        mess = mess + j['name'] + '\n'
                mess= '\n' + mess
                dispatcher.utter_message(text=f"{'I found these tasks: ' + mess }")
            print('-----------------------------------------------------')




# Action to ask To-Do list 
class ActionAskTodo(Action):

    def name(self) -> Text:
        return "action_ask_todo"

    def run(self, dispatcher,tracker,domain):
        print('---------- Ask To-Do List -------------')
        
        # redefine the list from previous call
        list = ""
        
        # counter tasks
        num_task = actions.find().count()

        # list of tasks
        task = actions.find()

        # index
        i = 0
        for x in task:
            i = i+1
            if(i==num_task):
                single_task =  str(i) + ': ' + x['name'] + '.'
                list = list + single_task
            else: 
                single_task =  str(i) + ': ' + x['name'] + ', '
                list = list + single_task
                
        dispatcher.utter_message(text=f"{'TODO list is: ' + list }")
        print('--------------------------------------')


# Action to register mail of the sender
class ActionRegisterMail(Action):
    
    def name(self) -> Text:
        return "register_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('------------- Register Mail of Sender  ---------------')
        entities = tracker.latest_message['entities']
        for e in entities:
            if e['entity']=='senderemail':
                email = e['value']
        print('------------------------------------------------------')
        return []


# Action to register the content of the mail
class ActionRegisterMailBody(Action):
    
    def name(self) -> Text:
        return "mail_content_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('---------- Register Content of Mail -----------------')
        entities = tracker.latest_message['entities']
        print(email)
        for e in entities:
            if e['entity']=='containermail':
                mailBody = e['value']
        print('-----------------------------------------------------')
        return []


# Action to send the email to the sender with the content of mail
# email : sender mail
# mailBody: content of the email
class ActionSendingMail(Action):
    
    def name(self) -> Text:
        return "mail_response"

    def run(self, dispatcher,tracker,domain):
        print('------------- Sending Mail ----------------')
        # elements about the mail of the bot
        sender = "jarvisunibo@gmail.com"
        receiver = email
        password = "JarvisNlp!"
        subject = "Jarvis mailing"
        body = mailBody
        
        # Header of the mail
        message = f"""From: Jarvis Unibo
        To: {receiver}
        Subject: {subject}\n
        {body}
        """
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        # Sending email
        print('Sending email...')
        try:
            server.login(sender,password)
            server.sendmail(sender, receiver, message)
            print("Mail has been sent!")
            print(body)
            dispatcher.utter_message(text=f"Mail has been sent to " + receiver)
        except smtplib.SMTPAuthenticationError:
            print("Unable to sign in")
            dispatcher.utter_message(text=f"I'm sorry i think there's a problem")
        print('------------------------------------------')
        return []


# Action to send a joke when you are unhappy, sad, bad or negative adjectives. Check nlu.yaml for more info about the action invocation
class ActionUnhappyResponse(Action):
    
    def name(self) -> Text:
        return "unhappy_response"

    def run(self, dispatcher,tracker,domain):
        print('------------- Sending Joke ---------------------')
        length=101
        while length > 100:
            # API of jokes from the link below
            joke_api_link = "https://jokes.guyliangilsing.me/retrieveJokes.php?type=dadjoke"
            joke_link = requests.get(joke_api_link) # request to the API
            joke = joke_link.json() # retrieve the json of response
            length=len(joke['joke']) # retrieve the length of the response
            print(f'Joke is {str(joke["joke"])}')
            # end of while
        dispatcher.utter_message(text = f"" + str(joke['joke'])) # utter_message on the joke retrieved from the API
        print('-------------------------------------------------')
        return []


# Action for the Wikipedia management
class ActionWikiAsk(Action):
    
    def name(self) -> Text:
        return "wiki_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('----------------------------- Wikipedia Action Invocation -----------------------------------')
        print("Wikipedia tracket for the latest message:", tracker.latest_message.get('text'))
        text = tracker.latest_message.get('text')
        sentence = text.replace('search', '')
        
        print("My sentence is:", sentence)
        nlp = spacy.load('en_core_web_sm')        
        try:                       
            doc = nlp(sentence)
            print("Part-of-Speech extrapolation")
            oblique_phrase = get_info_phrase(doc)   
            print("Result: " + str(oblique_phrase))
            print("Keys words: ", oblique_phrase)
            print(wikipedia.search(oblique_phrase))
            result = wikipedia.summary(oblique_phrase , auto_suggest=False)
        except wikipedia.exceptions.PageError:  
            # Page Error on Wikipedia scraping
            new_search=wikipedia.search(oblique_phrase)[0]
            result= wikipedia.summary(new_search)  
        except wikipedia.DisambiguationError as e:
            # Page Semantic Error on the Disambiguation
            result= wikipedia.summary(e.options[0])
            dispatcher.utter_message(text=f""+str(result))   
       
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
        output = model.inference('bert_input.json')
        for value in output[0].items():
            dispatcher.utter_message(text=f"The answer is: "+ str(value[1][1])) 
        print('-------------------------------------------------------------------------------------------')
        return []
