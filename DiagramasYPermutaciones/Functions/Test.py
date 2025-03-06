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

# Criterios de búsqueda estándar
CRITERIOS_BUSQUEDA = [
    ["H_LR"], ["H_RL"], ["V_TD"], ["V_BU"],
    ["D_LR"], ["D_RL"], ["DI_LR"], ["DI_RL"]
]

# Criterios específicos de Código Secuencia F
PATRONES_ESPECIFICOS = [
    ["D_LR", "V_BU", "D_LR", "H_LR"],
    ["D_LR", "V_BU", "DI_LR", "V_TD"],
    ["D_LR", "V_BU", "V_BU", "H_RL"],
    ["D_LR", "H_RL", "H_RL", "DI_LR"],
    ["D_LR", "V_BU", "H_RL", "V_TD"],
    ["V_BU", "V_BU", "D_LR", "H_LR"],
    ["V_BU", "V_BU", "H_LR", "DI_RL"],
    ["V_BU", "H_RL", "V_BU", "V_BU"],
    ["V_BU", "H_LR", "H_LR", "DI_LR"],
    ["H_LR", "H_LR", "DI_LR", "D_LR"],
    ["D_LR", "D_LR", "V_BU", "H_RL"],
    ["D_LR", "D_LR", "H_LR", "V_TD"],
    ["D_LR", "D_LR", "V_BU", "H_LR"],
    ["D_LR", "D_LR", "DI_LR", "DI_RL"],
    ["D_LR", "D_LR", "H_RL", "V_BU"]
]

# Función para buscar secuencias en la matriz según patrones predefinidos
def buscar_secuencias(matriz, x, y, patrones):
    resultados = []
    for patron in patrones:
        x_actual, y_actual = x, y
        secuencia_actual = [matriz[x][y]]
        for move in patron:
            dx, dy = MOVIMIENTOS[move]
            x_actual += dx
            y_actual += dy
            if 0 <= x_actual < len(matriz) and 0 <= y_actual < len(matriz[0]):
                secuencia_actual.append(matriz[x_actual][y_actual])
            else:
                break

        if len(secuencia_actual) == len(patron) + 1:  # Ajuste para longitud 4
            resultados.append(secuencia_actual)

    return resultados

# Función para comparar imágenes de diferentes tamaños y encontrar coincidencias de longitud 4
def comparar_imagenes(imagen1, imagen2):
    coincidencias = []
    filas1, columnas1 = len(imagen1), len(imagen1[0])
    filas2, columnas2 = len(imagen2), len(imagen2[0])
    filas_min = min(filas1, filas2)
    columnas_min = min(columnas1, columnas2)

    for i in range(filas_min):
        for j in range(columnas_min):
            if imagen1[i][j] == imagen2[i][j]:
                secuencia_actual = [(i, j, imagen1[i][j])]
                for dx, dy in MOVIMIENTOS.values():
                    x_nuevo, y_nuevo = i + dx, j + dy
                    if 0 <= x_nuevo < filas_min and 0 <= y_nuevo < columnas_min:
                        if imagen1[x_nuevo][y_nuevo] == imagen2[x_nuevo][y_nuevo]:
                            secuencia_actual.append((x_nuevo, y_nuevo, imagen1[x_nuevo][y_nuevo]))
                            if len(secuencia_actual) == 4:
                                coincidencias.append(secuencia_actual)
                                break
    return coincidencias

# Función de análisis principal con validación en una tercera imagen de diferente tamaño
def analizar_imagenes(imagen1, imagen2, imagen3=None, validar_en_tercera=False):
    resultados_1_2 = comparar_imagenes(imagen1, imagen2)  # Paso 1

    if validar_en_tercera and imagen3:
        nuevos_resultados = [
            secuencia for secuencia in resultados_1_2 if all(0 <= x < len(imagen3) and 0 <= y < len(imagen3[0]) and imagen3[x][y] == valor for x, y, valor in secuencia)
        ]  # Paso 2
    else:
        nuevos_resultados = resultados_1_2

    resultados_1_3 = comparar_imagenes(imagen1, imagen3) if imagen3 else []
    resultados_2_3 = comparar_imagenes(imagen2, imagen3) if imagen3 else []

    return {
        "Imagen1-Imagen2": resultados_1_2,
        "Nuevos Resultados": nuevos_resultados,
        "Imagen1-Imagen3": resultados_1_3,
        "Imagen2-Imagen3": resultados_2_3
    }

# Integración de Código Secuencia F (búsqueda de patrones específicos)
def buscar_patrones_especificos(matriz, patrones):
    resultados = []
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            secuencias = buscar_secuencias(matriz, i, j, patrones)
            resultados.extend(secuencias)
    return resultados

# Ejemplo de uso con matrices de diferentes tamaños
imagen1 = [
    [1, 2, 3, 10],
    [4, 5, 6, 11],
    [7, 8, 9, 12]
]

imagen2 = [
    [1, 0, 3],
    [4, 5, 0],
    [0, 8, 9]
]

imagen3 = [
    [1, 2],
    [4, 0]
]

# Análisis estándar
resultados_generales = analizar_imagenes(imagen1, imagen2, imagen3, validar_en_tercera=True)

