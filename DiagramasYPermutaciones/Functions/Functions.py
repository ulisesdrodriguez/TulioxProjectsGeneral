from itertools import permutations


def get_columns(image):
    return [[row[i] for row in image] for i in range(len(image[0]))]


def get_diagonals_lr(image):
    diagonals = []
    for i in range(len(image) + len(image[0]) - 1):
        diag = []
        for j in range(max(i - len(image[0]) + 1, 0), min(i + 1, len(image))):
            diag.append(image[j][i - j])
        diagonals.append(diag)
    return diagonals


def get_diagonals_rl(image):
    diagonals = []
    for i in range(len(image) + len(image[0]) - 1):
        diag = []
        for j in range(max(i - len(image[0]) + 1, 0), min(i + 1, len(image))):
            diag.append(image[j][len(image[0]) - 1 - (i - j)])
        diagonals.append(diag)
    return diagonals


# 1. Validación de imágenes
def validate_images(image1, image2, image3):
    """
    Valida las dimensiones y estructuras de las imágenes de entrada.
    """
    assert len(image1) > 0 and len(image2) > 0 and len(image3) > 0, "Las imágenes no pueden estar vacías"
    assert all(len(row) == len(image1[0]) for row in image1), "Image1 tiene filas de longitudes diferentes"
    assert all(len(row) == len(image2[0]) for row in image2), "Image2 tiene filas de longitudes diferentes"
    assert all(len(row) == len(image3[0]) for row in image3), "Image3 tiene filas de longitudes diferentes"

def find_sequences(line, sequence_length, direction, index):
    """
    Encuentra todas las secuencias en una línea específica.
    """
    matches = []
    for i in range(len(line) - sequence_length + 1):
        matches.append((line[i:i + sequence_length], direction, index))
    return matches


# 3. Generación y búsqueda de permutaciones
def find_permutations(image1, image2):
    matches = []
    directions1 = {
        "rows": image1,
        "columns": get_columns(image1),
        "diagonals_lr": get_diagonals_lr(image1),
        "diagonals_rl": get_diagonals_rl(image1),
    }
    directions2 = {
        "rows": image2,
        "columns": get_columns(image2),
        "diagonals_lr": get_diagonals_lr(image2),
        "diagonals_rl": get_diagonals_rl(image2),
    }
    for key1, lines1 in directions1.items():
        for line1 in lines1:
            if len(line1) >= 4:
                for i in range(len(line1) - 3):
                    sequence = tuple(line1[i:i+4])
                    if None not in sequence:
                        sequence_permutations = list(permutations(sequence))
                        for key2, lines2 in directions2.items():
                            for line2 in lines2:
                                if len(line2) >= 4:
                                    for j in range(len(line2) - 3):
                                        if tuple(line2[j:j+4]) in sequence_permutations:
                                            matches.append((sequence, f"{key1} in Image1", f"{key2} in Image2"))
    return matches


# 4. Detección de patrones geométricos
def find_patterns(image, pattern):
    found_patterns = []
    rows, cols = len(image), len(image[0])
    for r in range(rows):
        for c in range(cols):
            try:
                if pattern == "L":
                    if all(image[r + i][c] is not None for i in range(3)) and image[r + 2][c + 1] is not None:
                        found_patterns.append([(r, c), (r + 1, c), (r + 2, c), (r + 2, c + 1)])
                elif pattern == "T":
                    if all(image[r][c + i] is not None for i in range(3)) and image[r + 1][c + 1] is not None:
                        found_patterns.append([(r, c), (r, c + 1), (r, c + 2), (r + 1, c + 1)])
                elif pattern == "Cuadrado":
                    if all(image[r + i][c + j] is not None for i in range(2) for j in range(2)):
                        found_patterns.append([(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)])
                elif pattern == "Rombo":
                    if image[r][c + 1] is not None and image[r + 1][c] is not None and \
                       image[r + 1][c + 2] is not None and image[r + 2][c + 1] is not None:
                        found_patterns.append([(r, c + 1), (r + 1, c), (r + 1, c + 2), (r + 2, c + 1)])
            except IndexError:
                continue
    return found_patterns


