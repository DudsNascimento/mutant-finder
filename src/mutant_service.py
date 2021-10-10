import mutant_repository

def get_human_dna_statistics():
    print('Getting human DNA statistics')

    return mutant_repository.get_human_dna_statistics()

def process_human_dna(dna_sequence, size):

    def process_human_dna_recursive(dna_sequence, dna_sequence_visited, size, x_pos, y_pos, increment_down, increment_right, increment_oblique, increment_oblique_inverse, repetitions_found):

        dna_sequence_visited[(y_pos * size) + (x_pos)] = True

        if repetitions_found < 2:
            if (x_pos + 1 < size) and dna_sequence[y_pos][x_pos + 1] == dna_sequence[y_pos][x_pos]:
                repetitions_found = process_human_dna_recursive(dna_sequence, dna_sequence_visited, size, x_pos + 1, y_pos, 1, increment_right + 1, 1, 1, (repetitions_found + 1) if ((increment_right + 1) % 4 == 0) else repetitions_found)
                if repetitions_found == 2:
                        return repetitions_found

            if (y_pos + 1 < size) and dna_sequence[y_pos + 1][x_pos] == dna_sequence[y_pos][x_pos]:
                repetitions_found = process_human_dna_recursive(dna_sequence, dna_sequence_visited, size, x_pos, y_pos + 1, increment_down + 1, 1, 1, 1, (repetitions_found + 1) if ((increment_down + 1) % 4 == 0) else repetitions_found)
                if repetitions_found == 2:
                    return repetitions_found

            if (x_pos + 1 < size) and (y_pos + 1 < size) and dna_sequence[y_pos + 1][x_pos + 1] == dna_sequence[y_pos][x_pos]:
                repetitions_found = process_human_dna_recursive(dna_sequence, dna_sequence_visited, size, x_pos + 1, y_pos + 1, 1, 1, increment_oblique + 1, 1, (repetitions_found + 1) if ((increment_oblique + 1) % 4 == 0) else repetitions_found)
                if repetitions_found == 2:
                    return repetitions_found

            if (x_pos - 1 >= 0) and (y_pos + 1 < size) and dna_sequence[y_pos + 1][x_pos - 1] == dna_sequence[y_pos][x_pos]:
                repetitions_found = process_human_dna_recursive(dna_sequence, dna_sequence_visited, size, x_pos - 1, y_pos + 1, 1, 1, 1, increment_oblique_inverse + 1, (repetitions_found + 1) if ((increment_oblique_inverse + 1) % 4 == 0) else repetitions_found)
                if repetitions_found == 2:
                    return repetitions_found

        return repetitions_found

    dna_sequence_as_string = ",".join(dna_sequence)
    human_dna = mutant_repository.get_human_dna(dna_sequence_as_string)
    if human_dna is not None:
        return human_dna['is_mutant']

    repetitions_found = 0
    dna_sequence_visited = [False] * (size * size)
    for y in range(size):
        for x in range(size):

            if repetitions_found < 2 and not dna_sequence_visited[(y * size) + (x)]:
                repetitions_found = process_human_dna_recursive(dna_sequence, dna_sequence_visited, 4, x, y, 1, 1, 1, 1, repetitions_found)
            
            if repetitions_found == 2:
                mutant_repository.save_human_dna_and_update_human_dna_statistics(size, dna_sequence_as_string, True)
                return True

    mutant_repository.save_human_dna_and_update_human_dna_statistics(size, dna_sequence_as_string, False)
    return False
