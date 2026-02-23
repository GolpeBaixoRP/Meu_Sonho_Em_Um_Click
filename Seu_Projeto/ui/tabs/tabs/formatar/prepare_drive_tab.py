"""
PrepareDriveTab
VERSÃO ENTERPRISE (ULTRA PROFISSIONAL)
Mantém 100% compatibilidade híbrida e adiciona:
- Detecção USB vs HDD/SSD
- Ordenação inteligente (removíveis primeiro)
- Cores dinâmicas de uso
- Cache leve da Bridge
- Proteção reforçada da unidade do sistema
- Layout preservado
"""

import sys
import os
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

# ==================================================
# FIX UNIVERSAL DE PATH
# ==================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.services.device_service import DeviceService


class PrepareDriveTab(ctk.CTkFrame):

    CACHE_TTL = 5  # segundos

    # ==================================================
    def __init__(self, parent):
        super().__init__(parent)

        self.device_service = DeviceService()

        self.selected_drive = tk.StringVar()
        self.fs_type = tk.StringVar(value="FAT32")
        self.format_mode = tk.StringVar(value="quick")

        self._device_map = {}
        self._device_cache = None
        self._cache_time = 0

        self._build_ui()
        self.refresh_devices()

    # ==================================================
    # UI
    # ==================================================
    def _build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        root = ctk.CTkFrame(self)
        root.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # ================= TÍTULO =================
        ctk.CTkLabel(
            root,
            text="Preparar Unidade USB / HDD",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        # ================= DRIVE =================
        drive_frame = ctk.CTkFrame(root)
        drive_frame.pack(fill="x", pady=5)

        self.drive_combo = ttk.Combobox(
            drive_frame,
            textvariable=self.selected_drive,
            state="readonly",
        )
        self.drive_combo.pack(fill="x", padx=8, pady=8)
        self.drive_combo.bind("<<ComboboxSelected>>", self._on_drive_selected)

        ctk.CTkButton(
            drive_frame,
            text="Atualizar Unidades",
            command=self.refresh_devices,
        ).pack(pady=(0, 8))

        # ================= INFO =================
        info_frame = ctk.CTkFrame(root)
        info_frame.pack(fill="x", pady=5)

        self.drive_info_label = ctk.CTkLabel(
            info_frame,
            text="Selecione uma unidade...",
            justify="left",
            font=("Consolas", 12),
        )
        self.drive_info_label.pack(anchor="w", padx=8, pady=6)

        # Barra visual de uso
        self.usage_bar = ctk.CTkProgressBar(info_frame)
        self.usage_bar.pack(fill="x", padx=8, pady=(0, 8))
        self.usage_bar.set(0)

        # ================= FILESYSTEM =================
        fs_frame = ctk.CTkFrame(root)
        fs_frame.pack(fill="x", pady=5)

        for fs in ("FAT32", "NTFS", "exFAT"):
            ctk.CTkRadioButton(
                fs_frame,
                text=fs,
                value=fs,
                variable=self.fs_type,
            ).pack(anchor="w", padx=10)

        # ================= MODE =================
        mode_frame = ctk.CTkFrame(root)
        mode_frame.pack(fill="x", pady=5)

        for label, value in [
            ("Rápido", "quick"),
            ("Normal", "normal"),
            ("Avançado", "advanced"),
        ]:
            ctk.CTkRadioButton(
                mode_frame,
                text=label,
                value=value,
                variable=self.format_mode,
            ).pack(anchor="w", padx=10)

        # ================= BUTTONS =================
        btn_frame = ctk.CTkFrame(root)
        btn_frame.pack(fill="x", pady=15)

        self.format_btn = ctk.CTkButton(btn_frame, text="FORMATAR UNIDADE")
        self.format_btn.pack(fill="x", pady=4)

        ctk.CTkButton(btn_frame, text="Instalar Estrutura OPL").pack(fill="x", pady=4)
        ctk.CTkButton(btn_frame, text="Instalar POPStarter").pack(fill="x", pady=4)

    # ==================================================
    # Cache da bridge
    # ==================================================
    def _get_devices_cached(self):
        now = time.time()
        if self._device_cache and (now - self._cache_time) < self.CACHE_TTL:
            return self._device_cache

        devices = self.device_service.list_devices()
        self._device_cache = devices
        self._cache_time = now
        return devices

    # ==================================================
    # Atualizar lista
    # ==================================================
    def refresh_devices(self):

        try:
            devices = self._get_devices_cached()

            labels = []
            self._device_map.clear()

            system_drive = os.environ.get("SystemDrive", "C:").replace(":", "")

            # ordena: removíveis primeiro
            def sort_key(d):
                removable = str(d.get("removable", "")).lower() in ("true", "1")
                return (not removable, d.get("letter", ""))

            devices_sorted = sorted(devices, key=sort_key)

            for dev in devices_sorted:
                label = (
                    dev.get("letter")
                    or dev.get("drive_letter")
                    or dev.get("device")
                    or "Desconhecido"
                )

                is_system = label.upper().startswith(system_drive.upper())

                if is_system:
                    display_label = f"{label} (Sistema - BLOQUEADO)"
                else:
                    # tenta identificar USB
                    bus = str(dev.get("bus_type", "")).upper()
                    removable = str(dev.get("removable", "")).lower() in ("true", "1")

                    if "USB" in bus or removable:
                        display_label = f"{label} (USB)"
                    else:
                        display_label = label

                labels.append(display_label)
                self._device_map[display_label] = dev

            self.drive_combo["values"] = labels

            # auto seleção inteligente
            if labels and not self.selected_drive.get():
                self.selected_drive.set(labels[0])
                self._on_drive_selected()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ==================================================
    # Painel profissional
    # ==================================================
    def _on_drive_selected(self, event=None):

        label = self.selected_drive.get()
        dev = self._device_map.get(label)

        if not dev:
            return

        # ================= NORMALIZAÇÃO =================
        total = dev.get("total_bytes") or 0
        free = dev.get("free_bytes") or 0
        used = max(total - free, 0)

        filesystem = (
            dev.get("filesystem")
            or dev.get("file_system")
            or "-"
        )

        partition_style = (
            dev.get("partition_style")
            or dev.get("PartitionStyle")
            or "-"
        )

        if not filesystem or filesystem == "-":
            filesystem = "Desconhecido"

        if not partition_style or partition_style in ("-", "RAW", "Unknown"):
            partition_style = "Desconhecido"

        # ================= FUNÇÕES =================
        def gb(x):
            return f"{x / (1024**3):.2f} GB"

        usage_ratio = (used / total) if total > 0 else 0
        usage_ratio = min(max(usage_ratio, 0), 1)

        self.usage_bar.set(usage_ratio)

        # cores dinâmicas
        if usage_ratio < 0.5:
            self.usage_bar.configure(progress_color="#22c55e")  # verde
        elif usage_ratio < 0.8:
            self.usage_bar.configure(progress_color="#eab308")  # amarelo
        else:
            self.usage_bar.configure(progress_color="#ef4444")  # vermelho

        # bloqueia botão se for unidade do sistema
        if "BLOQUEADO" in label.upper():
            self.format_btn.configure(state="disabled")
        else:
            self.format_btn.configure(state="normal")

        # ================= PAINEL =================
        clean_label = label.split()[0]

        info_text = (
            f"{'Unidade:':20} {clean_label}\n"
            f"{'Sistema de Arquivos:':20} {filesystem}\n"
            f"{'Estilo de Partição:':20} {partition_style}\n"
            f"{'Espaço Total:':20} {gb(total)}\n"
            f"{'Usado:':20} {gb(used)}\n"
            f"{'Livre:':20} {gb(free)}"
        )

        self.drive_info_label.configure(text=info_text)


# ==================================================
# MODO STANDALONE
# ==================================================

def run_standalone():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Prepare Drive — Standalone")
    root.geometry("620x700")

    tab = PrepareDriveTab(root)
    tab.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    try:
        run_standalone()
    except Exception as e:
        print("FATAL:", e)
        input("Pressione ENTER para sair...")
