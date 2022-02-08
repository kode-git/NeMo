FROM rasa/rasa:2.3.0
# sudo root
USER root 
RUN pip install wikipedia
RUN pip install spacy
RUN pip install sqlalchemy
RUN python -m spacy download en_core_web_sm
CMD [ "run","actions","-p","5055" ]
