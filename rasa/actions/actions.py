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
from pymongo import MongoClient

email=""
mail=""
city=""

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
        temp_city = ((api_data['main']['temp'])-273.15)
        weather_desc = api_data['weather'][0]['description']
        print(tracker.slots['city'])
        dispatcher.utter_message(text=f"{'The weataomher in ' + city + ' is '+ weather_desc + ' and the temperature is '+ str(round(temp_city,1)) +'°'}")
    
        client = MongoClient('localhost:27017')
        mydb= client['prova']
        mycol= mydb['characters']
        print(mycol)

        data={'name':'oca toro'}
        mycol.insert_one(data)

        print(client.list_database_names())

        print(mydb.list_collection_names())

        for x in mycol.find({"name":"pino peppe"}) :
            print(x) 

        mycol.delete_one({"name":"pino peppe"})

        return []


class ActionAddTodo(Action):

    def name(self) -> Text:
        return "action_add_todo"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_ADD_TODO" )
         
        entities = tracker.latest_message['entities']
        for e in entities:
            task=e['value']
        print(task)
        dispatcher.utter_message(text=f"{'I added ' + task + ' to your list'}")
                
        client = MongoClient('localhost:27017')
        mydb= client['prova']
        mycol= mydb['characters']
        print(mycol)

        data={'name':task}
        mycol.insert_one(data)




class ActionCompleteTodo(Action):

    def name(self) -> Text:
        return "action_complete_todo"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_COMPLETE_TODO" )
         
        entities = tracker.latest_message['entities']
        for e in entities:
            task=e['value']
        print(task)
        dispatcher.utter_message(text=f"{'You have completed your task: ' + task }")
                
        client = MongoClient('localhost:27017')
        mydb= client['prova']
        mycol= mydb['characters']
        print(mycol)

        data={'name':task}
        mycol.delete_one(data)





class ActionAskTodo(Action):

    def name(self) -> Text:
        return "action_ask_todo"

    def run(self, dispatcher,tracker,domain):
        print("FROM ACTION_ASK_TODO" )
         
        list=""
        client = MongoClient('localhost:27017')
        mydb= client['prova']
        mycol= mydb['characters']
        
        num_task = mycol.find().count()
        task = mycol.find()

        i=0
        for x in task:
            i=i+1
            
            single_task = '\nNumber ' + str(i) + ': ' + x['name'] + '.'
            list = list + single_task
        
        dispatcher.utter_message(text=f"{'You have ' + str(num_task) + ' in your TODO list: ' + list }")
        
                



class ActionSendMail(Action):
    
    def name(self) -> Text:
        return "register_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        for e in entities:
            if e['entity']=='senderemail':
                email = e['value']

        dispatcher.utter_message(text=f"{email}")

        return []


class ActionSendMail(Action):
    
    def name(self) -> Text:
        return "mail_content_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        for e in entities:
            if e['entity']=='containermail':
                mail = e['value']

        dispatcher.utter_message(text=f"{mail}")

        return []


class ActionSendingMail(Action):
    
    def name(self) -> Text:
        return "utter_mail_confirmed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('WEEE')
        sender_email='weriti2829@zoeyy.com'
        rec_email=email
        message=mail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email,'1234')
        server.sendmail(sender_email,rec_email,message)
        print("MAIL HAS BEEN SENT")
        
        dispatcher.utter_message(text=f"{mail}")
        return []
