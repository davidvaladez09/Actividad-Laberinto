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

# Inicializar la variable de etiquetas
etiquetas = []

def generar_nueva_matriz():
    global matriz, etiquetas
    # Generar una nueva matriz aleatoria
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

    # Borrar la matriz anterior de la ventana y mostrar la nueva matriz
    for fila in range(filas):
        for columna in range(columnas):
            etiquetas[fila][columna].config(text=str(matriz[fila][columna]))

def encontrar_camino():
    # Reiniciar la matriz de visitados
    global visitado
    visitado = [[False] * columnas for _ in range(filas)]

    # Buscar el camino desde la posición (0, 0)
    if encontrar_camino_recursivo(0, 0):
        print("Se encontró un camino hacia la salida.")
        # Remplazar los valores del camino encontrado por el número 7, excepto la salida
        for fila in range(filas):
            for columna in range(columnas):
                if visitado[fila][columna] and matriz[fila][columna] != 2:
                    matriz[fila][columna] = 7
    else:
        print("No se encontró un camino hacia la salida.")

    # Actualizar la ventana con la matriz modificada
    for fila in range(filas):
        for columna in range(columnas):
            etiquetas[fila][columna].config(text=str(matriz[fila][columna]))

def encontrar_camino_recursivo(fila, columna):
    # Marcamos la casilla actual como visitada
    visitado[fila][columna] = True

    # Si la posición actual es la salida, retornamos True
    if matriz[fila][columna] == 2:
        return True

    # Lista de posibles movimientos: arriba, abajo, izquierda, derecha
    movimientos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]

    # Explorar cada movimiento posible
    for nueva_fila, nueva_columna in movimientos:
        # Verificar si la nueva posición está dentro de los límites de la matriz
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            # Verificar si la nueva posición no ha sido visitada y es un camino válido
            if not visitado[nueva_fila][nueva_columna] and matriz[nueva_fila][nueva_columna] != 1:
                # Llamar recursivamente a la función para explorar desde la nueva posición
                if encontrar_camino_recursivo(nueva_fila, nueva_columna):
                    return True

    # Si no se encuentra ningún camino válido desde esta posición, retroceder
    return False

# Crear ventana
ventana = tk.Tk()
ventana.title("Laberinto")

# Crear botón para generar una nueva matriz y buscar el resultado
boton_generar = tk.Button(ventana, text="Generar y Buscar", command=lambda: [generar_nueva_matriz(), encontrar_camino()])
boton_generar.grid(row=0, column=0, padx=5, pady=5)

# Crear etiquetas para mostrar la matriz
etiquetas = [[tk.Label(ventana, text=str(matriz[fila][columna])) for columna in range(columnas)] for fila in range(filas)]

# Colocar las etiquetas en la ventana
for fila in range(filas):
    for columna in range(columnas):
        etiquetas[fila][columna].grid(row=fila+1, column=columna, padx=5, pady=5)

ventana.mainloop()
