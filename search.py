import numpy as np

def opp_color_check(c1, c2):
    diff_colors = False
    
    #Card 1 is red, Card 2 is black
    if c1[0] == 'H' or c1[0] == 'D' and c2[0] == 'S' or c2[1] == 'C':
        diff_colors = True
    
    #Card 1 is black, Card 2 is red
    if c1[0] == 'S' or c1[0] == 'C' and c2[0] == 'H' or c2[1] == 'D':
        diff_colors = True
    
    return diff_colors

def get_actions(s):
    actions = []
    
    #See where Talon cards can be moved:
    for tal_idx, card in enumerate(s.reachable_talon):
        
        #Talon to tableau
        for tab_idx, stack in enumerate(s.tableau):
            
            #If different colors and tableau end is one number higher than talon card
            if opp_color_check(card, stack[0]) and stack[0][1] - card[1] == 1:
                new_entry = {'from':[0, tal_idx], 'to':[1,tab_idx,0]}
                actions.append(new_entry)
        
        #Talon to foundation
        for found_idx, stack in enumerate(s.foundation):
            if stack[0][0] == card[0] and stack[0][1] - card[1] == 1: #If suits match and proper next card
                new_entry = {'from':[0,tal_idx], 'to':[2,found_idx]}
 #-------------------------------------------------------------------------------------------------------               
    #See where tableau cards/stacks can be moved to
    for stack_idx, stack in enumerate(s.tableau): #For each stack
        
        #Tableau to tableau:
        for stack_depth in range(len(stack[0])): #For each card in a face up stack
            card = stack[0][stack_depth]
            
            for si2, stack2 in enumerate(s.tableau): #Iterate through each card in stack
                if opp_color_check(card,stack2[0][0]) and stack2[0][0][1] - card[1] == 1:
                    #Append a card if stack_depth = 0, append a bundle of cards starting from stack_depth
                    #if stack_depth > 0
                    new_entry = {'from':[1,stack_idx,stack_depth], 'to':[1,si2,0]}
                    actions.append(new_entry)
                
        
            #If next card in stack can't be moved, stop looping through stack
            if stack_depth < len(stack[0]):
                if stack[0][stack_depth+1] - stack[0][stack_depth] != 1: 
                    break
                    
    
        #Tableau to foundation:
        for found_idx, found_stack in enumerate(s.foundation):
            if stack[0][0] == found_stack[0] and found_stack[1] - stack[0][1] == 1:
                new_entry = {'from':[1,stack_idx,0], 'to':[2,found_idx]}
 #------------------------------------------------------------------------------------------------------- 
    #See where foundation cards can be moved to
    for stack_idx, stack in enumerate(s.foundation):
        #Foundation to tableau
        for tab_idx, tab_stack in enumerate(s.tableau):
            if opp_color_check(stack[0][0], tab_stack[0][0]) and tab_stack[0][1] - stack[0][1] == 1:
                #Move card from foundation to end of a tableau stack
                new_entry = {'from':[2,stack_idx], 'to':[1,tab_idx,0]} 
    
    
    return actions

def result(s,a):
    #Given an action and state, returns the new state
    
    #Will change two locations. Involves removing a card from one location
    #and adding it to the other location.
    '''
    Ex, adding card from talon to foundation
    
    if talon talon to foundation:
        s_new = s.copy
        s_new.talon[end].pop(a[from])
        s_new.foundation[ind].append(a[to])
        return s_new
    
    '''
    
    pass


def greedy(s,h): #Takes in starting state and a heuristic function
    actions = get_actions(s) #Grab available actions for initial state
    
    best_res = -float('inf') #Set to negative infinity for first loop
    while actions:
        for a in actions:
            res = h(result(s,a))
            if res > best_res:
                best_res = res
                best_a = a
        ap = best_a
        s = result(s,ap) #Take best action to next state
        actions = get_actions(s)
    
    return h(s)

def mns_rollout(s, hs, ns, a):
    
    while get_actions(s): #While we have an available action
        
        if ns[0] == -1: #i.e. no more levels of nesting
            return hs[0](s,a)
        
        else:
            actions = get_actions(s)
            best_val = -float('inf')
            for act in actions:
                new_n = ns.copy()
                new_n[0] -= 1
                val = mns_rollout(result(s,act), hs, new_n, act)
                
                if val > best_val:
                    best_val = val
                    best_a = act
            
            #Checks if value of taking best_a is less than the value of 
            #our current state.
            if hs[0](s) > best_val and len(hs) != 1:
                actions = get_actions(s)
                best_val = -float('inf')
                
                for act in actions:
                    #Move on to the next heuristic
                    val = mns_rollout(result(s,act), hs[1:], ns[1:], act)
                
                if val > best_val:
                    best_val = val
                    best_a = act
            
            s = result(s,best_a)
            #implement way to store the path we take
            
    return hs[0](s)
            
    
    
    
