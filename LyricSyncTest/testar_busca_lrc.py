# LyricSyncTest/testar_busca_lrc.py

from core.metadata_extractor import extrair_metadados
from core.lrc_fetcher import buscar_lrc, salvar_lrc
import os

caminho_musica = "assets/music/Santo pra sempre.mp3"

metadados = extrair_metadados(caminho_musica)
if metadados:
    print("🎵 Metadados extraídos:")
    print(metadados)

    lrc = buscar_lrc(
        track_name=metadados["titulo"],
        artist_name=metadados["artista"],
        duration=metadados["duracao"]
    )

    if lrc:
        print("\n📝 Letra sincronizada encontrada!\n")
        nome_base = os.path.splitext(os.path.basename(caminho_musica))[0]
        salvar_lrc(nome_base, lrc)
    else:
        print("❌ Nenhuma letra encontrada.")
