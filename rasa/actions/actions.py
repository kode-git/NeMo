# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import datetime as dt
from typing import Any, Text, Dict, List
import json
import requests 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import rasa_sdk.events
import smtplib
import os
from typing import Text
from pymongo import MongoClient
import re
import pprint
from bson.objectid import ObjectId     
from collections import OrderedDict
import json
import itertools
from pymongo import MongoClient

email=""
mail=""
city=""

                
client = MongoClient("mongodb+srv://Jarvis:JarvisNLP@cluster0.zbc0n.mongodb.net/todo_db?retryWrites=true&w=majority")    
db= client['todo_db']
actions= db['actions']
        

#

class ActionShowTime(Action):

    def name(self) -> Text:
        return "weather_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("FROM WEATHER_FORM")
        entities = tracker.latest_message['entities']
        for e in entities:
            if e['entity']=='cityname':
                loc = e['value']
                print(e['value'])
        location = loc
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&APPID=dbd3b02d8958d62185d02e944cd5f522"
        
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
        
        temp_city = ((api_data['main']['temp'])-273.15)
        weather_desc = api_data['weather'][0]['description']
      
        dispatcher.utter_message(text=f"{'The weather in ' + city + ' is '+ weather_desc + ' and the temperature is '+ str(round(temp_city,1)) +'°'}")
        
        return []


class ActionShowWheater(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_WEATHER" )
         
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
        
        return []
task=""

class ActionConfirmAdd(Action):

    def name(self) -> Text:
        return "action_confirm_add"

    def run(self, dispatcher,tracker,domain):
        print("FROM action_confirm_add" )
        global task
        entities = tracker.latest_message['entities']
        for e in entities:
            task=e['value']
        
        dispatcher.utter_message(text=f"{'Do you want to add ' + task + ' to your list'}")



class ActionAddTodo(Action):

    def name(self) -> Text:
        return "action_add_todo"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_ADD_TODO" )
        global task 
        data = {'name' : task}

        if db.actions.count_documents(data):
            dispatcher.utter_message(text=f"{'I have already added this task to your list'}")
        else:
            actions.insert_one(data)
            dispatcher.utter_message(text=f"{'I added ' + task + ' to your list'}")


                







class ActionCompleteTodo(Action):

    def name(self) -> Text:
        return "action_complete_todo"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_COMPLETE_TODO" )
         
        entities = tracker.latest_message['entities']
        for e in entities:
            task=e['value']

        new_list=[]
        id_list=[]
        
        data = {'name' : task}
        query = actions.find({ 'name': task })
        for i in query:
            print(i)
        check = format(query.retrieved)
        print(check)
        if int(check) == 1:  
            query = actions.delete_one(data)
            dispatcher.utter_message(text=f"{'You have completed your task: ' + task }")
        else:
            li = list(task.split(" "))
            for L in range(1, len(li)+1):
                for subset in itertools.combinations(li, L):
                    cont = L
                    string = ' { "$and" : [ { "name": { "$regex" : ".*'+ subset[0] +'.*" } } ] }'
                    for X in range(1, L):
                        string = string.replace('] }',', { "name": { "$regex" : ".*'+ subset[X] +'.*" } } ] }')

            data = json.loads(string)

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
                dispatcher.utter_message(text=f"{'I found those task: ' + mess }")






class ActionAskTodo(Action):

    def name(self) -> Text:
        return "action_ask_todo"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_ASK_TODO" )
         
        list=""
        
        num_task = actions.find().count()
        task = actions.find()

        i=0
        for x in task:
            i=i+1
            

            if(i==num_task):
                single_task =  str(i) + ': ' + x['name'] + '.'
                list = list + single_task
            else: 
                single_task =  str(i) + ': ' + x['name'] + ', '
                list = list + single_task
                
        
        dispatcher.utter_message(text=f"{'TODO list is: ' + list }")


class ActionSendMail(Action):
    
    def name(self) -> Text:
        return "register_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global email
        entities = tracker.latest_message['entities']
        for e in entities:
            if e['entity']=='senderemail':
                email = e['value']

        return []


class ActionSendMail(Action):
    
    def name(self) -> Text:
        return "mail_content_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global mail
        entities = tracker.latest_message['entities']
        print(email)
        for e in entities:
            if e['entity']=='containermail':
                mail = e['value']

        return []

class ActionSendingMail(Action):
    
    def name(self) -> Text:
        return "mail_response"

    def run(self, dispatcher,tracker,domain):
        global mail
        global email
            
        sender = "jarvisunibo@gmail.com"
        receiver = email
        password = "JarvisNlp!"
        subject = "Jarvis mailing"
        body = mail
        
        # header
        message = f"""From: Jarvis Unibo
        To: {receiver}
        Subject: {subject}\n
        {body}
        """

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(sender,password)
            server.sendmail(sender, receiver, message)
            print("Mail has been sent!")
            print(body)
            dispatcher.utter_message(text=f"Mail has been sent to " + receiver)
        except smtplib.SMTPAuthenticationError:
            print("Unable to sign in")
            dispatcher.utter_message(text=f"I'm sorry i think there's a problem")
            
                
        return []

