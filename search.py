import numpy as np


def get_actions(s):
    actions = {}
    '''
    Should contain information on from and to:
    
    from: Which parent it belongs to (talon,tableu, etc) and its index in that parent
    
    to: Which parent it going to, and its index in that parent.
    
    Ex:
    a = {from:Parent,card, to:Parent,card}
    Maybe a list of dictionaries?
    or some structure similar to that
    '''
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
            
    return hs[0](s)
            
    
    
    