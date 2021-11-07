import SolitaireClasses, deckGenerator, reimplementation, random, queue
from deckGenerator import State
import numpy as np

#Generate a random deck of cards
deck = deckGenerator.deckGen1()
#print(deck)
#print(len(deck))

#initialize the game by partitioning the deck
tableau = deckGenerator.tableauGen(deck)
foundation = deckGenerator.foundationGen()
stock = deckGenerator.StockGen(deck)
reachable_talon, unreachable_talon = deckGenerator.kplusTalon(deck)
#unreachable_talon = deckGenerator.unreachableTalonGen(deck)

s0 = State(tableau, foundation, reachable_talon, unreachable_talon)

#unique = deckGenerator.isUniqueDeck(deck)
unique = s0.isUniqueStacks()
if not unique:
    raise ValueError("ERROR Initializing: cards are not unique")


s0.printDeck()
s0.printDeckLength()

H1,H2 = s0.HeuristicH1H2()
print(H1,H2)



#Load up our classes

#something like
def loadClasses(deck):
    for _ in range(SolitaireClasses.Stock.cards):
        SolitaireClasses.Stock.cards = deck.pop
    #etc
    return 0

#loadClasses()



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