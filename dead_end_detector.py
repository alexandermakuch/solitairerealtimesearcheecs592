from os import stat
import deckGenerator
from deckGenerator import State
from collections import deque
from search import faux_mns, faux_mns_strategy
import numpy as np
import pickle
from heuristics import HeuristicH1, HeuristicH2, HeuristicH3
import gui
import time
import os
import csv
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



fileList = []
for filename in os.listdir("winnable_states"):
    fileList.append(filename)


file = open('winnable_states/'+fileList[16],'rb')
s0 = pickle.load(file)
file.close()

# file = open('important','rb')
# s0 = pickle.load(file)
# file.close()


history = []
h3 = HeuristicH3(1)
slist1 = [s0.copy()]
abbb = time.time()
result = faux_mns(s0.copy(), h3, history, slist1)
time1= time.time()-abbb
if result == 'Win':
    ans = 1
else:
    ans = 0

history = []
h3 = HeuristicH3(1)
slist2 = [s0.copy()]
abbb = time.time()
result = faux_mns_strategy(s0, h3, history, slist2)
time2 = time.time()-abbb
if result == 'Win':
    ans2 = 1
else:
    ans2 = 0

file = open('stateList', 'wb')
pickle.dump(slist2, file)
file.close()
fields=[len(slist1), time1, ans, len(slist2), time2, ans2]
print(fields)
# with open('strategy_testing.csv', 'a') as f:
#     writer = csv.writer(f)
#     writer.writerow(fields)



    # if filename.endswith(".asm") or filename.endswith(".py"): 
    #      # print(os.path.join(directory, filename))
    #     continue
    # else:
    #     continue



# if result == 'Win':
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~Win~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#     file = open('important', 'rb')
#     winning_state = pickle.load(file)
#     file.close()
#     file = open("win" + str((time.time())),'wb')
#     pickle.dump(winning_state, file)
#     file.close()
#gui.initGame(s0.reachable_talon, s0.unreachable_talon, s0.foundation, s0.tableau)