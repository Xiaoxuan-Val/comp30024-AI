
class Player:
    gamestate = {}
    colour = 'none'
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        self.colour = colour
        initial_white = [(0,0),(1,0),(3,0),(4,0),(6,0),(7,0),
                         (0,1),(1,1),(3,1),(4,1),(6,1),(7,1)]
        initial_black = [(0,6),(1,6),(3,6),(4,6),(6,6),(7,6),
                         (0,7),(1,7),(3,7),(4,7),(6,7),(7,7)]
        for x in range(0,7):
            for y in range(0,7):
                if (x,y) in initial_white:
                    self.gamestate[(x,y)] = ['white',1]
                elif (x,y) in initial_black:
                    self.gamestate[(x,y)] = ['black',1]
                else:
                    self.gamestate[(x,y)] = ['none',0]

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        return ("BOOM", (0, 0))


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
