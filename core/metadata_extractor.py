import os
import eyed3

def extrair_metadados(musica_path):
    if not os.path.isfile(musica_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {musica_path}")

    audio_file = eyed3.load(musica_path)
    if audio_file is None:
        raise IOError(f"Não foi possível abrir o arquivo de áudio: {musica_path}")

    titulo = audio_file.tag.title if audio_file.tag and audio_file.tag.title else "Desconhecido"
    artista = audio_file.tag.artist if audio_file.tag and audio_file.tag.artist else "Desconhecido"
    duracao = int(audio_file.info.time_secs) if audio_file.info else 0

    # Remove \ufeff e espaços extras
    titulo = titulo.replace('\ufeff', '').strip()
    artista = artista.replace('\ufeff', '').strip()

    return {
        "titulo": titulo,
        "artista": artista,
        "duracao": duracao
    }
