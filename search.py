import numpy as np
from deckGenerator import Kplus, State, winGen
from collections import deque
#from heuristics import HeuristicH1, HeuristicH2
# K+ initialization

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

def result(s: State,a: dict):
    '''
    s - state
    a - action. this should be  [{'from':[bin idx, location in talon], 'to':[bin idx, stack, location in stack] } ]
    '''

    if a['from'][0] == 0: #0 = from reachable_talon
        card = s.reachable_talon[a['from'][1]]
        s.stock, s.lens, s.reachable_talon, s.unreachable_talon, s.classes = Kplus(card, s.stock, s.lens, s.classes)
        if a['to'][0] == 1: #to tableau
            s.tableau[a['to'][1]][0].appendleft(card) #need to check if this will be pop or popleft
        if a['to'][0] == 2: #to foundation
            s.foundation[a['to'][1]].appendleft(card) #need to check if this will be pop or popleft
        ## need to recalculate kplus talon here
    elif a['from'][0] == 1: #1 = from tableau
        tab_stack = a['from'][1]
        if a['to'][0] == 1: #to tableau
            #multiple can be moved
            temp = deque([])
            for _ in range(a['from'][2]+1): #pop the number of times of the location (ind+1)
                xx = s.tableau[a['from'][1]][0].popleft()
                temp.appendleft(xx)
            s.tableau[a['to'][1]][0].extendleft(temp)
                
        if a['to'][0] == 2: #to foundation
            #only one can be moved
            xx = s.tableau[tab_stack][0].popleft()
            s.foundation[a['to'][1]].appendleft(xx)
        #check if we need to reveal cards
        if len(s.tableau[tab_stack][0]) == 0 and s.tableau[tab_stack][1]:
            s.tableau[tab_stack][0].appendleft(s.tableau[tab_stack][1].popleft())

    elif a['from'][0] == 2: #2 = from foundation
        #cards from foundation can only be moved to the tableau 
        xx = s.foundation[a['from'][1]].popleft()
        s.tableau[a['to'][1]][0].appendleft(xx) #need to check if this will be pop or popleft
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
            if len(tableau_stack[1]) >= 4: #there must be at least 4 face down cards (one of the same color and rank and 3 this card is blocking)
                if (card in tableau_stack[0]) and (opp_color in tableau_stack[1]): 
                    #(card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]) and (opp_color[0] == tableau_stack[1][0][0]) and (opp_color[1] == tableau_stack[1][0][1]):
                    #two cards of the same color and rank are in the same tableau stack where one is a face up card and the other is a face down card blocking at least 3 more face down cards
                    opp_color_index = tableau_stack[1].index(opp_color) #index where opp_color card is
                    blocking = []
                    for k in range(len(tableau_stack[1])):
                        if k > opp_color_index:
                            blocking.append(tableau_stack[1][k])
                    blocking = deque(blocking) #the cards that both cards of the same rank and color block


                    #these two cards have the same tableau build cards
                    tableau_build_cards = []
                    if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                        tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
                    elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
                        tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]

                    if (tableau_build_cards) and ((tableau_build_cards[0] in blocking) or (tableau_build_cards[1] in blocking)): #blocking one tableau build card
                        for card2 in blocking:
                            for card3 in blocking:
                                if (card2[1] < card[1]) and (card2[0] == card[0]) and (card3[1] < opp_color[1]) and (card3[0] == opp_color[0]): 
                                    #blocking a lower rank card of the same suit and opposite suit
                                    detectUnwinnable = True
                                    return detectUnwinnable


    return detectUnwinnable



def win(s):
    '''
    check if the passed in state s is a win state
    '''
    #recreate win state for comparison
    tableauWin, foundationWin, reachable_talonWin, unreachable_talonWin, stockWin, lensWin, classesWin = winGen()
    sWin = State(tableauWin, foundationWin, reachable_talonWin, unreachable_talonWin, stockWin, lensWin, classesWin)
        
    if s == sWin:
        return True
    else:
        return False



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

def loop_check(s):
    '''
    Needed: what data structure will the cached states be in?
    Also, how is "nesting level" of current state determined?
    '''

    for cached in HeuristicH1.cache:
        if State.__eq__(s,cached): 
            return True
    for cached in HeuristicH2.cache:
        if State.__eq__(s,cached): 
            return True
    return False
    
#-----------------------------------------------------------------------------
def cache_check(s,h, n):
    
    for idx, entry in enumerate(h.cache):
        if s == entry and n == h.n_cache[idx]:
            return True
        
    return False
