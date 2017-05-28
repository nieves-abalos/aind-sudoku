from utils import *

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    values=[]
    all_values = "123456789"
    for c in grid:
        if c == ".":
            values.append(all_values)
        #else:
        elif c in all_values:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # AIND SOLUTION:
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def my_eliminate(values):
    #My solution:
    for box in values.keys():      
        if len(values[box])==1:
            #then eliminate that number in peers
            for peer in peers[box]:
                values[peer] = values[peer].replace(values[box],"")
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    # AIND SOLUTION:
    for unit in unitlist:
        for digit in '123456789':
            distinct_places = [box for box in unit if digit in values[box]]
            if len(distinct_places) == 1:
                values[distinct_places[0]] = digit
    return values

def my_only_choice(values):   
    #My solution:
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
                        #print(value+" is UNIQUE in the box "+box)
                        #print("because of the unit...")
                        #print(unit_rcs)                   
                        values[box] = value
    return values

def my_reduce_puzzle(values):
    #print("\nSTART SOLVING PUZZLE:")
    stalled = False
    i = 0
    while not stalled:
        #print("Iteration reducing puzzle:" + str(i))
        i = i +1
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values =  my_eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = my_only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    #print("\nFINISHED!")
    return values


def reduce_puzzle(values):
    #print("\nSTART SOLVING PUZZLE:")
    stalled = False
    i = 0
    while not stalled:
        #print("Iteration reducing puzzle:" + str(i))
        i = i +1
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    #print("\nFINISHED!")
    return values


def my_search(values, path):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    puzzle = my_reduce_puzzle(values)
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

            path.append(cbox)
            # Now use recursion to solve each one of the resulting sudokus, and if one returns a 
            # value (not False), return that answer!

            for digit in values[cbox]:  
                new_values_branch = values.copy()
                new_values_branch[cbox] = digit
                tryOK = my_search(new_values_branch, path)
                if tryOK:
                    return tryOK
                #else:
                #    print("Not found with "+digit+" in box "+cbox)
            
            #path.remove(cbox) 
            return False    
        else: #all values are filled
            print(path)
            return values
    else: # Sanity check... when reduced returned false
        return False
        # If you're stuck, see the solution.py tab!


def search(values, path):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        print(path)
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    path.append(s)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku, path)
        if attempt:
            return attempt



example = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
solution = "483921657967345821251876493548132976729564138136798245372689514814253769695417382"

print("\n============ NAS =============")

grid = grid_values(example)
print("\n**** GRID ****")
display(grid)

print("\n**** Strategy 1: ELIMINATION ****")
myel= eliminate(grid) #my_
display(myel)

print("\n**** Strategy 2: ONLY CHOICE ****")
myoc= my_only_choice(myel)
display(myoc)

print("\n============ UDACITY =============")

u_grid = grid_values(example)
print("\n**** GRID ****")
display(u_grid)
#Looks good!
#123456789 123456789     3     |123456789     2     123456789 |    6     123456789 123456789 
#    9     123456789 123456789 |    3     123456789     5     |123456789 123456789     1     
#123456789 123456789     1     |    8     123456789     6     |    4     123456789 123456789 
#------------------------------+------------------------------+------------------------------
#123456789 123456789     8     |    1     123456789     2     |    9     123456789 123456789 
#    7     123456789 123456789 |123456789 123456789 123456789 |123456789 123456789     8     
#123456789 123456789     6     |    7     123456789     8     |    2     123456789 123456789 
#------------------------------+------------------------------+------------------------------
#123456789 123456789     2     |    6     123456789     9     |    5     123456789 123456789 
#    8     123456789 123456789 |    2     123456789     3     |123456789 123456789     9     
#123456789 123456789     5     |123456789     1     123456789 |    3     123456789 123456789 

print("\n**** Strategy 1: ELIMINATION ****")
u_myel= eliminate(u_grid)
display(u_myel)
#Looks good!
#   45    4578    3   |   49     2     147  |   6     5789    57  
#   9    24678    47  |   3      47     5   |   78    278     1   
#   25    257     1   |   8      79     6   |   4    23579   2357 
#---------------------+---------------------+---------------------
#  345    345     8   |   1     3456    2   |   9    34567  34567 
#   7    123459   49  |  459   34569    4   |   1    13456    8   
#  1345  13459    6   |   7     3459    8   |   2     1345   345  
#---------------------+---------------------+---------------------
#  134    1347    2   |   6     478     9   |   5     1478    47  
#   8     1467    47  |   2     457     3   |   17    1467    9   
#   46    4679    5   |   4      1      47  |   3    24678   2467 

print("\n**** Strategy 2: ONLY CHOICE ****")
u_myoc= only_choice(u_myel)
display(u_myoc)
#Looks good!
#  4     8     3   |  9     2     1   |  6     5     7   
#  9     6     7   |  3     4     5   |  8     2     1   
#  2     5     1   |  8     7     6   |  4     9     3   
#------------------+------------------+------------------
#  5    345    8   |  1    3456   2   |  9     7     6   
#  7     2     9   |  5   34569   4   |  1   13456   8   
#  1   13459   6   |  7    3459   8   |  2    1345   5   
#------------------+------------------+------------------
#  3     7     2   |  6     8     9   |  5     1     4   
#  8     1     4   |  2     5     3   |  7     6     9   
#  6     9     5   |  4     1     7   |  3     8     2 


print("\n**** CONSTRAINT PROPAGATION ****")
print("\n============ NAS =============")
newgrid = grid_values(example)
solved = my_reduce_puzzle(newgrid)
display(solved)

print("\n============ UDACITY =============")
newgrid2 = grid_values(example)
solved2 = reduce_puzzle(newgrid2)
display(solved2)

example2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values = grid_values(example2)
print("\n============ NAS =============")
solved = my_reduce_puzzle(values)
display(solved)
print("\n============ UDACITY =============")
solved = reduce_puzzle(values)
display(solved)


print("\n**** Strategy 3: SEARCH ****")
print("\n============ NAS =============")
newgrid = grid_values(example2)
path = []
solved = my_search(newgrid, path)
display(solved)

print("\n============ UDACITY =============")
newgrid2 = grid_values(example2)
path = []
solved2 = search(newgrid2, path)
display(solved2)
