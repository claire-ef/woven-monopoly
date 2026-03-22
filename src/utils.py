import json
from src.game import Board, Property, Go

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
    Load the board from the raw data format.

    Args:
        board_data (list[dict]): a list of space information of the board
    
    Returns:
        The loaded board of Class Board
    """
    board = []
    for space_data in board_data:
        if space_data.get("type") == "property":
            board.append(Property(**space_data))
        elif space_data.get("type") == "go":
            board.append(Go(**space_data))
        else:
            raise KeyError("Undefined space type: ", space_data.get("type"))

    return Board(board)