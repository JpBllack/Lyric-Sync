from processamento.processar_audio import processar_audio
from sincronizacao.sincronizar_holyrics import (
    extrair_metadados,
    buscar_letra_holyrics,
    gerar_lrc,
    enviar_letra_holyrics,
    reproduzir_musica
)
import os

def main():
    caminho_audio = 'testes/vou-deixar-na-cruz.mp3'  # Caminho do arquivo MP3

    # Extrair Título e Artista
    titulo, artista = extrair_metadados(caminho_audio)
    print("Título:", titulo, "| Artista:", artista)

    # Buscar Letra
    letra = buscar_letra_holyrics(titulo, artista)
    if letra is None:
        print("Letra não encontrada. Encerrando.")
        return

    # Processar Áudio (timestamps)
    timestamps = processar_audio(caminho_audio)
    print("Timestamps:", timestamps)

    # Gerar LRC
    lrc_content = gerar_lrc(timestamps, letra)
    print("Conteúdo LRC Gerado:\n", lrc_content)

    # Reproduzir Música e Sincronizar Letra
    reproduzir_musica(caminho_audio, timestamps, letra)

    # Enviar Letra ao Holyrics
    # Se a função de sincronização já estiver enviando a letra, essa linha pode ser opcional
    # enviar_letra_holyrics(lrc_content)

if __name__ == "__main__":
    main()