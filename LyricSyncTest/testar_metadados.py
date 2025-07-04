from core.metadata_extractor import extrair_metadados

# Caminho do mp3 já salvo em assets/music
caminho_musica = "assets/music/Santo pra sempre.mp3"

metadados = extrair_metadados(caminho_musica)

print("Título:", metadados["titulo"])
print("Artista:", metadados["artista"])
print("Duração:", metadados["duracao"], "segundos")
