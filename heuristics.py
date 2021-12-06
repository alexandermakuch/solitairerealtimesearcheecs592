#heuristic functions and class

import random
from collections import deque
from deckGenerator import State
from search import detectUnwinnable, win
class HeuristicH1:
    def __init__(self, nesting_level):
        self.cache = [] #empty cache
        self.n_cache = []
        self.nestingLevel = nesting_level

    def HeuristicStringH1(self, s):

        if win(s):
            return float('inf')

        elif detectUnwinnable(s):
            return -float('inf')

        else:
            return self.H1(s.tableau,s.foundation,s.reachable_talon,s.unreachable_talon)



    def h(self, s):
        tableau = s.tableau
        foundation = s.foundation
        reachable_talon = s.reachable_talon
        unreachable_talon = s.unreachable_talon
        
        deck = [] #to recreate the deck from the passed stacks
        tableau_face_down = []
        tableau_face_up = []
        foundation_all = []
        blocking_cards = []
        for tableau_stack in tableau:
            for card in tableau_stack[0]:
                deck.append(card)
                tableau_face_up.append(card)
                if (card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]): #it is the last face up card, it is a blocking card
                    blocking_cards.append(card)
            for card in tableau_stack[1]:
                deck.append(card)
                tableau_face_down.append(card)
                if not((card[0] == tableau_stack[1][-1][0]) and (card[1] == tableau_stack[1][-1][1])): #not the last face down card, so it is a blocking card
                    blocking_cards.append(card)
        
        for foundation_stack in foundation:
            for card in foundation_stack:
                deck.append(card)
                foundation_all.append(card)
        
        for card in reachable_talon:
            deck.append(card)

        for card in unreachable_talon:
            deck.append(card)


        H1 = 0
        num_elses = 0

        for card in deck:
            h1 = 0
            if card in foundation_all: #number 1 in table 1
                h1 = 5 - (card[1] - 1) #-1 because the rank value starts at 0
            elif card in tableau_face_down: #number 2 in table 1
                h1 = (card[1] - 1) - 13
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

            elif card in reachable_talon: #number 3 in table 1
                h1 = 0

            
            elif card in blocking_cards: #blocking card
                tableau_build_cards = []
                if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                    tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
                elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
                    tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]

                blocking = []

                for tableau_stack in tableau:
                    if (card in tableau_stack[0]): #it must be the last face up card since it is a blocking card
                        blocking = tableau_stack[1] #blocking all face down cards
                        break

                    elif(card in tableau_stack[1]):
                        card_idx = tableau_stack[1].index(card)
                        blocking = tableau_stack[1][card_idx+1:]
                        break


                if blocking:
                    for card2 in blocking: 
                        if card2 in tableau_build_cards: #number 6 in table1
                            h1 = -10
                            break
                        elif card2[1] < card[1]: #number 5 in table 1
                            h1 = -5
                            break
                        else:
                            h1 = 0 #not blocking any card of interest 
                else:
                    h1 = 0 #not blocking any card of interest

            else: #I dont think this should be needed as every card should fall into a category. Is the K+ talon wrong?
                h1 = 0
                num_elses += 1

            H1 += h1 #sum the heuristic for this card

        #print(num_elses)
        return H1


