import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from itertools import permutations
from Functions.Functions import *

# Lista global para almacenar los datos
datos = {
    "Diagrama_Ger": [],
    "Diagrama_Ra_1": [],
    "Diagrama_Ra_2": []
}


# Función para guardar datos en la lista
def guardar_datos(entries, key):
    valores = [entry.get() for entry in entries]
    concatenated_values = ' '.join(valores)

    if concatenated_values.strip():  # Asegurarse de que no esté vacío
        datos[key].append(concatenated_values.split())  # Guardar como lista de listas
        messagebox.showinfo("Guardado", "Datos guardados correctamente")
        for entry in entries:
            entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa al menos un campo")


# Función para crear una ventana con el formulario
def crear_ventana(coords, titulo, key):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.configure(bg="#117864")  # Cambiar el color de fondo de la ventana secundaria al color RGB especificado

    entries = []
    for r, c in coords:
        entry = tk.Entry(ventana, width=3, bg="gray20",
                         fg="white")  # Cambiar el fondo de las entradas a gris oscuro y el texto a blanco
        entry.grid(row=r, column=c, padx=5, pady=5)
        entries.append(entry)

    boton_guardar = tk.Button(ventana, text="Guardar", command=lambda: guardar_datos(entries, key), bg="gray30",
                              fg="white")  # Cambiar el fondo del botón a gris oscuro y el texto a blanco
    boton_guardar.grid(row=14, column=6, columnspan=3, pady=10)


# Función para mostrar permutaciones comunes
def mostrar_permutaciones():
    # Obtener los datos guardados como imágenes
    image1 = datos["Diagrama_Ger"]
    image2 = datos["Diagrama_Ra_1"]
    image3 = datos["Diagrama_Ra_2"]

    # Buscar permutaciones y coincidencias
    matches1_2 = find_permutations(image1, image2)
    results1_2_3 = find_matches_in_third_image(matches1_2, image3)

    # Crear una ventana para mostrar los resultados
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de Permutaciones")
    ventana_resultados.configure(bg="#ebf5fb")

    # Mostrar los resultados en la ventana
    resultados_texto = tk.Text(ventana_resultados, width=100, height=30, bg="#ebf5fb", fg="black")
    resultados_texto.pack(pady=20)

    # Mostrar los resultados de Image1 y Image2 encontrados en Image3
    resultados_texto.insert(tk.END, f"Permutaciones encontradas Ger vs Ra1: {len(matches1_2)}\n")
    resultados_texto.insert(tk.END, f": {matches1_2}\n")
    resultados_texto.insert(tk.END, f"Permutaciones encontradas en  Ger vs Ra1 y Ra2: {len(results1_2_3)}\n")
    resultados_texto.insert(tk.END, f": {results1_2_3}\n")

    for result1 in matches1_2:
        resultados_texto.insert(tk.END, f"Sequence {result1[0]} found in {result1[1]}, {result1[2]} and {result1[3]}\n")

    for result in results1_2_3:
        resultados_texto.insert(tk.END, f"Sequence {result[0]} found in {result[1]}, {result[2]} and {result[3]}\n")




# Coordenadas del primer formulario en forma de rombo
coords_1 = [
    (1, 6),
    (2, 6),
    (3, 5), (3, 7),
    (4, 4), (4, 6), (4, 8),
    (5, 3), (5, 4), (5, 6), (5, 8), (5, 9),
    (6, 2), (6, 10),
    (7, 0), (7, 1), (7, 3), (7, 4),    (7, 6),   (7, 8), (7, 9), (7, 11), (7, 12),
    (8, 2), (8, 10),
    (9, 3), (9, 4), (9, 6), (9, 8), (9, 9),
    (10, 4), (10, 6), (10, 8),
    (11, 5), (11, 7),
    (12, 6),
    (13, 6),


]

# Coordenadas del segundo formulario (modificadas)
coords_2 = [
    (0, 3), (0, 6), (0, 9),
    (2, 6),
    (3, 3), (3, 5), (3, 7), (3, 9),
    (4, 3), (4, 9),
    (6, 6),
    (7, 5), (7, 7),
    (8, 4), (8, 6), (8, 8),
    (9, 3), (9, 5), (9, 7), (9, 9),
    (10, 2), (10, 4), (10, 6), (10, 8), (10, 10),
    (11, 1), (11, 3), (11, 5), (11, 7), (11, 9), (11, 11)
]

# Coordenadas del tercer formulario (modificadas)
coords_3 = [
    (0, 3), (0, 6), (0, 9),
    (2, 6),
    (3, 3), (3, 5), (3, 7), (3, 9),
    (4, 3), (4, 9),
    (6, 6),
    (7, 5), (7, 7),
    (8, 4), (8, 6), (8, 8),
    (9, 3), (9, 5), (9, 7), (9, 9),
    (10, 2), (10, 4), (10, 6), (10, 8), (10, 10),
    (11, 1), (11, 3), (11, 5), (11, 7), (11, 9), (11, 11)
]

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("App de Tuliox que nos dara money")
ventana_principal.geometry("600x750")  # Cambia el tamaño según tus necesidades
ventana_principal.configure(bg="#ebf5fb")  # Cambiar el color de fondo de la ventana principal al color RGB especificado

image_path = "excaliburicon.jpg"  # Cambia esto a la ruta de tu imagen
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)  # Crear un widget Label para la imagen
image_label = tk.Label(ventana_principal, image=photo)
image_label.place(relx=0.5, rely=0.5, anchor="center")

# Botones para abrir las otras ventanas
boton1 = tk.Button(ventana_principal, text="Diagrama Ger",
                   command=lambda: crear_ventana(coords_1, "Diagrama Ger", "Diagrama_Ger"))
boton1.pack(pady=10)

boton2 = tk.Button(ventana_principal, text="Diagrama Ra 1",
                   command=lambda: crear_ventana(coords_2, "Diagrama Ra 1", "Diagrama_Ra_1"))
boton2.pack(pady=10)

boton3 = tk.Button(ventana_principal, text="Diagrama Ra 2",
                   command=lambda: crear_ventana(coords_3, "Diagrama Ra 2", "Diagrama_Ra_2"))
boton3.pack(pady=10)

boton4 = tk.Button(ventana_principal, text="Permutaciones", command=mostrar_permutaciones)
boton4.pack(pady=10)

# Iniciar el bucle de la interfaz gráfica
ventana_principal.mainloop()
