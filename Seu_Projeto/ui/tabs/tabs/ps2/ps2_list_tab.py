import customtkinter as ctk
from tkinter import filedialog


class PS2ListTab(ctk.CTkFrame):

    def __init__(self, parent, services=None):
        super().__init__(parent)

        self.services = services
        self.destino_path = None

        # ================= GRID =================
        # 🔥 força as 3 colunas a terem exatamente o mesmo tamanho
        for col in (0, 1, 2):
            self.grid_columnconfigure(col, weight=1, uniform="ps2cols")
        self.grid_rowconfigure(1, weight=1)

        # ================= TÍTULO =================
        self.title_label = ctk.CTkLabel(
            self,
            text="Lista de Jogos PS2",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

        # =========================================================
        # 🔹 ESTILO DARK PADRÃO
        # =========================================================
        textbox_style = {
            "fg_color": "#1a1a1a",
            "text_color": "white",
            "border_color": "#333333"
        }

        # ================= ESQUERDA =================
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.left_frame, text="Jogos na Pasta").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.folder_list = ctk.CTkTextbox(self.left_frame, **textbox_style)
        self.folder_list.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.left_buttons = ctk.CTkFrame(self.left_frame)
        self.left_buttons.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.left_buttons.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            self.left_buttons,
            text="Selecionar Origem",
            command=self.select_source
        ).grid(row=0, column=0, padx=3, pady=3, sticky="ew")

        ctk.CTkButton(
            self.left_buttons,
            text="Atualizar"
        ).grid(row=0, column=1, padx=3, pady=3, sticky="ew")

        ctk.CTkButton(
            self.left_buttons,
            text="Criar Lista →"
        ).grid(row=0, column=2, padx=3, pady=3, sticky="ew")

        # ================= CENTRO =================
        self.mid_frame = ctk.CTkFrame(self)
        self.mid_frame.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
        self.mid_frame.grid_rowconfigure(1, weight=1)
        self.mid_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.mid_frame, text="Fila para Gravação").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.queue_list = ctk.CTkTextbox(self.mid_frame, **textbox_style)
        self.queue_list.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ctk.CTkButton(
            self.mid_frame,
            text="Remover"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # ================= DIREITA =================
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=1, column=2, padx=(5, 10), pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.right_frame, text="Jogos na Unidade").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.installed_list = ctk.CTkTextbox(self.right_frame, **textbox_style)
        self.installed_list.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.right_buttons = ctk.CTkFrame(self.right_frame)
        self.right_buttons.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.right_buttons.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            self.right_buttons,
            text="Selecionar Destino",
            command=self.select_destination
        ).grid(row=0, column=0, padx=3, pady=3, sticky="ew")

        ctk.CTkButton(
            self.right_buttons,
            text="Atualizar Unidade"
        ).grid(row=0, column=1, padx=3, pady=3, sticky="ew")

        ctk.CTkButton(
            self.right_buttons,
            text="Remover da Unidade",
            fg_color="#c0392b",
            hover_color="#e74c3c"
        ).grid(row=0, column=2, padx=3, pady=3, sticky="ew")

    # =====================================================
    # 🔹 AÇÕES
    # =====================================================
    def select_source(self):
        path = filedialog.askdirectory(title="Selecionar Pasta de Origem")
        if path:
            self.folder_list.insert("end", f"Origem: {path}\n")
            self.folder_list.see("end")

    def select_destination(self):
        path = filedialog.askdirectory(title="Selecionar Pasta de Destino")
        if path:
            self.destino_path = path
            self.installed_list.insert("end", f"Destino: {path}\n")
            self.installed_list.see("end")


# ========================================================
# 🔹 STANDALONE
# ========================================================
def run_standalone():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1200x700")
    root.title("PS2 List - Standalone")

    tab = PS2ListTab(root)
    tab.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    run_standalone()