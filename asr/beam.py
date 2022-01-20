import nemo.collections.asr as nemo_asr
import sys
import gzip
import os, shutil, wget

# TO-DO: Temporal Class
class Beam:

    def __init__(self):
        self.beam = self.setBeam()

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

beam = Beam()