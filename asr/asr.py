import time
import nemo.collections.asr as nemo_asr
import os


def dependencies_asr():
    # install dependencies

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


def import_asr_locally():
    quartzNet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")
    quartzNet.save_to('quartzNet_checkpoint.nemo')


def load_checkpoint():
    quartzNet = nemo_asr.models.EncDecCTCModel.restore_from(restore_path='quartzNet_checkpoint.nemo')
    print(f'{quartzNet.summarize()}')


if __name__ == '__main__':
    print(f'Execution time: {time.time()}')
    dependencies_asr()
    decision = input('Do you want to import asr model locally? Y for yes | other keys for no\n')
    if decision == 'Y' or decision == 'y':
        import_asr_locally()

    decision = input('Do you want to restore model? Y for yes | other keys for no\n')
    if decision == 'Y' or decision == 'y':
        load_checkpoint()

    print(f'Process finished at: {time.time()}')
