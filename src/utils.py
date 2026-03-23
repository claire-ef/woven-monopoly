import json
import random
from src.game import Board, Go, Property


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


def load_board(board_data: list[dict]) -> Board:
    """
    Load the board from the raw data format

    Args:
        board_data (list[dict]): a list of space information of the board

    Returns:
        The loaded board of Class Board
    """
    board = []
    # create spaces of different types
    for space_data in board_data:
        if space_data.get("type") == "property":
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
