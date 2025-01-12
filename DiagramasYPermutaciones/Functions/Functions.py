from itertools import permutations

# 1. Validación de imágenes
def validate_images(image1, image2, image3):
    """
    Valida las dimensiones y estructuras de las imágenes de entrada.
    """
    assert len(image1) > 0 and len(image2) > 0 and len(image3) > 0, "Las imágenes no pueden estar vacías"
    assert all(len(row) == len(image1[0]) for row in image1), "Image1 tiene filas de longitudes diferentes"
    assert all(len(row) == len(image2[0]) for row in image2), "Image2 tiene filas de longitudes diferentes"
    assert all(len(row) == len(image3[0]) for row in image3), "Image3 tiene filas de longitudes diferentes"

# 2. Búsqueda por criterios
def search_by_criteria(image, sequence_length=4, criteria=[]):
    """
    Realiza búsquedas específicas en la imagen basándose en criterios definidos (e.g., horizontal, vertical, diagonal).
    """
    matches = []
    rows, cols = len(image), len(image[0])

    for crit in criteria:
        if crit == "horizontal":
            for r in range(rows):
                row_str = "".join(map(str, image[r]))
                matches.extend(find_sequences(row_str, sequence_length, "horizontal", r))

        elif crit == "vertical":
            for c in range(cols):
                col_str = "".join(map(str, [image[r][c] for r in range(rows)]))
                matches.extend(find_sequences(col_str, sequence_length, "vertical", c))

        elif crit == "diagonal_main":
            for offset in range(-rows + 1, cols):
                diag_str = "".join(map(str, [image[r][r + offset] for r in range(rows) if 0 <= r + offset < cols]))
                matches.extend(find_sequences(diag_str, sequence_length, "diagonal_main", offset))

        elif crit == "diagonal_secondary":
            for offset in range(-rows + 1, cols):
                diag_str = "".join(map(str, [image[r][cols - r - 1 - offset] for r in range(rows) if 0 <= cols - r - 1 - offset < cols]))
                matches.extend(find_sequences(diag_str, sequence_length, "diagonal_secondary", offset))

    return matches

def find_sequences(line, sequence_length, direction, index):
    """
    Encuentra todas las secuencias en una línea específica.
    """
    matches = []
    for i in range(len(line) - sequence_length + 1):
        matches.append((line[i:i + sequence_length], direction, index))
    return matches

# 3. Generación y búsqueda de permutaciones
def find_permutations(sequence, image):
    """
    Genera permutaciones de una secuencia y busca su presencia en la imagen.
    """
    rows, cols = len(image), len(image[0])
    perms = list(permutations(sequence))
    matches = []

    for perm in perms:
        perm_str = "".join(map(str, perm))

        # Búsqueda horizontal
        for r in range(rows):
            row_str = "".join(map(str, image[r]))
            if perm_str in row_str:
                matches.append((perm, "horizontal", r))

        # Búsqueda vertical
        for c in range(cols):
            col_str = "".join(map(str, [image[r][c] for r in range(rows)]))
            if perm_str in col_str:
                matches.append((perm, "vertical", c))

    return matches

# 4. Detección de patrones geométricos
def detect_geometric_patterns(image):
    """
    Detecta patrones geométricos en la imagen (L, T, cuadrados, rombos).
    """
    patterns = []
    # Implementar lógica específica para detectar cada patrón.
    return patterns

# 5. Búsqueda en zigzag
def zigzag_search(image):
    """
    Realiza búsquedas en patrones de zigzag en la imagen.
    """
    zigzag_matches = []
    # Implementar lógica para buscar en zigzag.
    return zigzag_matches

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

# 7. Búsqueda de coincidencias directas entre imágenes
def find_matches(image1, image2):
    """
    Encuentra coincidencias directas entre dos imágenes.
    """
    matches = []
    for r1, row1 in enumerate(image1):
        for r2, row2 in enumerate(image2):
            if row1 == row2:
                matches.append((r1, r2))
    return matches

# 8. Ejecución del pipeline completo
def run_prime3_pipeline(image1, image2, image3):
    """
    Orquesta todas las funcionalidades para ejecutar el análisis completo.
    """
    validate_images(image1, image2, image3)
    geometric_patterns = detect_geometric_patterns(image1)
    zigzag_results = zigzag_search(image1)
    matches_12 = find_matches(image1, image2)
    matches_13 = find_matches(image1, image3)
    matches_23 = find_matches(image2, image3)

    cross_validated_12 = validate_cross_matches(matches_12, image3)

    results = {
        "geometric_patterns": geometric_patterns,
        "zigzag_results": zigzag_results,
        "matches_12": matches_12,
        "matches_13": matches_13,
        "matches_23": matches_23,
        "cross_validated_12": cross_validated_12,
    }
    return results