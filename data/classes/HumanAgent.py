# /* HumanAgent.py

import pygame

from data.classes.FifteenPuzzle import FifteenPuzzle

class HumanAgent:
    """Represents a human player who makes moves on the puzzle."""

    def choose_action(self, board: FifteenPuzzle) -> bool:
        """Applies one move to a board.
            Args:
                board: FifteenPuzzle instance representing current state of puzzle
            Returns:
                bool: True if a move applied, False if no solution is available."""
        choosing_move = True
        while choosing_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    x = mx // board.square_width
                    y = my // board.square_height
                    clicked_square = board.get_square_from_pos((x, y))
                    # if a square was clicked, try to move it
                    if board.handle_move(clicked_square):
                        return True
            board.draw()
        return False
