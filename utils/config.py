import os
import time

def environment(activate = 'venv/bin/activate'):
    print(f'Environment setting on {activate}')
    os.system(f'source {activate}')


def download():
    # install dependencies
    print('Installing dependencies...')
    print(f'Execution time: {time.time()}')

    os.system('pip install wget')
    os.system('apt-get install sox libsndfile1 ffmpeg')
    os.system('pip install unidecode')
    os.system('pip install matplotlib>=3.3.2')

    # install NeMo framework
    BRANCH = 'main'
    # BRANCH = 'stable'
    os.system(f'python -m pip install git+https://github.com/NVIDIA/NeMo.git@${BRANCH}#egg=nemo_toolkit[all]')

    # Grab of the configuration for the ASR model
    os.system('mkdir configs')
    os.system(f'wget -P configs/ https://raw.githubusercontent.com/NVIDIA/NeMo/${BRANCH}/examples/asr/conf/config.yaml')
    print(f'Execution time: {time.time()}')
    print(f'End configurations on dependencies')

environment('venv/bin/activate')
print('Environment is ready... OK')