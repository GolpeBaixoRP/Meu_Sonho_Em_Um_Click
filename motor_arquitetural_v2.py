import os
import ast
from collections import defaultdict, Counter

IGNORAR_PASTAS = {
    "venv", "site-packages", "pip", "packaging", "darkdetect", "__pycache__"
}

BASE_DIR = "Projeto_Extraido"

codigo_autoral = []
dependencias = defaultdict(set)
contagem_funcoes = {}
contagem_classes = {}

def eh_autoral(caminho):
    for pasta in IGNORAR_PASTAS:
        if pasta in caminho:
            return False
    return True

def analisar_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except:
        return
    
    funcoes = 0
    classes = 0
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcoes += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])

    contagem_funcoes[caminho] = funcoes
    contagem_classes[caminho] = classes
    dependencias[caminho] = set(imports)

def explorar():
    for raiz, pastas, arquivos in os.walk(BASE_DIR):
        if not eh_autoral(raiz):
            continue

        for arquivo in arquivos:
            if arquivo.endswith(".py"):
                caminho_completo = os.path.join(raiz, arquivo)
                if eh_autoral(caminho_completo):
                    codigo_autoral.append(caminho_completo)
                    analisar_arquivo(caminho_completo)

def gerar_relatorios():
    with open("01_codigo_autoral.txt", "w", encoding="utf-8") as f:
        for arquivo in codigo_autoral:
            f.write(f"{arquivo}\n")

    with open("02_mapa_dependencias.txt", "w", encoding="utf-8") as f:
        for arq, deps in dependencias.items():
            f.write(f"{arq}\n")
            for dep in deps:
                f.write(f"   -> {dep}\n")
            f.write("\n")

    ranking = sorted(contagem_funcoes.items(), key=lambda x: x[1], reverse=True)

    with open("03_ranking_importancia.txt", "w", encoding="utf-8") as f:
        for arq, qtd in ranking:
            f.write(f"{arq} | funcoes={qtd} | classes={contagem_classes[arq]}\n")

    if ranking:
        core = ranking[0][0]
        with open("04_possivel_core.txt", "w", encoding="utf-8") as f:
            f.write(f"Possível núcleo do sistema:\n{core}\n")

    with open("05_sugestao_arquitetura.txt", "w", encoding="utf-8") as f:
        f.write("Sugestão Estrutural:\n")
        f.write("- core/: lógica principal\n")
        f.write("- database/: persistência\n")
        f.write("- interface/: tabs e frontend\n")
        f.write("- forense_ul/: ferramentas UL\n")

def main():
    explorar()
    gerar_relatorios()
    print("Arquitetura analisada com sucesso.")

if __name__ == "__main__":
    main()