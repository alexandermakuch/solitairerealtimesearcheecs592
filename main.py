import deckGenerator
from deckGenerator import State
from search import faux_mns, faux_mns_strategy
import numpy as np
import pickle
from heuristics import HeuristicH1, HeuristicH2, HeuristicH3
import gui_cycler
import time
import os



def newState():
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
def pruningTest(heuristic,state='random'):
    '''
    heuristic: initialized heuristic
    state: random for new state, or int 1-51 for known winnable
    '''
    '''
    printed: num moves, win/loss, time (in seconds)
    '''
    if state=='random':
        newState()
        file = open('important', 'rb')
        s0 = pickle.load(file)
        file.close()
    else: 
        file = open('winnable_states/'+fileList[state],'rb')
        s0 = pickle.load(file)
        file.close()


    history = []
    slist1 = [s0.copy()]
    abbb = time.time()
    result = faux_mns(s0.copy(), heuristic, history, slist1)
    time1= time.time()-abbb
    if result == 'Win':
        ans = 1
    else:
        ans = 0

    history = []
    slist2 = [s0.copy()]
    abbb = time.time()
    result = faux_mns_strategy(s0, heuristic, history, slist2)
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


    print('Press right/left arrow keys to cycle through states, press R to play all to end')
    gui_cycler.main()

def heuristicTest(heuristic, state='random', pruning='original'):
    '''
    heuristic: initialized heuristic
    state: random for new state, or int 1-51 for known winnable
    pruning: 'original' for pruning from [2], 'proposed' for our proposed pruning
    '''
    '''
    printed: num moves, win/loss, time (in seconds)
    '''
    if state=='random':
        newState()
        file = open('important', 'rb')
        s0 = pickle.load(file)
        file.close()
    else: 
        file = open('winnable_states/'+fileList[state],'rb')
        s0 = pickle.load(file)
        file.close()

    if pruning=='original':
        history = []
        slist2 = [s0.copy()]
        time1 = time.time()
        result = faux_mns(s0, heuristic, history, slist2)
        time2 = time.time()-time1
        if result == 'Win':
            ans2 = 1
        else:
            ans2 = 0
        file = open('stateList', 'wb')
        pickle.dump(slist2, file)
        file.close()
        fields=[len(slist2), ans2,time2]
        print(fields)
    elif pruning == 'proposed':
        history = []
        slist2 = [s0.copy()]
        time1 = time.time()
        result = faux_mns_strategy(s0, heuristic, history, slist2)
        time2 = time.time()-time1
        if result == 'Win':
            ans2 = 1
        else:
            ans2 = 0
        file = open('stateList', 'wb')
        pickle.dump(slist2, file)
        file.close()
        fields=[len(slist2), ans2,time2]
        print(fields)
    else:
        raise Exception('Illegal input to pruning') 

    print('Press right/left arrow keys to cycle through states, press R to play all to end')
    print('Please note this is not real time, it takes ~1.5 seconds to display all moves')
    gui_cycler.main()






'''
Uncomment whichever heuristic you would like to run
Set state to 'random' to generate new state, or int 1-51 for known winnable
For heuristicTest, you can choose pruning, options are 'original' or 'proposed'
'''
# heuristic = HeuristicH1(1)
# heuristic = HeuristicH2(1)
heuristic = HeuristicH3(1)

if __name__ == '__main__':
    pruningTest(heuristic, state=51)
    #heuristicTest(heuristic)