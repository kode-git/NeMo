import time
import nemo.collections.asr as nemo_asr
import os
import pickle
import onnxruntime


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
    asr_model = ASR()
    asr_model.downloadModel(QUARTZNET_MODEL)
    filename = sys.argv[1]
    print(filename)
    sys.stdout.flush()



    # asr_model.importModel("quartzNet_model")

