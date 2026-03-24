import json
import random
import argparse
from src.game import Board, Go, Property
from src.constants import (DEFAULT_PLAYERS,
                           DEFAULT_INITIAL_BALANCE,
                           DEFAULT_RENT_MULTIPLIER,
                           DEFAULT_VERBOSITY,
                           CONSTANT_VERBOSITY)


def load_json_file(path: str) -> list:
    """
    Load json file at the given path

    Args:
        path (str): path to the json file

    Returns:
        A list containing the data in the json file
    """
    with open(path) as f:
        data = json.load(f)
    return data


def load_board(board_data: list[dict], rent_multiplier: float) -> Board:
    """
    Load the board from the raw data format

    Args:
        board_data (list[dict]): a list of space information of the board
        rent_multiplier (float): the proportion of the rent to the price of
                                 the property

    Returns:
        The loaded board of Class Board
    """
    board = []
    # create spaces of different types
    for space_data in board_data:
        if space_data.get("type") == "property":
            space_data["rent_multiplier"] = rent_multiplier
            board.append(Property(**space_data))
        elif space_data.get("type") == "go":
            board.append(Go(**space_data))
        else:
            raise KeyError("Undefined space type: ", space_data.get("type"))

    return Board(board)


def get_next_roll(rolls: list[int], current_roll_index: int,
                  is_random: bool = False) -> tuple[int, int]:
    """
    Get the next dice roll. If is_random is True, randomly generate a dice
    roll. Otherwise load the next dice roll from the preset list.

    Args:
        rolls (list[int]): a list of preset rolls. It is an empty list if
                            is_random is True
        current_roll_index (int): the index of the dice roll
        is_random (bool): whether to generate random dice roll or not.
                            The default is False

    Returns:
        Two integers, the first being the next dice roll, the second being the
        next dice roll index
    """
    # generate the next dice roll randomly
    if is_random:
        return random.randint(1, 6), current_roll_index + 1

    # generate the next dice roll from a preset list
    if current_roll_index >= len(rolls):
        raise IndexError(f"A roll at index {current_roll_index} is requested, "
                         f"but there are only {len(rolls)} rolls given")
    return rolls[current_roll_index], current_roll_index + 1


def get_inputs():
    """
    Parse command line inputs and return the arguments.
    """
    # set up parser to get game options from command line input
    parser = argparse.ArgumentParser(prog="woven_monopoly",
                                     description="This is a application that "
                                     "plays the game of Woven Monopoly")

    parser.add_argument("path_to_board", type=str,
                        help="Path to the board json file.")

    parser.add_argument("-p", "--path_to_rolls", type=str,
                        metavar="path_to_rolls",
                        help="Path to the dice rolls json file")

    parser.add_argument("-r", "--random_dice_roll",
                        action="store_true",
                        help="Whether or not to use random dice rolls, the "
                             "default is false")

    parser.add_argument("-v", "--verbosity", type=int,
                        choices=(0, 1, 2, 3), nargs="?",
                        default=DEFAULT_VERBOSITY, const=CONSTANT_VERBOSITY,
                        help="The level of verbosity of the output\n"
                             "0 (default): logo and game result\n"
                             "1 (const): level 0 with inital and ending game "
                             "state\n"
                             "2: level 1 with player actions\n"
                             "3: level 2 with game state at each turn")

    parser.add_argument("--initial_balance",
                        type=float,
                        default=DEFAULT_INITIAL_BALANCE,
                        help=f"The amount of money each player starts the "
                             f"game with, the default is "
                             f"${DEFAULT_INITIAL_BALANCE}")

    parser.add_argument("--rent_multiplier",
                        type=float,
                        default=DEFAULT_RENT_MULTIPLIER,
                        help=f"The proportion of the rent to the price of the"
                             f"property the default is "
                             f"${DEFAULT_RENT_MULTIPLIER}")

    parser.add_argument("--players", nargs="+", default=DEFAULT_PLAYERS,
                        metavar="player_name",
                        help="Participating player names in game order, "
                             "seperated by space. If not provided, a set of "
                             "four default players are used: Peter, Billy, "
                             "Charlotte, Sweedal")

    args = parser.parse_args()

    # check the validity of command line inputs
    if not args.random_dice_roll and args.path_to_rolls is None:
        # if random dice rolling is disabled, a file path to preset dice rolls
        # must be provided
        parser.error("Random dice rolling is disabled"
                     "but preset dice rolls are not provided.")
    if len(args.players) < 2:
        # there must be at least 2 players.
        parser.error(f"Only {len(args.players)} player provided."
                     f"There must be at least 2 players.")
    return args


def print_log(log: list[tuple[int, str]], verbosity: int):
    """
    Print game logging at the given verbosity.
    Args:
        log (list[tuple[int, str]]): a list of tuples that stores the
            progress of the game [(verbosity_level, log_message)
        verbosity (int): The level of verbosity of the output
    """
    for item in log:
        verbosity_level = item[0]
        log_msg = item[1]
        if verbosity_level <= verbosity:
            print(log_msg)