#-----------------------------------------------------------------------------
def mns_rollout_enhanced(s, hs, ns, top_layer, path):
    #s : Current state
    #hs : A list containing the heuristic functions
    #ns : A list containing the current nesting level for each heuristic 
    #top_layer : A boolean to check if this is the first call of the recurssive function
    #path : A list of all the states visited by the top layer
    
    
    #Infinity = WIN, negative infinity = LOSS
    if hs[0].h(s) == float('inf'): return float('inf') #If win, instantly return

    #if loop_check(s): return -float('inf') #If stuck, return a loss  

    
    #i.e. no more levels of nesting and is a dead end
    if not get_actions(s) and ns[0] == -1: 
        return hs[0].h(s)
    
    if cache_check(s,hs[0],ns[0]): #Check if already cached
        if len(hs) == 1: #On last heuristic
            return hs[0](s)
        else:
            return mns_rollout_enhanced(s,hs[1:],ns[1:], False, path)
        
    while hs[0].h(s) != -float('inf'):
        actions = get_actions(s)
        '''
        actions = prune_actions(s, actions)
        if not actions: return -float('inf')
        '''
        best_val = -float('inf') #Initialize as a loss
        for act in actions:
            new_n = ns.copy()
            new_n[0] -= 1
            val = mns_rollout_enhanced(result(s,act), hs, new_n, False, path)
            
            if val > best_val:
                best_val = val
                best_a = act
                    
        if best_val == float('inf'): #WIN
            return float('inf')
        
        #If LOSS or local maxima found when not on last heuristic
        if best_val == -float('inf') or (len(hs) != 0 and best_val < hs[0].h(s)):
            if len(hs)==1: return hs[0].h(s) #On last heuristic
            else: return mns_rollout_enhanced(result(s,best_a),hs[1:],ns[1:], False, path)
        
            
        s = result(s,best_a)
        if ns[0] != 0 and len(hs[0].cache) < 5000: #Only cache at non-zero nesting levels
            hs[0].cache.append(s) #Appends to appropriate heuristic
            hs[0].n_cache.append(ns[0]) #Save nesting level of heuristic
                    
        if top_layer:
            path.append(s)
            
    if top_layer:
        return path

            
#-----------------------------------------------------------------------------


def reveal_face_down(s: State, a: dict):
    '''
    Input: current state s and action a
    Output: True if taking action a in state s will reveal a face down card, False otherwise.
    Function should only be called when the 'from' key of the action == 1 (when we are moving from the tableau)
    '''

    sprime = result(s,a)

    for tab_idx in range(len(s.tableau)):
        s_tableau_stack = s.tableau[tab_idx]
        sprime_tableau_stack = sprime.tableau[tab_idx]

        if len(s_tableau_stack[1]) > len(sprime_tableau_stack[1]): #if state s has more face down cards than sprime
            return True

    return False


def foundation_progression(s: State, a: dict):
    '''
    Input: current state s and action a
    Output: True if all cards of rank two less are already in the foundation or card is an Ace or 2; False otherwise
    True means that foundation has progressed sufficiently that this action should not be taken
    '''
    foundation_stack_idx = a['from'][1]
    card = s.foundation[foundation_stack_idx][-1] #last card in this foundation stack is the one that is being moved

    if (card[1] == 1) or (card[1] == 2): #card is an Ace or a 2
        return True

    cards_rank_two_less = []
    Suits = ["D", "C", "H", "S"]
    ranks_two_less = [card[1]-1, card[1]-2]
    for i in Suits:
        for j in ranks_two_less:
            cards_rank_two_less.append([i,j])

    for card2 in cards_rank_two_less:
        if (card2 in s.foundation[0]) or (card2 in s.foundation[1]) or (card2 in s.foundation[2]) or (card2 in s.foundation[3]):
            continue
        else:
            return False

    return True

def KingToTableau(s: State, a: dict):
    '''
    Input: current state s and action a
    Output: True if moving a King that is not the bottom-most card in the tableau stack to leftmost empty tableau stack; False otherwise
    if the card is not a King, True is returned since KingToTableau is not relevant for this action
    '''
    if a['from'][0] == 1: #moving King from tableau to tableau
        tableau_stack_idx = a['from'][1]
        card_idx = a['from'][2]

        card = s.tableau[tableau_stack_idx][0][card_idx]
        if card[1] != 13: #not a King
            return True

        bottom_most = False
        face_down_cards = s.tableau[tableau_stack_idx][1]
        if len(face_down_cards) == 0:
            bottom_most = True

        if bottom_most:
            return False

    #moving valid King from tableau to tableau OR King from talon to tableau OR King from foundation to tableau
    
    multiple_empty_tableau_stacks = False
    empty_tableau_stacks_count = 0
    for tableau_stack in s.tableau:
        if len(tableau_stack[0]) == 0: #there are no face up cards in this stack so it must be empty
            empty_tableau_stacks_count += 1
    if empty_tableau_stacks_count >= 2:
        multiple_empty_tableau_stacks = True

    if not(multiple_empty_tableau_stacks):
        return True

    tableau_to_stack_idx = a['to'][1]
    if tableau_to_stack_idx == 0:
        return True

    return False

