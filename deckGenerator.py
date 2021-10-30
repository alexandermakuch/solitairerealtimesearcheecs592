import random
from collections import deque
#from SolitaireClasses import Talon

#Decision: Do we want the deck to be a list of tuples, 
#like Deck = [("S", "2"), ...] or a list of strings like ["S2", ...], 
# #I have implemented both, we can just copy the values of one into the final code to reduce computational complexity

Suits = ["S", "C", "H", "D"]
#Ace is 1, Jack is 11, Queen is 12, King is 13
#numbers will make comparisons easier later on
Elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def deckGen1():
    Deck = []
    for i in Suits:
        for j in Elements:
            Deck.append([i,j])
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
    reachableTalon = deque(Deck[28:44])
    return reachableTalon

def unreachableTalonGen(Deck):
    unreachableTalon = deque(Deck[44:52])
    return unreachableTalon

def foundationGen():
    foundation1 = [] #for spades
    foundation2 = [] #for clubs
    foundation3 = [] #for hearts
    foundation4 = [] #for diamonds
    Foundation = [foundation1,foundation2,foundation3,foundation4]
    return Foundation

def tableauGen(Deck):
    tableau1 = [deque([Deck[0]]), deque([])] #first array for face up, second array for face down 
    tableau2 = [deque([Deck[1]]), deque([Deck[2]])]
    tableau3 = [deque([Deck[3]]), deque(Deck[4:6])]
    tableau4 = [deque([Deck[6]]), deque(Deck[7:10])]
    tableau5 = [deque([Deck[10]]), deque(Deck[11:15])]
    tableau6 = [deque([Deck[15]]), deque(Deck[16:21])]
    tableau7 = [deque([Deck[21]]), deque(Deck[22:28])]
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
        #print(tableau_stack)
        #print(tableau_stack[0])
        #print(tableau_stack[1])
        
        #print(len(tableau_stack[0]))
        #print(len(tableau_stack[1]))
 
        tableauLength.append(len(tableau_stack[0])+len(tableau_stack[1]))
    foundationLength = []
    for foundation_stack in foundation:
        foundationLength.append(len(foundation_stack))
    print("Tableau: ", tableauLength)
    print("Foundation: ", foundationLength)
    print("Reachable Talon: ", len(reachable_talon))
    print("Unreachable Talon: ", len(unreachable_talon))
    print("Total: ", sum(tableauLength)+sum(foundationLength)+len(reachable_talon)+len(unreachable_talon))

#a function to make sure we have 52 unique cards
def isUniqueStacks(tableau,foundation,reachable_talon,unreachable_talon):
    isUnique = True
    deck = [] #to recreate the deck from the passed stacks
    for tableau_stack in tableau:
        for card in tableau_stack[0]:
            deck.append(card)
        for card in tableau_stack[1]:
            deck.append(card)
    
    for foundation_stack in foundation:
        for card in foundation_stack:
            deck.append(card)
    
    for card in reachable_talon:
        deck.append(card)

    for card in unreachable_talon:
        deck.append(card)

    
    for value in range(1,13,1): #range(start,end,step)
        current_value_cards = []
        for card in deck:
            if card[1] == value:
                current_value_cards.append(card)
        
        current_heart_cards = []
        current_diamond_cards = []
        current_spade_cards = []
        current_club_cards = []
        for card in current_value_cards:
            if card[0] == 'H':
                current_heart_cards.append(card)
            elif card[0] == 'D':
                current_diamond_cards.append(card)
            elif card[0] == 'S':
                current_spade_cards.append(card)
            elif card[0] == 'C':
                current_club_cards.append(card)
            else:
                print("ERROR: There is a card of unrecognized suit")
        
        if (len(current_heart_cards) != 1) or (len(current_diamond_cards) != 1) or (len(current_spade_cards) != 1) or (len(current_club_cards) != 1):
            isUnique = False
            print("ERROR: The cards are not unique at value of ", value)
            print(current_value_cards)
            return isUnique

    
    print("All cards are unique")
    return isUnique


def isUniqueDeck(deck):
    isUnique = True
    
    for value in range(1,13,1): #range(start,end,step)
        current_value_cards = []
        for card in deck:
            if card[1] == value:
                current_value_cards.append(card)
        
        current_heart_cards = []
        current_diamond_cards = []
        current_spade_cards = []
        current_club_cards = []
        for card in current_value_cards:
            if card[0] == 'H':
                current_heart_cards.append(card)
            elif card[0] == 'D':
                current_diamond_cards.append(card)
            elif card[0] == 'S':
                current_spade_cards.append(card)
            elif card[0] == 'C':
                current_club_cards.append(card)
            else:
                print("ERROR: There is a card of unrecognized suit")
        
        if (len(current_heart_cards) != 1) or (len(current_diamond_cards) != 1) or (len(current_spade_cards) != 1) or (len(current_club_cards) != 1):
            isUnique = False
            print("ERROR: The cards are not unique at value of ", value)
            print(current_value_cards)
            return isUnique

    
    print("All cards are unique")
    return isUnique