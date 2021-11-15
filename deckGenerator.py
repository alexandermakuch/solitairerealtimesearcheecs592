import random
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
    def __init__(self, tableau, foundation, reachable_talon, unreachable_talon):
        self.tableau = tableau
        self.foundation = foundation
        self.reachable_talon = reachable_talon
        self.unreachable_talon = unreachable_talon

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

def StockGen(Deck):
    Stock = deque(Deck[28:52])
    return Stock

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


def winGen(Deck):
    tableau1 = [deque([]),deque([])]
    Tableau = [tableau1,tableau1,tableau1,tableau1,tableau1,tableau1,tableau1] #empty tableau
    Reachable_Talon = deque([]) #empty reachable talon
    Unreachable_Talon = deque([]) #empty unreachable talon
    
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


    return Tableau, Foundation, Reachable_Talon, Unreachable_Talon


def turnstock(Stock:deque,Talon:list):
    Talon.append((deque([Stock.popleft(),Stock.popleft(),Stock.popleft()][::-1]))) #if we keep it like this, reversed, popleft is the proper way to remove from the talon. if we don't reverse we can just use pop instead
    return Talon

    
def kplusTalon(Stock:deque,Talon:list = []):
    '''
    Inputs: Stock, Talon
    Outputs: List of reachable states in Stock/Talon
    '''
    #First, we add every third card in the stock. These will always be reachable.
    sLen = len(Stock)

    reachable = deque([])
    unreachable = Stock.copy() #shallow copy of stock
    unreachable.extend(Talon) #adding cards in talon, they'll be removed as we 

    for x in range(int(sLen/3)):
        reachable.append(Stock[3*x+2])
        unreachable.remove(Stock[3*x+2])
    if (sLen % 3) != 0:
        reachable.append(Stock[sLen-1])
        unreachable.remove(Stock[sLen-1])

    if (len(Talon)) > 0:
        for x in range(len(Talon)):
            reachable.append(Talon[x][0])
            unreachable.remove((Talon[x][0]))

    #Next, we check if there are any lists in talon with length not equal to 3
    add = False
    frompoint = 52
    for x in range(len(Talon)):
        if len(Talon[x]) != 3:
            add = True
            frompoint = min(frompoint,x)
    
    if add:
        for x in range(frompoint,int(sLen/3)):
            reachable.append(Stock[3*x+1])
            unreachable.remove((Stock[3*x+1]))
        if (sLen % 3) != 0:
            reachable.append(Stock[sLen-2])
            unreachable.remove(Stock[sLen-2])

    #if reachable becomes binary, would be good to just return the reachable_talon and unreachable_talon here anyway
    return reachable, unreachable