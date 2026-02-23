import os
import ast
import hashlib
from collections import defaultdict

RAIZ = "Projeto_Extraido"

def hash_arquivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def analisar_imports_ast(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except:
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return imports

def mapear_projeto():
    arquivos = []
    hashes = {}
    imports_map = {}
    dependencia = defaultdict(set)
    importado_por = defaultdict(set)

    for root, dirs, files in os.walk(RAIZ):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                arquivos.append(path)
                hashes[path] = hash_arquivo(path)
                imports = analisar_imports_ast(path)
                imports_map[path] = imports

    # Criar grafo simples baseado no nome do módulo
    for arquivo, imports in imports_map.items():
        for imp in imports:
            for alvo in arquivos:
                if imp in alvo.replace("\\", "."):
                    dependencia[arquivo].add(alvo)
                    importado_por[alvo].add(arquivo)

    return arquivos, hashes, dependencia, importado_por

def gerar_relatorio():
    arquivos, hashes, dependencia, importado_por = mapear_projeto()

    with open("BIOPSIA_PROFUNDA_RELATORIO.txt", "w", encoding="utf-8") as f:

        f.write("===== DUPLICADOS =====\n")
        hash_map = defaultdict(list)
        for arq, h in hashes.items():
            hash_map[h].append(arq)

        for grupo in hash_map.values():
            if len(grupo) > 1:
                f.write("\n".join(grupo) + "\n\n")

        f.write("\n===== ORFAOS REAIS =====\n")
        for arq in arquivos:
            if arq not in importado_por:
                f.write(arq + "\n")

        f.write("\n===== NUCLEO (MAIS IMPORTADOS) =====\n")
        ranking = sorted(importado_por.items(), key=lambda x: len(x[1]), reverse=True)
        for arq, quem in ranking[:20]:
            f.write(f"{arq} | importado_por={len(quem)}\n")

        f.write("\n===== DEPENDENCIAS =====\n")
        for arq, deps in dependencia.items():
            if deps:
                f.write(f"\n{arq}\n")
                for d in deps:
                    f.write(f"   -> {d}\n")

if __name__ == "__main__":
    gerar_relatorio()