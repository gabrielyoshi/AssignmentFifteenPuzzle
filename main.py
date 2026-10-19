import argparse

from data.classes.PuzzleInstance import puzzle_instance
from data.classes.HumanAgent import HumanAgent
from data.classes.AStarAgent import AStarAgent

def main():
    parser = argparse.ArgumentParser(description="Initialize player for the game.")
    parser.add_argument(
        "player",
        choices=("Human", "AStar"),
        help="Select Human for manual play or AStar for the A* player scaffold",
    )
    args = parser.parse_args()
    # Reversed Order
    # initial_values = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, None]
    # One move away from solved
    initial_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, None, 15]
    if args.player == "Human":
        human_agent = HumanAgent()
        puzzle_instance(human_agent, initial_values)
    elif args.player == "AStar":
        puzzle_instance(AStarAgent(), initial_values)

if __name__ == '__main__':
    main()