class HeuristicH2:
    def __init__(self, nesting_level):
        self.cache = [] #empty cache
        self.n_cache = []
        self.nestingLevel = nesting_level

    def HeuristicStringH2(self, s):

        if win(s):
            return float('inf')

        elif detectUnwinnable(s):
            return -float('inf')

        else:
            return self.H2(s.tableau,s.foundation,s.reachable_talon,s.unreachable_talon)


    def h(self, s):
        tableau = s.tableau
        foundation = s.foundation
        reachable_talon = s.reachable_talon
        unreachable_talon = s.unreachable_talon
        
        deck = [] #to recreate the deck from the passed stacks
        tableau_face_down = []
        tableau_face_up = []
        foundation_all = []
        blocking_cards = []
        for tableau_stack in tableau:
            for card in tableau_stack[0]:
                deck.append(card)
                tableau_face_up.append(card)
                if (card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]): #it is the last face up card, it is a blocking card
                    blocking_cards.append(card)
            for card in tableau_stack[1]:
                deck.append(card)
                tableau_face_down.append(card)
                if not((card[0] == tableau_stack[1][-1][0]) and (card[1] == tableau_stack[1][-1][1])): #not the last face down card, so it is a blocking card
                    blocking_cards.append(card)
        
        for foundation_stack in foundation:
            for card in foundation_stack:
                deck.append(card)
                foundation_all.append(card)
        for card in reachable_talon:
            deck.append(card)

        for card in unreachable_talon:
            deck.append(card)


        H2 = 0
        num_elses = 0

        for card in deck:
            h2 = 0
            if card in foundation_all: #number 1 in table 1
                h2 = 5
            elif card in tableau_face_down: #number 2 in table 1
                h2 = (card[1] - 1) - 13
                if card[0] == "S":
                    counterpart = ["C", card[1]]
                elif card[0] == "C":
                    counterpart = ["S", card[1]]
                elif card[0] == "H":
                    counterpart = ["D", card[1]]
                elif card[0] == "D":
                    counterpart = ["H", card[1]]

                if counterpart in tableau_face_down: #number 4 in table 1
                    h2 = -1

            elif card in reachable_talon: #number 3 in table 1
                h2 = 1

            elif card in blocking_cards: #blocking card
                tableau_build_cards = []
                if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                    tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
                elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
                    tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]

                blocking = []

                for tableau_stack in tableau:
                    if (card in tableau_stack[0]): #it must be the last face up card since it is a blocking card
                        blocking = tableau_stack[1] #blocking all face down cards
                        break

                    elif(card in tableau_stack[1]):
                        card_idx = tableau_stack[1].index(card)
                        blocking = tableau_stack[1][card_idx+1:]
                        break


                if blocking:
                    for card2 in blocking: 
                        if card2 in tableau_build_cards: #number 6 in table1
                            h2 = -5
                            break
                        elif card2[1] < card[1]: #number 5 in table 1
                            h2 = -1
                            break
                        else:
                            h2 = 0 #not blocking any card of interest 
                else:
                    h2 = 0 #not blocking any card of interest

            else: #I dont think this should be needed as every card should fall into a category. Is the K+ talon wrong?
                h2 = 0
                num_elses += 1
            
            
            H2 += h2 #sum the heuristic for this card

        #print(num_elses)
        return H2




#new heuristic function card features

#foundation card is rank value reward
#card in reachable talon
#high reward if there is an ace or deuce in the reachable_talon -> encourage actions that make ace and 2 playable
#high reward if empty tableau stack and playable King (first face up card in a tableau stack or in reachable talon) -> encourage actions that clear a tableau stack and a King can immediately occupy it
#for each additional face down card in the same tableau stack, the negative reward increases. First, -1, then -2, etc. -> encourage actions that reveal face down cards
#and the lower rank the face down card, the worse the reward. rank value - 13. 
#x is blocking a same suit card of lower rank
#x is blocking one of its tableau build cards



