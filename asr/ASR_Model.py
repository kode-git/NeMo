import nemo.collections.asr as nemo_asr
import gzip
import os, shutil, wget
import numpy as np

ASR_MODEL = "QuartzNet15x5Base-En"



class ASR_Model:

    def __init__(self, name=ASR_MODEL):
        self.model_name = name
        self.model = None
        self.downloadModel(name)
        self.beam = self.setBeam()

    def getModelName(self):
        return self.model_name

    def setModelName(self, name):
        self.model_name = name


    def getModel(self):
        return self.model

    def setModel(self, model):
        self.model = model


    def downloadModel(self, name=ASR_MODEL):
        self.model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name=name)


    def exportModel(self, filename):
        if self.model == None:
            self.downloadModel(self.getModelName())
        self.model.save_to(f"./{filename}.onnx")

    def importModel(self, filename):
        return self.model.restore_from(f"./{filename}.onnx")
    
    def softmax(self, logits):
        e = np.exp(logits - np.max(logits))
        return e / e.sum(axis=-1).reshape([logits.shape[0], 1])

    def setBeam(self):
        lm_gzip_path = '3-gram.pruned.1e-7.arpa.gz'
        if not os.path.exists(lm_gzip_path):
            print('Downloading pruned 3-gram model.')
            lm_url = 'http://www.openslr.org/resources/11/3-gram.pruned.1e-7.arpa.gz'
            lm_gzip_path = wget.download(lm_url)
            print('Downloaded the 3-gram language model.')
        else:
            print('Pruned .arpa.gz already exists.')

        uppercase_lm_path = '3-gram.pruned.1e-7.arpa'
        if not os.path.exists(uppercase_lm_path):
            with gzip.open(lm_gzip_path, 'rb') as f_zipped:
                with open(uppercase_lm_path, 'wb') as f_unzipped:
                    shutil.copyfileobj(f_zipped, f_unzipped)
            print('Unzipped the 3-gram language model.')
        else:
            print('Unzipped .arpa already exists.')

        lm_path = 'lowercase_3-gram.pruned.1e-7.arpa'
        if not os.path.exists(lm_path):
            with open(uppercase_lm_path, 'r') as f_upper:
                with open(lm_path, 'w') as f_lower:
                    for line in f_upper:
                        f_lower.write(line.lower())
        print('Converted language model file to lowercase.')
        return nemo_asr.modules.BeamSearchDecoderWithLM(
            vocab=list(self.model.decoder.vocabulary),
            beam_width=16,
            alpha=2, beta=1.5,
            lm_path=lm_path,
            num_cpus=max(os.cpu_count(), 1),
            input_tensor=False)


if __name__ == "__main__":
    # first load is slow for the ASR encoding
    asr_model = ASR_Model()
    asr_model.downloadModel()
    # load the current audio file
    print('-------------')
    print('Current Directory:')
    print(os.path.abspath(os.path.curdir))
    print('-------------')
    wave_file = [os.path.abspath(os.path.curdir) + "/" +  "server/audio.wav"]
    print('--------------------------')
    print('Transcription starting...')
    text = asr_model.model.transcribe(paths2audio_files=wave_file)
    logits = asr_model.model.transcribe(paths2audio_files=wave_file, logprobs=True)[0]
    print(f'Text to audio: {text}')
    print(f'Logits: {logits}' )
    print('--------------------------')
    print('Adding softmax to the logits: ')
    probs = asr_model.softmax(logits)
    print(f'Probabilities from softmax: {probs}')
    transcript = asr_model.beam.forward(log_probs = np.expand_dims(probs, axis=0), log_probs_length=None)
    print(f'Input text: {text}')
    print(f'Trascription result: {transcript}')
    print(f'First transcript: {transcript[0][0][1]}')

