import numpy as np
import tkinter as tk
from tkinter import messagebox
import random
import time
import matplotlib.pyplot as plt

# Dimensiones de la matriz
filas = 6
columnas = 6

# Inicializar la matriz como una variable global
matriz = np.zeros((filas, columnas))
pos_3 = (0, 0)  # Estas se ponen en 0,0 con la única intención de que estén disponibles para que
pos_4 = (0, 0)  # la función de la generación de matriz la coloque aleatoriamente después
pos_111 = (0, 0)  # Variable para la casilla 111

etiquetas = []  # Lista para almacenar las etiquetas de la matriz
visitado = []   # Variable global para almacenar los nodos visitados

tiempos = []  # Lista para insertar todos los tiempos para encontrar la solucion

intentos = 0
max_intentos = 3

def generar_nueva_matriz():
    global matriz, pos_3, pos_4, pos_111, visitado  # Hacer matrices globales para poder modificarlas dentro de la función
    # Generar una nueva matriz aleatoria
    matriz = np.random.randint(2, size=(filas, columnas))
    # Asegurarse de que la posición (0,0) es un 0
    matriz[0, 0] = 0

    # Elegir posiciones aleatorias para colocar los valores 3 y 4
    pos_3 = (np.random.randint(1, filas), np.random.randint(1, columnas))
    pos_4 = (np.random.randint(1, filas), np.random.randint(1, columnas))

    while pos_3 == pos_4:  # Asegurarse de que las posiciones de los teletransportadores no sean iguales
        pos_4 = (np.random.randint(1, filas), np.random.randint(1, columnas))
    
    # Asegurarse de que las posiciones aleatorias no estén ocupadas por un 1
    while matriz[pos_3] == 1 or matriz[pos_4] == 1:
        pos_3 = (np.random.randint(1, filas), np.random.randint(1, columnas))
        pos_4 = (np.random.randint(1, filas), np.random.randint(1, columnas))
    
    # Colocar los valores 3 y 4 en las posiciones aleatorias
    matriz[pos_3] = 3
    matriz[pos_4] = 4

    # Elegir una posición aleatoria para colocar el valor 111
    pos_111 = (np.random.randint(1, filas), np.random.randint(1, columnas))

    # Asegurarse de que la posición aleatoria no esté ocupada por un 1, 2, 3 o 4
    while matriz[pos_111] != 0:
        pos_111 = (np.random.randint(1, filas), np.random.randint(1, columnas))

    # Colocar el valor 111 en la posición aleatoria
    matriz[pos_111] = 111

    # Colocar el número 2 en cualquier posicion, evitando la posición (0, 0)
    fila_random = random.randint(0, 5)
    columna_random = random.randint(0, 5)

    while fila_random == 0 and columna_random == 0:
        fila_random = random.randint(0, 5)
        columna_random = random.randint(0, 5)
    
    matriz[fila_random, columna_random] = 2

    # Inicializar la matriz de visitados
    visitado = [[False] * columnas for _ in range(filas)]

    # Borrar la matriz anterior de la ventana y mostrar la nueva matriz
    for fila in range(filas):
        for columna in range(columnas):
            etiquetas[fila][columna].config(text=str(matriz[fila][columna]))

def encontrar_camino(respuesta_correcta):
    global intentos
    if not respuesta_correcta:
        messagebox.showwarning("¡Atención!", "Debes responder correctamente la trivia para continuar.")
        return
    
    tiempo_inicio = time.time() # Tiempo de incio

    # Buscar el camino desde la posición (0, 0)
     # Buscar el camino desde la posición (0, 0)
    if encontrar_camino_recursivo(0, 0):
        mensaje = "Se encontró un camino hacia la salida."
        # Remplazar los valores del camino encontrado por el número 7, excepto la salida
        for fila in range(filas):
            for columna in range(columnas):
                if visitado[fila][columna] and matriz[fila][columna] != 2:
                    matriz[fila][columna] = 7
    else:
        mensaje = "No se encontró un camino hacia la salida."

    # Actualizar la ventana con la matriz modificada
    for fila in range(filas):
        for columna in range(columnas):
            etiquetas[fila][columna].config(text=str(matriz[fila][columna]))

    # Actualizar la ventana con la matriz modificada
    for fila in range(filas):
        for columna in range(columnas):
            etiquetas[fila][columna].config(text=str(matriz[fila][columna]))
    
    tiempo_fin = time.time() #Tiempo de finalizacion

    tiempo_total = tiempo_fin - tiempo_inicio # Tiempo total
    tiempos.append(tiempo_total) # Inserta los tiempos totales a la lista 
    mostrar_grafica() # Muestra la grafica de los tiempos

    # Generar mensaje si se encontró o no el camino
    mensaje_label = tk.Label(ventana, text=mensaje, font=("Arial", 12), fg="Black")
    mensaje_label.grid(row=8, column=0, columnspan=columnas, padx=5, pady=5, sticky="ew")

