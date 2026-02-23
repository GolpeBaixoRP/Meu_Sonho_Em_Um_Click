import os
import zipfile
import ast
from datetime import datetime

ZIP_NAME = "Meu_Sonho_Em_Um_Click.zip"
EXTRACT_FOLDER = "Projeto_Extraido"
OUTPUT_FILE = "INVENTARIO_ESTRUTURAL_ESTRATEGICO.txt"

def extract_zip():
    if not os.path.exists(EXTRACT_FOLDER):
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_FOLDER)

def classify_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".py"]:
        return "CODIGO_PYTHON"
    elif ext in [".ps1", ".bat", ".sh"]:
        return "SCRIPT_AUTOMACAO"
    elif ext in [".exe", ".dll"]:
        return "EXECUTAVEL_BINARIO"
    elif ext in [".txt", ".md", ".doc", ".pdf"]:
        return "DOCUMENTACAO"
    elif ext in [".json", ".yaml", ".yml", ".ini", ".cfg"]:
        return "CONFIGURACAO"
    elif ext in [".png", ".jpg", ".jpeg", ".bmp"]:
        return "IMAGEM"
    elif ext in [".zip", ".rar", ".7z"]:
        return "ARQUIVO_COMPACTADO"
    else:
        return "OUTROS"

def analyze_python(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        tree = ast.parse(content)

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)

        return {
            "linhas": len(content.splitlines()),
            "funcoes": functions,
            "classes": classes,
            "imports": imports
        }

    except Exception as e:
        return {"erro": str(e)}

def build_tree(root_dir):
    tree_lines = []
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * level
        tree_lines.append(f"{indent}├── {os.path.basename(root)}")
        subindent = '│   ' * (level + 1)
        for f in files:
            tree_lines.append(f"{subindent}├── {f}")
    return "\n".join(tree_lines)

def main():
    extract_zip()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        out.write("========== INVENTARIO ESTRUTURAL ESTRATEGICO ==========\n")
        out.write(f"Gerado em: {datetime.now()}\n\n")

        out.write("=== ARVORE ESTRUTURAL ===\n")
        out.write(build_tree(EXTRACT_FOLDER))
        out.write("\n\n")

        counter = 1

        for root, dirs, files in os.walk(EXTRACT_FOLDER):
            for name in files:
                file_path = os.path.join(root, name)
                size = os.path.getsize(file_path)
                created = datetime.fromtimestamp(os.path.getctime(file_path))
                modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                classification = classify_file(file_path)

                out.write(f"\n\n[{counter}] {name}\n")
                out.write(f"Caminho: {file_path}\n")
                out.write(f"Tamanho: {size} bytes\n")
                out.write(f"Criado: {created}\n")
                out.write(f"Modificado: {modified}\n")
                out.write(f"Classificacao: {classification}\n")

                if classification == "CODIGO_PYTHON":
                    analysis = analyze_python(file_path)
                    out.write("=== ANALISE PYTHON ===\n")
                    for key, value in analysis.items():
                        out.write(f"{key}: {value}\n")

                counter += 1

        out.write("\n\n========== FIM DO INVENTARIO ==========\n")

if __name__ == "__main__":
    main()