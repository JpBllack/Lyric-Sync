# LyricSync/core/audio_player.py

import time
import threading
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

def tocar_musica_sincronizado(caminho_musica, estrofes):
    audio = AudioSegment.from_mp3(caminho_musica)
    player = _play_with_simpleaudio(audio)

    inicio = time.time()

    for tempo, estrofe in estrofes:
        tempo_absoluto = inicio + tempo
        espera = tempo_absoluto - time.time()
        if espera > 0:
            time.sleep(espera)
        print(f"🎤 {estrofe}")  # No futuro, enviar para a interface gráfica ou Holyrics API

    player.wait_done()
