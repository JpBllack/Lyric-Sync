#LyricSync
import pyaudio
import librosa
import numpy as np
import wave
import matplotlib.pyplot as plt
import librosa.display

# Configurações
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
DURATION = 10

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

print("Capturando áudio...")

frames = []

for _ in range(0, int(SAMPLE_RATE/CHUNK_SIZE * DURATION)):
    data = stream.read(CHUNK_SIZE)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

print("Captura concluída.")

# Salvar o áudio capturado
wf = wave.open('audio_capturado.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(SAMPLE_RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Carregar o áudio salvo
y, sr = librosa.load('audio_capturado.wav', sr=44100)

# Detectar batidas
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_times = librosa.frames_to_time(np.nonzero(onset_env)[0], sr=sr)

print("Timestamps das batidas: ", onset_times)


# Carregar o áudio salvo (caso ainda não tenha carregado)
y, sr = librosa.load('audio_capturado.wav', sr=44100)

# Detectar batidas
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_frames = np.nonzero(onset_env)[0]
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Plotar o áudio
plt.figure(figsize=(14, 6))
librosa.display.waveshow(y, sr=sr, alpha=0.6)
plt.vlines(onset_times, ymin=-1, ymax=1, color='r', linestyle='--', label='Batidas Detectadas')
plt.title('Áudio Capturado com Batidas Detectadas')
plt.xlabel('Tempo (s)')
plt.legend()
plt.show()
