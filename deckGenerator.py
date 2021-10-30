import random
from collections import deque
#from SolitaireClasses import Talon

#Decision: Do we want the deck to be a list of tuples, 
#like Deck = [("S", "2"), ...] or a list of strings like ["S2", ...], 
# #I have implemented both, we can just copy the values of one into the final code to reduce computational complexity

Suits = ["S", "C", "H", "D"]
Elements = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def deckGen1():
    Deck = []
    for i in Suits:
        for j in Elements:
            Deck.append((i,j))
    random.shuffle(Deck)
    return Deck

def deckGen2():
    Deck = []
    for i in Suits:
        for j in Elements:
            Deck.append(i+j)
    random.shuffle(Deck)
    return Deck


def reachableTalonGen(Deck):
    reachableTalon = deque(Deck[27:46])
    return reachableTalon

def unreachableTalonGen(Deck):
    unreachableTalon = deque(Deck[46:51])
    return unreachableTalon

def foundationGen():
    foundation1 = [] #for spades
    foundation2 = [] #for clubs
    foundation3 = [] #for hearts
    foundation4 = [] #for diamonds
    Foundation = [foundation1,foundation2,foundation3,foundation4]
    return Foundation

def tableauGen(Deck):
    tableau1 = [deque(Deck[0]), deque([])] #first array for face up, second array for face down 
    tableau2 = [deque(Deck[1]), deque(Deck[2])]
    tableau3 = [deque(Deck[3]), deque(Deck[4:6])]
    tableau4 = [deque(Deck[6]), deque(Deck[7:10])]
    tableau5 = [deque(Deck[10]), deque(Deck[11:15])]
    tableau6 = [deque(Deck[15]), deque(Deck[15:20])]
    tableau7 = [deque(Deck[20]), deque(Deck[21:27])]
    Tableau = [tableau1,tableau2,tableau3,tableau4,tableau5,tableau6,tableau7]
    return Tableau

def printDeck(tableau,foundation,reachable_talon,unreachable_talon):
    print("Tableau: ", tableau)
    print("Foundation: ", foundation)
    print("Reachable Talon: ", reachable_talon)
    print("Unreachable Talon: ", unreachable_talon)

def printDeckLength(tableau,foundation,reachable_talon,unreachable_talon):
    tableauLength = []
    for tableau_stack in tableau:
        print(tableau_stack[0])
        print(tableau_stack[1])
        tableauLength.append(len(tableau_stack[0])+len(tableau_stack[1]))
    foundationLength = []
    for foundation_stack in foundation:
        foundationLength.append(len(foundation_stack))
    print("Tableau: ", tableauLength)
    print("Foundation: ", foundationLength)
    print("Reachable Talon: ", len(reachable_talon))
    print("Unreachable Talon: ", len(unreachable_talon))
    print("Total: ", sum(tableauLength)+sum(foundationLength)+len(reachable_talon)+len(unreachable_talon))