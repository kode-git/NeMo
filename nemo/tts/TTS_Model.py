import soundfile as sf
from nemo.collections.tts.models.base import SpectrogramGenerator, Vocoder
import os

_specGenerator = "tts_en_fastpitch"
_vocoderName = "tts_waveglow_88m"

class TTS_Model:

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
        print('Invocation of textToSpeech in TTS module')
        if self.vocoder == None or self.spectogramGenerator == None:
            raise Exception('Vocoder or Spectogram Generator are None. Please, setup them before invoke he textToSpeech method!')
        # clear the filename
        parsed = self.spectogramGenerator.parse(text)
        print('Parsed text is: ', parsed)
        print('Generate spectogram...')
        spectogram = self.spectogramGenerator.generate_spectrogram(tokens=parsed)
        print('Convert spectogram to audio...')
        audio = self.vocoder.convert_spectrogram_to_audio(spec=spectogram)
        print('Tensor Audio: ', audio)
        print('Writing file in: ', filename)
        sf.write(filename, audio.to('cpu').detach().numpy()[0], 22050)
        print('Return filename: ', filename)
        return filename



if __name__ == "__main__":
    tts = TTS_Model()
    tts.downloadSpectogramGenerator()
    tts.downloadVocoder()
    audio = tts.textToSpeech('The weather in Bologna is 39 celsius, sir')
    os.system(f"play {audio}")
    