import pygame
import time
import requests
from mutagen.easyid3 import EasyID3
import os  # Para variáveis de ambiente

from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

TOKEN = os.environ.get("HOLYRICS_TOKEN")
if not TOKEN:
    print("Erro: Token do Holyrics não encontrado nas variáveis de ambiente.")
    exit()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# URLs da API
API_BASE_URL = "http://localhost:8091/api"  # Mantenha a URL base em uma variável
LYRICS_ENDPOINT = f"{API_BASE_URL}/lyrics"
SLIDE_TEXT_ENDPOINT = f"{API_BASE_URL}/slide/text"


# Função para buscar a letra no Holyrics
def buscar_letra_holyrics(titulo, artista, api_url=LYRICS_ENDPOINT):  # Use a variável
    params = {'title': titulo, 'artist': artista}
    print(f"buscar_letra_holyrics - Iniciando busca de letra...")
    print(f"buscar_letra_holyrics - URL: {api_url}")
    print(f"buscar_letra_holyrics - Parâmetros: {params}")
    print(f"buscar_letra_holyrics - Headers: {HEADERS}")
    try:
        resposta = requests.get(api_url, params=params, headers=HEADERS)
        print(f"buscar_letra_holyrics - Resposta da API (Raw): {resposta.raw}") # Adicionado o raw
        print(f"buscar_letra_holyrics - Resposta da API (Headers): {resposta.headers}") # Adicionado os headers da resposta
        print(f"buscar_letra_holyrics - Resposta da API (Content): {resposta.content}") # Adicionado o conteúdo da resposta
        print(f"buscar_letra_holyrics - Resposta da API: {resposta.status_code} | {resposta.text}")
        if resposta.status_code == 200:
            dados = resposta.json()
            print(f"buscar_letra_holyrics - Dados da resposta: {dados}")
            return dados.get('lyrics')
        else:
            print(f"Erro na consulta da letra: {resposta.status_code} | {resposta.text}")  # Log detalhado
            return None
    except Exception as e:
        print("Erro ao conectar no Holyrics:", e)
        return None


# Função para extrair o título e artista do MP3
def extrair_metadados(caminho_audio):
    print(f"extrair_metadados - Extraindo metadados de: {caminho_audio}")
    try:
        audio = EasyID3(caminho_audio)
        titulo = audio.get('title', ['Desconhecido'])[0]
        artista = audio.get('artist', ['Desconhecido'])[0]
        print(f"extrair_metadados - Título: {titulo}, Artista: {artista}")
    except Exception as e:
        print("Erro ao extrair metadados:", e)
        titulo, artista = "Desconhecido", "Desconhecido"
    return titulo, artista


# Função para gerar LRC
def gerar_lrc(timestamps, letra_texto):
    print(f"gerar_lrc - Gerando LRC com timestamps: {timestamps} e letra: {letra_texto}")
    linhas_letra = letra_texto.splitlines()
    lrc_content = ""
    quantidade = min(len(timestamps), len(linhas_letra))
    for i in range(quantidade):
        tempo = timestamps[i]
        minutos = int(tempo // 60)
        segundos = tempo % 60
        time_tag = f"[{minutos:02}:{segundos:05.2f}]"
        lrc_content += f"{time_tag} {linhas_letra[i]}\n"
    print(f"gerar_lrc - Conteúdo LRC gerado: {lrc_content}")
    return lrc_content


# Função para enviar a letra ao Holyrics
def enviar_letra_holyrics(lrc_content, api_url=SLIDE_TEXT_ENDPOINT):  # Use a variável
    print(f"enviar_letra_holyrics - Enviando letra para: {api_url}")
    print(f"enviar_letra_holyrics - Conteúdo LRC: {lrc_content}")
    print(f"enviar_letra_holyrics - Headers: {HEADERS}")
    dados = {"text": lrc_content}
    try:
        resposta = requests.post(api_url, json=dados, headers=HEADERS)
        print(f"enviar_letra_holyrics - Resposta da API: {resposta.status_code} | {resposta.text}")
        if resposta.status_code == 200:
            print("Letra enviada com sucesso para o Holyrics!")
        else:
            print(f"Erro ao enviar letra: {resposta.status_code} | {resposta.text}")  # Log detalhado
    except Exception as e:
        print("Erro ao enviar requisição:", e)


# Função para reproduzir a música com a sincronização da letra
def reproduzir_musica(caminho_audio, timestamps, letra_texto):
    print(f"reproduzir_musica - Iniciando reprodução de: {caminho_audio}")
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
        print(f"reproduzir_musica - Enviando linha: {lrc_text}")
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