import librosa
import numpy as np

# Função para carregar o arquivo de áudio
def carregar_audio(caminho_audio):
    # Carregar o áudio com librosa
    y, sr = librosa.load(caminho_audio, sr=None)
    return y, sr

# Função para detectar batidas e gerar timestamps
def detectar_batidas(y, sr):
    # Detectar as batidas usando onset_detect
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    return onset_times

# Função principal de processamento
def processar_audio(caminho_audio):
    # Carregar o áudio
    y, sr = carregar_audio(caminho_audio)
    # Detectar batidas e gerar timestamps
    timestamps = detectar_batidas(y, sr)
    return timestamps
