import copy
import itertools


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        # self.backtrack_called is a int of how many times BACKTRACK function is called
        self.backtrack_called = 0

        # self.backtrack_called is a int of the number of times BACKTRACK function returned failure
        self.backtrack_called_failure = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def assignment_is_complete(self, assignment):
        for i in range(len(assignment.keys())):
            if len(list(assignment.values())[i]) > 1:
                return False
        return True


    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        self.backtrack_called += 1

        # if have a solution, return it
        if self.assignment_is_complete(assignment):
            print('The number of times BACKTRACK function was called: ', self.backtrack_called)
            print('the number of times BACKTRACK function returned failure: ', self.backtrack_called_failure)
            return assignment

        # var = first unassigned variable in assignment
        # var = self.select_unassigned_variable(assignment)

        # var  = most contrained variable in assigment
        var = self.select_MRV_variable(assignment)



        # iterates all values in the domain of var
        for value in (assignment[var]):
            # The deep copy is to ensure that any changes made to 'assignment'
            # does not have any side effects elsewhere.
            copy_assignment = copy.deepcopy(assignment)

            # assign the value under consideration to var
            copy_assignment[var] = value

            # makes the partial assignment under consideration arc consistent
            # if false, we have no consistent solution, return failure
            if self.inference(copy_assignment, self.get_all_neighboring_arcs(var)):

                # partial assignment is consistent with solution
                # evaluate further unassigned variables
                result = self.backtrack(copy_assignment)
                if result is not False:
                    return result

        self.backtrack_called_failure += 1
        return False



    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        # iterate all variable
        for i in range(len(assignment.keys())):
            # variable under consideration
            variable = list(assignment.keys())[i]

            # if the value of variable is not decided, return variable
            if len(list(assignment.values())[i]) > 1:
                return variable

    def select_MRV_variable(self, assignment):
        """Modified version of the function 'Select-Unassigned-Variable' that
        selects the variable with minimum remaining values (MRV).
        In other words, the most constrained variable.
        """

        mrv_var = None
        mrv_var_length = 0
        # iterate all variable
        for i in range(len(assignment.keys())):
            # variable under consideration
            variable = list(assignment.keys())[i]


            # if the value of variable is not decided, return variable
            if len(list(assignment.values())[i]) > 1:
                if mrv_var is None:
                    mrv_var = variable
                if mrv_var_length is 0:
                    mrv_var_length = len(assignment[mrv_var])

                # check number of constraints
                constrain_length = len(assignment[variable])

                if constrain_length < mrv_var_length:
                    mrv_var = variable

        return mrv_var

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        # while queue is not empty
        while queue:
            # pop of first two arbitrary variables
            x_i, x_j = queue.pop(0)

            # makes x_i is arc consistent with x_j
            if self.revise(assignment, x_i, x_j):

                #  checks for consistent solution
                if len(assignment[x_i]) == 0:
                    return False

                # get all neigboring arc of (x_k, x_i) and add them to queue for further consideration
                for x_k in self.get_all_neighboring_arcs(x_i):
                    if x_k not in self.get_all_neighboring_arcs(x_j):
                        queue.append((x_k[0], x_i))

        return True


    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        revised = False

        # iterates values of x_i
        for x in (assignment[i]):
            satisfy = False

            # iterates values of x_j
            for y in assignment[j]:

                # check if (x_i, x_j) satisfies solution
                if (x, y) in self.constraints[i][j]:
                    satisfy = True

            # removes the value under consideration from the domain of x_i
            # if it does not satisfy a solution
            if not satisfy:
                assignment[i].remove(x)
                revised = True
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)

    for constraint in csp.constraints:
        for entry in csp.constraints[constraint]:
            csp.constraints[constraint][entry] = list(csp.constraints[constraint][entry])
    return csp


def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str, range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    for constraint in csp.constraints:
        for entry in csp.constraints[constraint]:
            csp.constraints[constraint][entry] = list(csp.constraints[constraint][entry])
    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" "),
            if col == 2 or col == 5:
                print('|', end=" "),
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')


def main():
    print('#####################')
    print('---------EASY--------')

    csp = create_sudoku_csp("./boards/easy.txt")
    print_sudoku_solution(csp.backtracking_search())

    print('#####################')
    print('-------MEDIUM--------')

    csp = create_sudoku_csp("./boards/medium.txt")
    print_sudoku_solution(csp.backtracking_search())

    print('#####################')
    print('---------HARD--------')

    csp = create_sudoku_csp("./boards/hard.txt")
    print_sudoku_solution(csp.backtracking_search())

    print('#####################')
    print('-------VERYHARD------')

    csp = create_sudoku_csp("./boards/veryhard.txt")
    print_sudoku_solution(csp.backtracking_search())

    # Supposedly the hardest sudokoboard ever according to
    # The Telegraph (source: https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html)

    print('#####################')
    print('-------SUPERHARD------')

    csp = create_sudoku_csp("./boards/superhard.txt")
    print_sudoku_solution(csp.backtracking_search())



if __name__ == '__main__':
    main()














