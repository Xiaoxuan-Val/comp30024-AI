from random import shuffle

class ExamplePlayer:
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
        
        if colour == 'white':
            #record self tokens in format of (x,y): token number in a dict.
            self.tokens = {(0,0): 1, (0,1): 1, (1,0): 1, (1,1): 1,
                           (3,0): 1, (4,0): 1, (3,1): 1, (4,1): 1,
                           (6,0): 1, (7,0): 1, (6,1): 1, (7,1): 1}
            
            self.op_tokens = {(0,6): 1, (0,7): 1, (1,6): 1, (1,7): 1,
                              (3,6): 1, (3,7): 1, (4,6): 1, (4,7): 1,
                              (6,6): 1, (6,7): 1, (7,6): 1, (7,7): 1}
            
        else:
            self.op_tokens = {(0,0): 1, (0,1): 1, (1,0): 1, (1,1): 1,
                           (3,0): 1, (4,0): 1, (3,1): 1, (4,1): 1,
                           (6,0): 1, (7,0): 1, (6,1): 1, (7,1): 1}
            
            self.tokens = {(0,6): 1, (0,7): 1, (1,6): 1, (1,7): 1,
                              (3,6): 1, (3,7): 1, (4,6): 1, (4,7): 1,
                              (6,6): 1, (6,7): 1, (7,6): 1, (7,7): 1}
            
        self.all_pos ={(x,y) for x in range(0,8) for y in range(0,8)}
        
        self.state = State(self.tokens, self.op_tokens)
        #using magic number here for draft, will fix this later
        self.max_depth = 3

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        eval_score, selected_action = self._minimax(0, self.state, True, float('-inf'),float('inf'))
        
        return selected_action
        
        #return ("BOOM", (0, 0))


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
        self.state.apply_action(action)
        
    
    def _minimax(self, current_depth, state, is_max_turn, alpha, beta): 
        
        action_target = ()
        
        if current_depth ==self.max_depth or state.is_terminal():
            score = 0
            score = self.evaluation(state)
            return score, action_target
        
        possible_actions = state.legal_actions()
        
        shuffle(possible_actions)
        best_value = float('-inf') if is_max_turn else float('inf')
        
        
        for action in possible_actions:
            
            new_state = state.apply_action(action)
            
            eval_child, action_child = self._minimax(current_depth+1,new_state,not is_max_turn, alpha, beta)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, action_target
        
             
    
    
    def evaluation(self,state):
        
        if state.is_terminal():
            if state.tokens == {}:
                return 1000
            else:
                return -1000
        
        eval_value = 0
        
        eval_value = 100*(len(state.tokens))-100*(len(state.op_tokens))
        return eval_value
                
    
    
     

       
   
class State:
    
    def __init__(self, tokens, op_tokens):
            self.tokens = tokens
            self.op_tokens = op_tokens
            self.all_pos ={(x,y) for x in range(0,8) for y in range(0,8)}
            
    def legal_actions(self):
        
        legal_action_list =[]
        dist = 0
        for position in self.tokens:
            legal_action_list.append(("BOOM", position))
            
            dist = self.tokens[position]
            x_pos = position[0]
            y_pos = position[1]
            for step in range(1, dist+1):
                for i in range(1, step+1):
                    
                    for pos in ((x_pos+i, y_pos),(x_pos-i, y_pos),(x_pos, y_pos+i),(x_pos, y_pos-i)):
                        if pos in self.all_pos and pos not in self.op_tokens:
                            legal_action_list.append(("MOVE", i, position, pos))
        return legal_action_list
     
    #this function is used to count relative black token of a given position. 
    #parameter point is a tuple (x, y) indicate position
    def check_surrounding(self, tokens, op_tokens, point):
        x = point[0]
        y = point[1]
        final_list = []
        temp_list = []
        
        nearest_tokenlist=[(x-1, y+1),(x, y+1),(x+1, y+1),
                           (x-1, y),(x+1, y),(x-1, y-1),(x, y-1),(x+1, y-1)]
        
        #remove points outside the board        
        index = len(nearest_tokenlist) - 1
        while index > 0 :
            if nearest_tokenlist[index][0] < 0 or nearest_tokenlist[index][1] < 0 or nearest_tokenlist[index][0] > 7 or nearest_tokenlist[index][1] > 7:
                del nearest_tokenlist[index]
            index = index - 1
        
        for p in nearest_tokenlist:
            if p in tokens.keys() or p in op_tokens.keys():
                temp_list.append(p)  
        
        while len(temp_list) != 0 :
            temp_point = temp_list[0]
            
            final_list.append(temp_point)
            
            tempx = temp_point[0]
            tempy = temp_point[1]
            
            tempnearest_tokenlist=[(tempx-1, tempy+1),(tempx, tempy+1),(tempx+1, tempy+1),(tempx-1, tempy),
                               (tempx+1, tempy),(tempx-1, tempy-1),(tempx, tempy-1),(tempx+1, tempy-1)]
        
            for t in tempnearest_tokenlist:
                if t in tokens.keys() or t in op_tokens.keys():
                    if t not in temp_list and t not in final_list:
                        temp_list.append(t)        
            
            temp_list.remove(temp_point)
                
        return final_list
    
    
    
    def apply_action(self, action):
         
        if(action[0]=="BOOM"):
            remove_list =[]
            remove_list = self.check_surrounding(self.tokens, self.op_tokens, action[1])
            
            for pos in remove_list:
                if pos in self.tokens:
                    self.tokens.pop(pos)
                elif pos in self.op_tokens:
                    self.op_tokens.pop(pos)
            ###### not sure whether is is correct       
            return State(self.tokens, self.op_tokens)
        else:
            ##for debug
            print()
            print(action)
            self.tokens[action[2]] -= action[1]
            if (action[3] not in self.tokens.keys()):
                self.tokens[action[3]] = action[1]
            else:
                self.tokens[action[3]] += action[1]
            
            return State(self.tokens, self.op_tokens)
            
                  
       
    def is_terminal(self):
        if (self.tokens == {} or self.op_tokens == {}):
            return True
        return False               
                
                
                
    
        

