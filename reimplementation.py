#functions that are needed for reimplementing the paper

import random
from collections import deque

def HeuristicH1H2(tableau,foundation,reachable_talon,unreachable_talon):

    deck = [] #to recreate the deck from the passed stacks
    tableau_face_down = []
    tableau_face_up = []
    for tableau_stack in tableau:
        for card in tableau_stack[0]:
            deck.append(card)
            tableau_face_up.append(card)
        for card in tableau_stack[1]:
            deck.append(card)
            tableau_face_down.append(card)
    
    for foundation_stack in foundation:
        for card in foundation_stack:
            deck.append(card)
    
    for card in reachable_talon:
        deck.append(card)

    for card in unreachable_talon:
        deck.append(card)


    H1 = 0
    H2 = 0
    num_elses = 0

    for card in deck:
        h1 = 0
        h2 = 0
        if card in foundation: #number 1 in table 1
            h1 = 5 - card[1] - 1 #-1 because the rank value starts at 0
            h2 = 5
        elif card in tableau_face_down: #number 2 in table 1
            h1 = card[1] - 1 - 13
            h2 = card[1] - 1 - 13
            if card[0] == "S":
                counterpart = ["C", card[1]]
            elif card[0] == "C":
                counterpart = ["S", card[1]]
            elif card[0] == "H":
                counterpart = ["D", card[1]]
            elif card[0] == "D":
                counterpart = ["H", card[1]]

            if counterpart in tableau_face_down: #number 4 in table 1
                h1 = -5
                h2 = -1

        elif card in reachable_talon: #number 3 in table 1
            h1 = 0
            h2 = 1

        elif card in tableau_face_up: 
            tableau_build_cards = []
            if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
            elif ((card[0] == "H") or (card[0] == "D"))and (card[1] != 13):
                tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]
                
            for tableau_stack in tableau:
                for card2 in tableau_stack[0]:
                    if (card[0] == card2[0]) and (card[1] == card2[1]):
                        blocking = tableau_stack[1]
                        break
            
            for card2 in blocking: 
                if card2 in tableau_build_cards: #number 6 in table1
                    h1 = -10
                    h2 = -5
                    break
                elif card2[1] < card[1]: #number 5 in table 1
                    h1 = -5
                    h2 = -1
                    break

        else: #I dont think this should be needed as every card should fall into a category. Is the K+ talon wrong?
            h1 = 0
            h2 = 0
            num_elses += 1

        H1 += h1 #sum the heuristic for this card
        H2 += h2

    #print(num_elses)
    return H1, H2





