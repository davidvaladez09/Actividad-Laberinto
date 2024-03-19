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

# Definicion de la matriz para aplicar programacion dinamica
dp = np.full((filas, columnas), None)

def restaurar_colores():
    # Restaurar los colores de las casillas especiales
    for fila in range(filas):
        for columna in range(columnas):
            if matriz[fila][columna] == 2:
                etiquetas[fila][columna].config(text="", bg="#FF4646")  # Ocultar texto y cambiar color para las celdas con "2"
            elif matriz[fila][columna] == 1:
                etiquetas[fila][columna].config(text="", bg="#59545D")  # Ocultar texto y cambiar color para las celdas con "1"
            elif matriz[fila][columna] == 3:
                etiquetas[fila][columna].config(bg="#53B9F7")  # Restaurar color de fondo para las celdas con "3"
            elif matriz[fila][columna] == 4:
                etiquetas[fila][columna].config(text="", bg="#2374FA")  # Ocultar texto y cambiar color para las celdas con "4"
            elif matriz[fila][columna] == 111:
                etiquetas[fila][columna].config(text="", bg="#23FA3D")  # Ocultar texto y cambiar color para las celdas con "111"
            else:
                etiquetas[fila][columna].config(bg="#add8e6", text=str(matriz[fila][columna]))  # Restaurar color de fondo y texto para las demás celdas


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
            if matriz[fila][columna] == 1:
                etiquetas[fila][columna].config(text="", bg="#59545D")  # Ocultar texto y cambiar color para las celdas con "1"
            elif matriz[fila][columna] == 2:
                etiquetas[fila][columna].config(text="", bg="#FF4646")  # Ocultar texto y cambiar color para las celdas con "2"
            elif matriz[fila][columna] == 3:
                etiquetas[fila][columna].config(text="", bg="#53B9F7")  # Ocultar texto y cambiar color para las celdas con "3"
            elif matriz[fila][columna] == 4:
                etiquetas[fila][columna].config(text="", bg="#2374FA")  # Ocultar texto y cambiar color para las celdas con "4"
            elif matriz[fila][columna] == 111:
                etiquetas[fila][columna].config(text="", bg="#23FA3D")  # Ocultar texto y cambiar color para las celdas con "111"
            else:
                etiquetas[fila][columna].config(text="")

    restaurar_colores()

def eliminar_pared_obstaculo():
    global matriz, etiquetas
    # Encontrar una casilla de pared para eliminar
    fila_pared, columna_pared = -1, -1
    for fila in range(filas):
        for columna in range(columnas):
            if matriz[fila][columna] == 1:
                fila_pared, columna_pared = fila, columna
                break
        if fila_pared != -1:
            break
    
    if fila_pared != -1:
        # Marcar la casilla de la pared como libre en la matriz
        matriz[fila_pared][columna_pared] = 0  # Cambia el valor de la pared a libre en la matriz
        # Marcar la casilla de la pared como blanca en la interfaz gráfica
        etiquetas[fila_pared][columna_pared].config(bg="#FFFFFF")
        print("Se eliminó una pared en la posición:", (fila_pared, columna_pared))
        
        # Buscar camino nuevamente y marcarlo con "7"
        for fila in range(filas):
            for columna in range(columnas):
                visitado[fila][columna] = False  # Restaurar matriz de visitados antes de buscar camino
        if encontrar_camino_recursivo(0, 0, False):  # Encuentra el nuevo camino
            for fila in range(filas):
                for columna in range(columnas):
                    if visitado[fila][columna] and matriz[fila][columna] != 2:
                        matriz[fila][columna] = 7  # Marcar el camino con "7"
        return True
    else:
        print("No se encontraron paredes para eliminar.")
        return False

