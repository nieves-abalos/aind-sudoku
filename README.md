# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We add the new local constraint (check if there are naked twins and eliminate these values in other boxes in unit) to dramatically reduce the search space. We combine the functions eliminate and only_choice with naked_twins to reduce the space (our puzzle), applying three constraints repeatedly trying to solve it. We exclude possibilities in a group of squares looking for "twins": twin squares with the same values (2 digits in my case). Those two digits are excluded from the common peers of that twins, enforcing the constraint that no squares outside the two naked twins squares can contain the twin values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We add the new local constraint (diagonals must be taken into account as units) to dramatically reduce the search space. We take this new unit into account when aplying the other functions (eliminate, only_choice or naked_twins) and then search in a reduced space. In our case, if a square is in one of the sudoku diagonals, the "diagonal constraint" is applied to the values of that diagonal too (the numbers 1 to 9 should all appear exactly once), besides the other restrictions applied as sudoku general rules.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

