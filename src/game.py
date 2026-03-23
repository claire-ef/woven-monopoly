from math import ceil
from src.constants import (INITIAL_BALANCE,
                           RENT_MULTIPLIER,
                           FULL_SET_MULTIPLIER,
                           DEFAULT_PLAYERS,
                           SEPERATOR_LENGTH,
                           PASS_GO_BONUS,
                           COLOURS,
                           BOARD_ROW_TEMPLATE,
                           PLAYER_ROW_TEMPLATE)


class Player:
    """
    Represent a player of the game.

    Attributes:
        name (str): name of the player
        balance (int | INITIAL_BALANCE): how much money the player own,
                                         starting with INITIAL_BALANCE
        position (int): the position of the player on the board
    """
    def __init__(self, name: str, balance: int = INITIAL_BALANCE):
        self.name = name
        self.balance = balance
        # all players start on GO
        self.position = 0

    def __str__(self):
        return (f"{self.name} has ${self.balance} "
                f"and is at space {self.position}.")


class Space:
    """
    Represent a space on the game board.

    Attributes:
        name (str): name of the space
        type (str): type of the space
    """
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.type}: {self.name}."


class Go(Space):
    """
    Represent a type of space that is the go.
    """
    pass


class Property(Space):
    """
    Represent a type of space that is a property.

     Attributes:
        price (int): cost to purchase the property
        colour (str): colour of the property
        owner (Player | None): the player who currently owns the property
        rent (int): amount of money to pay the owner if land on the property.
                    Proportional to the property price and can be adjusted.
                    This amount is before applying the full set bonus.
    """
    def __init__(self, name: str, type: str, price: int, colour: str,
                 owner: Player = None):
        super().__init__(name, type)
        self.price = price
        self.colour = colour
        self.owner = owner
        self.rent = ceil(price * RENT_MULTIPLIER)

    def __str__(self):
        return (f"{self.type}: {self.name}, price: {self.price}, "
                f"colour: {self.colour}.")


class Board():
    """
    Represent a board of the game.

    Attributes:
        spaces (list[Space]): list of spaces on the board in game play order.
                                The first space is go.
        size (int): the number of spaces on the board
        sets (dict): stores different sets of properties of the same colour
    """
    def __init__(self, spaces: list[Space]):
        self.spaces = spaces
        self.size = len(spaces)

        # group properties by colour
        all_properties = [space for space in self.spaces
                          if isinstance(space, Property)]
        self.sets = dict()
        for property in all_properties:
            if property.colour in self.sets:
                self.sets[property.colour].append(property)
            else:
                self.sets[property.colour] = [property]

    def __str__(self):
        return "\n".join(str(space) for space in self.spaces)

    def calculate_rent(self, property: Property, log: list[str]) -> int:
        """
        Calculate the rent of the given property.
        """
        if property.owner is None:
            return 0

        # check if the owner of the property has the full set
        has_full_set = all(p.owner == property.owner
                           for p in self.sets[property.colour])
        # increase the rent if the owner has the full set
        if has_full_set:
            log.append(f"{property.owner.name} owns the whole set. "
                       f"Rent is multiplied by {FULL_SET_MULTIPLIER}.")
            return ceil(property.rent * FULL_SET_MULTIPLIER)
        return property.rent


