assignments = []

digits = '123456789'

rows = 'ABCDEFGHI'
cols = digits
reversed_cols = cols[::-1]


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
col_units = [cross(rows, col) for col in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
left_diag_units = [rows[i] + cols[i] for i in range(9)]
right_diag_units = [rows[i] + reversed_cols[i] for i in range(9)]
unitlist = row_units + col_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
row_units = dict((s, [u for u in row_units if s in u]) for s in boxes)
col_units = dict((s, [u for u in col_units if s in u]) for s in boxes)
square_units = dict((s, [u for u in square_units if s in u]) for s in boxes)


peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)
row_peers = dict((s, set(sum(row_units[s], [])) - {s}) for s in boxes)
col_peers = dict((s, set(sum(col_units[s], [])) - {s}) for s in boxes)
square_peers = dict((s, set(sum(square_units[s], [])) - {s}) for s in boxes)



def solved_judge(values):
    return all(len(values[s]) == 1 for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    for v in grid:
        if v == '.':
            values.append(digits)
        else:
            values.append(v)
    data = dict(zip(boxes, values))
    return data


def display(values):
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)


def eliminate(values):
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for solved_box in solved_boxes:
        for peer_box in peers[solved_box]:
            values[peer_box] = values[peer_box].replace(values[solved_box], '')

        if solved_box in left_diag_units:
            for peer_box in left_diag_units:
                if peer_box != solved_box:
                    values[peer_box] = values[peer_box].replace(values[solved_box], '')

        if solved_box in right_diag_units:
            for peer_box in right_diag_units:
                if peer_box != solved_box:
                    values[peer_box] = values[peer_box].replace(values[solved_box], '')

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins # Eliminate the naked twins as possibilities for their peers
    for box in boxes:
        v = values[box]
        for alone_peers in [row_peers[box], col_peers[box], square_peers[box]]:
            twin_k = None
            twin_v = None
            count = 0
            for peer_box in alone_peers:
                if len(v) == 2 and values[peer_box] == v:
                    count += 1
                    twin_k = peer_box
                    twin_v = v

            if twin_k and count == 1:
                for peer_box in alone_peers:
                    for digit in twin_v:
                        if peer_box not in [box, twin_k]:
                            if len(values[peer_box]) > 1:
                                values[peer_box] = values[peer_box].replace(digit, '')
    return values


def find_fewest_box(values):
    fewest = 9
    box = 'A1'
    for k, v in values.items():
        possibilities = len(v)
        if 1 < possibilities < fewest:
            box = k
            fewest = len(v)

    return box


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]) > 0:
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False

    if solved_judge(values):
        return values

    box = find_fewest_box(values)
    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

    return values


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    display(values)
    print("\n")

    display(eliminate(grid_values(diag_sudoku_grid)))
    values = solve(diag_sudoku_grid)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
