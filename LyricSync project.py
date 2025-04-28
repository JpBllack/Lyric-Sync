#LyricSync
import pyaudio
import numpy as np

#configurações
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
DURATION = 10

p = pyaudio.PyAudio()

stream = p.open (format=FORMAT,
                 channels=CHANNELS,
                 rate=SAMPLE_RATE,
                 input=True,
                 frames_per_buffer=CHUNK_SIZE)

print ("Capturando áudio...")

frames = []

for _ in range(0, int(SAMPLE_RATE/CHUNK_SIZE * DURATION)):
    data = stream.read(CHUNK_SIZE)
    frames.append(data)

    stream.stop_stream()
    stream.close()

p.terminate()

print("Captura concluída.")


