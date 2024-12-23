import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EDAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise Exploratória de Dados")
        self.root.geometry("800x600")

        #Aplicando tema sv-ttk
        sv_ttk.set_theme("dark")    
        self.load_button = ttk.Button(root, text="Carregar Arquivo", command=self.load_csv)
        self.load_button.pack(pady=10)

        #Cria tabela
        self.tree = ttk.Treeview(root)
        self.tree.pack(pady=20, fill="both", expand=True)

        #Mostrar estatisticas
        self.status_button = ttk.Button(root, text="Mostrar Estatísticas", command=self.show_status)
        self.status_button.pack(pady=10)

        #Mostrar graficos
        self.plot_button = ttk.Button(root, text="Gerar Gráfico", command=self.plot_data)
        self.plot_button.pack(pady=10)
        self.df = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            self.df = pd.read_csv(file_path)
            self.display_data()

        except Exception as e:
            messagebox.showerror("Erro:", f" não foi possivel carregar o arquivo!\n {e}")

    def display_data(self):
        if self.df is not None:
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(self.df.columns)
            self.tree["show"] = "headings"

        for column in self.df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")
        
        for i in range(min(len(self.df), 10)):
            self.tree.insert('', 'end', values=list(self.df.iloc[i]))
             
    def show_status(self):
        if self.df is not None:
            status = self.df.describe()
            status_window = tk.Toplevel(self.root)
            status_window.title("Estatísticas")

            text = tk.Text(status_window, wrap="none", width=100, height=20)
            text.insert("1.0", status.to_string())
            text.pack(padx=10, pady=10)
        else:
            messagebox.showwarning("AVISO", "Arquivo CSV não carregado!")

    def plot_data(self):
        if self.df is not None:
            column_names = self.df.select_dtypes(include="number").columns.tolist()
            if not column_names :
                messagebox.showwarning("AVISO", "Não há colunas numéricas para inserir no gráfico")
                return
            
            #Matplotlib 
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Gráficos")

            fig, ax = plt.subplots()

            self.df[column_names[0]].plot(kind='hist', ax = ax, title=f"Historiograma de {column_names[0]}")
            
            canvas = FigureCanvasTkAgg(fig, plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(padx=10, pady=10)
        else:
            messagebox.showwarning("AVISO", "Arquivo CSV não carregado!")
    


if __name__ == "__main__":
    root = tk.Tk()
    app = EDAApp(root)
    root.mainloop()