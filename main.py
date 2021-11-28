from collections import deque
import deckGenerator
from heuristics import HeuristicH1, HeuristicH2
from deckGenerator import State, Kplus, initKplus
from search import detectUnwinnable, get_actions
import copy
import numpy as np

#Generate a random deck of cards
deck = deckGenerator.deckGen()
#print(deck)
#print(len(deck))

#initialize the game by partitioning the deck
tableau = deckGenerator.tableauGen(deck)
foundation = deckGenerator.foundationGen()
stock = deckGenerator.StockGen(deck)
lens= np.array([3,3,3,3,3,3,3,3])
classes = np.tile(np.array([0,0,1]),8)
reachable_talon, unreachable_talon = initKplus(stock)

s0 = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)

#unique = deckGenerator.isUniqueDeck(deck)
unique = s0.isUniqueStacks()
if not unique:
    raise ValueError("ERROR Initializing: cards are not unique")

s0.printDeck()
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


#fabricated states to test detectUnwinnable(s)
tableau = deckGenerator.tableauGen(deck)
foundation = deckGenerator.foundationGen()
stock = deckGenerator.StockGen(deck)
lens= np.array([3,3,3,3,3,3,3,3])
classes = np.tile(np.array([0,0,1]),8)
reachable_talon, unreachable_talon = deckGenerator.initKplus(stock)

tableau[6][0] = deque([['S', 12]])
tableau[6][1] = deque([['S', 2],['S', 5],['D', 13],['H', 7],['D', 5],['H', 13]])

suwtest = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)
#suwtest.printDeck()

print("Testing Unwinnable Case #1")
print(detectUnwinnable(suwtest)) #should be True

suwtest.tableau[6][0] = deque([['D', 10]])
suwtest.tableau[6][1] = deque([['H', 10],['H', 6],['C', 11],['D', 9],['S', 3],['H', 5]])

print("Testing Unwinnable Case #2")
print(detectUnwinnable(suwtest)) #should be True

print("Testing Unwinnable s0:")
print(detectUnwinnable(s0))