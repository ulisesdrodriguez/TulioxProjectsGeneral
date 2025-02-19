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
        secuencia_actual = [matriz[x][y]]
        for move in patron:
            dx, dy = MOVIMIENTOS[move]
            x_actual += dx
            y_actual += dy
            if 0 <= x_actual < len(matriz) and 0 <= y_actual < len(matriz[0]):
                secuencia_actual.append(matriz[x_actual][y_actual])
            else:
                break

        if len(secuencia_actual) == len(patron) + 1:  # Validamos secuencias de longitud 4
            resultados.append(secuencia_actual)

    return resultados

# Función para comparar imágenes y encontrar coincidencias
def comparar_imagenes(imagen1, imagen2, imagen3=None, validar_en_tercera=False):
    coincidencias = []
    for i in range(len(imagen1)):
        for j in range(len(imagen1[0])):
            # Verificar si las coordenadas están dentro de los límites de imagen2 e imagen3
            if i < len(imagen2) and j < len(imagen2[0]) and imagen1[i][j] == imagen2[i][j]:
                if validar_en_tercera and imagen3 and i < len(imagen3) and j < len(imagen3[0]):
                    if imagen1[i][j] == imagen3[i][j]:
                        coincidencias.append((i, j, imagen1[i][j]))
                else:
                    coincidencias.append((i, j, imagen1[i][j]))
    return coincidencias

# Permutaciones de secuencias
def generar_permutaciones(secuencia):
    return list(permutations(secuencia))

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
            secuencias = buscar_secuencias(matriz, i, j, patrones)
            resultados.extend(secuencias)
    return resultados

# Criterios de búsqueda estándar
CRITERIOS_BUSQUEDA = [
    ["H_LR"], ["H_RL"], ["V_TD"], ["V_BU"],
    ["D_LR"], ["D_RL"], ["DI_LR"], ["DI_RL"]
]

# Criterios específicos de Código Secuencia F ajustados para secuencias de longitud 4
PATRONES_ESPECIFICOS = [
    ["D_LR", "V_BU", "D_LR"],  # Mismo patrón con un movimiento menos
    ["D_LR", "V_BU", "DI_LR"],
    ["D_LR", "V_BU", "V_BU"],
    ["D_LR", "H_RL", "H_RL"],
    ["D_LR", "V_BU", "H_RL"],
    ["V_BU", "V_BU", "D_LR"],
    ["V_BU", "V_BU", "H_LR"],
    ["V_BU", "H_RL", "V_BU"],
    ["V_BU", "H_LR", "H_LR"],
    ["H_LR", "H_LR", "DI_LR"],
    ["D_LR", "D_LR", "V_BU"],
    ["D_LR", "D_LR", "H_LR"],
    ["D_LR", "D_LR", "V_BU"],
    ["D_LR", "D_LR", "DI_LR"],
    ["D_LR", "D_LR", "H_RL"]
]