def trivia(respuesta_correcta):
    global intentos
    intentos += 1
    # Pregunta y opciones
    pregunta = "¿Cuál es el nombre del profesor de la clase?"
    opciones = ["a) Jorge Ernesto (correcta)", "b) Luis Ernesto", "c) Jorge Alberto"]

    # Función para comprobar la respuesta seleccionada
    def comprobar_respuesta(respuesta_seleccionada):
        if respuesta_seleccionada == "a) Jorge Ernesto (correcta)":
            messagebox.showinfo("¡Correcto!", "¡Respuesta correcta!")
            ventana_trivia.destroy()
            encontrar_camino(True)
        else:
            messagebox.showerror("¡Incorrecto!", "¡Respuesta incorrecta!")
            if intentos >= max_intentos:
                messagebox.showinfo("¡Fin del juego!", "¡Has agotado tus intentos! El juego se cerrará.")
                ventana.destroy()

    # Crear ventana de la trivia
    ventana_trivia = tk.Toplevel()
    ventana_trivia.title("Trivia")
    ventana_trivia.geometry("300x150")

    # Crear etiqueta para la pregunta
    label_pregunta = tk.Label(ventana_trivia, text=pregunta)
    label_pregunta.pack()

    # Crear botones para las opciones
    for opcion in opciones:
        boton_opcion = tk.Button(ventana_trivia, text=opcion, command=lambda resp=opcion: comprobar_respuesta(resp))
        boton_opcion.pack()

def encontrar_camino_recursivo(fila, columna):
    global visitado  # Hacer la variable visitado global

    # Marcamos la casilla actual como visitada
    visitado[fila][columna] = True

    # Si la posición actual es la salida, retornamos True
    if matriz[fila][columna] == 2:
        return True

    # Si la posición actual es un teletransportador, cambiamos la posición actual
    elif matriz[fila][columna] == 3:
        fila, columna = pos_4
    elif matriz[fila][columna] == 4:
        fila, columna = pos_3

    # Si la posición actual es la casilla "111", activamos la trivia
    elif fila == pos_111[0] and columna == pos_111[1] and matriz[fila][columna] == 111:
        trivia(True)

    # Lista de posibles movimientos: arriba, abajo, izquierda, derecha
    movimientos = [(fila - 1, columna), (fila + 1, columna), (fila, columna - 1), (fila, columna + 1)]

    # Explorar cada movimiento posible
    for nueva_fila, nueva_columna in movimientos:
        time.sleep(.001)
        # Verificar si la nueva posición está dentro de los límites de la matriz
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            # Verificar si la nueva posición no ha sido visitada y es un camino válido
            if not visitado[nueva_fila][nueva_columna] and matriz[nueva_fila][nueva_columna] != 1:
                # Llamar recursivamente a la función para explorar desde la nueva posición
                if encontrar_camino_recursivo(nueva_fila, nueva_columna):
                    return True

    # Si no se encuentra ningún camino válido desde esta posición, retroceder
    return False

def mostrar_grafica():
    plt.figure(figsize=(8,5))
    plt.plot(range(1, len(tiempos) + 1), tiempos, marker='o', color='b')
    plt.title('TIEMPOS DE EJECUCION')
    plt.xlabel('Intento')
    plt.ylabel('Tiempo (s)')
    plt.grid(True)
    plt.show()

def generar_ventana_principal():
    # Crear ventana principal
    global ventana
    ventana = tk.Tk()
    ventana.title("Act06")
    ventana.geometry("500x500")

    # Crear botón para generar una nueva matriz y buscar el resultado
    boton_generar = tk.Button(ventana, text="Generar", command=lambda: [generar_nueva_matriz(), habilitar_trivia()])
    boton_generar.grid(row=3, column=6, padx=5, pady=5)
    boton_generar = tk.Button(ventana, text="Buscar", command=lambda: [encontrar_camino(False)])
    boton_generar.grid(row=4, column=6, padx=5, pady=5)

    # Crear boton para generar el boton de la trivia
    boton_trivia = tk.Button(ventana, text= "Trivia",command=lambda: [trivia(False)])
    boton_trivia.grid(row=5, column=6, padx=5, pady=5)
    boton_trivia.config(state=tk.DISABLED)

    # Generar el titulo del programa
    titulo_label = tk.Label(ventana, text="Laberinto", font=("Arial", 16))
    titulo_label.grid(row=0, column=0, columnspan=columnas, padx=5, pady=5, sticky="ew")  # Utilizar columnspan para abarcar todas las columnas y sticky para centrar horizontalmente

    # Crear etiquetas para mostrar la matriz con color de fondo y contorno
    global etiquetas
    etiquetas = [
        [
            tk.Label(
                ventana, 
                text=str(matriz[fila][columna]), 
                bg="#add8e6", 
                width=3, 
                height=2, 
                borderwidth=15,  # Ajusta este valor según el grosor de cada recuadro de la matriz
                relief="flat",  # Tipo de relieve del borde
                highlightthickness=1,  # Grosor del contorno
                highlightbackground="#ED804A"  # Color del contorno
            ) 
            for columna in range(columnas)
        ] 
        for fila in range(filas)
    ]

    # Colocar las etiquetas en la ventana, comenzando desde la fila siguiente al título
    for fila in range(filas):
        for columna in range(columnas):
            etiquetas[fila][columna].grid(row=fila+1, column=columna, padx=0, pady=0)
    def habilitar_trivia():
        boton_trivia.config(state=tk.NORMAL)

    ventana.mainloop()

# Ejecutar la ventana principal
if __name__ == "__main__":
    generar_ventana_principal()
