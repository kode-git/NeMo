from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
import requests
from requests import status_codes

# main invoke
def index(request):
    return render(request, 'index.html', {'name': 'Jarvis'})


# sending Message
@csrf_exempt
def sendMessage(request):
    question = request.POST.__getitem__('text')
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
    return JsonResponse(client_response, safe=False)


    