import tkinter as tk
import random

# Crear la matriz del laberinto 6x6 con algunos 1 aleatorios
def crear_matriz():
    matriz = []
    for _ in range(6):
        fila = []
        for _ in range(6):
            # Generar aleatoriamente 1 o 0
            valor = random.choice([0, 1])
            fila.append(valor)
        matriz.append(fila)
    return matriz

# Mostrar la Gui con la matriz
def mostrar_matriz(matriz, frame):
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            # Configurar el color de fondo y el contorno
            bg_color = "#add8e6"  # Azul claro
            bd_color = "#ffff00"  # Amarillo

            label = tk.Label(frame, text=str(valor), width=5, height=2, relief=tk.FLAT,
                             bg=bg_color, bd=2, borderwidth=2, highlightthickness=0)

            # Configurar el contorno del widget y dividirlo en recuadros
            label.configure(highlightbackground=bd_color, highlightcolor=bd_color)
            label.grid(row=i, column=j, padx=0.5, pady=0.5)

# Título y tamaño de la matriz
root = tk.Tk()
root.title("Laberinto")
root.geometry("500x300")

# Título "Laberinto"
titulo_label = tk.Label(root, text="Laberinto", font=("Helvetica", 16))
titulo_label.pack(pady=10)

# Frame de la matriz con color
matriz_frame = tk.Frame(root, bg="#ED804A") 
matriz_frame.pack(expand=True)

matriz_frame.grid_rowconfigure(0, weight=1)
matriz_frame.grid_columnconfigure(0, weight=1)

mi_matriz = crear_matriz()
mostrar_matriz(mi_matriz, matriz_frame)

root.mainloop()
