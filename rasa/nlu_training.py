from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelCongif
from rasa_nlu.model import Trainer
from rasa_nlu import config

training_data=load_data("data/nlu_data.json")

trainer= Trainer(config.load("nlu_config.yml"))

interpreter= trainer.train(training_data)

model_directory=trainer.persist("models/nlu", fixed_mode_name="current")