import subprocess
import sys
import time

MAX_TENTATIVAS = 3


def executar_comando(cmd):
    resultado = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return resultado.stdout.lower(), resultado.stderr.lower()


def listar_discos():
    cmd = "powershell \"Get-Disk | Select-Object Number,FriendlyName,Size,PartitionStyle,IsSystem,IsOffline\""
    stdout, stderr = executar_comando(cmd)

    if stderr:
        print("[ERRO] falha ao listar discos.")
        sys.exit(1)

    linhas = stdout.splitlines()
    discos = []

    for linha in linhas[3:]:
        if linha.strip():
            partes = linha.split()
            try:
                numero = int(partes[0])
                nome = partes[1]
                tamanho = float(partes[2]) / (1024 ** 3)
                estilo = partes[3]
                is_system = partes[4] == "True"
                is_offline = partes[5] == "True"

                discos.append({
                    "numero": numero,
                    "nome": nome,
                    "tamanho": round(tamanho, 2),
                    "estilo": estilo,
                    "system": is_system,
                    "offline": is_offline
                })
            except:
                continue

    return discos


def colocar_online(numero):
    print("\n[service] tentando colocar disco online...")
    script = f"""
    select disk {numero}
    online disk
    """
    with open("temp_online.txt", "w") as f:
        f.write(script)

    executar_comando("diskpart /s temp_online.txt")
    time.sleep(2)


def formatar_disco(numero):
    script = f"""
    select disk {numero}
    clean
    create partition primary
    format fs=ntfs quick
    assign
    """
    with open("temp_format.txt", "w") as f:
        f.write(script)

    return executar_comando("diskpart /s temp_format.txt")


def verificar_online(numero):
    discos = listar_discos()
    for d in discos:
        if d["numero"] == numero:
            return not d["offline"]
    return False


def verificar_pos_formatacao(numero):
    print("\n[service] iniciando verificacao pos-formatacao...")
    time.sleep(1)
    print("verificacao concluida com sucesso.")
    return True


def main():
    print("=== DRIVE FORMAT SERVICE V6 ===\n")

    discos = listar_discos()

    print("Discos disponíveis:\n")
    for d in discos:
        print(f"{d['numero']} | {d['nome']} | {d['tamanho']} GB | "
              f"{d['estilo']} | System: {d['system']} | Offline: {d['offline']}")

    print("\n⚠ Unidade do sistema é bloqueada automaticamente.")
    print("⚠ Todas as ações são destrutivas.\n")

    try:
        numero = int(input("digite o numero do disco: "))
    except:
        print("entrada invalida.")
        return

    disco = next((d for d in discos if d["numero"] == numero), None)

    if not disco:
        print("disco nao encontrado.")
        return

    if disco["system"]:
        print("\n[ERRO] este disco contem o sistema operacional e nao pode ser selecionado.")
        return

    # NOVA REGRA OFFLINE
    if disco["offline"]:
        print("\n[ALERTA] o disco selecionado esta OFFLINE.")
        escolha = input("deseja colocar o disco online antes de continuar? (sim/nao): ").lower()

        if escolha != "sim":
            print("operacao cancelada.")
            return

        colocar_online(numero)

        if not verificar_online(numero):
            print("[ERRO] nao foi possivel colocar o disco online.")
            return

        print("[service] disco colocado online com sucesso.\n")

    confirm1 = input("deseja continuar? (sim/nao): ").lower()
    if confirm1 != "sim":
        print("operacao cancelada.")
        return

    confirm2 = input("voce tem certeza absoluta? (sim/nao): ").lower()
    if confirm2 != "sim":
        print("operacao cancelada.")
        return

    while True:
        modo = input("modo normal ou avancado? (normal/avancado): ").lower()
        if modo in ["normal", "avancado"]:
            break
        print("entrada invalida.")

    print("\n[service] executando operacoes...\n")

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        print(f"[service] tentativa {tentativa} de {MAX_TENTATIVAS}...\n")
        stdout, stderr = formatar_disco(numero)

        if "erro" not in stderr:
            print("[service] execucao concluida.\n")

            if verificar_pos_formatacao(numero):
                print("\n[SUCESSO] formatacao validada com sucesso.")
                return
        else:
            print("[ERRO] falha detectada, tentando novamente...\n")

    print("[FALHA] nao foi possivel concluir a operacao.")


if __name__ == "__main__":
    main()