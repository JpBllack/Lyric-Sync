import os
import requests
from urllib.parse import quote

LRC_DIR = "assets/lrc/"
API_URL = "https://lrclib.net/api/search"

def buscar_lrc(titulo, artista):
    if not os.path.exists(LRC_DIR):
        os.makedirs(LRC_DIR)

    try:
        titulo_codificado = quote(titulo)
        artista_codificado = quote(artista)

        url = f"{API_URL}?title={titulo_codificado}&artist={artista_codificado}"
        print(f"🔍 URL gerada para a busca: {url}")

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data or "syncedLyrics" not in data[0]:
            print(f"❌ Letra sincronizada não encontrada para: {titulo} - {artista}")
            return None

        lrc_content = data[0]["syncedLyrics"]
        lrc_file_path = os.path.join(LRC_DIR, f"{titulo}_{artista}.lrc")

        with open(lrc_file_path, "w", encoding="utf-8") as lrc_file:
            lrc_file.write(lrc_content)

        print(f"✅ LRC baixado e salvo em: {lrc_file_path}")
        return lrc_file_path

    except Exception as e:
        print(f"❌ Erro ao buscar LRC: {e}")
        return None
