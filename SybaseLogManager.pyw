import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

class LogApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sybase Log Manager")
        
        # Criação do Notebook (abas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)
        
        # Frame para a aba de Aplicação de Log
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Aplicação de Log")
        
        # Frame para a aba de Desvinculo de Log
        self.unlink_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.unlink_frame, text="Desvinculo de Log")

        # Configuração da aba de Aplicação de Log
        self.create_log_tab()
        
        # Configuração da aba de Desvinculo de Log
        self.create_unlink_tab()

    def create_log_tab(self):
        # Seleção do arquivo de banco de dados
        self.db_file_label = tk.Label(self.log_frame, text="Selecionar arquivo contabil.db:")
        self.db_file_label.pack(pady=5)
        self.db_file_entry = tk.Entry(self.log_frame, width=50)
        self.db_file_entry.pack(pady=5)
        self.db_file_button = tk.Button(self.log_frame, text="Selecionar arquivo", command=lambda: self.browse_file(self.db_file_entry, "*.db"))
        self.db_file_button.pack(pady=5)

        # Seleção do arquivo de log
        self.log_file_label = tk.Label(self.log_frame, text="Selecionar arquivo contabil.log:")
        self.log_file_label.pack(pady=5)
        self.log_file_entry = tk.Entry(self.log_frame, width=50)
        self.log_file_entry.pack(pady=5)
        self.log_file_button = tk.Button(self.log_frame, text="Selecionar arquivo", command=lambda: self.browse_file(self.log_file_entry, "*.log"))
        self.log_file_button.pack(pady=5)

        # Botão para aplicar o log
        self.apply_log_button = tk.Button(self.log_frame, text="Aplicar Log", command=self.apply_log)
        self.apply_log_button.pack(pady=10)
        
        # Label de progresso
        self.progress_label = tk.Label(self.log_frame, text="Progresso: 0%")
        self.progress_label.pack(pady=10)

    def create_unlink_tab(self):
        # Mensagem de destaque
        self.warning_label = tk.Label(self.unlink_frame, text="IMPORTANTE: Faça uma cópia do banco de dados antes de realizar o desvinculo de log!", fg="red")
        self.warning_label.pack(pady=10)

        # Seleção do arquivo de banco de dados
        self.unlink_db_file_label = tk.Label(self.unlink_frame, text="Selecionar arquivo contabil.db:")
        self.unlink_db_file_label.pack(pady=5)
        self.unlink_db_file_entry = tk.Entry(self.unlink_frame, width=50)
        self.unlink_db_file_entry.pack(pady=5)
        self.unlink_db_file_button = tk.Button(self.unlink_frame, text="Selecionar arquivo", command=lambda: self.browse_file(self.unlink_db_file_entry, "*.db"))
        self.unlink_db_file_button.pack(pady=5)

        # Botão para desvincular o log
        self.unlink_log_button = tk.Button(self.unlink_frame, text="Desvincular Log", command=self.unlink_log)
        self.unlink_log_button.pack(pady=10)
        
        # Label de progresso
        self.unlink_progress_label = tk.Label(self.unlink_frame, text="Progresso: 0%")
        self.unlink_progress_label.pack(pady=10)

    def browse_file(self, entry, filetype):
        # Função para abrir o diálogo de seleção de arquivos
        filename = filedialog.askopenfilename(filetypes=[("Database Files", filetype)])
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def apply_log(self):
        # Recupera os caminhos dos arquivos
        db_file = self.db_file_entry.get()
        log_file = self.log_file_entry.get()
        
        # Verifica se os arquivos existem
        if not os.path.exists(db_file) or not os.path.exists(log_file):
            messagebox.showerror("Erro", "Arquivo(s) não encontrado(s).")
            return

        # Verifica se os arquivos têm as extensões corretas
        if not db_file.endswith(".db") or not log_file.endswith(".log"):
            messagebox.showerror("Erro", "Selecione os arquivos corretos.")
            return
        
        try:
            # Construir o comando de forma robusta
            command = ["dbeng17", db_file, "-a", log_file]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Verifica o resultado do comando
            if process.returncode == 0:
                self.progress_label.config(text="Progresso: 100%")
                messagebox.showinfo("Sucesso", "Log aplicado com sucesso.")
            else:
                self.progress_label.config(text="Progresso: 0%")
                messagebox.showerror("Erro", f"Erro ao aplicar o log: {stderr.decode()}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar o log: {str(e)}")

    def unlink_log(self):
        # Recupera o caminho do arquivo de banco de dados
        db_file = self.unlink_db_file_entry.get()
        
        # Verifica se o arquivo existe
        if not os.path.exists(db_file):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            return

        # Verifica se o arquivo tem a extensão correta
        if not db_file.endswith(".db"):
            messagebox.showerror("Erro", "Selecione o arquivo correto.")
            return
        
        try:
            # Construir o comando de forma robusta
            command = ["dbeng17", db_file, "-f", "-o", "logininicializacao.txt"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Verifica o resultado do comando
            if process.returncode == 0:
                self.unlink_progress_label.config(text="Progresso: 100%")
                messagebox.showinfo("Sucesso", "Log desvinculado com sucesso.")
            else:
                self.unlink_progress_label.config(text="Progresso: 0%")
                messagebox.showerror("Erro", f"Erro ao desvincular o log: {stderr.decode()}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao desvincular o log: {str(e)}")

if __name__ == "__main__":
    app = LogApplication()
    app.mainloop()