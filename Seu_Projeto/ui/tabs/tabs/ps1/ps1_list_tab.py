"""
PS1 List Tab — PRO HYBRID (FIXED)

✔ Híbrido real (main + standalone)
✔ Herdando Frame corretamente
✔ Tema dark preservado
✔ Layout mantido
✔ Seguro para futuras integrações
✔ Colunas proporcionais
✔ Seleção de drive via dropdown (somente raiz)
"""

from __future__ import annotations

import os
import string
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class PS1ListTab(tk.Frame):
    CHECK_ON = "☑"
    CHECK_OFF = "☐"

    # =========================================================
    def __init__(self, parent, services=None):
        super().__init__(parent)

        self.parent = parent
        self.services = services

        # compatibilidade com container
        self.game_service = None
        if services:
            self.game_service = getattr(services, "games", None)

        self.source_folder = tk.StringVar()
        self.dest_drive = tk.StringVar()

        self._configure_dark_theme()
        self._build_ui()
        self.refresh_drive()

    # =========================================================
    # THEME
    # =========================================================
    def _configure_dark_theme(self):
        try:
            style = ttk.Style(self)
            style.theme_use("default")

            style.configure(
                "Treeview",
                background="#1e1e1e",
                foreground="#e6e6e6",
                fieldbackground="#1e1e1e",
                rowheight=24,
            )

            style.map(
                "Treeview",
                background=[("selected", "#094771")],
                foreground=[("selected", "#ffffff")],
            )

            style.configure(
                "Treeview.Heading",
                background="#2d2d2d",
                foreground="#ffffff",
                relief="flat",
            )
        except Exception as e:
            print("Theme warning:", e)

    # =========================================================
    # UI
    # =========================================================
    def _build_ui(self):
        self.configure(bg="#1e1e1e")

        root_frame = tk.Frame(self, bg="#1e1e1e")
        root_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title = tk.Label(
            root_frame,
            text="Lista de Jogos PS1",
            bg="#1e1e1e",
            fg="#e6e6e6",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(anchor="w", pady=(0, 8))

        panes = tk.Frame(root_frame, bg="#1e1e1e")
        panes.pack(fill="both", expand=True)

        # 🔥 colunas exatamente iguais
        for col in (0, 1, 2):
            panes.columnconfigure(col, weight=1, uniform="ps1cols")
        panes.rowconfigure(0, weight=1)

        self._build_left_panel(panes)
        self._build_middle_panel(panes)
        self._build_right_panel(panes)

    # =========================================================
    # LEFT — SOURCE
    # =========================================================
    def _build_left_panel(self, parent):
        frame = tk.LabelFrame(parent, text="Jogos na Pasta", bg="#1e1e1e", fg="#e6e6e6")
        frame.grid(row=0, column=0, sticky="nsew", padx=(8, 4))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree_source = ttk.Treeview(frame, columns=("check", "name"), show="headings")
        self.tree_source.heading("check", text="✔")
        self.tree_source.heading("name", text="Nome")
        self.tree_source.column("check", width=40, anchor="center")
        self.tree_source.column("name", width=220)

        self.tree_source.grid(row=0, column=0, sticky="nsew")
        self.tree_source.bind("<Button-1>", self._toggle_source_checkbox)

        scroll = ttk.Scrollbar(frame, command=self.tree_source.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree_source.configure(yscrollcommand=scroll.set)

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)

        tk.Button(btn_frame, text="Selecionar Origem",
                  command=self.select_folder,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Atualizar",
                  command=self.refresh_source,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Criar Lista →",
                  command=self.add_selected_to_queue,
                  bg="#0e639c", fg="white").pack(side="right", padx=2)

    # =========================================================
    # MIDDLE — QUEUE
    # =========================================================
    def _build_middle_panel(self, parent):
        frame = tk.LabelFrame(parent, text="Fila para Gravação", bg="#1e1e1e", fg="#e6e6e6")
        frame.grid(row=0, column=1, sticky="nsew", padx=4)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree_queue = ttk.Treeview(frame, columns=("check", "name"), show="headings")
        self.tree_queue.heading("check", text="✔")
        self.tree_queue.heading("name", text="Jogos Selecionados")
        self.tree_queue.column("check", width=40, anchor="center")
        self.tree_queue.column("name", width=220)

        self.tree_queue.grid(row=0, column=0, sticky="nsew")
        self.tree_queue.bind("<Button-1>", self._toggle_queue_checkbox)

        scroll = ttk.Scrollbar(frame, command=self.tree_queue.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree_queue.configure(yscrollcommand=scroll.set)

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)

        tk.Button(btn_frame, text="Remover",
                  command=self.remove_from_queue,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

    # =========================================================
    # RIGHT — DRIVE
    # =========================================================
    def _build_right_panel(self, parent):
        frame = tk.LabelFrame(parent, text="Jogos na Unidade", bg="#1e1e1e", fg="#e6e6e6")
        frame.grid(row=0, column=2, sticky="nsew", padx=(4, 8))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree_drive = ttk.Treeview(frame, columns=("check", "name"), show="headings")
        self.tree_drive.heading("check", text="✔")
        self.tree_drive.heading("name", text="Instalados")
        self.tree_drive.column("check", width=40, anchor="center")
        self.tree_drive.column("name", width=220)

        self.tree_drive.grid(row=0, column=0, sticky="nsew")
        self.tree_drive.bind("<Button-1>", self._toggle_drive_checkbox)

        scroll = ttk.Scrollbar(frame, command=self.tree_drive.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree_drive.configure(yscrollcommand=scroll.set)

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)

        # 🔥 DROPDOWN DE UNIDADES
        self.drive_combo = ttk.Combobox(btn_frame, state="readonly", width=10)
        self.drive_combo.pack(side="left", padx=2)
        self.drive_combo.bind("<<ComboboxSelected>>", self._on_drive_selected)

        self._populate_drive_list()

        tk.Button(btn_frame, text="Atualizar Unidade",
                  command=self.refresh_drive,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Remover da Unidade",
                  command=self.remove_from_drive,
                  bg="#c74e39", fg="white").pack(side="right", padx=2)

    # =========================================================
    # DRIVE LIST
    # =========================================================
    def _populate_drive_list(self):
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)

        self.drive_combo["values"] = drives

        if drives:
            self.drive_combo.current(0)
            self.dest_drive.set(drives[0])

    def _on_drive_selected(self, event=None):
        self.dest_drive.set(self.drive_combo.get())

    # =========================================================
    # CHECKBOX CORE
    # =========================================================
    def _toggle_checkbox(self, tree, event):
        if tree.identify("region", event.x, event.y) != "cell":
            return
        if tree.identify_column(event.x) != "#1":
            return

        item = tree.identify_row(event.y)
        if not item:
            return

        values = list(tree.item(item, "values"))
        values[0] = self.CHECK_ON if values[0] != self.CHECK_ON else self.CHECK_OFF
        tree.item(item, values=values)

    def _toggle_source_checkbox(self, event):
        self._toggle_checkbox(self.tree_source, event)

    def _toggle_queue_checkbox(self, event):
        self._toggle_checkbox(self.tree_queue, event)

    def _toggle_drive_checkbox(self, event):
        self._toggle_checkbox(self.tree_drive, event)

    # =========================================================
    # ACTIONS
    # =========================================================
    def select_folder(self):
        path = filedialog.askdirectory(title="Selecionar pasta de jogos PS1")
        if path:
            self.source_folder.set(path)
            self.refresh_source()

    def refresh_source(self):
        self.tree_source.delete(*self.tree_source.get_children())
        folder = self.source_folder.get()

        if not folder or not os.path.isdir(folder):
            return

        for file in os.listdir(folder):
            if file.lower().endswith((".bin", ".img", ".iso")):
                self.tree_source.insert("", "end", values=(self.CHECK_OFF, file))

    def refresh_drive(self):
        self.tree_drive.delete(*self.tree_drive.get_children())

        if not self.game_service:
            return

        try:
            jogos = self.game_service.get_all_ps1_games()
        except Exception:
            jogos = []

        for jogo in jogos:
            nome = jogo.get("nome") if isinstance(jogo, dict) else str(jogo)
            self.tree_drive.insert("", "end", values=(self.CHECK_OFF, nome))

    def add_selected_to_queue(self):
        for item in self.tree_source.get_children():
            if self.tree_source.item(item, "values")[0] == self.CHECK_ON:
                name = self.tree_source.item(item, "values")[1]
                self.tree_queue.insert("", "end", values=(self.CHECK_OFF, name))

    def remove_from_queue(self):
        for item in list(self.tree_queue.get_children()):
            if self.tree_queue.item(item, "values")[0] == self.CHECK_ON:
                self.tree_queue.delete(item)

    def remove_from_drive(self):
        for item in list(self.tree_drive.get_children()):
            if self.tree_drive.item(item, "values")[0] == self.CHECK_ON:
                self.tree_drive.delete(item)


# =============================================================
# STANDALONE
# =============================================================
def run_standalone():
    root = tk.Tk()
    root.title("PS1 List Tab — PRO")
    root.geometry("1100x600")
    PS1ListTab(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    run_standalone()