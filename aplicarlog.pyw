import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class LogApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicação de Log")
        
        # File selection
        self.create_file_selection()
        
        # Apply log button
        self.apply_log_button = tk.Button(self, text="Aplicar Log", command=self.apply_log)
        self.apply_log_button.pack(pady=10)
        
        # Progress
        self.progress_label = tk.Label(self, text="Progresso: 0%")
        self.progress_label.pack(pady=10)

    def create_file_selection(self):
        self.db_file_label = tk.Label(self, text="Selecionar arquivo contabil.db:")
        self.db_file_label.pack(pady=5)
        self.db_file_entry = tk.Entry(self, width=50)
        self.db_file_entry.pack(pady=5)
        self.db_file_button = tk.Button(self, text="Selecionar arquivo", command=lambda: self.browse_file(self.db_file_entry, "*.db"))
        self.db_file_button.pack(pady=5)

        self.log_file_label = tk.Label(self, text="Selecionar arquivo contabil.log:")
        self.log_file_label.pack(pady=5)
        self.log_file_entry = tk.Entry(self, width=50)
        self.log_file_entry.pack(pady=5)
        self.log_file_button = tk.Button(self, text="Selecionar arquivo", command=lambda: self.browse_file(self.log_file_entry, "*.log"))
        self.log_file_button.pack(pady=5)

    def browse_file(self, entry, filetype):
        filename = filedialog.askopenfilename(filetypes=[("Database Files", filetype)])
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def apply_log(self):
        db_file = self.db_file_entry.get()
        log_file = self.log_file_entry.get()
        
        if not os.path.exists(db_file) or not os.path.exists(log_file):
            messagebox.showerror("Erro", "Arquivo(s) não encontrado(s).")
            return

        if not db_file.endswith(".db") or not log_file.endswith(".log"):
            messagebox.showerror("Erro", "Selecione os arquivos corretos.")
            return
        
        try:
            # Construir o comando de forma robusta
            command = ["dbeng17", db_file, "-a", log_file]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.progress_label.config(text="Progresso: 100%")
                messagebox.showinfo("Sucesso", "Log aplicado com sucesso.")
            else:
                self.progress_label.config(text="Progresso: 0%")
                messagebox.showerror("Erro", f"Erro ao aplicar o log: {stderr.decode()}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar o log: {str(e)}")

if __name__ == "__main__":
    app = LogApplication()
    app.mainloop()