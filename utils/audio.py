# audio.py for recording and reproduce speech from input stream

import pyaudio
import wave
import simpleaudio as sa

format_audio = pyaudio.paInt16


def record(out_file, rate=44100, seconds=5, channels=2, chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=format_audio,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print(f'Recording setting:\nFormat: {format_audio}\nChannels: {channels}\nRate: {rate}\nChunks: {chunk}\n')

    for i in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Closing ')
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format_audio))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def reproduce(filename):
    print(f'Starting reproducing of {filename} audio file')
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # wait until sound has finished playing
    print('Closing file')
