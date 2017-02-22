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

