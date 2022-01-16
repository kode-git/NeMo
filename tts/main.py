import soundfile as sf
from nemo.collections.tts.models.base import SpectrogramGenerator, Vocoder
import os

_specGenerator = "tts_en_fastpitch"
_vocoderName = "tts_hifigan"

class TTS:

    def __init__(self, vocoderName=_vocoderName, spectGenName=_specGenerator):
        self.vocoder = None
        self.spectogramGenerator = None
        self.vocoderName = vocoderName
        self.spectGenName = spectGenName
    
    def getVocoder(self):
        return self.vocoder
    
    def getSpectogramGenerator(self):
        return self.spectogramGenerator

    def getVocoderName(self):
        return self.vocoderName

    def getSpectGenName(self):
        return self.spectGenName
    
    def setVocoder(self, vocoder):
        self.vocoder = vocoder

    def setSpectogramGenerator(self, spectrogramGenerator):
        self.spectogramGenerator = spectrogramGenerator
    
    def setVocoderName(self, name):
        self.vocoderName = name

    def setSpectGenName(self, name):
        self.spectGenName = name

    def downloadVocoder(self):
        self.vocoder = Vocoder.from_pretrained(model_name=self.vocoderName)

    def downloadSpectogramGenerator(self):
        self.spectogramGenerator = SpectrogramGenerator.from_pretrained(model_name=self.spectGenName)

    def exportVocoder(self, filename):
        if self.vocoder == None:
            if self.vocoderName == None:
                raise KeyError('You need to set the vocoder name before export')
            self.downloadVocoder()
        self.vocoder.export(f"{filename}.onnx")


    def exportSpectogramGenerator(self, filename):
        if self.spectogramGenerator == None:
            if self.spectGenName == None:
                raise KeyError('You need to set the spectGenName before export')
            self.downloadSpectogramGenerator()
        self.spectogramGenerator.export(f"{filename}.onnx")


    def textToSpeech(self, text : str, filename):
        if self.vocoder == None or self.spectogramGenerator == None:
            raise Exception('Vocoder or Spectogram Generator are None. Please, setup them before invoke he textToSpeech method!')
        parsed = self.spectogramGenerator.parse(text)
        spectogram = self.spectogramGenerator.generate_spectrogram(tokens=parsed)
        audio = self.vocoder.convert_spectrogram_to_audio(spec=spectogram)
        sf.write(f"{filename}.wav", audio.to('cpu').detach().numpy()[0], 22050)
        return f"{filename}.wav"



if __name__ == "__main__":
    tts = TTS()
    tts.downloadSpectogramGenerator()
    tts.downloadVocoder()
    tts.textToSpeech('The weather in Bologna is 39 celsius, sir', "audio")
    audio = tts.textToSpeech('Hello World', "audio")
    os.system(f"play {audio}")
    