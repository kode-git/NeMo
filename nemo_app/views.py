from django.shortcuts import render
from asr.main import ASR
from tts.main import TTS
# Create your views here.

ASR_MODEL = "QuartzNet15x5Base-En"

asr_model = ASR()
asr_model.downloadModel()


def asr_transcribe():
    pass


def tts_translate():
    pass