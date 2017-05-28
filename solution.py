assignments = []

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal1 = [[rs+cs for rs,cs in zip('ABCDEFGHI','123456789')]]
diagonal2 = [[rs+cs for rs,cs in zip('ABCDEFGHI','987654321')]]
unitlist = row_units + column_units + square_units + diagonal1 + diagonal2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Find all instances of naked twins
        #naked_twins = [[box1, box2] for box1 in unit for box2 in unit if (len(values[box1]) == 2) and (values[box1] == values[box2]) and box1 != box2]
        naked_twins = []
        for box1 in unit:
            for box2 in unit:
                 if box1 != box2 and len(values[box1]) == 2 and values[box1] == values[box2]:
                     naked_twins.append([box1, box2])
        # Eliminate the naked twins as possibilities for their peers
        for twin in naked_twins:
            # 2 digits in each box, the same digits:
            if values[twin[0]] == values[twin[1]] and len(values[twin[0]]) == 2: #sanity check?:
                digits = values[twin[0]]
                for box in unit:
                    for d in digits:
                        if box not in twin:
                            values[box] = values[box].replace(d, '')
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
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    values=[]
    all_values = "123456789"
    for c in grid:
        if c == ".":
            values.append(all_values)
        elif c in all_values:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for box in values.keys():
        if len(values[box])==1:
            #then eliminate that number in peers
            for peer in peers[box]:
                values[peer] = values[peer].replace(values[box],"")
    return values

def only_choice(values):
    for box in values.keys():
        if len(values[box])!=1:
            values_to_find = values[box]
            for value in values_to_find:
                for unit_rcs in units[box]:
                    appears = False
                    #is 'value' unique in the value of any units[box] list?
                    for unit in unit_rcs:
                        if unit != box: #and len(values[unit])!=1
                            if value in values[unit]:
                                appears = True
                    if not appears:
                        values[box] = value
    return values

def reduce_puzzle(values):
    stalled = False
    i = 0
    while not stalled:
        i = i + 1
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # NAKED TWINS
        values = naked_twins(values)
        # Your code here: Use the Eliminate Strategy
        values =  eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    puzzle = reduce_puzzle(values)
    if puzzle:
        # Choose one of the unfilled squares with the fewest possibilities
        unfilled_squares = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
        for box in puzzle.keys():
            if len(puzzle[box]) >= 1:
                unfilled_squares[len(puzzle[box])].append(box)

        if len(unfilled_squares[1]) < 81:
            cbox = 0
            i = 2
            found = False
            while not found:
                if i <= 9:
                    if len(unfilled_squares[i]) > 0:
                        cbox = unfilled_squares[i][0]
                        found = True
                    else:
                        i = i + 1
                else:
                    found = True
            # Now use recursion to solve each one of the resulting sudokus, and if one returns a
            # value (not False), return that answer!
            for digit in values[cbox]:
                new_values_branch = values.copy()
                new_values_branch[cbox] = digit
                tryOK = search(new_values_branch)
                if tryOK:
                    return tryOK

            return False
        else: #all values are filled
            return values
    else: # Sanity check... when reduced returned false
        return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # create a dictionary
    sudoku_dictionary = grid_values(grid)
    solution = search(sudoku_dictionary)
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    solution = solve(diag_sudoku_grid)
    if solution:
        display(solution)
    else:
        print("no solution")

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
