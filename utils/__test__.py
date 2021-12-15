import audio

filename = 'audio.wav'


def test_record():
    chunk_size = 1024
    print('Record start..')
    audio.record(filename, seconds=10)
    print(f'Record end and saved on file {filename}')


def test_reproduce():
    audio.reproduce(filename)



test_record()
test_reproduce()