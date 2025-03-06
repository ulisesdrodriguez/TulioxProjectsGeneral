from itertools import permutations

# Movimientos definidos para búsqueda de secuencias
MOVIMIENTOS = {
    "H_LR": (0, 1),  # Horizontal Izquierda a Derecha
    "H_RL": (0, -1),  # Horizontal Derecha a Izquierda
    "V_TD": (1, 0),  # Vertical Arriba-Abajo
    "V_BU": (-1, 0),  # Vertical Abajo-Arriba
    "D_LR": (1, 1),  # Diagonal Izquierda-Derecha
    "D_RL": (1, -1),  # Diagonal Derecha-Izquierda
    "DI_LR": (-1, 1),  # Diagonal Invertida Izquierda-Derecha
    "DI_RL": (-1, -1)  # Diagonal Invertida Derecha-Izquierda
}


# Función para buscar secuencias en la matriz según patrones predefinidos
def buscar_secuencias(matriz, x, y, patrones):
    resultados = []
    for patron in patrones:
        x_actual, y_actual = x, y
        secuencia_actual = []

        for move in patron:
            if move not in MOVIMIENTOS:  # Validación de patrón
                continue

            dx, dy = MOVIMIENTOS[move]
            x_actual += dx
            y_actual += dy

            if 0 <= x_actual < len(matriz) and 0 <= y_actual < len(matriz[0]):
                if matriz[x_actual][y_actual] is not None:  # Evitar valores None
                    secuencia_actual.append(matriz[x_actual][y_actual])
                else:
                    break  # Si hay un None, detener la secuencia
            else:
                break  # Salir si se excede el tamaño de la matriz

        if len(secuencia_actual) == len(patron):
            resultados.append(secuencia_actual)

    return resultados


# Función para comparar imágenes y encontrar coincidencias
def comparar_imagenes(imagen1, imagen2, imagen3=None, validar_en_tercera=False):
    if not imagen1 or not imagen2:
        return []  # Return an empty list if either image is empty

    max_filas = min(len(imagen1), len(imagen2))
    max_columnas = min(len(imagen1[0]), len(imagen2[0]))

    coincidencias = []
    for i in range(max_filas):
        for j in range(max_columnas):
            if imagen1[i][j] == imagen2[i][j]:
                if validar_en_tercera and imagen3:
                    if i < len(imagen3) and j < len(imagen3[0]) and imagen1[i][j] == imagen3[i][j]:
                        coincidencias.append((i, j, imagen1[i][j]))
                else:
                    coincidencias.append((i, j, imagen1[i][j]))

    return coincidencias



# Permutaciones de secuencias
def generar_permutaciones(secuencia):
    secuencia_filtrada = [num for num in secuencia if num is not None]  # Evitar valores None
    return list(permutations(set(secuencia_filtrada)))  # Convertir a set para eliminar duplicados


# Función de análisis principal
def analizar_imagenes(imagen1, imagen2, imagen3=None, validar_en_tercera=False):
    coincidencias = comparar_imagenes(imagen1, imagen2, imagen3, validar_en_tercera)
    secuencias_encontradas = []

    for x, y, valor in coincidencias:
        secuencias = buscar_secuencias(imagen1, x, y, CRITERIOS_BUSQUEDA)
        for sec in secuencias:
            permutaciones = generar_permutaciones(sec)
            secuencias_encontradas.extend(permutaciones)

    return secuencias_encontradas


# Integración de Código Secuencia F (búsqueda de patrones específicos)
def buscar_patrones_especificos(matriz, patrones):
    resultados = []
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] is not None:  # Evitar buscar en valores None
                secuencias = buscar_secuencias(matriz, i, j, patrones)
                resultados.extend(secuencias)

    return resultados


# Criterios de búsqueda estándar
CRITERIOS_BUSQUEDA = [
    ["H_LR"], ["H_RL"], ["V_TD"], ["V_BU"],
    ["D_LR"], ["D_RL"], ["DI_LR"], ["DI_RL"]
]

# Criterios específicos de Código Secuencia F
PATRONES_ESPECIFICOS = [
    ["D_LR", "V_BU", "D_LR", "V_BU"],
    ["D_LR", "V_BU", "DI_LR", "H_LR"],
    ["D_LR", "V_BU", "V_BU", "DI_RL"],
    ["D_LR", "H_RL", "H_RL", "V_TD"],
    ["D_LR", "V_BU", "H_RL", "H_LR"],
    ["V_BU", "V_BU", "D_LR", "V_BU"],
    ["V_BU", "V_BU", "H_LR", "H_RL"],
    ["V_BU", "H_RL", "V_BU", "DI_LR"],
    ["V_BU", "H_LR", "H_LR", "DI_RL"],
    ["H_LR", "H_LR", "DI_LR", "D_RL"],
    ["D_LR", "D_LR", "V_BU", "H_RL"],
    ["D_LR", "D_LR", "H_LR", "V_BU"],
    ["D_LR", "D_LR", "V_BU", "H_LR"],
    ["D_LR", "D_LR", "DI_LR", "V_BU"],
    ["D_LR", "D_LR", "H_RL", "V_BU"]
]