import os
import ast
from collections import defaultdict

ROOT_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(ROOT_DIR, "analise_saida")

os.makedirs(OUTPUT_DIR, exist_ok=True)

estrutura = []
classificacao = defaultdict(list)
mapa_tecnologico = []
candidatos_core = []

def analisar_python(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read())

        imports = []
        funcoes = 0
        classes = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
            elif isinstance(node, ast.FunctionDef):
                funcoes += 1
            elif isinstance(node, ast.ClassDef):
                classes += 1

        return imports, funcoes, classes

    except Exception:
        return [], 0, 0


for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, ROOT_DIR)

        estrutura.append(rel_path)

        ext = os.path.splitext(file)[1].lower()

        if ext in [".txt", ".md", ".docx"]:
            classificacao["Documentacao"].append(rel_path)
        elif ext in [".py"]:
            classificacao["Scripts_Python"].append(rel_path)

            imports, funcoes, classes = analisar_python(file_path)

            mapa_tecnologico.append(
                f"{rel_path} | imports={imports} | funcoes={funcoes} | classes={classes}"
            )

            if funcoes > 3 or classes > 1:
                candidatos_core.append(rel_path)

        elif ext in [".ps1"]:
            classificacao["Scripts_PowerShell"].append(rel_path)

        elif ext in [".exe", ".dll"]:
            classificacao["Binarios"].append(rel_path)

        elif ext in [".zip", ".rar"]:
            classificacao["Compactados"].append(rel_path)

        else:
            classificacao["Outros"].append(rel_path)


def salvar(nome, conteudo):
    with open(os.path.join(OUTPUT_DIR, nome), "w", encoding="utf-8") as f:
        if isinstance(conteudo, list):
            for item in conteudo:
                f.write(str(item) + "\n")
        elif isinstance(conteudo, dict):
            for chave, valores in conteudo.items():
                f.write(f"\n## {chave}\n")
                for v in valores:
                    f.write(str(v) + "\n")


salvar("01_Estrutura_Geral.txt", estrutura)
salvar("02_Classificacao.txt", classificacao)
salvar("03_Mapa_Tecnologico.txt", mapa_tecnologico)
salvar("04_Candidatos_a_Core.txt", candidatos_core)

relatorio_final = []
relatorio_final.append("=== RESUMO ESTRATEGICO ===")
relatorio_final.append(f"Total de arquivos: {len(estrutura)}")
relatorio_final.append(f"Python: {len(classificacao['Scripts_Python'])}")
relatorio_final.append(f"Documentacao: {len(classificacao['Documentacao'])}")
relatorio_final.append(f"Binarios: {len(classificacao['Binarios'])}")

salvar("05_Relatorio_Final.txt", relatorio_final)

print("Analise concluida. Verifique a pasta 'analise_saida'.")