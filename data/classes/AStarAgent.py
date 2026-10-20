from data.classes.FifteenPuzzle import FifteenPuzzle
from time import perf_counter

class AStarAgent:
    """Scaffold for an A* solver; implement search before using it to play."""

    def __init__(self): 
        """Initializes AStarAgent with list of moves that can
        be filled with solution moves after search() is called."""
        self.moves: list[int] | None = None
        self.search_seconds: float | None = None
        self.solution_length: int | None = None

    def search(self, board: FifteenPuzzle) -> list[int] | None:
        """Search for shortest solution using A* algorithm to the puzzle
        Board is NOT modified during search. 

        Args: 
            board: FifteenPuzzle instance representing current state of puzzle

        Returns:
            list of tile indices representing moves to solve the puzzle
            If no solution is found, returns None.
        """
        # converts current board into tuple of values as a state representation
        start = tuple(square.value for square in board.squares)
        goal = tuple(board.solved_values)

        # dictionary tracks fewest moves to reach each state from start
        g_costs_num_moves = {}
        g_costs_num_moves[start] = 0

        # tracks states that have been visited but not yet processed
        unprocessed_states = {start}

        # dictionary tracks prior state and move index that led to each state
        # used for reconstructing solution once goal is reached
        came_from = {}

        while unprocessed_states:
            #A* FORMULA: f(n) = g(n) + h(n)
            # current state has lowest f(n) value among open states
            current = min(unprocessed_states, key=lambda state: g_costs_num_moves[state] + 
                          self.heuristic(state, goal))
            # returns winning moves if goal is reached
            if current == goal:
                winning_moves = []
                while current != start:
                    previous, move_index = came_from[current]
                    # appends index of moved tile to winning_moves list
                    winning_moves.append(move_index)
                    current = previous
                # reverses winning_moves to get correct order from start to goal
                winning_moves.reverse()
                return winning_moves     
            # Removes current state from open_states marking as processed
            unprocessed_states.remove(current)
            # Loops through neighboring states of current and computes
            # tentative_g_cost for each neighboring state.
            for next_state, move_index in self.get_neighbor_states(current):
                tentative_g_cost_num_moves = g_costs_num_moves[current] + 1
                # If the new path to next_state is better than the previous one,
                # update the g_cost and came_from dictionaries.
                if tentative_g_cost_num_moves < g_costs_num_moves.get(
                    next_state, float("inf")):
                    # Relaxation step: update g_cost and came_from for next_state
                    g_costs_num_moves[next_state] = tentative_g_cost_num_moves
                    came_from[next_state] = (current, move_index)
                    # add next_state to unprocessed_states for further exploration
                    unprocessed_states.add(next_state)
        return None

    def heuristic(self, state, goal) -> int:
        """Computes Manhattan distances for all non-empty tiles. Means for
        each tile, compute distance from current state to goal position. 
        
        Args: 
            state: tuple of values representing current board state
            goal: tuple of values representing goal board state
            
        Returns:
            int: sum of Manhattan distances for all numbered tiles"""
        # Dictionary maps each tile to goal position (row, col)
        goal_positions = {}
        
        for index, value in enumerate(goal):
            if value is not None:
                #converts index to (row, col) in 4x4 grid
                goal_positions[value] = divmod(index, 4)
        # initialize total Manhattan distance
        distance = 0
        # iterate thru each tile in current state
        for index, value in enumerate(state):
            if value is not None:
                # converts current tile index to (row, col) in 4x4 grid
                row, col = divmod(index, 4)
                # gets goal position of current tile
                goal_row, goal_col = goal_positions[value]
                # computes Manhattan distance
                distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def get_neighbor_states(self, state):
        """Computes all neighboring states defined as all possible board states
         produced by moving a single tile and the index of the moved tile.

        Args:
            state: tuple of values representing current board state

        Returns:
            list of tuples each representing a neighboring state and 
            index of moved tile of the form (next_state, move_index)
        """
        blank_index = state.index(None)
        # converts index to row and column in 4x4 grid
        row, col = divmod(blank_index, 4)

        # get possible moves around blank tile
        neighbors = []

        # check valid moves in each direction [up, down, left, right]
        # for-loop iterates through four possible directions (i.e. tuple unpacking)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row = row + dr 
            next_col = col + dc 
            # checks if within bounds of 4x4 grid
            if 0 <= next_row < 4 and 0 <= next_col < 4:
                # convert back to index
                next_blank_index = next_row * 4 + next_col
                # create a mutable copy of the unchanged original state 
                # to swap with the blank tile
                next_state = list(state)
                # swap blank with neighboring tile
                next_state[blank_index], next_state[next_blank_index] = (
                    next_state[next_blank_index], next_state[blank_index]
                )
                # adds new state and index of moved tile to neighbors list
                neighbors.append((tuple(next_state), next_blank_index))
        return neighbors


    def choose_action(self, board: FifteenPuzzle) -> bool:
        """Applies next move in the solution, if needed.
        Args:
            board: FifteenPuzzle instance representing current state of puzzle
        Returns:
            bool: True if a move applied, False if no solution is available."""
        # calls search() to find solution moves if moves list contains only None
        if self.moves is None:
            started = perf_counter()
            self.moves = self.search(board)
            self.search_seconds = perf_counter() - started

            self.solution_length = len(self.moves) if self.moves is not None else 0

            print(f"Search time: {self.search_seconds:.6f} seconds")
            print(f"Solution length: {self.solution_length} moves")
            

        if not self.moves:
            return False
        # removes & returns first move
        move_index = self.moves.pop(0)
        return board.handle_move(board.squares[move_index])