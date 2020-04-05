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
    position_dict = {}
    for key in data:
        if key == 'white':
            for token in data[key]:
                coords = (token[1],token[2])
                value = 'w' + str(token[0])
                board_dict.update({coords:value})
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
            
    
                        
    print(board_dict)
    print(blacktoken_dict)
    print_board(board_dict, message="", unicode=True, compact=True)
    print(search_goal_square(board_dict, blacktoken_dict))
    


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
        if nearest_tokenlist[index][0] < 0 and nearest_tokenlist[index][1] < 0 and nearest_tokenlist[index][0] > 7 and nearest_tokenlist[index][1] > 7:
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
    
    goal_list = []
    
    while len(blacktoken_dict) != 0: 
        
        best_point = (0 ,0)
        best_count = 0
        n = 0
        
        for p in board_dict:
            if board_dict[p] == '0':
                temp_result = check_surrounding(blacktoken_dict, p)
                n = temp_result[0]
                if n > best_count:
                    best_count = n
                    best_point = p
        
        goal_list.append(best_point)
        
        result = check_surrounding(blacktoken_dict, best_point)
        covered_blacktoken = result[1]
        
        #print(best_point)
        
        for p in covered_blacktoken:
            del blacktoken_dict[p]
            
        #print(blacktoken_dict)
    
    return goal_list


if __name__ == '__main__':
    main()
