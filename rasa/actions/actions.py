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
              
 
        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=dbd3b02d8958d62185d02e944cd5f522"
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
        
        if(api_data== '{"cod":"404","message":"city not found"}'):
            return [SlotSet("city", 'NONE')]
        else:
            temp_city = ((api_data['main']['temp'])-273.15)
            weather_desc = api_data['weather'][0]['description']
            print(tracker.slots['city'])
            dispatcher.utter_message(text=f"{'The weather in ' + city + ' is '+ weather_desc + ' and the temperature is '+ str(round(temp_city,1)) +'°'}")
        
        return []


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
