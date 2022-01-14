FROM rasa/rasa:2.3.0-full
CMD [ "test","nlu","--nlu","data/nlu.yml","--config","config_1.yml","config_2.yml" ]


