import numpy as np

def opp_color_check(c1, c2):
    diff_colors = False
    
    #Card 1 is red, Card 2 is black
    if (c1[0] == 'H' or c1[0] == 'D') and (c2[0] == 'S' or c2[0] == 'C'):
        diff_colors = True
    
    #Card 1 is black, Card 2 is red
    if (c1[0] == 'S' or c1[0] == 'C') and (c2[0] == 'H' or c2[0] == 'D'):
        diff_colors = True
    
    return diff_colors

def get_actions(s):
    actions = []
    
    #See where Talon cards can be moved:
    for tal_idx, card in enumerate(s.reachable_talon):
        
        #Talon to tableau
        for tab_idx, stack in enumerate(s.tableau):
            
            #If tableau end is different colors and one number higher than talon card
            if opp_color_check(card, stack[0]) and stack[0][1] - card[1] == 1:
                new_entry = {'from':[0, tal_idx], 'to':[1,tab_idx,0]}
                actions.append(new_entry)
        
        #Talon to foundation
        for found_idx, stack in enumerate(s.foundation):
            if stack: #Make sure there's cards in the stack
                if stack[0][0] == card[0] and stack[0][1] - card[1] == 1: #If suits match and proper next card
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
                if opp_color_check(card,stack2[0][0]) and stack2[0][0][1] - card[1] == 1:
                    #Append a card if stack_depth = 0, append a bundle of cards starting from stack_depth
                    #if stack_depth > 0
                    new_entry = {'from':[1,stack_idx,stack_depth], 'to':[1,si2,0]}
                    actions.append(new_entry)

            #If next card in stack can't be moved, stop looping through stack
            if stack_depth < len(stack[0])-1:
                if stack[0][stack_depth+1][1] - stack[stack_depth][1] != 1: 
                    break
                    
    
        #Tableau to foundation:
        for found_idx, found_stack in enumerate(s.foundation):
            if found_stack: #Verify it's not empty
                if stack[0][0] == found_stack[0] and found_stack[0][1] - stack[0][1] == 1:
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
                if tab_stack: #Nonempty tableau stack

                    if opp_color_check(stack[0][0], tab_stack[0][0]) and tab_stack[0][1] - stack[0][1] == 1:
                        #Move card from foundation to end of a tableau stack
                        new_entry = {'from':[2,stack_idx], 'to':[1,tab_idx,0]}
                        
                else: #Empty tableau stack
                    if tab_stack[0][1] == 13:
                        new_entry = {'from':[2,stack_idx], 'to':[1,tab_idx,0]}
    
    
    return actions

def result(s: State,a):
    '''
    s - state
    a - action. this should be  [{'from':[bin idx, location in talon], 'to':[bin idx, stack, location in stack] } ]
    '''

    if a['from'][0] == 0: #0 = from reachable_talon
        if a['to'][0] == 1: #to tableau
            s.tableau[a['to'][1]][0].appendleft(s.reachable_talon[a['from'][1]].popleft()) #need to check if this will be pop or popleft
        if a['to'][0] == 2: #to foundation
            s.foundation[a['to'][1]].appendleft(s.reachable_talon[a['from'][1]].popleft()) #need to check if this will be pop or popleft
        ## need to recalculate kplus talon here

    elif a['from'][0] == 1: #1 = from tableau
        if a['to'][0] == 1: #to tableau
            pass
        if a['to'][0] == 2: #to foundation
            pass
        #check if we need to reveal cards
        if len(s.tableau[a['from'][1]][0]) == 0:
            s.tableau[a['from'][1]][0] = deque(s.tableau[a['from'][1]][0].popleft())

    elif a['from'][0] == 2: #2 = from foundation
        #cards from foundation can only be moved to the tableau 
        s.tableau[a['to'][1]][0].appendleft(s.foundation[a['from'][1]].popleft()) #need to check if this will be pop or popleft
    else:
        print("ERROR INVALID INDEX")
        return 0

    return s


def detectUnwinnable(s): #need state from result(s,a) for each possible action returned by get_actions
    '''
    Input: a State object
    Output: a flag telling whether this state is unwinnable or not
    Implements two unwinnable cases covered in the paper
    '''

    detectUnwinnable = False

    deck = [] #to recreate the deck from the passed stacks
    tableau_face_down = []
    tableau_face_up = []
    foundation_all = []
    for tableau_stack in s.tableau:
        for card in tableau_stack[0]:
            deck.append(card)
            tableau_face_up.append(card)
        for card in tableau_stack[1]:
            deck.append(card)
            tableau_face_down.append(card)
    
    for foundation_stack in s.foundation:
        for card in foundation_stack:
            deck.append(card)
            foundation_all.append(card)
    
    for card in s.reachable_talon:
        deck.append(card)

    for card in s.unreachable_talon:
        deck.append(card)


    #for case 1 from the paper
    for card in tableau_face_up: #find the tableau build cards for last face up card in each tableau stack
        tableau_build_cards = []
        if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
            tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
        elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
            tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]

        for tableau_stack in s.tableau:
            if (card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]): #for this card to be blocking, it has to be the last face up card in a tableau stack 
                #this is the last face up card in a tableau stack
                blocking = tableau_stack[1]
                
                if (tableau_build_cards) and (tableau_build_cards[0] in blocking) and (tableau_build_cards[1] in blocking): #tableau_build_cards cannot be empty, using short circuiting
                    for card2 in blocking:
                        if (card2[1] < card[1]) and (card2[0] == card[0]): #blocking a lower rank card of the same suit
                            detectUnwinnable = True
                            return detectUnwinnable

    #for case 2 from the paper
    for card in tableau_face_up:
        if card[0] == "S":
            opp_color = ["C", card[1]] #opposite color card of same rank
        elif card[0] == "C":
            opp_color = ["S", card[1]] 
        elif card[0] == "H":
            opp_color = ["D", card[1]] 
        elif card[0] == "D":
            opp_color = ["H", card[1]] 

        for tableau_stack in s.tableau:
            if tableau_stack[1]: #the face down cards cannot be empty
                if (card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]) and (opp_color[0] == tableau_stack[1][0][0]) and (opp_color[1] == tableau_stack[1][0][1]):
                    #two cards of the same color and rank are in the same tableau stack where one is the last face up card and the other is the first face down card
                    blocking = tableau_stack[1]

                    #these two cards have the same tableau build cards
                    tableau_build_cards = []
                    if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                        tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
                    elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
                        tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]

                    if (tableau_build_cards) and (tableau_build_cards[0] in blocking) or (tableau_build_cards[1] in blocking): #blocking one tableau build card
                        for card2 in blocking:
                            for card3 in blocking:
                                if (card2[1] < card[1]) and (card2[0] == card[0]) and (card3[1] < opp_color[1]) and (card3[0] == opp_color[0]): 
                                    #blocking a lower rank card of the same suit and opposite suit
                                    detectUnwinnable = True
                                    return detectUnwinnable


    return detectUnwinnable


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
            
    
    
    
