from msilib.schema import Error
from  nemo_collections.nlp.models import QAModel
import json
QA_MODEL = "qa_squadv1.1_bertbase"

class QAModel:

    def __init__(self, name=QA_MODEL):
        self.model_name = name
        self.model = QAModel.from_pretrained(QA_MODEL)
    
    def getModelName(self):
        return self.model_name
    
    def setModelName(self, model_name):
        self.model_name = model_name
    
    def getModel(self):
        return self.model
    
    def setModel(self, model):
        self.model = model
    
    def downloadQAModel(self, name_model):
        try:
            self.model = QAModel.from_pretrained(name_model)
        except Error:
            # do nothing
            print('Model not found')

    