FROM alpine
FROM rasa/rasa:2.3.0


# sudo root
USER root 
RUN apt-get update
RUN apt-get install build-essential -y --fix-missing
RUN pip install --upgrade pip
RUN pip install sqlalchemy

CMD [ "run","actions","-p","5055" ]
