from collections import deque
import deckGenerator
from heuristics import HeuristicH1, HeuristicH2
from deckGenerator import State, Kplus, initKplus
<<<<<<< Updated upstream
from search import detectUnwinnable, get_actions, result
from state_setter import state_setter
import copy
import numpy as np

#Generate a random deck of cards
deck = deckGenerator.deckGen()
#print(deck)
#print(len(deck))

#initialize the game by partitioning the deck
random_game = True
if random_game:
    tableau = deckGenerator.tableauGen(deck)
    foundation = deckGenerator.foundationGen()
    stock = deckGenerator.StockGen(deck)
    
else:
    stock,foundation,tableau = state_setter()
    
lens= np.array([3,3,3,3,3,3,3,3])
classes = np.tile(np.array([0,0,1]),8)
reachable_talon, unreachable_talon = initKplus(stock)

s0 = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)
s0.printDeck()


#unique = deckGenerator.isUniqueDeck(deck)
unique = s0.isUniqueStacks()
if not unique:
    raise ValueError("ERROR Initializing: cards are not unique")

s0.printDeckLength()


#tableauWin, foundationWin, reachable_talonWin, unreachable_talonWin, stockWin, lensWin, classesWin = deckGenerator.winGen()
#sWin = State(tableauWin, foundationWin, reachable_talonWin, unreachable_talonWin, stockWin, lensWin, classesWin)
#sWin.printDeck()
#sWin.printDeckLength()

#H1,H2 = HeuristicH1(s0.tableau,s0.foundation,s0.reachable_talon,s0.unreachable_talon),HeuristicH2(s0.tableau,s0.foundation,s0.reachable_talon,s0.unreachable_talon)
#print(H1,H2)
#print('')
#print('')
#H1,H2 = HeuristicH1(sWin.tableau,sWin.foundation,sWin.reachable_talon,sWin.unreachable_talon),HeuristicH2(sWin.tableau,sWin.foundation,sWin.reachable_talon,sWin.unreachable_talon)
#print(H1,H2)
#print('')
#print('')

#H1,H2 = s0.HeuristicH1H2()
#print(H1,H2, '\n\n')
#H1,H2 = sWin.HeuristicH1H2()
#print(H1,H2, '\n\n')

#tester code for get_actions, result, and detectUnwinnable functions
a0 = get_actions(s0)
print("actions:", a0)

#UNCOMMENT below to get the results for get_actions()
#s1 = [] #to hold the corresponding states for the actions in a0
#a0_possible = [] #for a deepcopy of get_actions
#for a in a0: #a is a dictionary with keys of 'to' and 'from'
#    sprime = result(s0,a) #get the resulting state for this action
#    if not detectUnwinnable(sprime):
#        d2 = copy.deepcopy(a)
#        a0_possible.append(d2)
#        s1.append(sprime)

#now, a0_possible and s1 should hold the actions and resulting states that are not unwinnable
#next, we need to decide which action we will actually take depending on the heuristic
=======
from search import detectUnwinnable, faux_mns, get_actions, prune_actions, result
from search import mns_rollout_enhanced
from state_setter import state_setter
import copy
import numpy as np
import sys
import gui
sys.setrecursionlimit(2700)


def main():
    #Generate a random deck of cards
    deck = deckGenerator.deckGen()
    #print(deck)
    #print(len(deck))

    #initialize the game by partitioning the deck
    random_game = True
    if random_game:
        tableau = deckGenerator.tableauGen(deck)
        foundation = deckGenerator.foundationGen()
        stock = deckGenerator.StockGen(deck)
        
    else:
        stock,foundation,tableau = state_setter()
        
    lens= np.array([3,3,3,3,3,3,3,3])
    classes = np.tile(np.array([0,0,1]),8)
    reachable_talon, unreachable_talon = initKplus(stock)

    s0 = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)

    #s0.printDeck()


    unique = s0.isUniqueStacks()
    if not unique:
        raise ValueError("ERROR Initializing: cards are not unique")
    #--------------------------------------------------------------------------------

    H1 = HeuristicH1(1)
    H2 = HeuristicH2(1)
    hs = [H1,H2]
    ns = [H1.nestingLevel, H2.nestingLevel]
    history = deque([])
    print(faux_mns(s0, H1, history))
    #mns_rollout_enhanced(s0,hs,ns,True,[])
    print("not broken")
    gui.initGame(s0.reachable_talon,s0.unreachable_talon,s0.foundation,s0.tableau)
    #mns_rollout_enhanced(s0, hs, ns, top_layer=True, path=[])

    #--------------------------------------------------------------------------------
    #UNCOMMENT below to get the results for get_actions()
    #s1 = [] #to hold the corresponding states for the actions in a0
    #a0_possible = [] #for a deepcopy of get_actions
    #for a in a0: #a is a dictionary with keys of 'to' and 'from'
    #    sprime = result(s0,a) #get the resulting state for this action
    #    if not detectUnwinnable(sprime):
    #        d2 = copy.deepcopy(a)
    #        a0_possible.append(d2)
    #        s1.append(sprime)

    #now, a0_possible and s1 should hold the actions and resulting states that are not unwinnable
    #next, we need to decide which action we will actually take depending on the heuristic


    '''
    #fabricated states to test detectUnwinnable(s)
    tableau = deckGenerator.tableauGen(deck)
    foundation = deckGenerator.foundationGen()
    stock = deckGenerator.StockGen(deck)
    lens= np.array([3,3,3,3,3,3,3,3])
    classes = np.tile(np.array([0,0,1]),8)
    reachable_talon, unreachable_talon = deckGenerator.initKplus(stock)
>>>>>>> Stashed changes

    tableau[6][0] = deque([['S', 12]])
    tableau[6][1] = deque([['S', 2],['S', 5],['D', 13],['H', 7],['D', 5],['H', 13]])

<<<<<<< Updated upstream
#fabricated states to test detectUnwinnable(s)
tableau = deckGenerator.tableauGen(deck)
foundation = deckGenerator.foundationGen()
stock = deckGenerator.StockGen(deck)
lens= np.array([3,3,3,3,3,3,3,3])
classes = np.tile(np.array([0,0,1]),8)
reachable_talon, unreachable_talon = deckGenerator.initKplus(stock)
=======
    suwtest = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)
    #suwtest.printDeck()
>>>>>>> Stashed changes

    print("Testing Unwinnable Case #1")
    print(detectUnwinnable(suwtest)) #should be True

    suwtest.tableau[6][0] = deque([['D', 10]])
    suwtest.tableau[6][1] = deque([['H', 10],['H', 6],['C', 11],['D', 9],['S', 3],['H', 5]])

    print("Testing Unwinnable Case #2")
    print(detectUnwinnable(suwtest)) #should be True

    print("Testing Unwinnable s0:")
    print(detectUnwinnable(s0))
    '''


<<<<<<< Updated upstream
print("Testing Unwinnable s0:")
print(detectUnwinnable(s0))
=======
if __name__ == '__main__':
    main()
>>>>>>> Stashed changes
