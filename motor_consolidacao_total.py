import os
import hashlib
import csv
from collections import defaultdict

BASE_PATH = "Projeto_Extraido/Nova pasta"
PASTA_A = os.path.join(BASE_PATH, "Frontend-Backup")
PASTA_B = os.path.join(BASE_PATH, "seu_projeto")
SAIDA = "consolidacao_relatorio"

os.makedirs(SAIDA, exist_ok=True)

def gerar_hash(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def mapear_arquivos(base):
    arquivos = {}
    for root, dirs, files in os.walk(base):
        for file in files:
            caminho = os.path.join(root, file)
            relativo = os.path.relpath(caminho, base)
            arquivos[relativo] = caminho
    return arquivos

print("🔍 Mapeando arquivos...")
mapa_a = mapear_arquivos(PASTA_A)
mapa_b = mapear_arquivos(PASTA_B)

todos_relativos = set(mapa_a.keys()).union(set(mapa_b.keys()))

iguais = []
diferentes = []
exclusivos_a = []
exclusivos_b = []

print("🧬 Comparando arquivos...")

for rel in todos_relativos:
    a = mapa_a.get(rel)
    b = mapa_b.get(rel)

    if a and b:
        hash_a = gerar_hash(a)
        hash_b = gerar_hash(b)
        if hash_a == hash_b:
            iguais.append(rel)
        else:
            diferentes.append(rel)
    elif a:
        exclusivos_a.append(rel)
    elif b:
        exclusivos_b.append(rel)

def salvar_lista(nome, lista):
    with open(os.path.join(SAIDA, nome), "w", encoding="utf-8") as f:
        for item in sorted(lista):
            f.write(item + "\n")

salvar_lista("03_iguais.txt", iguais)
salvar_lista("04_diferentes.txt", diferentes)
salvar_lista("05_exclusivos_backup.txt", exclusivos_a)
salvar_lista("06_exclusivos_seu_projeto.txt", exclusivos_b)

print("📊 Gerando estatísticas...")

total = len(todos_relativos)
estatisticas = f"""
TOTAL DE ARQUIVOS ANALISADOS: {total}

IGUAIS: {len(iguais)}
DIFERENTES: {len(diferentes)}
EXCLUSIVOS Frontend-Backup: {len(exclusivos_a)}
EXCLUSIVOS seu_projeto: {len(exclusivos_b)}
"""

with open(os.path.join(SAIDA, "07_estatisticas.txt"), "w", encoding="utf-8") as f:
    f.write(estatisticas)

recomendacao = ""

if len(exclusivos_b) > len(exclusivos_a):
    recomendacao = "Recomendação: seu_projeto parece mais evoluído."
elif len(exclusivos_a) > len(exclusivos_b):
    recomendacao = "Recomendação: Frontend-Backup parece mais completo."
else:
    recomendacao = "Recomendação: Ambos possuem evolução paralela. Necessário merge estratégico."

with open(os.path.join(SAIDA, "08_recomendacao_estrategica.txt"), "w", encoding="utf-8") as f:
    f.write(recomendacao)

print("✅ Consolidação concluída. Verifique a pasta 'consolidacao_relatorio'.")