# ==========================================
# AUDITORIA TOTAL DO ZIP
# Meu Sonho em Um Clique PS2
# ==========================================

param (
    [string]$ZipPath = "Meu_Sonho_Em_Um_Click.zip"
)

$ExtractPath = "$env:TEMP\MeuSonho_Extract"
$OutputFile = "INVENTARIO_COMPLETO.txt"

# Limpar pasta temporária
if (Test-Path $ExtractPath) {
    Remove-Item -Recurse -Force $ExtractPath
}

New-Item -ItemType Directory -Path $ExtractPath | Out-Null

# Extrair ZIP
Expand-Archive -Path $ZipPath -DestinationPath $ExtractPath -Force

# Início do relatório
"===== INVENTÁRIO COMPLETO =====" | Out-File $OutputFile
"Data: $(Get-Date)" | Out-File $OutputFile -Append
"" | Out-File $OutputFile -Append

$counter = 1
$totalSize = 0
$fileCount = 0
$folderCount = 0

function Is-TextFile($filePath) {
    try {
        $bytes = Get-Content -Path $filePath -Encoding Byte -TotalCount 1024
        foreach ($b in $bytes) {
            if ($b -eq 0) { return $false }
        }
        return $true
    }
    catch {
        return $false
    }
}

Get-ChildItem -Recurse $ExtractPath | ForEach-Object {

    "--------------------------------------------" | Out-File $OutputFile -Append
    "ITEM $counter" | Out-File $OutputFile -Append
    "Nome: $($_.Name)" | Out-File $OutputFile -Append
    "Caminho: $($_.FullName)" | Out-File $OutputFile -Append

    if ($_.PSIsContainer) {
        "Tipo: Pasta" | Out-File $OutputFile -Append
        $folderCount++
    }
    else {
        "Tipo: Arquivo ($($_.Extension))" | Out-File $OutputFile -Append
        "Tamanho (bytes): $($_.Length)" | Out-File $OutputFile -Append
        $totalSize += $_.Length
        $fileCount++

        # Se for texto ou script, ler conteúdo
        if (Is-TextFile $_.FullName) {
            "" | Out-File $OutputFile -Append
            "---- CONTEÚDO INÍCIO ----" | Out-File $OutputFile -Append
            try {
                Get-Content $_.FullName -ErrorAction Stop | Out-File $OutputFile -Append
            }
            catch {
                "Erro ao ler conteúdo." | Out-File $OutputFile -Append
            }
            "---- CONTEÚDO FIM ----" | Out-File $OutputFile -Append
        }
        else {
            "Arquivo binário (conteúdo não exibido)." | Out-File $OutputFile -Append
        }
    }

    $counter++
}

# Estatísticas finais
"" | Out-File $OutputFile -Append
"===== ESTATÍSTICAS GERAIS =====" | Out-File $OutputFile -Append
"Total de Itens: $($counter - 1)" | Out-File $OutputFile -Append
"Total de Arquivos: $fileCount" | Out-File $OutputFile -Append
"Total de Pastas: $folderCount" | Out-File $OutputFile -Append
"Tamanho Total (bytes): $totalSize" | Out-File $OutputFile -Append
"===== FIM DO INVENTÁRIO =====" | Out-File $OutputFile -Append

Write-Host "Auditoria concluída. Arquivo gerado: $OutputFile"