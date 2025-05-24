import re

def parse_lrc(caminho_lrc):
    try:
        with open(caminho_lrc, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        estrofes = []
        for linha in linhas:
            partes = re.findall(r'\[(\d+):(\d+\.\d+)\](.*)', linha)
            for min, sec, texto in partes:
                tempo_segundos = int(min) * 60 + float(sec)
                estrofes.append((tempo_segundos, texto.strip()))

        estrofes.sort(key=lambda x: x[0])
        return estrofes

    except Exception as e:
        print(f"❌ Erro ao fazer parse do LRC: {e}")
        return []
