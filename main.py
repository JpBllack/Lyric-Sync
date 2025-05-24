import os
import shutil
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment

from core import metadata_extractor
from core import lrc_fetcher

ASSETS_MUSIC_DIR = "assets/music"

def selecionar_musica():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione a música",
        filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.flac *.mp4")]
    )
    if caminho_arquivo:
        print(f"🎵 Música selecionada: {caminho_arquivo}")
        return caminho_arquivo
    print("❌ Nenhuma música selecionada.")
    return None

def converter_para_mp3(caminho_arquivo):
    try:
        nome_arquivo_mp3 = os.path.splitext(os.path.basename(caminho_arquivo))[0] + ".mp3"
        destino_mp3 = os.path.join(ASSETS_MUSIC_DIR, nome_arquivo_mp3)

        audio = AudioSegment.from_file(caminho_arquivo)
        audio.export(destino_mp3, format="mp3")

        print(f"🎵 Música convertida para MP3: {destino_mp3}")
        return destino_mp3
    except Exception as e:
        print(f"❌ Erro ao converter a música: {e}")
        return None

def preparar_arquivo(caminho_arquivo):
    os.makedirs(ASSETS_MUSIC_DIR, exist_ok=True)

    if not caminho_arquivo.lower().endswith(".mp3"):
        caminho_arquivo = converter_para_mp3(caminho_arquivo)

    if caminho_arquivo:
        nome_arquivo = os.path.basename(caminho_arquivo)
        destino = os.path.join(ASSETS_MUSIC_DIR, nome_arquivo)
        shutil.copy2(caminho_arquivo, destino)
        print(f"✅ Música copiada para: {destino}")
        return destino
    return None

if __name__ == "__main__":
    caminho = selecionar_musica()
    if caminho:
        caminho_final = preparar_arquivo(caminho)
        if caminho_final:
            metadata = metadata_extractor.extrair_metadados(caminho_final)
            if "erro" in metadata:
                print(f"❌ Erro ao extrair metadados: {metadata['erro']}")
            else:
                print("📄 Metadados extraídos:", metadata)
                lrc_path = lrc_fetcher.buscar_lrc(metadata["titulo"], metadata["artista"])
                if lrc_path:
                    print(f"📥 LRC salvo em: {lrc_path}")
                else:
                    print("❌ LRC não encontrado ou erro na busca.")
