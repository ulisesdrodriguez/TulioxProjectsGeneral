import numpy as np
from itertools import permutations



def rotate_image_90(image):
    return np.rot90(image).tolist()


def rotate_image_180(image):
    return np.rot90(image, 2).tolist()


def rotate_image_270(image):
    return np.rot90(image, 3).tolist()


def generate_rotations(image):
    return [image, rotate_image_90(image), rotate_image_180(image), rotate_image_270(image)]


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


def search_by_criteria(image, sequence_length=4, criteria=[]):
    results = {}
    rows, cols = len(image), len(image[0])

    def add_result(sequence, positions, criterion):
        if sequence not in results:
            results[sequence] = []
        results[sequence].append({"positions": positions, "criterion": criterion})

    if "horizontal_lr" in criteria:
        for r in range(rows):
            for c in range(cols - sequence_length + 1):
                sequence = tuple(image[r][c:c + sequence_length])
                if None not in sequence:
                    add_result(sequence, [(r, c + i) for i in range(sequence_length)], "horizontal_lr")

    if "horizontal_rl" in criteria:
        for r in range(rows):
            for c in range(sequence_length - 1, cols):
                sequence = tuple(image[r][c - i] for i in range(sequence_length))
                if None not in sequence:
                    add_result(sequence, [(r, c - i) for i in range(sequence_length)], "horizontal_rl")

    if "vertical_td" in criteria:
        for c in range(cols):
            for r in range(rows - sequence_length + 1):
                sequence = tuple(image[r + i][c] for i in range(sequence_length))
                if None not in sequence:
                    add_result(sequence, [(r + i, c) for i in range(sequence_length)], "vertical_td")

    if "vertical_bu" in criteria:
        for c in range(cols):
            for r in range(sequence_length - 1, rows):
                sequence = tuple(image[r - i][c] for i in range(sequence_length))
                if None not in sequence:
                    add_result(sequence, [(r - i, c) for i in range(sequence_length)], "vertical_bu")

    if "diagonal_principal" in criteria:
        for r in range(rows - sequence_length + 1):
            for c in range(cols - sequence_length + 1):
                sequence = tuple(image[r + i][c + i] for i in range(sequence_length))
                if None not in sequence:
                    add_result(sequence, [(r + i, c + i) for i in range(sequence_length)], "diagonal_principal")

    if "diagonal_secundaria" in criteria:
        for r in range(rows - sequence_length + 1):
            for c in range(sequence_length - 1, cols):
                sequence = tuple(image[r + i][c - i] for i in range(sequence_length))
                if None not in sequence:
                    add_result(sequence, [(r + i, c - i) for i in range(sequence_length)], "diagonal_secundaria")

    if "zigzag" in criteria:
        for r in range(rows - sequence_length + 1):
            for c in range(cols - sequence_length + 1):
                sequence = tuple(image[r + i][c + (i % 2)] for i in range(sequence_length))
                if None not in sequence:
                    add_result(sequence, [(r + i, c + (i % 2)) for i in range(sequence_length)], "zigzag")

    return results


def search_custom_pattern(image, pattern, sequence_length=4):
    rows, cols = len(image), len(image[0])
    results = {}

    def add_result(sequence, positions, criterion):
        if sequence not in results:
            results[sequence] = []
        results[sequence].append({"positions": positions, "criterion": criterion})

    for r in range(rows):
        for c in range(cols):
            positions = [(r, c)]
            sequence = [image[r][c]]
            valid = True

            for dr, dc in pattern:
                nr, nc = positions[-1][0] + dr, positions[-1][1] + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    positions.append((nr, nc))
                    sequence.append(image[nr][nc])
                else:
                    valid = False
                    break

            if valid and len(sequence) == sequence_length and None not in sequence:
                add_result(tuple(sequence), positions, "custom_pattern")

    return results


def search_in_image_with_rotations(image, sequence_length=4, criteria=[], custom_pattern=None):
    results = {}
    rotations = generate_rotations(image)

    for idx, rotated_image in enumerate(rotations):
        rotation_label = f"rotation_{idx * 90}°"

        if custom_pattern:
            found = search_custom_pattern(rotated_image, custom_pattern, sequence_length)
        else:
            found = search_by_criteria(rotated_image, sequence_length, criteria)

        for sequence, occurrences in found.items():
            if sequence not in results:
                results[sequence] = []
            results[sequence].extend(
                {
                    "positions": occ["positions"],
                    "criterion": f"{occ['criterion']} ({rotation_label})",
                }
                for occ in occurrences
            )
    return results


def main_prime4(image1, image2, image3=None, sequence_length=4, custom_pattern=None):
    all_criteria = [
        "horizontal_lr",
        "horizontal_rl",
        "vertical_td",
        "vertical_bu",
        "diagonal_principal",
        "diagonal_secundaria",
        "zigzag",
    ]
    results = {
        "image1_image2": search_in_image_with_rotations(image1, sequence_length, all_criteria, custom_pattern),
        "image1_image3": search_in_image_with_rotations(image1, sequence_length, all_criteria,
                                                        custom_pattern) if image3 else None,
        "image2_image3": search_in_image_with_rotations(image2, sequence_length, all_criteria,
                                                        custom_pattern) if image3 else None,
    }
    return results