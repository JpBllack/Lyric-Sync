import pygame
import time
import re
import unicodedata
import string
from difflib import SequenceMatcher

# ---------- Estrofes do Holyrics ----------
holyrics_estrofes = [
    """Sua morte ali na cruz
Carregando a minha dor
Você se expôs por mim""",

    """Se entregou em meu lugar
E me deu uma nova chance
Eu vou recomeçar""",

    """Vou deixar na cruz
Tudo o que passou
Tudo o que ficou pra trás""",

    """Olho pra Você
Corro pra Você
O Seu amor me chama""",

    """Eu dependo desse amor
Do Seu amor mais que tudo
Eu confio que esse amor
Tem poder pra curar dores"""
]

# ---------- Funções ----------
def limpar_texto(texto):
    stopwords = {"o", "a", "os", "as", "de", "do", "da", "que", "e", "em", "pra", "por", "com"}
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    palavras = texto.lower().strip().split()
    palavras = [p for p in palavras if p not in stopwords]
    return ' '.join(palavras)


def parse_lrc(lrc_text):
    lines = lrc_text.strip().split('\n')
    parsed = []
    for line in lines:
        match = re.match(r'\[(\d+):(\d+\.\d+)\](.*)', line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            text = match.group(3).strip()
            time_sec = minutes * 60 + seconds
            if text:
                parsed.append((time_sec, text))
    return parsed

def agrupar_estrofes_lrc(lrc_linhas, intervalo=3.5):
    estrofes = []
    atual = []
    tempos = []
    for tempo, texto in lrc_linhas:
        if not atual or tempo - tempos[-1] <= intervalo:
            atual.append(texto)
            tempos.append(tempo)
        else:
            estrofes.append((tempos[0], tempos[-1], '\n'.join(atual)))
            atual = [texto]
            tempos = [tempo]
    if atual:
        estrofes.append((tempos[0], tempos[-1], '\n'.join(atual)))
    return estrofes

def similaridade(a, b):
    a = limpar_texto(a)
    b = limpar_texto(b)
    return SequenceMatcher(None, a, b).ratio()

def mapear_repeticoes(lrc_estrofes, holyrics_estrofes, limite_similaridade=0.5):
    mapeamento = []
    for inicio, fim, trecho in lrc_estrofes:
        melhor_score = 0
        melhor_est = None
        for h in holyrics_estrofes:
            score = similaridade(h, trecho)
            if score > melhor_score:
                melhor_score = score
                melhor_est = h
        if melhor_score >= limite_similaridade:
            mapeamento.append({'inicio': inicio, 'fim': fim, 'letra': melhor_est})
    return mapeamento

# ---------- Execução Principal ----------
if __name__ == "__main__":
    with open("LyricSyncTest/musica.lrc", "r", encoding="utf-8") as f:
        lrc_text = f.read()

    lrc_linhas = parse_lrc(lrc_text)
    lrc_estrofes = agrupar_estrofes_lrc(lrc_linhas)
    estrofes_mapeadas = mapear_repeticoes(lrc_estrofes, holyrics_estrofes)

    pygame.mixer.init()
    pygame.mixer.music.load("LyricSyncTest/vou-deixar-na-cruz.mp3")
    pygame.mixer.music.play()
    print("🎵 Tocando música...")

    mostradas = set()
    inicio_tempo = time.time()

    try:
        while pygame.mixer.music.get_busy():
            agora = time.time() - inicio_tempo
            for i, est in enumerate(estrofes_mapeadas):
                if est['inicio'] <= agora <= est['fim'] and i not in mostradas:
                    mostradas.add(i)
                    print(f"\n🕐 {est['inicio']:.2f}s até {est['fim']:.2f}s")
                    print("📖 Estrofe atual:")
                    print(est['letra'])
            time.sleep(0.1)
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        print("Parado pelo usuário.")
