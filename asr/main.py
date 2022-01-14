import nemo.collections.asr as nemo_asr
import sys


ASR_MODEL = "QuartzNet15x5Base-En"

class ASR:

    def __init__(self, name=ASR_MODEL):
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


    def downloadModel(self, name=ASR_MODEL):
        self.model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name=name)


    def exportModel(self, filename):
        if self.model == None:
            self.downloadModel(self.getModelName())
        self.model.save_to(f"./{filename}.onnx")

    def importModel(self, filename):
        return self.model.restore_from(f"./{filename}.onnx")


if __name__ == "__main__":
    # first load is slow for the ASR encoding
    asr_model = ASR()
    asr_model.downloadModel()
    # load the current audio file
    wave_file = ["../server/audio.wav"]
    text = asr_model.model.transcribe(paths2audio_files=wave_file)
    print("@") # tagging start
    print(text)
    print("@") # tagging end
    sys.stdout.flush()
