import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from itertools import permutations
from Functions.Functions import *


datos = {
    "Diagrama_Ger": [],
    "Diagrama_Ra_1": [],
    "Diagrama_Ra_2": [],
    "Diagrama_Texte_1": [],
    "Diagrama_Texte_2": []
}


def guardar_datos(entries, key, ventana):
    valores = [entry.get() for entry in entries]
    concatenated_values = ' '.join(valores)

    if concatenated_values.strip():
        datos[key].append(concatenated_values.split())
        messagebox.showinfo("Guardado", "Datos guardados correctamente")
        for entry in entries:
            entry.delete(0, tk.END)
        ventana.destroy()
    else:
        messagebox.showwarning("Advertencia", "Completa al menos un campo")



def crear_ventana(coords, titulo, key):
    ventana = tk.Toplevel()
    ventana.title(titulo)
    ventana.configure(bg="#117864")

    entries = []
    for r, c in coords:
        entry = tk.Entry(ventana, width=3, bg="gray20",fg="white")
        entry.grid(row=r, column=c, padx=5, pady=5)
        entries.append(entry)

    boton_guardar = tk.Button(ventana, text="Guardar", command=lambda: guardar_datos(entries, key, ventana), bg="gray30", fg="white")
    boton_guardar.grid(row=14, column=6, columnspan=3, pady=10)



def mostrar_permutaciones():
    image1 = datos["Diagrama_Ger"]
    image2 = datos["Diagrama_Ra_1"]
    image3 = datos["Diagrama_Ra_2"]
    image4 = datos["Diagrama_Texte_1"]
    image5 = datos["Diagrama_Texte_2"]



    Ger_Ra1 = main_prime4(image1, image2)
    Ger_Ra2 = main_prime4(image1, image2)


    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de Permutaciones")
    ventana_resultados.configure(bg="#ebf5fb")

    resultados_texto = tk.Text(ventana_resultados, width=100, height=30, bg="#ebf5fb", fg="black")
    resultados_texto.pack(pady=20)

    # Ger vs Ra1
    resultados_texto.insert(tk.END, f"Permutaciones encontradas en Ger vs Ra1: {len(Ger_Ra1)}\n")
    resultados_texto.insert(tk.END, f"\n{Ger_Ra1}\n")

    #for key, value in Ger_Ra1.items():
    #    resultados_texto.insert(tk.END, f"{Ger_Ra1}")


    





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

coords_texte_1 = [
    (0, 0), (0, 2), (0, 4),(0, 6),
    (1, 1), (1, 3), (1, 5),
    (2, 2), (2, 4),
    (3, 0), (3, 1), (3, 3), (3, 5), (3, 6),
    (4, 0), (4, 1), (4, 2), (4, 4), (4, 5), (4, 6),
    (5, 0), (5, 1), (5, 3), (5, 5), (5, 6)
]

coords_texte_2 = [
    (0, 0), (0, 2), (0, 4),(0, 6),
    (1, 1), (1, 3), (1, 5),
    (2, 2), (2, 4),
    (3, 0), (3, 1), (3, 3), (3, 5), (3, 6),
    (4, 0), (4, 1), (4, 2), (4, 4), (4, 5), (4, 6),
    (5, 0), (5, 1), (5, 3), (5, 5), (5, 6)
]

ventana_principal = tk.Tk()
ventana_principal.title("App de Tuliox que nos dara money")
ventana_principal.geometry("600x750")
ventana_principal.configure(bg="#ebf5fb")

image_path = "excaliburicon.jpg"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(ventana_principal, image=photo)
image_label.place(relx=0.5, rely=0.6, anchor="center")


boton1 = tk.Button(ventana_principal, text="Diagrama Ger",command=lambda: crear_ventana(coords_1, "Diagrama Ger", "Diagrama_Ger"))
boton1.pack(pady=10)

boton2 = tk.Button(ventana_principal, text="Diagrama Ra 1",command=lambda: crear_ventana(coords_2, "Diagrama Ra 1", "Diagrama_Ra_1"))
boton2.pack(pady=10)

boton3 = tk.Button(ventana_principal, text="Diagrama Ra 2",command=lambda: crear_ventana(coords_3, "Diagrama Ra 2", "Diagrama_Ra_2"))
boton3.pack(pady=10)

boton_texte_1 = tk.Button(ventana_principal, text="Diagrama Texte 1",command=lambda: crear_ventana(coords_texte_1, "Diagrama Texte 1", "Diagrama_Texte_1"))
boton_texte_1.pack(pady=10)

boton_texte_2 = tk.Button(ventana_principal, text="Diagrama Texte 2",command=lambda: crear_ventana(coords_texte_2, "Diagrama Texte 2", "Diagrama_Texte_2"))
boton_texte_2.pack(pady=10)

boton4 = tk.Button(ventana_principal, text="Permutaciones", command=mostrar_permutaciones)
boton4.pack(pady=10)


ventana_principal.mainloop()
