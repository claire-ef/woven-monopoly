from src.game import Game
from src.utils import load_json_file, load_board, get_next_roll
from src.constants import (MONOPOLY_LOGO,
                           SEPERATOR_LENGTH,
                           PRINT_LOG)
from src.utils import get_inputs


def main():
    """
    Main game play function.
    Receives game options from command line; loads the board; coordinates game
    play; displays the game result.
    """
    # parse command line inputs
    args = get_inputs()
    # load dices rolls
    if args.random_dice_roll:
        # use random dice rolls
        dice_rolls = []
    else:
        # use preset dice rolls
        dice_rolls = load_json_file(args.path_to_rolls)

    # load json files containing board structures
    game = Game(load_board(load_json_file(args.path_to_board)), args.players)

    print(MONOPOLY_LOGO)
    print(" The board is loaded! ".center(SEPERATOR_LENGTH, "~"))
    print(game)

    # start game playing
    print(" Game has started! ".center(SEPERATOR_LENGTH, "~"))
    log = []
    roll_index = 0
    while not game.is_over:
        log.append(f" Turn {roll_index + 1} ".center(SEPERATOR_LENGTH, "~"))
        # player rolls the dice
        roll_value, roll_index = get_next_roll(dice_rolls, roll_index,
                                               args.random_dice_roll)
        log.append(f"{game.current_player.name} rolled {roll_value}.")
        # apply the effect of the dice roll
        game.update(roll_value, log)
        # log.append(str(game))

    # print the process of the game if PRINT_LOG is True
    if PRINT_LOG:
        print("\n".join(log))

    # end the game when game is over
    game.end()
    print(game)


if __name__ == "__main__":
    main()
