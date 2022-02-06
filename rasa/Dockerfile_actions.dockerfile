FROM rasa/rasa:2.3.0
# sudo root
USER root 
RUN pip install wikipedia
RUN pip install spacy
RUN pip install sqlalchemy
CMD [ "run","actions","-p","5055" ]
