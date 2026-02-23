"""
DeviceService
Detecção completa de dispositivos no Windows
Inclui:
- Letra
- FileSystem (FAT32 / NTFS / exFAT)
- Partition Style (MBR / GPT)
- Total
- Livre
- Usado
"""

import subprocess
import json
import platform
from typing import List, Dict


class DeviceService:

    def list_devices(self) -> List[Dict]:

        if platform.system().lower() != "windows":
            return []

        try:
            # ===============================
            # 1) VOLUMES (filesystem + espaço)
            # ===============================
            ps_volumes = """
            Get-Volume |
            Where-Object {$_.DriveLetter -ne $null} |
            Select-Object DriveLetter, FileSystem, Size, SizeRemaining |
            ConvertTo-Json
            """

            result_vol = subprocess.run(
                ["powershell", "-Command", ps_volumes],
                capture_output=True,
                text=True
            )

            volumes = json.loads(result_vol.stdout) if result_vol.stdout else []

            if isinstance(volumes, dict):
                volumes = [volumes]

            # ===============================
            # 2) DISCOS (MBR / GPT)
            # ===============================
            ps_disks = """
            Get-Disk |
            Select-Object Number, PartitionStyle |
            ConvertTo-Json
            """

            result_disk = subprocess.run(
                ["powershell", "-Command", ps_disks],
                capture_output=True,
                text=True
            )

            disks = json.loads(result_disk.stdout) if result_disk.stdout else []

            if isinstance(disks, dict):
                disks = [disks]

            disk_map = {
                disk["Number"]: disk["PartitionStyle"]
                for disk in disks
            }

            devices = []

            # ===============================
            # 3) Vincular volume → disco
            # ===============================
            for vol in volumes:

                letter = vol.get("DriveLetter")
                if not letter:
                    continue

                disk_number = self._get_disk_number(letter)
                partition_style = disk_map.get(disk_number, "-")

                total = vol.get("Size", 0)
                free = vol.get("SizeRemaining", 0)
                used = total - free if total else 0

                devices.append({
                    "letter": letter,
                    "filesystem": vol.get("FileSystem", "-"),
                    "partition_style": partition_style,
                    "total_bytes": total,
                    "free_bytes": free,
                    "used_bytes": used
                })

            return devices

        except Exception as e:
            raise RuntimeError(f"Erro ao detectar dispositivos: {e}")

    # ==================================================
    # Descobre qual disco pertence à letra
    # ==================================================
    def _get_disk_number(self, drive_letter):

        try:
            ps_cmd = f"""
            Get-Partition -DriveLetter {drive_letter} |
            Select-Object DiskNumber |
            ConvertTo-Json
            """

            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True
            )

            data = json.loads(result.stdout) if result.stdout else {}

            if isinstance(data, dict):
                return data.get("DiskNumber")

            return None

        except:
            return None