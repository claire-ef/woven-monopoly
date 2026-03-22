DEFAULT_PLAYERS = ["Peter", "Billy", "Charlotte", "Sweedal"]
INITIAL_BALANCE = 16

class Space:
    """ 
    Represent a space on the game board.
    """
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
    
    def __str__(self):
        return f"{self.type}: {self.name}."

class Go(Space):
    """
    Represent a type of space that is GO.
    """
    pass

class Property(Space):
    """
    Represent a type of space that is a property.
    """
    def __init__(self, name: str, type: str, price: int, colour: str):
        super().__init__(name, type)
        self.price = price
        self.colour = colour

    def __str__(self):
        return f"{self.type}: {self.name}, price: {self.price}, colour: {self.colour}."

class Board():
    """
    Represent a board state
    """
    def __init__(self, spaces: list[Space]):
        self.spaces = spaces
    
    def __str__(self):
        return "\n".join(str(space) for space in self.spaces)

class Player:
    """
    Represent a player state.
    """

    def __init__(self, name: str, balance: int = INITIAL_BALANCE):
        self.name = name
        self.balance = balance
    
    def __str__(self):
        return f"{self.name} has ${self.balance}."

class Game:
    """
    Represent a game state.
    """

    def __init__(self, board: Board):
        self.board = board
        self.players = [Player(name) for name in DEFAULT_PLAYERS]

    def __str__(self):
        return ("---Board---\n" + 
                 str(self.board) +
                 "\n---Players---\n" +
                 "\n".join(str(player) for player in self.players))