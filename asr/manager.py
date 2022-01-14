import onnxruntime
import tempfile
from nemo.collections.asr.models.ctc_models import EncDecCTCModel
from nemo.collections.asr.data.audio_to_text import AudioToCharDataset
import os
import torch
import yaml
from omegaconf import DictConfig
import json
import numpy as np


QUARTZNET_MODEL = "QuartzNet15x5Base-En"
neMo_file = f'{QUARTZNET_MODEL}.nemo'
onnx_file = f'{QUARTZNET_MODEL}.onnx'
config_yaml = f'{QUARTZNET_MODEL}.yaml'

# your quartznet config
config_path = config_yaml
# your exported onnx model path
model_to_load = onnx_file


def softmax(logits):
    e = np.exp(logits - np.max(logits))
    return e / e.sum(axis=-1).reshape([logits.shape[0], 1])

def get_nemo_dataset(config, vocab, sample_rate=16000):
    augmentor = None

    config = {
        'manifest_filepath': os.path.join(config['temp_dir'], 'manifest.json'),
        'sample_rate': sample_rate,
        'labels': vocab,
        'batch_size': min(config['batch_size'], len(config['paths2audio_files'])),
        'trim_silence': True,
        'shuffle': False,
    }

    dataset = AudioToCharDataset(
        manifest_filepath=config['manifest_filepath'],
        labels=config['labels'],
        sample_rate=config['sample_rate'],
        int_values=config.get('int_values', False),
        augmentor=augmentor,
        max_duration=config.get('max_duration', None),
        min_duration=config.get('min_duration', None),
        max_utts=config.get('max_utts', 0),
        blank_index=config.get('blank_index', -1),
        unk_index=config.get('unk_index', -1),
        normalize=config.get('normalize_transcripts', False),
        trim=config.get('trim_silence', True),
        load_audio=config.get('load_audio', True),
        parser=config.get('parser', 'en'),
        add_misc=config.get('add_misc', False),
    )

    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=config['batch_size'],
        collate_fn=dataset.collate_fn,
        drop_last=config.get('drop_last', False),
        shuffle=True,
        num_workers=config.get('num_workers', 0),
        pin_memory=config.get('pin_memory', False),
    )

def get_letters(probs):
    letters = []
    for idx in range(0, probs.shape[0]):
        current_char_idx = np.argmax(probs[idx])
        if labels[current_char_idx] != "blank":
            letters.append([labels[current_char_idx], idx])
    return letters

with open(config_path) as f:
    params = yaml.safe_load(f)

# create onnx session with model (assuming you already exported your model)
sess = onnxruntime.InferenceSession(model_to_load)
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

# create preprocessor (NeMo does this inside EncDecCTCModel, here we do it explicitly since we are going to use onnx and not EncDecCTCModel)
preprocessor_cfg = DictConfig(params).preprocessor
preprocessor = EncDecCTCModel.from_config_dict(preprocessor_cfg)

audio_file = "../server/audio.wav-"
labels = params['decoder']['vocabulary'] #"vocabulary" could be something else depending on model

# this part is just copy pasted from NeMo library code
with tempfile.TemporaryDirectory() as dataloader_tmpdir:
    with open(os.path.join(dataloader_tmpdir, 'manifest.json'), 'w') as fp:
        entry = {'audio_filepath': audio_file, 'duration': 100000, 'text': 'nothing'}
        fp.write(json.dumps(entry) + '\n')
    out_batch = []
    config = {'paths2audio_files': [audio_file], 'batch_size': 1, 'temp_dir': dataloader_tmpdir}
    temporary_datalayer = get_nemo_dataset(config, labels, 16000)
    for test_batch in temporary_datalayer:
        out_batch.append(test_batch)

# preprocess audio just like NeMo does
processed_signal, processed_signal_length = preprocessor(input_signal=out_batch[0][0], length=out_batch[0][1], )
processed_signal = processed_signal.cpu().numpy()

# finally make an inference using onnx model
logits = sess.run([label_name], {input_name: processed_signal})
probabilities = logits[0][0]

probs = softmax(probabilities)

#silence
labels.append("blank")

letters = get_letters(probs)