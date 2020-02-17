# ;==================================================================
# ; Title:  A* Algorithm using manhattan distance and misplaced tiles
# ; Author: Bhanu Prakash Reddy ,Satabdhi Reddy
# ; Date:   10 Feb 2019

# ;==================================================================
import numpy as np
from copy import deepcopy
import collections

print("enter input by giving spaces example:1 2 3 4 5 6 7 8 0 ")
initial_node = list(map(int,input("Enter Input node:").split()))               #input initial node
initial_node = np.array(initial_node)
final_node = list(map(int,input("Enter Output node:").split()))                #input final node
final_node = np.array(final_node)
Astarmethod=0      #flag for manhatton or misplaced tiles Astarmethod=0 manhattan 1 for misplaced tiles


# definition to calculate hn using manhattan distance
def manhattan_distance(mlist):
    copy = mlist
    mhtndist = 0
    for i, list_item in enumerate(copy):
        if list_item != 0:
            for j,list_item_final in enumerate(final_node):
                if list_item_final == list_item:
                    lr = j
                    break
            row1,col1 = int(i/ 3) , i% 3
            row2,col2 = int((lr) / 3), (lr) % 3
            mhtndist += abs(row1-row2) + abs(col1 - col2)
    return mhtndist

#definition to calculate hn using misplaced tiles
def misplaced_tiles(mlist):
    copy = mlist
    mis_dist=0
    for i, list_item in enumerate(copy):
        if list_item != 0 and final_node[i] != list_item:
            mis_dist = mis_dist+1
    return  mis_dist

#definition to calculate successor nodes of the node to be expanded
def successorNodes(board):
    global open_struct_array
    global closed_struct_array
    global nodeid
    moves = np.array(
        [
            ([0, 1, 2], -3),
            ([6, 7, 8], 3),
            ([0, 3, 6], -1),
            ([2, 5, 8], 1)
        ],
        dtype=[
            ('pos', list),
            ('ind', int)
        ]
    )

    gn=board[1]+1
    state = board[0]
    loc = int(np.where(state == 0)[0])
    parentid=board[4]
    for m in moves:
        if loc not in m['pos']:
            nodepresent = 0
            succ = deepcopy(state)
            delta_loc = loc + m['ind']
            succ[loc], succ[delta_loc] = succ[delta_loc], succ[loc]

            for i in closed_struct_array:             #checking if successor nodes are duplicates
                if(i[0]==succ).all():
                    nodepresent = 1

            for i in open_struct_array:               #checking if successor nodes are duplicates
                if (i[0] == succ).all():
                    nodepresent = 1

            if nodepresent == 0:
                #print("inloop")

                if (Astarmethod == 0):
                    hn = manhattan_distance(succ)
                else:
                    hn = misplaced_tiles(succ)
                fn=gn + hn
                nodeid=nodeid+1                            #increment value of nodeid for each node genereated
                #appending successor nodes to open_struct_array
                open_struct_array=np.append(open_struct_array, np.array([(succ, gn, hn, fn, nodeid, parentid)], STATE), 0)

#definition to check if the node is final node
def solution(board):
    global STATE
    STATE = [
        ('board', list),
        ('gn', int),
        ('hn', int),
        ('fn', int),
        ('nodeid',int),
        ('parentid',int)
    ]
    global open_struct_array
    global closed_struct_array
    global nodeid
    nodeid = 0
    if(Astarmethod==0):
        hn=manhattan_distance(board)
    else:
        hn=misplaced_tiles(board)
    open_struct_array = np.array([(board, 0, hn, 0 + hn, 0, -1)], STATE)

    varran=np.array([0,0,0,0,0,0,0,0,0])                                      #closed struct array 1 time initialization
    closed_struct_array=np.array([(varran, 0, 0, 0, 0, 0)], STATE)
    closed_struct_array=np.delete(closed_struct_array, 0, 0)

    while True:
        length_queques = len(open_struct_array) + len(closed_struct_array)    #checking if total nodes are crossing the threshold value
        if length_queques >3000:
            break
        a=open_struct_array[0]
        s=a[0]
        if (s == final_node).all():                    #comparing with final node
            return len(closed_struct_array), nodeid
        open_struct_array = np.delete(open_struct_array, 0, 0)
        closed_struct_array=np.append(closed_struct_array, np.array([(a[0], a[1], a[2], a[3], a[4], a[5])], STATE), 0) #appending expanded node to closed node
        successorNodes(a)
        open_struct_array = np.sort(open_struct_array, kind='mergesort', order=['fn', 'nodeid'])  #sorting bosed on
    return 0,0

#definition to find the path of the final node
def solutionpath(open_structured_array, closedNode):
    storelastelement = open_structured_array[0][0]
    parentidd=open_structured_array[0][5]
    con = np.concatenate((open_structured_array, closedNode), axis=0)
    de = collections.deque([])
    de.append(storelastelement)
    while(parentidd != -1):
        for i in con:
            if i[4] == parentidd:
                de.appendleft(i[0])
                parentidd = i[5]
                break
    print('cost to reach final_node:',len(de)-1)

    for i in de:
        print(np.reshape(i,(3,3)),'\n')

#definintion to print output using both manhattan distance and misplaced tiles as hn
def main():
    global open_struct_array
    global closed_struct_array
    global Astarmethod


    comparearrays = (np.sort(initial_node) == np.sort(final_node)).all()     #checking if input is correct
    if not comparearrays:
        print('incorrect input')
        return
    else:
        nodes_expanded,nodes_generated=solution(initial_node)                #if correct input find path
        if(nodes_expanded==0 and nodes_generated ==0):
            print('no solution')
            return
    print("--------------------------------A* Manhattan DIstance-------------------------------------------")
    # print(open_struct_array)
    # print(closed_struct_array)
    print('nodes_generated:',nodes_generated)
    print('nodes_expanded',nodes_expanded)

    solutionpath(open_struct_array, closed_struct_array)         #finding solution path hn= manhattan distance
    print("-------------------------------A* Misplaced Tiles-------------------------------------------------")
    Astarmethod=1                                                #set Astarmethod=1
    open_struct_array=[]                                         #empty both open and closed
    closed_struct_array=[]
    nodes_expanded, nodes_generated = solution(initial_node)
    if (nodes_expanded == 0 and nodes_generated == 0):           #return 0,0 if no solution
        print('no solution')
        return
    # print(open_struct_array)
    # print(closedNode)
    print('nodes_generated:',nodes_generated)
    print('nodes_expanded',nodes_expanded)
    solutionpath(open_struct_array, closed_struct_array)          #finding solution path hn=misplaced tiles


if __name__ == "__main__":
    main()

