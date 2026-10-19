from data.classes.FifteenPuzzle import FifteenPuzzle


class AStarAgent:
    """Scaffold for an A* solver; implement search before using it to play."""

    def search(self, board: FifteenPuzzle) -> list[int] | None:
        """Search for a solution to the puzzle and return a list of moves."""
        # converts current board into tuple of values as a state representation
        start = tuple(square.value for square in board.squares)
        goal = tuple(board.solved_values)

        # tracks fewest moves to reach each state
        g_costs = {}
        g_costs[start] = 0

        # tracks states that have been visited but not yet processed
        open_states = {start}

        # tracks prior state and move index that led to each state
        # used for reconstructing solution once goal is reached
        came_from = {}

        while open_states:
            current = min(open_states, key=lambda state: g_costs[state] + 
                          self.heuristic(state, goal))
            # Keep existing goal check and path reconstruction logic
            open_states.remove(current)

            for next_state, move_index in self.get_neighbors(current):
                tentative_g_cost = g_costs[current] + 1
            if current == goal:
                moves = []

                while current != start:
                    previous, move_index = came_from[current]
                    moves.append(move_index)
                    current = previous

                moves.reverse()
                return moves

        raise NotImplementedError(
            "A* is not implemented yet. Add the search logic here."
        )

    # get_neighbors accepts a state (tuple of values representing the board)
    # and returns a list containing pairs of neighboring board states (tuples) 
    # and the index of the moved tile 
    def get_neighbors(self, state):
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
        """Apply one move and return True, or False if no solution is available."""
        raise NotImplementedError(
            "A* is not implemented yet. Add the search and move-selection logic here."
        )
