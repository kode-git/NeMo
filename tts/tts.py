import soundfile as sf
from nemo.collections.tts.models.base import SpectrogramGenerator, Vocoder
import time

spec_generator = None
vocoder = None

def download_model(model_spec = "tts_en_fastpitch", model_vocoder = "tts_higigan"):
    spec_generator = SpectrogramGenerator.from_pretrained(model_name=model_spec).cuda()
    vocoder = Vocoder.from_pretrained(model_name=model_vocoder).cuda()

# you must have NVIDIA driver to support the Pytorch Lightning dependencies
def text_to_speech(text : str):
    if spec_generator is None or vocoder is None:
        download_model()
    parsed = spec_generator(parse(text))
    spectrogram = spec_generator.generate_spectrogram(tokens=parsed)
    audio = vocoder.convert_spectrogram_to_audio(spec=spectrogram)
    sf.write("speech.wav", audio.to('cpu').detach().numpy()[0], 22050)

if __name__ == '__main__':
    print(f'Execution time: {time.time()}')
    decision = input('Do you want to import tts model locally? Y for yes | other keys for no\n')
    if decision == 'Y' or decision == 'y':
        download_model()

    decision = input('Do you want to test model? Y for yes | other keys for no\n')
    if decision == 'Y' or decision == 'y':
        input_text = input('Write a string to perform the TTS model: ')
        text_to_speech(input_text)

    print(f'Process finished at: {time.time()}')

