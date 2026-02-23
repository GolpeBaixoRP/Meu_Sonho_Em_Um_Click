import os
import re

INPUT_FILE = "BIOPSIA_PROFUNDA_RELATORIO.txt"

OUTPUT_FILES = {
    "core": "01_CORE_VALIDO.txt",
    "externo": "02_DEPENDENCIAS_EXTERNAS.txt",
    "reaproveitavel": "03_CODIGO_REAPROVEITAVEL.txt",
    "ruido": "04_RUIDO_DESCARTAVEL.txt",
    "alerta": "05_ALERTAS_SEGURANCA.txt"
}

def classificar_linha(linha):
    l = linha.lower()

    # ALERTAS
    if any(p in l for p in ["virus", "malware", "trojan", "suspeito"]):
        return "alerta"

    # BINÁRIOS
    if any(ext in l for ext in [".exe", ".dll", ".bin"]):
        return "externo"

    # DEPENDÊNCIAS EXTERNAS
    if "site-packages" in l or "dist-packages" in l:
        return "externo"

    # CÓDIGO AUTORAL CORE
    if any(ext in l for ext in [".py", ".ps1"]):
        if "core" in l or "main" in l:
            return "core"
        return "reaproveitavel"

    # ARQUIVOS DE CONFIG
    if any(ext in l for ext in [".json", ".yaml", ".yml", ".ini"]):
        return "reaproveitavel"

    # OUTROS POSSÍVEIS RUÍDOS
    if any(ext in l for ext in [".png", ".jpg", ".log", ".tmp"]):
        return "ruido"

    return "reaproveitavel"


def main():
    if not os.path.exists(INPUT_FILE):
        print("Arquivo de entrada não encontrado.")
        return

    resultados = {k: [] for k in OUTPUT_FILES.keys()}

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for linha in f:
            categoria = classificar_linha(linha)
            resultados[categoria].append(linha.strip())

    for categoria, arquivo in OUTPUT_FILES.items():
        with open(arquivo, "w", encoding="utf-8") as out:
            out.write(f"=== {categoria.upper()} ===\n\n")
            for item in resultados[categoria]:
                out.write(item + "\n")

    print("Classificação final concluída com sucesso.")


if __name__ == "__main__":
    main()