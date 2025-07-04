# core/lrc_fetcher.py

import requests
import os

def buscar_lrc(track_name, artist_name, duration=None, album_name=None):
    url = "https://lrclib.net/api/get"

    params = {
        "track_name": track_name,
        "artist_name": artist_name,
    }

    if duration:
        params["duration"] = int(duration)
    if album_name:
        params["album_name"] = album_name

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        if "syncedLyrics" in data and data["syncedLyrics"]:
            return data["syncedLyrics"]
        else:
            print("Letra sincronizada não encontrada.")
            return None
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


def salvar_lrc(nome_musica, lrc_texto):
    os.makedirs("assets/lrc", exist_ok=True)
    nome_arquivo = f"assets/lrc/{nome_musica}.lrc"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(lrc_texto)
        print(f"✅ Letra salva com sucesso em: {nome_arquivo}")
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao salvar o arquivo .lrc: {e}")
        return None
