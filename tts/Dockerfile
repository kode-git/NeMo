FROM ubuntu
FROM python:3.8
WORKDIR /usr/app
COPY tts.py /usr/app
RUN apt-get update && apt-get install -y libsndfile1 ffmpeg sox
RUN pip install Cython
RUN pip install nemo_toolkit[tts]
RUN pip install soundfile   
CMD ["python","tts.py"]
