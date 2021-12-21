# rasa working only on python 3.7 or 3.8
FROM python:3.8-slim-bullseye

# defines the venv directory 
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# setup of the PATH global variable
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# import official rasa container
FROM rasa/rasa

# setting working directory on the subfolder of the current environment
WORKDIR /opt/app/rasa

# expose on 5005 with 4000 for express.js
EXPOSE 5005

# defines WORK_DIR global variable
RUN export WORK_DIR=/opt/app/rasa

# copy content
COPY data $WORK_DIR  
COPY actions/ $WORK_DIR
COPY .rasa $WORKDIR
COPY models/ $WORK_DIR
COPY tests $WORK_DIR
COPY config.yml $WORK_DIR
COPY credentials.yml $WORK_DIR
COPY domain.yml $WORK_DIR
COPY endpoints.yml $WORK_DIR

CMD [ "rasa", "--enable-api"]
