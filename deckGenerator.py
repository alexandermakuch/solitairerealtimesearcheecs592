import random

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