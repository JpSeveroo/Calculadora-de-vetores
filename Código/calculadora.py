import tkinter as tk
from tkinter import ttk, messagebox
import math

class VectorCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Vetores - Geometria Analítica")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis de controle
        self.vector_type = tk.StringVar(value="2D")
        self.operation = tk.StringVar()
        self.scalar_value = tk.StringVar()
        
        self.setup_ui()
        self.update_vector_inputs()
        self.update_operations()
    
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="CALCULADORA DE VETORES", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Seção de tipo de vetor
        type_frame = tk.LabelFrame(main_frame, text="Tipo de Vetor", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        type_frame.pack(fill='x', pady=(0, 10))
        
        tk.Radiobutton(type_frame, text="Bidimensional (2D)", variable=self.vector_type, 
                      value="2D", command=self.on_vector_type_change, 
                      font=('Arial', 10), bg='#f0f0f0').pack(side='left', padx=20, pady=10)
        
        tk.Radiobutton(type_frame, text="Tridimensional (3D)", variable=self.vector_type, 
                      value="3D", command=self.on_vector_type_change,
                      font=('Arial', 10), bg='#f0f0f0').pack(side='left', padx=20, pady=10)
        
        # Seção de entrada de vetores
        self.vectors_frame = tk.LabelFrame(main_frame, text="Coordenadas dos Vetores", 
                                          font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        self.vectors_frame.pack(fill='x', pady=(0, 10))
        
        # Seção de operações
        operation_frame = tk.LabelFrame(main_frame, text="Operação", 
                                       font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        operation_frame.pack(fill='x', pady=(0, 10))
        
        self.operation_combo = ttk.Combobox(operation_frame, textvariable=self.operation, 
                                           font=('Arial', 10), state='readonly', width=30)
        self.operation_combo.pack(pady=10)
        self.operation_combo.bind('<<ComboboxSelected>>', self.on_operation_change)
        
        # Seção de escalar (inicialmente oculta)
        self.scalar_frame = tk.LabelFrame(main_frame, text="Valor do Escalar", 
                                         font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        
        self.scalar_entry = tk.Entry(self.scalar_frame, textvariable=self.scalar_value, 
                                    font=('Arial', 10), width=15, justify='center')
        self.scalar_entry.pack(pady=10)
        
        # Botões de ação
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 10))
        
        calculate_btn = tk.Button(button_frame, text="CALCULAR", command=self.calculate,
                                 font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                 width=15, height=2, cursor='hand2')
        calculate_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="LIMPAR", command=self.clear_all,
                             font=('Arial', 12, 'bold'), bg='#f39c12', fg='white',
                             width=15, height=2, cursor='hand2')
        clear_btn.pack(side='left', padx=(0, 10))
        
        exit_btn = tk.Button(button_frame, text="SAIR", command=self.root.quit,
                            font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                            width=15, height=2, cursor='hand2')
        exit_btn.pack(side='right')
        
        # Seção de resultado
        result_frame = tk.LabelFrame(main_frame, text="Resultado", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        result_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(result_frame, font=('Courier', 11), height=8, 
                                  bg='#ecf0f1', fg='#2c3e50', wrap='word')
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar para o resultado
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.result_text.config(yscrollcommand=scrollbar.set)
    
    def on_vector_type_change(self):
        self.update_vector_inputs()
        self.update_operations()
        self.clear_result()
    
    def on_operation_change(self, event=None):
        self.update_scalar_visibility()
        self.clear_result()
    
    def update_vector_inputs(self):
        # Limpar frame de vetores
        for widget in self.vectors_frame.winfo_children():
            widget.destroy()
        
        is_3d = self.vector_type.get() == "3D"
        
        # Criar campos de entrada baseados no tipo de vetor
        self.vector_entries = {}
        
        # Vetor A
        vector_a_frame = tk.Frame(self.vectors_frame, bg='#f0f0f0')
        vector_a_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(vector_a_frame, text="Vetor A:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', width=10).pack(side='left')
        
        self.vector_entries['A'] = {}
        for coord in ['X', 'Y'] + (['Z'] if is_3d else []):
            tk.Label(vector_a_frame, text=f"{coord}:", font=('Arial', 9), 
                    bg='#f0f0f0').pack(side='left', padx=(10, 2))
            entry = tk.Entry(vector_a_frame, width=8, font=('Arial', 9), justify='center')
            entry.pack(side='left', padx=(0, 10))
            self.vector_entries['A'][coord] = entry
        
        # Vetor B
        vector_b_frame = tk.Frame(self.vectors_frame, bg='#f0f0f0')
        vector_b_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(vector_b_frame, text="Vetor B:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', width=10).pack(side='left')
        
        self.vector_entries['B'] = {}
        for coord in ['X', 'Y'] + (['Z'] if is_3d else []):
            tk.Label(vector_b_frame, text=f"{coord}:", font=('Arial', 9), 
                    bg='#f0f0f0').pack(side='left', padx=(10, 2))
            entry = tk.Entry(vector_b_frame, width=8, font=('Arial', 9), justify='center')
            entry.pack(side='left', padx=(0, 10))
            self.vector_entries['B'][coord] = entry
        
        # Vetor C (apenas para produto misto em 3D)
        self.vector_c_frame = tk.Frame(self.vectors_frame, bg='#f0f0f0')
        
        tk.Label(self.vector_c_frame, text="Vetor C:", font=('Arial', 10, 'bold'), 
                bg='#f0f0f0', width=10).pack(side='left')
        
        self.vector_entries['C'] = {}
        if is_3d:
            for coord in ['X', 'Y', 'Z']:
                tk.Label(self.vector_c_frame, text=f"{coord}:", font=('Arial', 9), 
                        bg='#f0f0f0').pack(side='left', padx=(10, 2))
                entry = tk.Entry(self.vector_c_frame, width=8, font=('Arial', 9), justify='center')
                entry.pack(side='left', padx=(0, 10))
                self.vector_entries['C'][coord] = entry
    
    def update_operations(self):
        is_3d = self.vector_type.get() == "3D"
        
        operations = [
            "Adição",
            "Subtração", 
            "Produto por Escalar",
            "Produto Interno (Escalar)"
        ]
        
        if is_3d:
            operations.extend(["Produto Vetorial", "Produto Misto"])
        
        self.operation_combo['values'] = operations
        self.operation_combo.set('')
    
    def update_scalar_visibility(self):
        if self.operation.get() == "Produto por Escalar":
            self.scalar_frame.pack(fill='x', pady=(0, 10), before=self.vectors_frame.master.winfo_children()[-3])
        else:
            self.scalar_frame.pack_forget()
        
        # Mostrar/ocultar vetor C para produto misto
        if self.operation.get() == "Produto Misto":
            self.vector_c_frame.pack(fill='x', padx=10, pady=5)
        else:
            self.vector_c_frame.pack_forget()
    
    def get_vector_values(self, vector_name):
        """Extrai e valida os valores de um vetor"""
        coords = ['X', 'Y'] + (['Z'] if self.vector_type.get() == "3D" else [])
        values = []
        
        for coord in coords:
            try:
                value = float(self.vector_entries[vector_name][coord].get())
                values.append(value)
            except ValueError:
                raise ValueError(f"Valor inválido para {vector_name}.{coord}")
        
        return values
    
    def calculate(self):
        try:
            self.clear_result()
            
            operation = self.operation.get()
            if not operation:
                raise ValueError("Selecione uma operação")
            
            # Obter vetores necessários
            if operation in ["Adição", "Subtração", "Produto Interno (Escalar)", "Produto Vetorial"]:
                v1 = self.get_vector_values('A')
                v2 = self.get_vector_values('B')
            elif operation == "Produto por Escalar":
                v1 = self.get_vector_values('A')
                try:
                    escalar = float(self.scalar_value.get())
                except ValueError:
                    raise ValueError("Digite um valor válido para o escalar")
            elif operation == "Produto Misto":
                v1 = self.get_vector_values('A')
                v2 = self.get_vector_values('B')
                v3 = self.get_vector_values('C')
            
            # Executar operação
            if operation == "Adição":
                resultado = self.somar_vetores(v1, v2)
                self.show_result(f"A + B = {resultado}")
                
            elif operation == "Subtração":
                resultado = self.subtrair_vetores(v1, v2)
                self.show_result(f"A - B = {resultado}")
                
            elif operation == "Produto por Escalar":
                resultado = self.multiplicar_por_escalar(v1, escalar)
                self.show_result(f"{escalar} × A = {resultado}")
                
            elif operation == "Produto Interno (Escalar)":
                resultado = self.produto_interno(v1, v2)
                self.show_result(f"A · B = {resultado}")
                
            elif operation == "Produto Vetorial":
                resultado = self.produto_vetorial(v1, v2)
                self.show_result(f"A × B = {resultado}")
                
            elif operation == "Produto Misto":
                resultado = self.produto_misto(v1, v2, v3)
                if resultado == 0:
                    self.show_result(f"[A, B, C] = {resultado}\n\nOs vetores são coplanares (estão no mesmo plano).")
                else:
                    self.show_result(f"[A, B, C] = {resultado}\n\nVolume do paralelepípedo: {abs(resultado)} unidades cúbicas")
        
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def show_result(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
    
    def clear_result(self):
        self.result_text.delete(1.0, tk.END)
    
    def clear_all(self):
        # Limpar todas as entradas
        for vector in self.vector_entries.values():
            for entry in vector.values():
                entry.delete(0, tk.END)
        
        self.scalar_value.set('')
        self.operation.set('')
        self.clear_result()
        self.scalar_frame.pack_forget()
        self.vector_c_frame.pack_forget()
    
    # ==================== FUNÇÕES DE OPERAÇÕES ====================
    
    def somar_vetores(self, v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]
    
    def subtrair_vetores(self, v1, v2):
        return [v1[i] - v2[i] for i in range(len(v1))]
    
    def multiplicar_por_escalar(self, v, escalar):
        return [v[i] * escalar for i in range(len(v))]
    
    def produto_interno(self, v1, v2):
        return sum(a * b for a, b in zip(v1, v2))
    
    def produto_vetorial(self, v1, v2):
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]
    
    def produto_misto(self, v1, v2, v3):
        return (
            v1[0] * (v2[1] * v3[2] - v2[2] * v3[1]) -
            v1[1] * (v2[0] * v3[2] - v2[2] * v3[0]) +
            v1[2] * (v2[0] * v3[1] - v2[1] * v3[0])
        )

def main():
    root = tk.Tk()
    app = VectorCalculatorGUI(root)
    
    # Centralizar janela na tela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()