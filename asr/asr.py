import time
import nemo.collections.asr as nemo_asr
import os
import onnxruntime
import sys

# sys.path.append('/path/to/ffmpeg')


QUARTZNET_MODEL = "QuartzNet15x5Base-En"

class ASR:

    def __init__(self, name="QuartzNet15x5Base-En"):
        self.model_name = name
        self.model = None

    def getModelName(self):
        return self.model_name

    def setModelName(self, name):
        self.model_name = name


    def getModel(self):
        return self.model

    def setModel(self, model):
        self.model = model


    def downloadModel(self, name):
        self.model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name=name)


    def exportModel(self, filename):
        if self.model == None:
            self.downloadModel(self.getModelName())
        self.model.export(f"{filename}.onnx")

    def importModel(self, filename):
        onnxruntime.InferenceSession(f"{filename}.onnx")


if __name__ == "__main__":
    # first load is slow for the ASR encoding
    asr_model = ASR()
    asr_model.downloadModel(QUARTZNET_MODEL)
    # load the current audio file
    wave_file = ["../server/audio.wav"]
    text = asr_model.model.transcribe(paths2audio_files=wave_file)
    print("@") # tagging start
    print(text)
    print("@") # tagging end
    sys.stdout.flush()