def encontrar_camino(respuesta_correcta):
    global intentos
    if not respuesta_correcta and intentos > 0:  
        messagebox.showwarning("¡Atención!", "Debes responder correctamente la trivia para continuar.")
        return
    
    tiempo_inicio = time.time() 

    encontrada_casilla_111 = False  

    # Buscar el camino desde la posición (0, 0)
    if encontrar_camino_recursivo(0, 0, encontrada_casilla_111):
        mensaje = "Se encontró un camino hacia la salida."
        # Remplazar los valores del camino encontrado por el número 7, excepto la salida
        for fila in range(filas):
            for columna in range(columnas):
                if visitado[fila][columna] and matriz[fila][columna] != 2:
                    matriz[fila][columna] = 7
    else:
        mensaje = "No se encontró un camino hacia la salida. Intentando eliminar una pared."

        # Intentar eliminar una pared obstáculo
        if eliminar_pared_obstaculo():
            # Volver a buscar el camino
            if encontrar_camino_recursivo(0, 0, encontrada_casilla_111):
                mensaje = "Se encontró un camino hacia la salida después de eliminar una pared."
            else:
                mensaje = "No se encontró un camino hacia la salida después de intentar eliminar una pared."
        else:
            mensaje = "No se encontró una pared para eliminar."

    # Mostrar la trivia si se encontró la casilla 111 durante la búsqueda del camino
    if encontrada_casilla_111:
        trivia(True)  # Mostrar trivia

    # Actualizar la ventana con la matriz modificada
    for fila in range(filas):
        for columna in range(columnas):
            if matriz[fila][columna] == 1:
                etiquetas[fila][columna].config(text="", bg="#59545D")  
            elif matriz[fila][columna] == 2:
                etiquetas[fila][columna].config(text="", bg="#FF4646")  
            elif matriz[fila][columna] == 3:
                etiquetas[fila][columna].config(text="", bg="#53B9F7")  
            elif matriz[fila][columna] == 4:
                etiquetas[fila][columna].config(text="", bg="#2374FA")  
            elif matriz[fila][columna] == 111:
                etiquetas[fila][columna].config(text="", bg="#23FA3D")  
            else:
                etiquetas[fila][columna].config(text=str(matriz[fila][columna]))
    
    tiempo_fin = time.time() 
    tiempo_total = tiempo_fin - tiempo_inicio 
    tiempos.append(tiempo_total) 
    mostrar_grafica() 

    # Generar mensaje si se encontró o no el camino
    mensaje_label = tk.Label(ventana, text=mensaje, font=("Arial", 12), fg="black")
    mensaje_label.grid(row=8, column=0, columnspan=columnas, padx=5, pady=5, sticky="ew")

def trivia(respuesta_correcta):
    global intentos
    intentos += 1
    # Pregunta y opciones
    pregunta = "¿Cuál es el nombre del profesor de la clase?"
    opciones = ["a) Jorge Ernesto", "b) Luis Ernesto", "c) Jorge Alberto"]

    # Función para comprobar la respuesta seleccionada
    def comprobar_respuesta(respuesta_seleccionada):
        global intentos  # No necesitas 'nonlocal' aquí
        if respuesta_seleccionada == "a) Jorge Ernesto":
            messagebox.showinfo("¡Correcto!", "¡Respuesta correcta!")
            ventana_trivia.destroy()
            # Llamar a encontrar_camino con respuesta_correcta=True para continuar la búsqueda del camino
            encontrar_camino(True)
        else:
            if intentos < max_intentos:
                messagebox.showerror("¡Incorrecto!", "¡Respuesta incorrecta! Inténtalo de nuevo.")
                intentos += 1
            else:
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
        
def encontrar_camino_recursivo(fila, columna, encontrada_casilla_111):
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

    # IMPLEMENTACION PROGRAMACION DINAMICA 
    # Si ya se calculo el resultado de esta posicion se devuelve
    if dp[fila][columna] is not None:
        return dp[fila][columna]

    # Explorar cada movimiento posible
    for nueva_fila, nueva_columna in movimientos:
        time.sleep(.001)
        # Verificar si la nueva posición está dentro de los límites de la matriz
        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            # Verificar si la nueva posición no ha sido visitada y es un camino válido
            if not visitado[nueva_fila][nueva_columna] and matriz[nueva_fila][nueva_columna] != 1:
                # Llamar recursivamente a la función para explorar desde la nueva posición
                if encontrar_camino_recursivo(nueva_fila, nueva_columna, encontrada_casilla_111):
                    # Se guarda el resultado en la matriz para guardar en memoria
                    dp[fila][columna] = True
                    return True

    # Si no se encuentra ningún camino válido desde esta posición, retroceder
    dp[fila][columna] = False
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
    ventana.geometry("700x700")

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
                highlightbackground="#59545D"  # Color del contorno
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
