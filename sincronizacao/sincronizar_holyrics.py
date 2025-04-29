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

# Função para gerar o LRC
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

# Função para enviar o LRC ao Holyrics
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
