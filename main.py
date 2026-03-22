import argparse
from src.game import Game
from src.utils import load_json_file, load_board

def main():

    # parse command line inputs
    parser = argparse.ArgumentParser(description="Let's play Woven Monopoly!")
    parser.add_argument("path_to_board", help="File path to the board file.")
    parser.add_argument("path_to_rolls", help="File path to the dice rolls file.")
    args = parser.parse_args()

    # load json files containing board structures and dice rolls
    dice_rolls = load_json_file(args.path_to_rolls)
    print(dice_rolls)
    game = Game(load_board(load_json_file(args.path_to_board)))
    print(game)

if __name__ == "__main__":
    main()