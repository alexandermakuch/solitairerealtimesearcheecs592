import numpy as np
from collections import deque
from deckGenerator import State


def opp_color_check(c1: str, c2: str):
    diff_colors = False
    
    #Card 1 is red, Card 2 is black
    if (c1[0] == 'H' or c1[0] == 'D') and (c2[0] == 'S' or c2[0] == 'C'):
        diff_colors = True
    
    #Card 1 is black, Card 2 is red
    if (c1[0] == 'S' or c1[0] == 'C') and (c2[0] == 'H' or c2[0] == 'D'):
        diff_colors = True
    
    return diff_colors

def get_actions_revB(s:State):
    actions = []
    
    #See where Talon cards can be moved:
    for tal_idx, card in enumerate(s.reachable_talon):
        #Talon to tableau
        for tab_idx, stack in enumerate(s.tableau):
            if stack[0]:
                if opp_color_check(card, stack[0][0]) and stack[0][0][1] - card[1] == 1:
                     new_entry = {'from':[0, tal_idx], 'to':[1,tab_idx,0]}
                     actions.append(new_entry)
            elif card[1] == 13: #King
                print("elif")
                new_entry = {'from':[0,tal_idx], 'to':[1,tab_idx,0]}
                actions.append(new_entry)
        #Talon to foundation
        for found_idx, stack in enumerate(s.foundation):
            if stack: #Make sure there's cards in the stack
                if stack[0][0] == card[0] and stack[0][1] - card[1] == -1: #If suits match and proper next card
                    new_entry = {'from':[0,tal_idx], 'to':[2,found_idx]}
                    actions.append(new_entry)
            else: #No cards in foundation stack
                if card[1] == 1: #is ace
                    if found_idx == 0:
                        suit = 'D'
                    elif found_idx == 1:
                        suit = 'C'
                    elif found_idx == 2:
                        suit = 'H'
                    elif found_idx == 3:
                        suit = 'S'
                    
                    if card[0] == suit: #Matchs stack suit
                        new_entry = {'from':[0,tal_idx], 'to':[2,found_idx]}
                        actions.append(new_entry)
                    
 #-------------------------------------------------------------------------------------------------------               
    #See where tableau cards/stacks can be moved to
    for stack_idx, stack in enumerate(s.tableau): #For each stack
        #Tableau to tableau:
        for stack_depth in range(len(stack[0])): #For each card in a face up stack
            card = stack[0][stack_depth]
            
            for si2, stack2 in enumerate(s.tableau): #Iterate through each card in stack
                if stack2[0]:
                    if opp_color_check(card,stack2[0][0]) and stack2[0][0][1] - card[1] == 1:
                        #Append a card if stack_depth = 0, append a bundle of cards starting from stack_depth
                        #if stack_depth > 0
                        new_entry = {'from':[1,stack_idx,stack_depth], 'to':[1,si2,0]}
                        actions.append(new_entry)
                elif card[1] == 13: #Empty stack, and king
                    new_entry = {'from':[1,stack_idx,stack_depth], 'to':[1,si2,0]}
                    actions.append(new_entry)
            #If next card in stack can't be moved, stop looping through stack
            if stack_depth < len(stack[0])-1:
                if stack[0][stack_depth+1][1] - stack[0][stack_depth][1] != 1: 
                    break
                    
    
        #Tableau to foundation:
        if stack[0]:
            for found_idx, found_stack in enumerate(s.foundation):
                if found_stack: #Verify it's not empty
                    if stack[0][0][0] == found_stack[0][0] and stack[0][0][1] - found_stack[0][1] == 1:
                        new_entry = {'from':[1,stack_idx,0], 'to':[2,found_idx]}
                        actions.append(new_entry)
                else: #Empty foundation stack
                    if stack[0][0][1] == 1: #Is ace
                        if found_idx == 0:
                            suit = 'D'
                        elif found_idx == 1:
                            suit = 'C'
                        elif found_idx == 2:
                            suit = 'H'
                        elif found_idx == 3:
                            suit = 'S'
                        
                    
                        if stack[0][0][0] == suit: #Matchs stack suit
                            new_entry = {'from':[1,stack_idx,0], 'to':[2,found_idx]}
                            actions.append(new_entry)
                        
 #------------------------------------------------------------------------------------------------------- 
    #See where foundation cards can be moved to
    for stack_idx, stack in enumerate(s.foundation):
        #Foundation to tableau
        if stack:
            for tab_idx, tab_stack in enumerate(s.tableau):
                if tab_stack[0]: #Nonempty tableau stack
                    if opp_color_check(stack[0][0], tab_stack[0][0][0]) and tab_stack[0][0][1] - stack[0][1] == 1:
                        #Move card from foundation to end of a tableau stack
                        new_entry = {'from':[2,stack_idx], 'to':[1,tab_idx,0]}
                        #actions.append(new_entry)
                else: #Empty tableau stack
                    if stack[0][1] == 13:
                        new_entry = {'from':[2,stack_idx], 'to':[1,tab_idx,0]}
                        #actions.append(new_entry)
    return actions
    #return prune_actions(s, actions)

def loopChecker(a, b):
    """ Use only when elements are neither hashable nor sortable! """
    unmatched = list(b)
    for element in a:
        try:
            unmatched.remove(element)
        except ValueError:
            return False
    return not unmatched



def get_actions_supreme(s: State, history: deque, history_limit=2):
    actions = get_actions_revB(s)

    loop = False
    if len(history) > history_limit:
        for b in history:
            if loopChecker(actions, b):
                loop= True
    else:
        history.append(actions)
        return actions, history

    if loop:
        print("Loop Detected")
        return [], history
    else:
        history.append(actions)
        return actions, history