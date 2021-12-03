from actions import *
from collections import deque
import deckGenerator


deck = deckGenerator.deckGen()
#print(deck)
#print(len(deck))

#initialize the game by partitioning the deck
random_game = True
if random_game:
    tableau = deckGenerator.tableauGen(deck)
    foundation = deckGenerator.foundationGen()
    stock = deckGenerator.StockGen(deck)
    
lens= np.array([3,3,3,3,3,3,3,3])
classes = np.tile(np.array([0,0,1]),8)
reachable_talon, unreachable_talon = deckGenerator.initKplus(stock)
s0 = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)
hist = deque([])

#s0.printDeck()
a,b = get_actions_supreme(s0, hist)
print("actions: ", a)
print("history:", b)

a,b = get_actions_supreme(s0, hist)
print("actions: ", a)
print("history:", b)
a,b = get_actions_supreme(s0, hist)
print("actions: ", a)
print("history:", b)

a,b = get_actions_supreme(s0, hist)
print("actions: ", a)
print("history:", b)

# a = [
# {'from': [1, 2, 5], 'to': [1, 1, 0]},
# {'from': [1, 3, 1], 'to': [1, 5, 0]},
# {'from': [1, 3, 2], 'to': [1, 2, 0]},
# {'from': [1, 4, 1], 'to': [1, 6, 0]},
# {'from': [1, 4, 3], 'to': [1, 0, 0]},
# {'from': [1, 5, 0], 'to': [1, 2, 0]},
# {'from': [1, 5, 6], 'to': [1, 1, 0]}
# ]

# b = [
# {'from': [1, 2, 5], 'to': [1, 1, 0]},
# {'from': [1, 4, 1], 'to': [1, 6, 0]},
# {'from': [1, 3, 1], 'to': [1, 5, 0]},
# {'from': [1, 3, 2], 'to': [1, 2, 0]},
# {'from': [1, 4, 3], 'to': [1, 0, 0]},
# {'from': [1, 5, 0], 'to': [1, 2, 0]},
# {'from': [1, 5, 6], 'to': [1, 1, 0]}
# ]



