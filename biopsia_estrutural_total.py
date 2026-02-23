import os
import ast
import hashlib
from collections import defaultdict, Counter

BASE_DIR = "Projeto_Extraido"
IGNORAR = {"venv", "site-packages", "__pycache__", "pip", "packaging", "darkdetect"}

arquivos_py = []
imports_mapa = defaultdict(set)
importado_por = defaultdict(set)
hash_mapa = {}
duplicados_hash = defaultdict(list)

def ignorar(caminho):
    for pasta in IGNORAR:
        if pasta in caminho:
            return True
    return False

def coletar_arquivos():
    for raiz, _, arquivos in os.walk(BASE_DIR):
        if ignorar(raiz):
            continue
        for arq in arquivos:
            if arq.endswith(".py"):
                caminho = os.path.join(raiz, arq)
                if not ignorar(caminho):
                    arquivos_py.append(caminho)

def calcular_hash(caminho):
    with open(caminho, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def analisar_imports(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except:
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports_mapa[caminho].add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports_mapa[caminho].add(node.module.split(".")[0])

def mapear_dependencias():
    nomes_modulos = {os.path.splitext(os.path.basename(a))[0]: a for a in arquivos_py}
    for arq in arquivos_py:
        for imp in imports_mapa[arq]:
            if imp in nomes_modulos:
                importado_por[nomes_modulos[imp]].add(arq)

def classificar():
    classificacao = {}
    for arq in arquivos_py:
        if len(importado_por[arq]) >= 3:
            classificacao[arq] = "CORE_CANDIDATO"
        elif len(importado_por[arq]) == 0:
            classificacao[arq] = "ORFAO"
        else:
            classificacao[arq] = "UTIL_RELEVANTE"
    return classificacao

def detectar_duplicados():
    for arq in arquivos_py:
        h = calcular_hash(arq)
        hash_mapa[arq] = h
        duplicados_hash[h].append(arq)

def gerar_relatorio(classificacao):
    with open("BIOPSIA_RELATORIO_COMPLETO.txt", "w", encoding="utf-8") as f:
        f.write("===== DUPLICADOS POR CONTEUDO =====\n\n")
        for h, lista in duplicados_hash.items():
            if len(lista) > 1:
                for arq in lista:
                    f.write(f"{arq}\n")
                f.write("\n")

        f.write("\n===== CLASSIFICACAO =====\n\n")
        for arq, tipo in classificacao.items():
            f.write(f"{tipo} | {arq}\n")

        f.write("\n===== CENTRALIDADE =====\n\n")
        for arq, dependentes in sorted(importado_por.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"{arq} | importado_por={len(dependentes)}\n")

def main():
    coletar_arquivos()
    for arq in arquivos_py:
        analisar_imports(arq)
    mapear_dependencias()
    detectar_duplicados()
    classificacao = classificar()
    gerar_relatorio(classificacao)
    print("Biopsia estrutural concluida.")

if __name__ == "__main__":
    main()