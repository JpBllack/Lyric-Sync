import re
from difflib import SequenceMatcher

# Estrofes do Holyrics
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

# Função para ler e parsear o arquivo LRC
def parse_lrc(lrc_text):
    lines = lrc_text.strip().split('\n')
    parsed = []
    for line in lines:
        match = re.match(r'\[(\d+):(\d+\.\d+)\](.*)', line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            text = match.group(3).strip()
            time = minutes * 60 + seconds
            if text:
                parsed.append((time, text))
    return parsed

# Agrupa por estrofes com base no intervalo entre linhas
def agrupar_estrofes_lrc(lrc_linhas, intervalo=6.0):
    estrofes = []
    atual = []
    tempos = []
    for i, (tempo, texto) in enumerate(lrc_linhas):
        if not atual:
            atual.append(texto)
            tempos = [tempo]
        else:
            if tempo - tempos[-1] <= intervalo:
                atual.append(texto)
                tempos.append(tempo)
            else:
                estrofes.append((tempos[0], tempos[-1], '\n'.join(atual)))
                atual = [texto]
                tempos = [tempo]
    if atual:
        estrofes.append((tempos[0], tempos[-1], '\n'.join(atual)))
    return estrofes

# Similaridade entre dois blocos de texto
def similaridade(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Mapeia as estrofes do Holyrics com as do LRC
def mapear_estrofes(lrc_estrofes, holyrics_estrofes):
    mapeamento = []
    usados = set()
    for h_est in holyrics_estrofes:
        melhor_score = 0
        melhor = None
        for i, (inicio, fim, l_est) in enumerate(lrc_estrofes):
            if i in usados:
                continue
            score = similaridade(h_est, l_est)
            if score > melhor_score:
                melhor_score = score
                melhor = (inicio, fim, l_est, i)
        if melhor:
            usados.add(melhor[3])
            mapeamento.append({'inicio': melhor[0], 'fim': melhor[1], 'letra': h_est})
    return mapeamento

# Código principal
if __name__ == "__main__":
    with open('musica.lrc', 'r', encoding='utf-8') as f:
        lrc_text = f.read()

    lrc_linhas = parse_lrc(lrc_text)
    lrc_estrofes = agrupar_estrofes_lrc(lrc_linhas)
    mapeamento = mapear_estrofes(lrc_estrofes, holyrics_estrofes)

    for i, est in enumerate(mapeamento):
        print(f"Estrofe {i+1}: {est['inicio']:.2f}s até {est['fim']:.2f}s")
        print(est['letra'])
        print('-' * 40)
