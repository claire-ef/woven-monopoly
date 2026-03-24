from src.game import Game, Player
from src.utils import (get_inputs, load_json_file, load_board, get_next_roll,
                       print_log)
from src.constants import MONOPOLY_LOGO, SEPERATOR_LENGTH


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
    players = [Player(player_name, args.initial_balance)
               for player_name in args.players]
    game = Game(load_board(load_json_file(args.path_to_board),
                           args.rent_multiplier),
                players)

    # a list of tuples to store the progress of the game
    # list[tuple[int, str]]: [(verbosity_level, log_message)]
    log = []
    log.append((0, MONOPOLY_LOGO))
    log.append((0, " Welcome to Woven Monopoly! ".center(
        SEPERATOR_LENGTH, "-")))
    log.append((0, " Game has started! ".center(SEPERATOR_LENGTH, "-")))
    log.append((0, " Game Running... ".center(SEPERATOR_LENGTH, "-")))
    log.append((1, str(game)))

    # start game playing
    roll_index = 0
    while not game.is_over:
        log.append((2,
                    f" Turn {roll_index + 1} ".center(SEPERATOR_LENGTH, "-")))
        # player rolls the dice
        roll_value, roll_index = get_next_roll(dice_rolls, roll_index,
                                               args.random_dice_roll)
        log.append((2, f"{game.current_player.name} rolled {roll_value}."))
        # apply the effect of the dice roll
        game.update(roll_value, log)
        log.append((3, str(game)))

    # end the game when game is over
    game.end(log)

    # print game result
    print_log(log, args.verbosity)


if __name__ == "__main__":
    main()
