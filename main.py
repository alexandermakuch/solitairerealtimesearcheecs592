import SolitaireClasses, deckGenerator, random, queue
import numpy as np

#Generate a random deck of cards
deck = deckGenerator.deckGen1()
#print(deck)
#print(len(deck))

tableau = deckGenerator.tableauGen(deck)
foundation = deckGenerator.foundationGen()
reachable_talon = deckGenerator.reachableTalonGen(deck)
unreachable_talon = deckGenerator.unreachableTalonGen(deck)

deckGenerator.printDeck(tableau,foundation,reachable_talon,unreachable_talon)
deckGenerator.printDeckLength(tableau,foundation,reachable_talon,unreachable_talon)

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