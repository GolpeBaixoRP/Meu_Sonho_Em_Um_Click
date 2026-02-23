import customtkinter as ctk


class PS2WriteTab(ctk.CTkFrame):

    def __init__(self, parent, services=None):
        super().__init__(parent)

        # 🔹 ponteiro híbrido (mesmo que não use ainda)
        self.services = services

        # ================= GRID PRINCIPAL =================
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # ================= ESQUERDA - Banco =================
        self.db_list = ctk.CTkTextbox(self)
        self.db_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # ================= CENTRO - Logs =================
        self.log_box = ctk.CTkTextbox(self, width=250)
        self.log_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # ================= DIREITA - USB =================
        self.usb_list = ctk.CTkTextbox(self)
        self.usb_list.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # ================= PROGRESSO POR ISO =================
        self.progress_iso = ctk.CTkProgressBar(self, height=22)
        self.progress_iso.set(0)
        self.progress_iso.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=20,
            pady=(5, 5),
            sticky="ew"
        )

        # ================= PROGRESSO TOTAL =================
        self.progress_total = ctk.CTkProgressBar(self, height=22)
        self.progress_total.set(0)
        self.progress_total.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=20,
            pady=(0, 10),
            sticky="ew"
        )

        # ================= BOTÃO =================
        self.start_button = ctk.CTkButton(
            self,
            text="INICIAR GRAVAÇÃO",
            command=self.start_write
        )
        self.start_button.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=20,
            pady=(0, 20),
            sticky="ew"
        )

    # =====================================================
    def start_write(self):
        self.log_box.insert("end", "Iniciando gravaação...\n")
        self.log_box.see("end")


# ========================================================
# 🔹 STANDALONE BLINDADO
# ========================================================
def run_standalone():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1000x600")
    root.title("PS2 Write - Standalone")

    tab = PS2WriteTab(root)
    tab.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    try:
        run_standalone()
    except Exception as e:
        print("FATAL:", e)
        input("Pressione ENTER para sair...")