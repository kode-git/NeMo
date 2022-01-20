from django.http import JsonResponse
from django.shortcuts import render
from asr.main import ASR
from tts.main import TTS
from nemo import asr as nemo_asr
import json
from django.views.decorators.csrf import csrf_exempt
import gzip
import os, shutil, wget

# Create your views here.

ASR_MODEL = "QuartzNet15x5Base-En"

asr_model = ASR()
asr_model.downloadModel()
tts_model = TTS()
tts_model.downloadSpectogramGenerator()
tts_model.downloadVocoder()  

# Import LM 


@csrf_exempt
def asr_transcribe(request):
    print(f'Filepath is: {os.getcwd()}')
    print(f'Audio file to transcribe: ./server/audio.wav')
    _text = asr_model.model.transcribe(paths2audio_files=['./server/audio.wav'])
    data = {'text' : _text}
    print(f"Prediction text: {data}")
    return JsonResponse(data) 

@csrf_exempt
def tts_translate(request):
    jsonData = json.loads(request.body.decode("utf-8"))
    audio = tts_model.textToSpeech(jsonData["text"], "speech")
    data = {'audio_file' : audio}
    os.system(f"play {audio}")
    return JsonResponse(data)