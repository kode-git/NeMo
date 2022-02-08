FROM alpine
FROM rasa/rasa:2.3.0


# sudo root
USER root 
RUN apt-get update
RUN apt-get install build-essential -y --fix-missing
RUN pip install --upgrade pip
RUN pip install wikipedia
RUN pip install spacy
RUN pip install sqlalchemy
RUN pip install nemo_toolkit[nlp] --no-cache
RUN python -m spacy download en_core_web_sm

CMD [ "run","actions","-p","5055" ]
