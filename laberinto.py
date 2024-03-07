import numpy as np

# Dimensiones del laberinto
filas = 6
columnas = 6

# Crear matriz de ceros (0 para caminos y 1 para paredes)
laberinto = np.zeros((filas, columnas), dtype=int)

# Establecer la entrada en la posición (0,0)
laberinto[0, 0] = 0

# Establecer la salida en una posición aleatoria
salida_fila = np.random.randint(filas)
salida_columna = np.random.randint(columnas)
laberinto[salida_fila, salida_columna] = 2

# Función para explorar recursivamente el laberinto
def explorar_laberinto(laberinto, fila_inicio, columna_inicio, fila_fin, columna_fin):
    # Verificar si estamos en la salida
    if fila_inicio == fila_fin and columna_inicio == columna_fin:
        return True
    
    # Recorrer las celdas vecinas
    movimientos = [(fila_inicio - 1, columna_inicio), (fila_inicio + 1, columna_inicio),
                   (fila_inicio, columna_inicio - 1), (fila_inicio, columna_inicio + 1)]
    
    for nueva_fila, nueva_columna in movimientos:
        # Verificar si la nueva posición está dentro de los límites del laberinto
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            # Verificar si la celda vecina es un camino válido
            if laberinto[nueva_fila, nueva_columna] == 0:
                # Marcar la celda como visitada
                laberinto[nueva_fila, nueva_columna] = 3
                
                # Explorar recursivamente desde la nueva posición
                if explorar_laberinto(laberinto, nueva_fila, nueva_columna, fila_fin, columna_fin):
                    return True
    
    # Si no se encuentra ningún camino válido, retroceder
    return False

# Llamar a la función explorar_laberinto con la entrada y la salida como parámetros
if explorar_laberinto(laberinto, 0, 0, salida_fila, salida_columna):
    print("Se encontró un camino desde la entrada hasta la salida.")
else:
    print("No se encontró un camino desde la entrada hasta la salida.")

# Añadir celdas especiales (teletransporte)
teletransporte1 = (1, 1)  # Celda de teletransporte (3 lleva al 4)
teletransporte2 = (4, 4)  # Celda de teletransporte (4 lleva al 3)
teletransporte3 = (2, 3)  # Celda de teletransporte (3 lleva al 4)

laberinto[teletransporte1] = 7
laberinto[teletransporte2] = 7
laberinto[teletransporte3] = 7

print("Laberinto con celdas especiales:")
print(laberinto)
