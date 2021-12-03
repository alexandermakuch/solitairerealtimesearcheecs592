import random
import numpy as np
from collections import deque
#from SolitaireClasses import Talon

#Decision: Do we want the deck to be a list of tuples, 
#like Deck = [("S", "2"), ...] or a list of strings like ["S2", ...], 
# #I have implemented both, we can just copy the values of one into the final code to reduce computational complexity

Suits = ["D", "C", "H", "S"]
#Ace is 1, Jack is 11, Queen is 12, King is 13
#numbers will make comparisons easier later on
Elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


class State:
    def __init__(self, tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes):
        self.tableau = tableau.copy()
        self.foundation = foundation
        self.reachable_talon = reachable_talon
        self.unreachable_talon = unreachable_talon
        self.stock = stock
        self.lens = lens
        self.classes = classes

    def copy(self):
        tableau1 = [self.tableau[0][0].copy(), self.tableau[0][1].copy()]
        tableau2 = [self.tableau[1][0].copy(), self.tableau[1][1].copy()]
        tableau3 = [self.tableau[2][0].copy(), self.tableau[2][1].copy()]
        tableau4 = [self.tableau[3][0].copy(), self.tableau[3][1].copy()]
        tableau5 = [self.tableau[4][0].copy(), self.tableau[4][1].copy()]
        tableau6 = [self.tableau[5][0].copy(), self.tableau[5][1].copy()]
        tableau7 = [self.tableau[6][0].copy(), self.tableau[6][1].copy()]
        Tableau = [tableau1,tableau2,tableau3,tableau4,tableau5,tableau6,tableau7]


        foundation1 = self.foundation[0].copy() #for spades
        foundation2 = self.foundation[1].copy() #for clubs
        foundation3 = self.foundation[2].copy() #for hearts
        foundation4 = self.foundation[3].copy() #for diamonds
        Foundation = [foundation1,foundation2,foundation3,foundation4]





        return State(Tableau, Foundation, self.reachable_talon.copy(), self.unreachable_talon.copy(), self.stock.copy(), self.lens.copy(), self.classes.copy())

    def __eq__(self, other):
        return self.tableau == other.tableau and self.foundation == other.foundation and self.stock == other.stock

    def printDeck(self):
        print("Tableau: ", self.tableau)
        print("Foundation: ", self.foundation)
        print("Reachable Talon: ", self.reachable_talon)
        print("Unreachable Talon: ", self.unreachable_talon)

    def printDeckLength(self):
        tableauLength = []
        for tableau_stack in self.tableau:
            #print(tableau_stack)
            #print(tableau_stack[0])
            #print(tableau_stack[1])
            
            #print(len(tableau_stack[0]))
            #print(len(tableau_stack[1]))
    
            tableauLength.append(len(tableau_stack[0])+len(tableau_stack[1]))
        foundationLength = []
        for foundation_stack in self.foundation:
            foundationLength.append(len(foundation_stack))
        print("Tableau: ", tableauLength)
        print("Foundation: ", foundationLength)
        print("Reachable Talon: ", len(self.reachable_talon))
        print("Unreachable Talon: ", len(self.unreachable_talon))
        print("Total: ", sum(tableauLength)+sum(foundationLength)+len(self.reachable_talon)+len(self.unreachable_talon))

    #a function to make sure we have 52 unique cards
    def isUniqueStacks(self):
        isUnique = True
        deck = [] #to recreate the deck from the passed stacks
        for tableau_stack in self.tableau:
            for card in tableau_stack[0]:
                deck.append(card)
            for card in tableau_stack[1]:
                deck.append(card)
        
        for foundation_stack in self.foundation:
            for card in foundation_stack:
                deck.append(card)
        
        for card in self.reachable_talon:
            deck.append(card)

        for card in self.unreachable_talon:
            deck.append(card)

        
        for value in range(1,13,1): #range(start,end,step)
            current_value_cards = []
            for card in deck: #card is one [suit,value]
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

    def HeuristicH1H2(self):

        deck = [] #to recreate the deck from the passed stacks
        tableau_face_down = []
        tableau_face_up = []
        foundation_all = []
        for tableau_stack in self.tableau:
            for card in tableau_stack[0]:
                deck.append(card)
                tableau_face_up.append(card)
            for card in tableau_stack[1]:
                deck.append(card)
                tableau_face_down.append(card)
        
        for foundation_stack in self.foundation:
            for card in foundation_stack:
                deck.append(card)
                foundation_all.append(card)
        
        for card in self.reachable_talon:
            deck.append(card)

        for card in self.unreachable_talon:
            deck.append(card)


        H1 = 0
        H2 = 0
        num_elses = 0

        for card in deck:
            h1 = 0
            h2 = 0
            if card in foundation_all: #number 1 in table 1
                h1 = 5 - (card[1] - 1) #-1 because the rank value starts at 0
                h2 = 5

            elif card in tableau_face_down: #number 2 in table 1
                h1 = (card[1] - 1) - 13
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
                    h1 = -5
                    h2 = -1

            elif card in self.reachable_talon: #number 3 in table 1
                h1 = 0
                h2 = 1

            elif card in tableau_face_up: 
                tableau_build_cards = []
                if ((card[0] == "S") or (card[0] == "C")) and (card[1] != 13):
                    tableau_build_cards = [["H",card[1]+1],["D",card[1]+1]]
                elif ((card[0] == "H") or (card[0] == "D")) and (card[1] != 13):
                    tableau_build_cards = [["S",card[1]+1],["C",card[1]+1]]
                    
                for tableau_stack in self.tableau:
                    if (card[0] == tableau_stack[0][-1][0]) and (card[1] == tableau_stack[0][-1][1]): #for this card to be blocking, it has to be the last face up card in a tableau stack 
                    #for card2 in tableau_stack[0]:
                        #if (card[0] == card2[0]) and (card[1] == card2[1]):
                        #    blocking = tableau_stack[1] #if the card is face up in the tableau, find the list of cards it is blocking
                        #    break
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
            H2 += h2 #sum the heuristic for this card

        #print(num_elses)
        return H1, H2
        
    


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



