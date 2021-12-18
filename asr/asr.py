import time
import nemo.collections.asr as nemo_asr
import os


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