#0: talon, tal_idx is the index of the card you are moving from the reachable talon
#1: tableau, 0-6, the depth of cards to move starting at 0 (relevant for tableau to tableau)
#2: foundation, 0-3 for the foundation stack

def prune_actions(s: State, possible_actions):
    '''
    Inputs: current state s and list of possible actions in state s
    Output: the best actions as a dictionary
    Explanation: the best actions is based on action ordering from the paper. The heuristic is only used for tie-breaking, which is not done in this function.
    TODO: additional ordering from strategy guide?
    '''

    if len(possible_actions) == 1: #there is only one possible action
        return possible_actions[0]
    
    if len(possible_actions) == 0: #there are no possible actions
        return []

    
    a01_actions = [] #actions that move a card from tableau to foundation and reveal a face down card
    a02_actions = [] #actions that move a card to the foundation
    a03_actions = [] #actions that move a card from tableau to tableau and reveal a face down card
    a04_actions = [] #actions that move a card from the talon to the tableau
    a05_actions = [] #actions that move a card from the foundation to the tableau
    a06_actions = [] #actions that move a card from tableau to tableau and do not reveal a face down card
    a07_actions = [] #all other actions. Just to check but this should never happen.

    for action in possible_actions:

        card = None
        if action['from'][0] == 1: #moving from tableau
            tableau_stack_idx = action['from'][1]
            card_idx = action['from'][2]
            card = s.tableau[tableau_stack_idx][0][card_idx]
        elif action['from'][0] == 0: #moving from talon
            card_idx = action['from'][1]
            card = s.reachable_talon[card_idx]
        elif action['from'][0] == 2: #moving from foundation
            foundation_stack_idx = action['from'][1]
            card = s.foundation[foundation_stack_idx][-1]


        if (action['from'][0] == 1) and (action['to'][0] == 2) and (reveal_face_down(s,action)): #action that moves card from tableau to foundation and reveals a face down card
            a01_actions.append(action)
        
        elif action['to'][0] == 2: #action that moves card to foundation
            a02_actions.append(action)
        
        elif (action['from'][0] == 1) and (action['to'][0] == 1) and (reveal_face_down(s,action)): #action that moves card from tableau to tableau and reveals a face down card
            if (card[1] == 13): #card being moved is a King
                if (KingToTableau(s,action)):
                    a03_actions.append(action)
            else:
                a03_actions.append(action)
        
        elif (action['from'][0] == 0) and (action['to'][0] == 1): #action that moves card from talon to tableau
            if (card[1] == 13): #card being moved is a King
                if (KingToTableau(s,action)):
                    a04_actions.append(action)
            else:
                a04_actions.append(action)

        elif (action['from'][0] == 2) and (action['to'][0] == 1) and (not(foundation_progression(s,action))): #action that moves card from foundation to tableau
            if (card[1] == 13): #card being moved is a King
                if (KingToTableau(s,action)):
                    a05_actions.append(action)
            else:
                a05_actions.append(action)

        elif (action['from'][0] == 1) and (action['to'][0] == 1): #action that moves card from tableau to tableau and does not reveal a face down card
            if (card[1] == 13): #card being moved is a King
                if (KingToTableau(s,action)):
                    a06_actions.append(action)
            else:
                a06_actions.append(action)

        else:
            a07_actions.append(action) #all other actions

    #best_val = -float('inf')
    #best_act = None

    if len(a01_actions) > 0:
        # for action in a01_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a01_actions

    if len(a02_actions) > 0:
        # for action in a02_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a02_actions

    if len(a03_actions) > 0:
        # for action in a03_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a03_actions

    if len(a04_actions) > 0:
        # for action in a04_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a04_actions

    if len(a05_actions) > 0:
        # for action in a05_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a05_actions

    if len(a06_actions) > 0:
        # for action in a06_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a06_actions

    if len(a07_actions) > 0:
        # for action in a07_actions:
        #     val = HEURISTIC(result(s,action)) #???How do we call heuristic? And how do we know which heuristic to use?
        #     if  val > best_val:
        #         best_val = val
        #         best_act = action
        # return best_act
        return a07_actions