class Game:
    """
    Represent the evolving state of a game.

    Attributes:
        board (Board): the game board containing spaces
        players (list[Player]): players participating the game in playing order
        current_player (Player): the player who is currently taking the turn
        current_player_index (int): the index of the current player
        is_over (bool): whether the game has ended, game ends when anyone of
                        the players is bankrupted
    """
    def __init__(self, board: Board):
        self.board = board
        self.players = [Player(name) for name in DEFAULT_PLAYERS]
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.is_over = False

    def end(self):
        """
        End the game if the game is over and print the result of the game.
        """
        if self.is_over:
            print(" Game is over! ".center(SEPERATOR_LENGTH, "~"))
            # find out which player(s) has(have) the most money remaining
            max_balance = max(player.balance for player in self.players)
            winners = [player for player in self.players
                       if player.balance == max_balance]

            # print who is the winner
            if len(winners) == 1:
                print(f"{winners[0].name} won the game.")
            else:
                print("There is a Tie!" + ", ".join(winner.name
                                                    for winner in winners)
                      + "won the game together!")

    def update(self, roll, log):
        """
        Apply the effect of the dice roll to the game state.
        """
        # get current player
        player = self.current_player

        # next posotion of the player if board is unwrapped
        unwrapped_position = player.position + roll

        # find how many time the player has past go
        pass_go_count = unwrapped_position // self.board.size
        for _ in range(pass_go_count):
            log.append(f"{player.name} got ${PASS_GO_BONUS} for passing GO.")
        # update player balance for passing go
        player.balance += pass_go_count * PASS_GO_BONUS

        # find the actual next position of the player and move the player
        player.position = unwrapped_position % self.board.size

        # get the space the player landed on
        landed_space = self.board.spaces[player.position]
        log.append(f"{player.name} landed on {landed_space.name}.")
        # check if the player landed on a property
        if isinstance(landed_space, Property):
            # buy the property if its not owned
            if landed_space.owner is None:
                log.append(f"{landed_space.name} is not owned by anyone.")
                player.balance -= landed_space.price
                landed_space.owner = player
                # check whether the player has bankrupted
                if player.balance < 0:
                    # game is over if bankrupted
                    self.is_over = True
                    log.append(f"{player.name} bankrupted when buying "
                               f"{landed_space.name} "
                               f"for ${landed_space.price}.")
                else:
                    log.append(f"{player.name} bought {landed_space.name} for "
                               f"${landed_space.price}.")

            # pay rent if the property is owned by someone else
            elif landed_space.owner is not player:
                log.append(f"{landed_space.name} is owned "
                           f"by {landed_space.owner.name}.")
                rent = self.board.calculate_rent(landed_space, log)
                player.balance -= rent
                landed_space.owner.balance += rent
                # check whether the player has bankrupted
                if player.balance < 0:
                    # game is over if bankrupted
                    self.is_over = True
                    log.append(f"{player.name} bankrupted when paying "
                               f"{landed_space.owner.name} ${rent} rent "
                               f"for {landed_space.name}.")
                else:
                    log.append(f"{player.name} paid {landed_space.owner.name} "
                               f"${rent} rent for {landed_space.name}.")

            # do nothing if the property is owned by the player themself
            elif landed_space.owner is player:
                log.append(f"{landed_space.name} is owned "
                           f"by {landed_space.owner.name}. "
                           "No rent needs to be paid.")
                # potential extension for building upgardes to increase rent

        if not self.is_over:
            # move to the next player if game is not over
            self.current_player_index = ((self.current_player_index + 1)
                                         % len(self.players))
            self.current_player = self.players[self.current_player_index]

    def __str__(self):
        """
        Create a string representing the state of game for printing.
        """
        board_heading = ["Type", "Name", "Owned By", "On Space"]
        board_print_cells = []
        for space in self.board.spaces:
            if isinstance(space, Go):
                space_print_cells = [space.type, space.name, ""]
            elif isinstance(space, Property):
                color_code = COLOURS[space.colour]
                color_reset = COLOURS["Reset"]
                if space.owner is None:
                    space_print_cells = [space.type,
                                         (f"{color_code}{space.name:^30}"
                                          f"{color_reset}"),
                                         ""]
                else:
                    space_print_cells = [space.type,
                                         (f"{color_code}{space.name:^30}"
                                          f"{color_reset}"),
                                         space.owner.name]
            board_print_cells.append(space_print_cells)

        players_heading = ["Name", "Balance"]
        players_print_cells = []
        players_on_space = dict()
        for player in self.players:
            players_print_cells.append([player.name, "$"
                                        + str(player.balance)])
            if player.position in players_on_space:
                players_on_space[player.position].append(player.name)
            else:
                players_on_space[player.position] = [player.name]

        board_str = ""
        for space_i in range(self.board.size):
            if space_i in players_on_space:
                players_on_space_i = players_on_space[space_i]
                board_row = (board_print_cells[space_i]
                             + [players_on_space_i[0]])
                board_str += BOARD_ROW_TEMPLATE.format(*board_row) + "\n"
                if len(players_on_space_i) > 1:
                    for player_on_space_i in players_on_space_i[1:]:
                        board_row = ["", "", "", player_on_space_i]
                        board_str += (BOARD_ROW_TEMPLATE.format(*board_row)
                                      + "\n")
            else:
                board_row = board_print_cells[space_i] + [""]
                board_str += BOARD_ROW_TEMPLATE.format(*board_row) + "\n"

        return (" Board ".center(SEPERATOR_LENGTH, "-") + "\n" +
                BOARD_ROW_TEMPLATE.format(*board_heading) + "\n" +
                board_str +
                " Players ".center(SEPERATOR_LENGTH, "-") + "\n" +
                PLAYER_ROW_TEMPLATE.format(*players_heading) + "\n" +
                "\n".join([PLAYER_ROW_TEMPLATE.format(*row)
                           for row in players_print_cells]))