class HeuristicH3:
    def __init__(self, nesting_level):
        self.cache = [] #empty cache
        self.n_cache = []
        self.nestingLevel = nesting_level

    def HeuristicStringH3(self, s):

        if win(s):
            return float('inf')

        elif detectUnwinnable(s):
            return -float('inf')

        else:
            return self.H3(s.tableau,s.foundation,s.reachable_talon,s.unreachable_talon)


    def h(self, s):
        tableau = s.tableau
        foundation = s.foundation
        reachable_talon = s.reachable_talon
        unreachable_talon = s.unreachable_talon
        
        deck = [] #to recreate the deck from the passed stacks
        tableau_face_down = []
        tableau_face_up = []
        foundation_all = []
        blocking_cards = []
        for tableau_stack in tableau:
            for card in tableau_stack[0]:
                deck.append(card)
                tableau_face_up.append(card)
                if (card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]): #it is the last face up card, it is a blocking card
                    blocking_cards.append(card)
            for card in tableau_stack[1]:
                deck.append(card)
                tableau_face_down.append(card)
                if not((card[0] == tableau_stack[1][-1][0]) and (card[1] == tableau_stack[1][-1][1])): #not the last face down card, so it is a blocking card
                    blocking_cards.append(card)
        
        for foundation_stack in foundation:
            for card in foundation_stack:
                deck.append(card)
                foundation_all.append(card)
        
        for card in reachable_talon:
            deck.append(card)

        for card in unreachable_talon:
            deck.append(card)


        H3 = 0
        num_elses = 0
        tab0_count = 0
        tab1_count = 0
        tab2_count = 0
        tab3_count = 0
        tab4_count = 0
        tab5_count = 0
        tab6_count = 0

        for card in deck:
            h3 = 0
            if card in foundation_all: #number 1 in table 1
                h3 = card[1] - 1 #the rank value of the card. The higher the rank value, the greater the heuristic (to encourage movement of cards to foundation)
            elif card in tableau_face_down: #modified number 2 in table 1
                #h3 = (card[1] - 1) - 13
                #if card[0] == "S":
                #    counterpart = ["C", card[1]]
                #elif card[0] == "C":
                #    counterpart = ["S", card[1]]
                #elif card[0] == "H":
                #    counterpart = ["D", card[1]]
                #elif card[0] == "D":
                #    counterpart = ["H", card[1]]

                #if counterpart in tableau_face_down: #number 4 in table 1
                #    h3 = -1

                for tab_idx, tableau_stack in enumerate(tableau):
                    if (card in tableau_stack[1]) and tab_idx == 0:
                        h3 = (card[1] - 1) - 13 - tab0_count
                        tab0_count = tab0_count + 1
                        break
                    elif (card in tableau_stack[1]) and tab_idx == 1:
                        h3 = (card[1] - 1) - 13 - tab1_count
                        tab1_count = tab1_count + 1
                        break
                    elif (card in tableau_stack[1]) and tab_idx == 2:
                        h3 = (card[1] - 1) - 13 - tab2_count
                        tab2_count = tab2_count + 1
                        break
                    elif (card in tableau_stack[1]) and tab_idx == 3:
                        h3 = (card[1] - 1) - 13 - tab3_count
                        tab3_count = tab3_count + 1
                        break
                    elif (card in tableau_stack[1]) and tab_idx == 4:
                        h3 = (card[1] - 1) - 13 - tab4_count
                        tab4_count = tab4_count + 1
                        break
                    elif (card in tableau_stack[1]) and tab_idx == 5:
                        h3 = (card[1] - 1) - 13 - tab5_count
                        tab5_count = tab5_count + 1
                        break
                    elif (card in tableau_stack[1]) and tab_idx == 6:
                        h3 = (card[1] - 1) - 13 - tab6_count
                        tab6_count = tab6_count + 1
                        break


            elif (card[1] == 13) and (card in tableau_face_up or card in reachable_talon):
                for tableau_stack in tableau:
                    if len(tableau_stack[0]) == 0: #empty tableau stack for King
                        h3 = 3
                        break

            
            elif card in reachable_talon: #number 3 in table 1
                h3 = 1
                if (card[1] == 1 or card[1] == 2): #a playable ace or 2 card
                    h3 = 3


            elif card in blocking_cards: #blocking card
                tableau_build_cards = []
                if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                    tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
                elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
                    tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]

                blocking = []

                for tableau_stack in tableau:
                    if (card in tableau_stack[0]): #it must be the last face up card since it is a blocking card
                        blocking = tableau_stack[1] #blocking all face down cards
                        break

                    elif(card in tableau_stack[1]):
                        card_idx = tableau_stack[1].index(card)
                        blocking = tableau_stack[1][card_idx+1:]
                        break


                if blocking:
                    for card2 in blocking: 
                        if card2 in tableau_build_cards: #number 6 in table1
                            h3 = -5
                            break
                        elif (card2[0] == card[0]) and (card2[1] < card[1]): #modified number 5 in table 1
                            h3 = -1
                            break
                        else:
                            h3 = 0 #not blocking any card of interest 
                else:
                    h3 = 0 #not blocking any card of interest



            else: #I dont think this should be needed as every card should fall into a category.
                h3 = 0
                num_elses += 1
            
            
            H3 += h3 #sum the heuristic for this state

        #print(num_elses)
        return H3