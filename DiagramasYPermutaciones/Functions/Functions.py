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

# Patrones en forma de L, T, Cuadrado, y Rombo
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

# Contar secuencias repetidas en una imagen
def count_repeated_sequences(image):
    counts = {}
    directions = {
        "rows": image,
        "columns": get_columns(image),
        "diagonals_lr": get_diagonals_lr(image),
        "diagonals_rl": get_diagonals_rl(image),
    }
    for key, lines in directions.items():
        for line in lines:
            if len(line) >= 4:
                for i in range(len(line) - 3):
                    sequence = tuple(line[i:i+4])
                    if None not in sequence:  # Ignorar secuencias con 'None'
                        counts[sequence] = counts.get(sequence, 0) + 1
    return {seq: count for seq, count in counts.items() if count > 1}

# Buscar permutaciones entre imágenes
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

# Función para buscar resultados en una tercera imagen
def find_matches_in_third_image(matches, image3):
    results = []
    directions3 = {
        "rows": image3,
        "columns": get_columns(image3),
        "diagonals_lr": get_diagonals_lr(image3),
        "diagonals_rl": get_diagonals_rl(image3),
    }
    for match in matches:
        sequence, loc1, loc2 = match
        for key3, lines3 in directions3.items():
            for line3 in lines3:
                if len(line3) >= 4:
                    for i in range(len(line3) - 3):
                        if tuple(line3[i:i+4]) == sequence:
                            results.append((sequence, loc1, loc2, f"{key3} in Image3"))
    return results
