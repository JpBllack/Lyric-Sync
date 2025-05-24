import eyed3

def extrair_metadados(musica_path):
    # Carregar o arquivo de música com eyed3
    audio_file = eyed3.load(musica_path)

    # Extrair informações dos metadados
    titulo = audio_file.tag.title
    artista = audio_file.tag.artist
    duracao = audio_file.info.time_secs  # Tempo total da música em segundos

    # Exibir as informações
    print(f"Título: {titulo}")
    print(f"Artista: {artista}")
    print(f"Duração: {duracao:.2f} segundos")

    return titulo, artista, duracao

# Teste com o arquivo de música
musica_path = ''  # Altere o caminho conforme necessário
titulo, artista, duracao = extrair_metadados(musica_path)
