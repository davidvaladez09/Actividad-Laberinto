import numpy as np
import tkinter as tk

# Dimensiones de la matriz
filas = 6
columnas = 6

# Crear matriz de ceros y unos aleatorios
matriz = np.random.randint(2, size=(filas, columnas))

# Asegurarse de que la posición (0,0) es un 0
matriz[0, 0] = 0

# Elegir una posición aleatoria para colocar el número 2
fila_aleatoria = np.random.randint(filas)
columna_aleatoria = np.random.randint(columnas)

# Asegurarse de que la posición aleatoria no esté ocupada por un 1
while matriz[fila_aleatoria, columna_aleatoria] == 1:
    fila_aleatoria = np.random.randint(filas)
    columna_aleatoria = np.random.randint(columnas)

# Colocar el número 2 en la posición aleatoria
matriz[fila_aleatoria, columna_aleatoria] = 2

# Crear ventana
ventana = tk.Tk()
ventana.title("Matriz Aleatoria")

# Crear etiquetas para mostrar la matriz
etiquetas = [[tk.Label(ventana, text=str(matriz[fila][columna])) for columna in range(columnas)] for fila in range(filas)]

# Colocar las etiquetas en la ventana
for fila in range(filas):
    for columna in range(columnas):
        etiquetas[fila][columna].grid(row=fila, column=columna, padx=5, pady=5)

ventana.mainloop()
