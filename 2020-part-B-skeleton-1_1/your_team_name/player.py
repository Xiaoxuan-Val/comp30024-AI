class ExamplePlayer:
    gamestate = {}
    colour = 'none'
    enemy_colour = 'none'
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
        # Set up state representation.
        self.colour = colour
        if colour == 'white':
            self.enemy_colour = 'black'
        else:
            self.enemy_colour = 'white'
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
        # Update state representation in response to action.
        self.gamestate = apply_action(self.gamestate,action)
    
    # Since there are initialliy 12 tokens of each side on the board, 
    # the evaluation score will be in between 0 and 12
    def evaluation(self,state):
        selftoken_num = 0
        enemytoken_num = 0
        #count tokens
        for valuepair in state.values():
            if valuepair[0] == self.colour:
                selftoken_num += valuepair[1]
            elif valuepair[0] == self.enemy_colour:
                enemytoken_num += valuepair[1]
        return selftoken_num - enemytoken_num
    
    def isGameEnd(state):
        whitetoken_num = 0
        blacktoken_num = 0
        #count tokens
        for valuepair in state.values():
            if valuepair[0] == 'white':
                whitetoken_num += valuepair[1]
            elif valuepair[0] == 'black':
                blacktoken_num += valuepair[1]
        
        if whitetoken_num == 0 or blacktoken_num == 0:
            return True
        return False
    
    # given  a state and an action (in the for of a tuple as the assignment spec),
    # applies the action on the state and return the result state
    # (the input action is assumed to be a legal action)
    def apply_action(state,action):
        resultstate = state
        if action[0] == "MOVE":
            # move action
            curr_loc = resultstate[action[2]]
            if curr_loc[1] - action[1] == 0:
                resultstate[action[2]] = ['none',0]
            else:
                resultstate[action[2]] = [curr_loc[0],curr_loc[1] - action[1]]
            goal_loc = resultstate[action[3]]
            resultstate[action[3]] = [goal_loc[0],goal_loc[1] + action[1]]
        if action[0] == "BOOM":
            # boom action
            boom_loc = resultstate[action[1]]
            resulestate = recursive_boom(state,boom_loc)
        
        return resultstate
    
    # a recursive function used to apply boom action to a given point on the state
    def recursive_boom(state,location):
        # get the list of legal points within 3x3 area of the input location
        surroundings = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        slist = []
        for s in surroundings:
            newpoint = (location[0]+s[0],location[1]+s[1])
            if newpoint[0]>=0 and newpoint[0]<=7 and newpoint[1]>=0 and newpoint[1]<=7:
                result.append(newpoint)
        
        newstate = state
        # remove tokens on the centre of boom
        newstate[location] = ['none',0]
        # remove tokens in the area of boom
        for p in slist:
            if newstate[p][1] > 0:
                newstate = recursive_boom(newstate,p)
        return newstate
    
    # given a state and color of a player, 
    # return all possible legal moves the player can do on next turn
    def possible_actions(colour,state):
        #if game ends at this state, no need to move anymore
        if isGameEnd(state):
            return []
        
        possibleactions = []
        #loop through all blocks with tokens of this player's side
        for block in state:
            coor_x = block[0]
            coor_y = block[1]
            if state[block][0] == colour:
                # There're tokens of the player's side on this block
                n_tokens = state[block][1] # the num of tokens on the location
                for n in range(1,n_tokens+1):
                    # move n tokens from the stack
                    possible_goals = [(coor_x-n,coor_y),(coor_x+n,coor_y),
                                      (coor_x,coor_y-n),(coor_x,coor_y+n)]
                    for goal in possible_goals:
                        if goal[0]>=0 and goal[0]<=7 and goal[1]>=0 and goal[1]<=7 and (state[goal][0] == colour or state[goal][0] == 'none'):
                            possibleactions.append(("MOVE",n,block,goal))
                possibleactions.append(("BOOM",block))
        return possibleactions
                    
                    
                