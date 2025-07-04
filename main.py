import os
import shutil
import tkinter as tk
from tkinter import filedialog
from core.metadata_extractor import extrair_metadados
from core.lrc_fetcher import buscar_lrc

ASSETS_MUSIC_DIR = "assets/music"

def selecionar_musica():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione a música (.mp3 apenas)",
        filetypes=[("MP3 files", "*.mp3")]
    )
    if caminho_arquivo:
        print(f"🎵 Música selecionada: {caminho_arquivo}")
        return caminho_arquivo
    print("❌ Nenhuma música selecionada.")
    return None

def preparar_arquivo(caminho_original):
    if not os.path.exists(ASSETS_MUSIC_DIR):
        os.makedirs(ASSETS_MUSIC_DIR)

    nome_arquivo = os.path.basename(caminho_original)
    destino = os.path.join(ASSETS_MUSIC_DIR, nome_arquivo)

    # Faz a cópia do arquivo em vez de mover
    shutil.copy(caminho_original, destino)

    print(f"✅ Música copiada para: {destino}")
    return destino

if __name__ == "__main__":
    caminho = selecionar_musica()
    if caminho:
        caminho_final = preparar_arquivo(caminho)
        print("📄 Extraindo metadados...")
        metadados = extrair_metadados(caminho_final)
        print(f"📄 Metadados extraídos: {metadados}")

        # 🔍 Buscar o LRC agora que temos título e artista
        buscar_lrc(metadados["titulo"], metadados["artista"])
