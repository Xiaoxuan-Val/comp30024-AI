from random import shuffle
from copy import deepcopy

class ExamplePlayer:
    def __init__(self, colour):
        
        self.colour = colour      
        self.board = Board(self.colour)
        self.state = State(self.board)
        #using magic number here for draft, will fix this later
        self.max_depth = 3

    def action(self):
        
        eval_score, selected_action = self._minimax(0, self.state, True, float('-inf'),float('inf'))
        
        return selected_action
        
        #return ("BOOM", (0, 0))


    def update(self, colour, action):
        
        self.board.update_board(action)
        self.state.board = self.board
        
    
    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):      
        
        action_target = ()
        possible_actions = state.legal_actions()
        shuffle(possible_actions)
        
        
        best_value = float('-inf') if is_max_turn else float('inf')
        
        #print("---------------------")
        #print()
        #print(state.board.tokens)
        #print()
        #print(possible_actions)
        #print("---------------------")
        
        
        
        for action in possible_actions:
            
            new_state = state.apply_action(action)
            
            if current_depth ==self.max_depth or state.is_terminal():
                action_target = action
                score = 0
                score = self.evaluation(state)
                return score, action_target
            
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
            if state.board.tokens == {}:
                return 1000
            else:
                return -1000
        
        eval_value = 0
        
        eval_value = 100*(len(state.board.tokens))-100*(len(state.board.op_tokens))
        return eval_value
                
    

class Board:
    
    def __init__(self, colour): 
        
        self.colour = colour
        #record self tokens in format of (x,y): token number in a dict.
        self.white_tokens = {(0,0): 1, (0,1): 1, (1,0): 1, (1,1): 1,
                       (3,0): 1, (4,0): 1, (3,1): 1, (4,1): 1,
                       (6,0): 1, (7,0): 1, (6,1): 1, (7,1): 1}
            
        self.black_tokens = {(0,6): 1, (0,7): 1, (1,6): 1, (1,7): 1,
                          (3,6): 1, (3,7): 1, (4,6): 1, (4,7): 1,
                          (6,6): 1, (6,7): 1, (7,6): 1, (7,7): 1}   
        if colour == 'white':
            self.tokens = self.white_tokens
            self.op_tokens = self.black_tokens
        else:
            self.op_tokens = self.white_tokens
            self.tokens = self.black_tokens
            
        self.all_pos ={(x,y) for x in range(0,8) for y in range(0,8)}
        
    #this function is used to count relative tokens of a given position. 
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
    
    def update_board(self, action):
        
        if(action[0]=="BOOM"):
            
            remove_list =[]
            remove_list = self.check_surrounding(self.tokens, self.op_tokens, action[1])
            for pos in remove_list:
                if pos in self.tokens:
                    self.tokens.pop(pos)
                elif pos in self.op_tokens:
                    self.op_tokens.pop(pos)
        else:
            if action[2] in self.tokens.keys():
                self.tokens[action[2]] -= action[1]
                if(self.tokens[action[2]]==0):
                    self.tokens.pop(action[2])
                
                if (action[3] not in self.tokens.keys()):
                    self.tokens[action[3]] = action[1]
                else:
                    self.tokens[action[3]] += action[1]
            else:
                self.op_tokens[action[2]] -= action[1]
                if(self.op_tokens[action[2]]==0):
                    self.op_tokens.pop(action[2])
                
                if (action[3] not in self.op_tokens.keys()):
                    self.op_tokens[action[3]] = action[1]
                else:
                    self.op_tokens[action[3]] += action[1]
                
                       
        
    
   
class State:
    
    def __init__(self, board):
            self.board = board
            
    def legal_actions(self):
        
        legal_action_list =[]
        dist = 0
        for position in self.board.tokens:
            
            legal_action_list.append(("BOOM", position))
            
            dist = self.board.tokens[position]
            x_pos = position[0]
            y_pos = position[1]
            for step in range(1, dist+1):
                for i in range(1, step+1):
                    for pos in ((x_pos+i, y_pos),(x_pos-i, y_pos),(x_pos, y_pos+i),(x_pos, y_pos-i)):
                        if pos in self.board.all_pos and pos not in self.board.op_tokens:
                            legal_action_list.append(("MOVE", i, position, pos))
                            
         ##debug
         
        return legal_action_list
        
  
    ##for evaluation in minimax algorithm
    def apply_action(self, action):
        
        ##for debug
        #print()
        #print(action)
        
        new_state = deepcopy(self)
         
        if(action[0]=="BOOM"):
            remove_list =[]
            remove_list = new_state.board.check_surrounding(new_state.board.tokens, new_state.board.op_tokens, action[1])
            
            for pos in remove_list:
                if pos in new_state.board.tokens:
                    new_state.board.tokens.pop(pos)
                elif pos in new_state.board.op_tokens:
                    new_state.board.op_tokens.pop(pos)    
            return new_state
        else:
            
            new_state.board.tokens[action[2]] -= action[1]
            if(new_state.board.tokens[action[2]]== 0):
                new_state.board.tokens.pop(action[2])
            
            if (action[3] not in new_state.board.tokens.keys()):
                new_state.board.tokens[action[3]] = action[1]
            else:
                new_state.board.tokens[action[3]] += action[1]
            
            return new_state
                
    def is_terminal(self):
        if (self.board.tokens == {} or self.board.op_tokens == {}):
            return True
        return False               
                
                
                
    
        

