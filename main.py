import argparse
from src.game import Game
from src.utils import load_json_file, load_board, get_next_roll

RANDOM_DICE_ROLL = False

def main():
    """
    Main game play function.
    Receives game options from command line; loads the board; coordinates game play; displays the game result.
    """
    # parse command line inputs
    parser = argparse.ArgumentParser(description="Let's play Woven Monopoly!")
    parser.add_argument("path_to_board", help="File path to the board file.")
    parser.add_argument("path_to_rolls", help="File path to the dice rolls file.")
    args = parser.parse_args()

    # load json files containing board structures
    game = Game(load_board(load_json_file(args.path_to_board)))
    print("The board is loaded!")

    # load dices rolls
    if RANDOM_DICE_ROLL:
        # use random dice rolls
        dice_rolls = []
    else:
        # use preset dice rolls
        dice_rolls = load_json_file(args.path_to_rolls)
    roll_index = 0

    # start game playing
    while not game.is_over:
        # player rolls the dice
        roll_value, roll_index = get_next_roll(dice_rolls, roll_index, RANDOM_DICE_ROLL)
        print(f"{game.current_player.name} rolled {roll_value}!")
        # apply the effect of the dice roll
        game.update(roll_value)
    
    # end the game when game is over
    game.end()

if __name__ == "__main__":
    main()