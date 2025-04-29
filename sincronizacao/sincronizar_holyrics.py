import pygame
import time
import requests
from mutagen.easyid3 import EasyID3

# TOKEN e HEADERS fixos
TOKEN = "N3bPkOuJ4ds02RCR"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# Função para buscar a letra no Holyrics
def buscar_letra_holyrics(titulo, artista, api_url='http://localhost:8091/api/lyrics'):
    params = {'title': titulo, 'artist': artista}
    try:
        resposta = requests.get(api_url, params=params, headers=HEADERS)
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados.get('lyrics')
        else:
            print(f"Erro na consulta da letra: {resposta.status_code} | {resposta.text}")
            return None
    except Exception as e:
        print("Erro ao conectar no Holyrics:", e)
        return None

# Função para extrair o título e artista do MP3
def extrair_metadados(caminho_audio):
    try:
        audio = EasyID3(caminho_audio)
        titulo = audio.get('title', ['Desconhecido'])[0]
        artista = audio.get('artist', ['Desconhecido'])[0]
    except Exception as e:
        print("Erro ao extrair metadados:", e)
        titulo, artista = "Desconhecido", "Desconhecido"
    return titulo, artista

# Função para gerar LRC
def gerar_lrc(timestamps, letra_texto):
    linhas_letra = letra_texto.splitlines()
    lrc_content = ""
    quantidade = min(len(timestamps), len(linhas_letra))
    for i in range(quantidade):
        tempo = timestamps[i]
        minutos = int(tempo // 60)
        segundos = tempo % 60
        time_tag = f"[{minutos:02}:{segundos:05.2f}]"
        lrc_content += f"{time_tag} {linhas_letra[i]}\n"
    return lrc_content

# Função para enviar a letra ao Holyrics
def enviar_letra_holyrics(lrc_content, api_url="http://localhost:8091/api/slide/text"):
    dados = {"text": lrc_content}
    try:
        resposta = requests.post(api_url, json=dados, headers=HEADERS)
        if resposta.status_code == 200:
            print("Letra enviada com sucesso para o Holyrics!")
        else:
            print(f"Erro ao enviar letra: {resposta.status_code} | {resposta.text}")
    except Exception as e:
        print("Erro ao enviar requisição:", e)

# Função para reproduzir a música com a sincronização da letra
def reproduzir_musica(caminho_audio, timestamps, letra_texto):
    # Inicializa o mixer do Pygame
    pygame.mixer.init()
    pygame.mixer.music.load(caminho_audio)  # Carrega a música
    pygame.mixer.music.play()  # Começa a tocar a música
    
    print("Música tocando...")

    # Enviar as letras com base no timestamp
    linhas_letra = letra_texto.splitlines()
    for i, tempo in enumerate(timestamps):
        minutos = int(tempo // 60)
        segundos = tempo % 60
        time_tag = f"[{minutos:02}:{segundos:05.2f}]"

        # Espera até o momento do timestamp
        time.sleep(tempo - pygame.mixer.music.get_pos() / 1000.0)  # Ajusta o tempo de espera com base na posição da música

        # Envia a letra ao Holyrics
        lrc_text = f"{time_tag} {linhas_letra[i]}"
        enviar_letra_holyrics(lrc_text)

# Função principal
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

    # Processar Áudio (timestamps) - Exemplo com timestamps fictícios
    timestamps = [0, 10, 20, 30, 40]  # Timestamps fictícios, você precisa gerar isso a partir da música real
    print("Timestamps:", timestamps)

    # Gerar LRC
    lrc_content = gerar_lrc(timestamps, letra)
    print("Conteúdo LRC Gerado:\n", lrc_content)

    # Reproduzir a música e sincronizar com a letra
    reproduzir_musica(caminho_audio, timestamps, letra)

if __name__ == "__main__":
    main()