def deckGen():
    Deck = []
    for i in Suits:
        for j in Elements:
            Deck.append([i,j])
    random.shuffle(Deck)
    return Deck

def StockGen(Deck):
    Stock = deque(Deck[28:52])
    return Stock

def foundationGen():
    foundation1 = deque([]) #for spades
    foundation2 = deque([]) #for clubs
    foundation3 = deque([]) #for hearts
    foundation4 = deque([]) #for diamonds
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


def winGen():
    tableau1 = [deque([]),deque([])]
    Tableau = [tableau1,tableau1,tableau1,tableau1,tableau1,tableau1,tableau1] #empty tableau
    Reachable_Talon = deque([]) #empty reachable talon
    Unreachable_Talon = deque([]) #empty unreachable talon
    stock = []
    classes = np.array([])
    lens = np.array([])
    
    foundation1 = deque([]) #for spades
    foundation2 = deque([]) #for clubs
    foundation3 = deque([]) #for hearts
    foundation4 = deque([]) #for diamonds

    for i in Suits:
        for j in reversed(Elements):#the K should be at the top and the A at the bottom
            if i == 'S':
                foundation1.append([i,j])
            elif i == 'C':
                foundation2.append([i,j])
            elif i == 'H':
                foundation3.append([i,j])
            elif i == 'D':
                foundation4.append([i,j])
    
    Foundation = [foundation1,foundation2,foundation3,foundation4]


    return Tableau, Foundation, Reachable_Talon, Unreachable_Talon, stock, lens, classes


def initKplus(x: list):
    reachable = deque([])
    unreachable = deque([])
    for a, val in enumerate(np.tile(np.array([False, False, True]), 8)):
        if val:
            reachable.append(x[a])
        else:
            unreachable.append(x[a])
    return reachable, unreachable


def Kplus(element, x: list,lens: np.array, classes: np.array):
    ind = x.index(element) #index in x of the element we're popping
    elemClass = classes[ind] #class of the element we're popping
    xLen = len(x)
    if elemClass == 2:
        lens =  np.tile(3,int(xLen/3))
        if xLen % 3 == 2:
            lens = np.append(lens,2)
        elif xLen %3 == 1:
            lens = np.append(lens,1)
        lens[int((ind)/3)] -= 1
        xLen -= 1
    elif elemClass == 1:
        lens[int((ind)/3)] -= 1
        xLen -= 1
    else:
        return None, None, None, None, None
    x.remove(element)

    def resort(tempLens):
        for i in range(len(tempLens)):
                    index = int(3*i + tempLens[i]-1)
                    reachability[index] = True
                    modClass[index] = 2

    if 0 in lens: #need to remove this index from lens
        lens = np.delete(lens,np.argwhere(lens == 0))

    modClass = np.zeros(xLen)
    reachability = np.zeros(xLen, dtype=bool)
    # add all from last non 3 (excluding final value) onwards as class 1.
    if xLen > 3:
        lensflip = lens[::-1][1:]
        lastInd = len(lensflip) - np.argmax(lensflip < 3) -1 #last non 3 index of lens
        index = int(np.sum(lens[:lastInd])-1+lens[lastInd])
        reachability[index] = True
        modClass[index] = 1
        for i in range(1,len(lens)-lastInd):
            index = int(np.sum(lens[:lastInd])-1+lens[lastInd]+3*i)
            if index < xLen:
                reachability[index] = True
                modClass[index] = 1
        
        #resort the deck and add last of each pile to reachable and set their class to 2
        tempLens = 3*np.ones(int(xLen/3))
        tempLens = np.append(tempLens, xLen % 3)
        resort(tempLens)
    elif xLen > 0:
        #len -> 1
        tempLens = 3*np.ones(int(xLen/3))
        tempLens = np.append(tempLens, xLen % 3)
        if len(lens) == 1:
            pass #just the last card is playable
        elif len(lens) == 2:
            if ind > lens[0]: #we're in pile 2
                resort(tempLens)
            else:
                #last card in 1st pile, then resort
                reachability[lens[0]-1] = True
                modClass[lens[0]-1] = 1
                resort(tempLens)
        elif len(lens) == 3:
            if ind > (lens[0]+lens[1]): #we're in pile 3
                resort(tempLens)
            elif ind > (lens[0]): #we're in pile 2
                reachability[lens[0]+lens[1]-1] = True
                modClass[lens[0]+lens[1]-1] = 1
                resort(tempLens)

            else: #we're in pile 1
                reachability[lens[0]-1] = True
                modClass[lens[0]-1] = 1
                reachability[lens[0]-1] = True
                modClass[lens[0]-1] = 1
                resort(tempLens)

    else:
        return None, None, None, None, None
    #make last card immediately playable    
    modClass[-1] = 1
    reachability[-1] = True

    reachable = deque([])
    unreachable = deque([])
    for a, val in enumerate(reachability):
        if val:
            reachable.append(x[a])
        else:
            unreachable.append(x[a])

    return x, lens, reachable, unreachable, modClass