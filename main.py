import deckGenerator
from heuristics import HeuristicH1, HeuristicH2
from deckGenerator import State
from search import get_actions

#Generate a random deck of cards
deck = deckGenerator.deckGen1()
#print(deck)
#print(len(deck))

#initialize the game by partitioning the deck
tableau = deckGenerator.tableauGen(deck)
foundation = deckGenerator.foundationGen()
stock = deckGenerator.StockGen(deck)
talon = []
reachable_talon, unreachable_talon = deckGenerator.kplusTalon(stock,talon)
#unreachable_talon = deckGenerator.unreachableTalonGen(deck)

s0 = State(tableau, foundation, reachable_talon, unreachable_talon)

#unique = deckGenerator.isUniqueDeck(deck)
unique = s0.isUniqueStacks()
if not unique:
    raise ValueError("ERROR Initializing: cards are not unique")

s0.printDeck()
s0.printDeckLength()


tableauWin, foundationWin, reachable_talonWin, unreachable_talonWin = deckGenerator.winGen(deck)
sWin = State(tableauWin, foundationWin, reachable_talonWin, unreachable_talonWin)
sWin.printDeck()
sWin.printDeckLength()

#H1,H2 = HeuristicH1(s0.tableau,s0.foundation,s0.reachable_talon,s0.unreachable_talon),HeuristicH2(s0.tableau,s0.foundation,s0.reachable_talon,s0.unreachable_talon)
#print(H1,H2)
#print('')
#print('')

H1,H2 = s0.HeuristicH1H2()
print(H1,H2)
print('')
print('')
H1,H2 = sWin.HeuristicH1H2()
print(H1,H2)
print('')
print('')
#a = get_actions(s0)


# A New State Representation: K+ Solitaire
#This may not stay as a function, I'm just putting it here so there's somewhere to keep it
#example talon queue for testing
#talon = queue.LifoQueue()
#talon.put("5D")
#talon.put("AS")
#talon.put("10H")
#talon.put("3C")
#talon.put("QH")

def compressedSearchTree():
    return 0

def isReachable():
    '''
    Helper function for compressed search tree
    '''
    return 0