import re

def parse_lrc(lrc_path):
    estrofes = []

    with open(lrc_path, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            partes = re.findall(r'\[(\d+):(\d+\.\d+)\](.*)', linha)
            for minuto, segundo, texto in partes:
                tempo = int(minuto) * 60 + float(segundo)
                texto = texto.strip()
                if texto:
                    estrofes.append((tempo, texto))

    estrofes.sort(key=lambda x: x[0])
    return estrofes
