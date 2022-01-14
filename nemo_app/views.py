from django.shortcuts import render
from asr.main import ASR
from tts.main import TTS
import json
# Create your views here.

ASR_MODEL = "QuartzNet15x5Base-En"

asr_model = ASR()
asr_model.downloadModel()
tts_model = TTS()
tts_model.downloadSpectogramGenerator()
tts_model.downloadVocoder()

def asr_transcribe(request):
    jsonData = json.loads(request.body.decode("utf-8"))
    text = asr_model.model.trascribe(jsonData.audioPath)
    return text    


def tts_translate(request):
    jsonData = json.loads(request.body.decode("utf-8"))
    audio = tts_model.textToSpeech(jsonData.text)
    return audio