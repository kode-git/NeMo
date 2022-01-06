FROM ubuntu
FROM python:3.8
RUN apt-get update && apt-get install -y libsndfile1 ffmpeg sox
RUN pip install Cython
RUN pip install nemo_toolkit[tts]
RUN pip install nemo_toolkit[asr]
RUN pip install django
RUN pip install django-debug-toolbar
RUN pip install requests
RUN pip install soundfile   
RUN pip install onnxruntime
CMD ["bash"]
