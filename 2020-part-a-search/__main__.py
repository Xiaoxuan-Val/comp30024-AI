import sys
import json

from util import print_move, print_boom, print_board


def main():
    
    with open(sys.argv[1]) as file:
        data = json.load(file)
        
    # TODO: find and print winning action sequence
    
    #load board
    #format new dictionary with (x, y) tuples as keys, " token number + w/b" as value.
    board_dict = {}
    blacktoken_dict = {}
    whitetoken_list = []
    position_dict = {}
    goal_list = []
    for key in data:
        if key == 'white':
            for token in data[key]:
                coords = (token[1],token[2])
                value = 'w' + str(token[0])
                board_dict.update({coords:value})
                whitetoken_list.append(coords)
        else:
            for token in data[key]:
                coords = (token[1],token[2])
                value = 'b' + str(token[0])
                board_dict.update({coords:value})
                blacktoken_dict.update({coords:value})
    coords = [(x,7-y) for y in range(8) for x in range(8)]
    for xy in coords:
        if xy not in board_dict:
            board_dict.update({xy:'0'})
            
    #for debug print   
                        
    #print(blacktoken_dict)
    print_board(board_dict, message="", unicode=True, compact=True)
    goal_list = search_goal_square(board_dict, blacktoken_dict)
    #print("goal list")
    print(goal_list)
    print(path_search(whitetoken_list[0], goal_list[0], blacktoken_dict))
    


#this function is used to count relative black token of a given position. 
#parameter point is a tuple (x, y) indicate position
def check_surrounding(blacktoken_dict, point):
    x = point[0]
    y = point[1]
    final_list = []
    temp_list = []
    blacktoken_number = 0
    
    nearest_tokenlist=[(x-1, y+1),(x, y+1),(x+1, y+1),
                       (x-1, y),(x+1, y),(x-1, y-1),(x, y-1),(x+1, y-1)]
    
    #remove points outside the board        
    index = len(nearest_tokenlist) - 1
    while index > 0 :
        if nearest_tokenlist[index][0] < 0 or nearest_tokenlist[index][1] < 0 or nearest_tokenlist[index][0] > 7 or nearest_tokenlist[index][1] > 7:
            del nearest_tokenlist[index]
        index = index - 1
    
    for p in nearest_tokenlist:
        if p in blacktoken_dict.keys():
            temp_list.append(p)  
    
    while len(temp_list) != 0 :
        temp_point = temp_list[0]
        
        final_list.append(temp_point)
        
        tempx = temp_point[0]
        tempy = temp_point[1]
        
        tempnearest_tokenlist=[(tempx-1, tempy+1),(tempx, tempy+1),(tempx+1, tempy+1),(tempx-1, tempy),
                           (tempx+1, tempy),(tempx-1, tempy-1),(tempx, tempy-1),(tempx+1, tempy-1)]
    
        for t in tempnearest_tokenlist:
            if t in blacktoken_dict.keys():
                if t not in temp_list and t not in final_list:
                    temp_list.append(t)        
        
        temp_list.remove(temp_point)
        
    #account total black token number affected by the tested position    
    for p in final_list:
        blacktoken_number += int(blacktoken_dict[p][1:])
        
    return (blacktoken_number, final_list)



#this function is used to find destination square list
def search_goal_square(board_dict,blacktoken_dict):
    blacktoken_dict_copy = blacktoken_dict.copy()
    
    goal_list = []
    
    while len(blacktoken_dict_copy) != 0: 
        
        best_point = (0 ,0)
        best_count = 0
        n = 0
        
        for p in board_dict:
            if board_dict[p] == '0':
                temp_result = check_surrounding(blacktoken_dict_copy, p)
                n = temp_result[0]
                if n > best_count:
                    best_count = n
                    best_point = p
        
        goal_list.append(best_point)
        
        result = check_surrounding(blacktoken_dict_copy, best_point)
        covered_blacktoken = result[1]
        
        #print(best_point)
        
        for p in covered_blacktoken:
            del blacktoken_dict_copy[p]
            
        #print(blacktoken_dict)
    
    return goal_list



def get_dist(g_dist, curr_pos, goal_pos):
    #using Manhattan distance as heuristic
    h_dist = abs(curr_pos[0]-goal_pos[0]) + abs(curr_pos[1]-goal_pos[1])
    f_dist = g_dist + h_dist  
    return f_dist

#find path to a position for a white token, using A star search
def path_search(whitetoken, goal_position, blacktoken_dict):

    
    #using a list to record position we have already reached
    path_list = [whitetoken]
    #a dictionary to record cost already spend for each point
    path_dict = {whitetoken: 0}
    #another list to record position that cannot go anywhere
    failedposition_list = []
    
    
    while path_list[-1]!= goal_position :
        
        #debug print
        #print("current point")
        #print(path_list[-1])
        
        
        #current location
        temp_pos = path_list[-1]
        
        x = temp_pos[0]
        y = temp_pos[1]
        
        g_dist =path_dict[temp_pos] + 1
        
        #valid next position
        possible_pos = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        
        #remove points outside the board and occupied by black tokens    
        index = len(possible_pos) - 1
        while index >= 0 :
            if possible_pos[index][0] < 0 or possible_pos[index][1] < 0 or possible_pos[index][0] > 7 or possible_pos[index][1] > 7 or (possible_pos[index] in blacktoken_dict):
                possible_pos.pop(index)
            index = index - 1
        
        #remove point already passed by
        for p in path_dict:
            if p in possible_pos:
                possible_pos.remove(p)
        #remove position already failed
        for p in failedposition_list:
            if p in possible_pos:
                possible_pos.remove(p)
        #if no possible next position
        if len(possible_pos) == 0:
            failedposition_list.append(path_list.pop())
            continue
        #sort possible next positions by estimated total cost f
        next_point = possible_pos[0]
        min_dist = get_dist(g_dist, next_point, goal_position)
        for p in possible_pos:
            #for debug
            #print(p)
            #print(get_dist(g_dist, p, goal_position))
            if get_dist(g_dist, p, goal_position) < min_dist:
                next_point = p
                min_dist = get_dist(g_dist, p, goal_position)
        
        path_list.append(next_point)
        path_dict.update({next_point:g_dist})
        
        #debug
        #print(path_list)
          
    return path_list



if __name__ == '__main__':
    main()