# 5. Búsqueda en zigzag
def search_zigzag(image, sequence_length=4):
    rows, cols = len(image), len(image[0])
    results = []

    # Zigzag horizontal
    for r in range(rows):
        if r % 2 == 0:  # Izquierda a derecha
            for c in range(cols - sequence_length + 1):
                sequence = tuple(image[r][c:c + sequence_length])
                if None not in sequence:
                    results.append({"sequence": sequence, "positions": [(r, c + i) for i in range(sequence_length)],
                                    "direction": "zigzag_horizontal_lr"})
        else:  # Derecha a izquierda
            for c in range(cols - 1, sequence_length - 2, -1):
                sequence = tuple(image[r][c:c - sequence_length:-1])
                if None not in sequence:
                    results.append({"sequence": sequence, "positions": [(r, c - i) for i in range(sequence_length)],
                                    "direction": "zigzag_horizontal_rl"})

    # Zigzag vertical
    for c in range(cols):
        if c % 2 == 0:  # Arriba hacia abajo
            for r in range(rows - sequence_length + 1):
                sequence = tuple(image[r + i][c] for i in range(sequence_length))
                if None not in sequence:
                    results.append({"sequence": sequence, "positions": [(r + i, c) for i in range(sequence_length)],
                                    "direction": "zigzag_vertical_td"})
        else:  # Abajo hacia arriba
            for r in range(rows - 1, sequence_length - 2, -1):
                sequence = tuple(image[r - i][c] for i in range(sequence_length))
                if None not in sequence:
                    results.append({"sequence": sequence, "positions": [(r - i, c) for i in range(sequence_length)],
                                    "direction": "zigzag_vertical_bu"})

    return results


# 6. Validación cruzada en una tercera imagen
def validate_cross_matches(matches, reference_image):
    """
    Valida las coincidencias utilizando una tercera imagen como referencia.
    """
    validated_matches = []
    for match in matches:
        sequence, direction, index = match
        if sequence_in_image(sequence, reference_image):
            validated_matches.append(match)
    return validated_matches


def sequence_in_image(sequence, image):
    """
    Verifica si una secuencia está presente en una imagen.
    """
    sequence_str = "".join(map(str, sequence))
    for row in image:
        if sequence_str in "".join(map(str, row)):
            return True
    return False

def find_permutations(image1, image2):
    matches = []
    directions1 = {
        "rows": image1,
        "columns": get_columns(image1),
        "diagonals_lr": get_diagonals_lr(image1),
        "diagonals_rl": get_diagonals_rl(image1),
    }
    directions2 = {
        "rows": image2,
        "columns": get_columns(image2),
        "diagonals_lr": get_diagonals_lr(image2),
        "diagonals_rl": get_diagonals_rl(image2),
    }
    for key1, lines1 in directions1.items():
        for line1 in lines1:
            if len(line1) >= 4:
                for i in range(len(line1) - 3):
                    sequence = tuple(line1[i:i+4])
                    if None not in sequence:
                        sequence_permutations = list(permutations(sequence))
                        for key2, lines2 in directions2.items():
                            for line2 in lines2:
                                if len(line2) >= 4:
                                    for j in range(len(line2) - 3):
                                        if tuple(line2[j:j+4]) in sequence_permutations:
                                            matches.append((sequence, f"{key1} in Image1", f"{key2} in Image2"))
    return matches





# 8. Ejecución del pipeline completo
def run_prime3_pipeline(image1, image2, image3):
    """
    Orquesta todas las funcionalidades para ejecutar el análisis completo.
    """
    validate_images(image1, image2, image3)
    geometric_patterns_L = find_patterns(image1, "L")
    geometric_patterns_T = find_patterns(image1, "T")
    geometric_patterns_Cuadrado = find_patterns(image1, "Cuadrado")
    geometric_patterns_Rombo = find_patterns(image1, "Rombo")
    zigzag_results = search_zigzag(image1)
    matches_12 = find_permutations(image1, image2)
    matches_13 = find_permutations(image1, image3)
    matches_23 = find_permutations(image2, image3)

    cross_validated_12 = validate_cross_matches(matches_12, image3)

    results = {
        "patron geometrico L\n": geometric_patterns_L,
        "patron geometrico T\n": geometric_patterns_T,
        "patron geometrico Cuadrado\n": geometric_patterns_Cuadrado,
        "patron geometrico Rombo\n": geometric_patterns_Rombo,
        "zigzag_results\n": zigzag_results,
        "matches_12\n": matches_12,
        "matches_13\n": matches_13,
        "matches_23\n": matches_23,
        "cross_validated_12\n": cross_validated_12
    }


    return results
