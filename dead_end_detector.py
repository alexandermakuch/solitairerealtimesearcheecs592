import deckGenerator
from deckGenerator import State
from collections import deque
from search import faux_mns
import numpy as np
import pickle
from heuristics import HeuristicH1, HeuristicH2
import gui
NEW_STATE = False

if NEW_STATE:
    file = open('important','wb')
    deck = deckGenerator.deckGen()
    tableau = deckGenerator.tableauGen(deck)
    foundation = deckGenerator.foundationGen()
    stock = deckGenerator.StockGen(deck)
    lens= np.array([3,3,3,3,3,3,3,3])
    classes = np.tile(np.array([0,0,1]),8)
    reachable_talon, unreachable_talon = deckGenerator.initKplus(stock)
    s0 = State(tableau, foundation, reachable_talon, unreachable_talon, stock, lens, classes)
    pickle.dump(s0, file)
    file.close()

file = open('important','rb')
s0 = pickle.load(file)
file.close()

history = []
H1 = HeuristicH1(1)
H2 = HeuristicH2(1)
slist = []
print(faux_mns(s0, H2, history, slist))


 

file = open('stateList','wb')
pickle.dump(slist, file)
file.close()
print(len(slist))

gui.initGame(s0.reachable_talon, s0.unreachable_talon, s0.foundation, s0.tableau)