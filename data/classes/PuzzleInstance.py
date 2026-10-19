# /* PuzzleInstance.py

import pygame

from data.classes.FifteenPuzzle import FifteenPuzzle
from typing import Protocol


class Agent(Protocol):
    def choose_action(self, board: FifteenPuzzle) -> bool:
        """Apply one move and return whether play should continue."""

def puzzle_instance(agent: Agent, initial_values: list[int | None]):
    pygame.init()
    WINDOW_SIZE = (600, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    board = FifteenPuzzle(screen, WINDOW_SIZE[0], WINDOW_SIZE[1])
    if not board.set_squares(initial_values):
        print("Invalid or unsolvable initial values!")
        pygame.quit()
        return
    moves_count: int = 0

    # Run the main game loop
    running = not board.is_solved()
    if not running:
        print('Player solved!')
        board.highlight()
        board.draw()
    while running:
        try:
            chosen_action = agent.choose_action(board)
        except NotImplementedError as error:
            print(error)
            running = False
            break
        moves_count += 1
        if chosen_action == False or moves_count > 1000:
            print('Player did not solve')
            running = False
        elif board.is_solved():
            print('Player solved!')
            board.highlight()
            running = False
        board.draw()

    board.draw()

    # Allow the player to view the result
    viewing = True
    while viewing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                viewing = False
    pygame.quit()
