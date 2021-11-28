import numpy as np
import csv
from collections import deque



#Stock: List of lists
#Talon: Not relevant
#Foundation: List of deques
#Tableau: List of lists of deques of lists (the cards)

def state_setter(file='C:/Users/jacob/Documents/Classes/EECS592/test_state_11_26.csv'):

    with open(file,newline='') as csvfile:
        data = csv.reader(csvfile)
        rows = list(data)
    
    
    bin_indxs = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37]
    for bindx in bin_indxs:
        indexer = 0
    
        if rows[bindx][0] != '':
    
            while True:
                if len(rows[bindx]) > 1 and rows[bindx][indexer] == '':
                    rows[bindx].pop(indexer)
                else:
                    indexer += 1
                    
                
                if indexer + 1 > len(rows[bindx]):
                    break
    
    
    
    #Read stock
    stock = []
    if rows[1][0] != '':
        for i in range(int(len(rows[1]) / 2)):
            stock.append([rows[1][2*i], rows[1][2*i + 1]])
        
    
    #Read talon (line 4)
    talon = []
    if rows[4][0] != '':
        for i in range(int(len(rows[4]) / 2)):
            talon.append([rows[4][2*i], rows[4][2*i + 1]])
    
    #Read foundation (lines 7-16)
    foundation1 = deque() #for spades
    foundation2 = deque() #for clubs
    foundation3 = deque() #for hearts
    foundation4 = deque() #for diamonds
    foundation = [foundation1,foundation2,foundation3,foundation4]
    
    found_idxs = [7, 10, 13, 16]
    for found_num, stack_idx in enumerate(found_idxs):
    
        if rows[stack_idx][0] != '':
            for i in range(int(len(rows[stack_idx]) / 2)):
    
                foundation[found_num].append([rows[stack_idx][2*i], rows[stack_idx][2*i + 1]])
    
    
    #Read tableau
    tab1 = [deque(), deque()]
    tab2 = [deque(), deque()]
    tab3 = [deque(), deque()]
    tab4 = [deque(), deque()]
    tab5 = [deque(), deque()]
    tab6 = [deque(), deque()]
    tab7 = [deque(), deque()]
    tableau = [tab1, tab2, tab3, tab4, tab5, tab6, tab7]
    tab_idxs = [19, 22, 25, 28, 31, 34, 37]
    
    for tab_num, stack_idx in enumerate(tab_idxs):
        flipped = False
        if rows[stack_idx][0] != '': #Make sure not empty tableau stack
            
            if len(rows[stack_idx]) % 2 == 0: #All faceup tableau stack
            
                for i in range(int(len(rows[stack_idx]) / 2)):
                    tableau[tab_num][0].append([rows[stack_idx][2*i], rows[stack_idx][2*i + 1]])
    
                    
            else: #Some facedown cards
                i = 0
                while i < len(rows[stack_idx]):
                    if not flipped:
                    
                        if rows[stack_idx][2*i] == 'FLIP':
                            flipped = True
                            i = i*2 + 1
                        else: #Append to faceup deque
                            tableau[tab_num][0].append([rows[stack_idx][2*i], rows[stack_idx][2*i + 1]])
                            i += 1
                    else: #Append to facedown deque
                        tableau[tab_num][1].append([rows[stack_idx][i], rows[stack_idx][i + 1]])
                        i += 2

    return [stock, foundation, tableau]


        
        