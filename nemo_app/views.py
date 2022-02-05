from django.http import JsonResponse
from django.shortcuts import render
from asr.main import ASR
from tts.main import TTS
from nlp.QAModel import _QAModel
import json
from django.views.decorators.csrf import csrf_exempt
import os
import numpy as np

# Create your views here.

ASR_MODEL = "QuartzNet15x5Base-En"
asr_model = ASR()
asr_model.downloadModel()
qa_model = _QAModel()
tts_model = TTS()
tts_model.downloadSpectogramGenerator()
tts_model.downloadVocoder()  



@csrf_exempt
def asr_transcribe(request):
    print(f'Filepath is: {os.getcwd()}')
    print(f'Audio file to transcribe: ./server/audio.wav')
    _transcript = asr_model.model.transcribe(paths2audio_files=['./server/audio.wav'], logprobs=True)[0]
    probs = asr_model.softmax(_transcript)
    _text = asr_model.beam.forward(log_probs = np.expand_dims(probs, axis=0), log_probs_length=None)
    if _text[0][0][1] != None:
        data = {'text' : _text[0][0][1]}
    else:
        data = {'text' : _transcript}
    print(f"Prediction text: {data}")
    return JsonResponse(data) 

@csrf_exempt
def tts_translate(request):
    jsonData = json.loads(request.body.decode("utf-8"))
    audio = tts_model.textToSpeech(jsonData["text"], "speech")
    data = {'audio_file' : audio}
    os.system(f"play {audio}")
    return JsonResponse(data)