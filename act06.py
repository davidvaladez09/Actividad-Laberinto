import numpy as np

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

print("Matriz:")
print(matriz)
