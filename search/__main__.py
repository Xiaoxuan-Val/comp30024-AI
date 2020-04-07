import sys
import json

from search.util import print_move, print_boom, print_board


def main():
    
    with open(sys.argv[1]) as file:
        data = json.load(file)
        
    board_dict = {}
    blacktoken_dict = {}
    whitetoken_dict = {}
    position_dict = {}
    goal_list = []
    
    #format new dictionary with (x, y) tuples as keys, " token number + w/b" as value.
    for key in data:
        if key == 'white':
            for token in data[key]:
                coords = (token[1],token[2])
                value = 'w' + str(token[0])
                board_dict.update({coords:value})
                whitetoken_dict.update({coords:value})
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
                               
    goal_list = search_goal_square(board_dict, blacktoken_dict, whitetoken_dict)
    
    #for each goal point, evaluate its nearest white token and generate a path
    temp_wtlist = list(whitetoken_dict.keys())
    for g in goal_list:
        wt =[]
        min_dist = 1000
        for wti in temp_wtlist:
            temp_d = distance_evaluation(g, wti)
            if temp_d < min_dist:
                min_dist = temp_d
                wt = wti
        temp_wtlist.remove(wt)
        
        #generate path search between this goal point and the white token
        path_result = path_search(wt,g,blacktoken_dict)
        
        #print the result
        print_path(path_result)



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
def search_goal_square(board_dict,blacktoken_dict, whitetoken_dict):
    
    blacktoken_dict_copy = blacktoken_dict.copy()
    board_dict_copy = board_dict.copy()
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
                    #check whether reachable for white tokens
                    reachable_flag = 0
                    for wt in whitetoken_dict:
                        if (path_search(wt, p, blacktoken_dict_copy)!= []):
                            reachable_flag = 1
                    if reachable_flag == 1:
                        best_count = n
                        best_point = p 
        
        goal_list.append(best_point)
        
        result = check_surrounding(blacktoken_dict_copy, best_point)
        covered_blacktoken = result[1]
        
        
        for p in covered_blacktoken:
            del blacktoken_dict_copy[p]
            

    
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
             #no solution path
            if len(path_list) == 0:
                return []
            continue
        #sort possible next positions by estimated total cost f
        next_point = possible_pos[0]
        min_dist = get_dist(g_dist, next_point, goal_position)
        for p in possible_pos:
            if get_dist(g_dist, p, goal_position) < min_dist:
                next_point = p
                min_dist = get_dist(g_dist, p, goal_position)
        
        path_list.append(next_point)
        path_dict.update({next_point:g_dist})
        
        
    return path_list
    
#Manhattan distance 
def distance_evaluation(pos0,pos1):
    return abs(pos1[0]-pos0[0])+abs(pos1[1]-pos0[1])

#given a list of points in a path, print it as a sequence of moves [unfinished]
def print_path(path_list):
    for i in range(0,len(path_list)-1):
        print_move(1,path_list[i][0],path_list[i][1],path_list[i+1][0],path_list[i+1][1])
    print_boom(path_list[-1][0],path_list[-1][1])
    return

if __name__ == '__main__':
    main()
