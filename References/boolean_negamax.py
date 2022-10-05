# Cmput 455 sample code
# Boolean Negamax
# Written by Martin Mueller

import time
from game_basics import colorAsString, isBlackWhite, opponent

def negamaxBoolean(state):
    if state.endOfGame():
        return state.staticallyEvaluateForToPlay()
    for m in state.legalMoves():
        state.play(m)
        success = not negamaxBoolean(state)
        state.undoMove()
        if success:
            return True
    return False

def negamaxBooleanSolveAll(state):
    if state.endOfGame():
        return state.staticallyEvaluateForToPlay()
    wins = []
    for m in state.legalMoves():
        state.play(m)
        success = not negamaxBoolean(state)
        state.undoMove()
        if success:
            wins.append(m)
    return wins

def solveForColor(state, color): 
# use for 3-outcome games such as TicTacToe
    assert isBlackWhite(color)
    saveOldDrawWinner = state.drawWinner
    # to check if color can win, count all draws as win for opponent
    state.setDrawWinner(opponent(color)) 
    start = time.process_time()
    winForToPlay = negamaxBoolean(state)
    timeUsed = time.process_time() - start
    state.setDrawWinner(saveOldDrawWinner)
    winForColor = winForToPlay == (color == state.toPlay)
    return winForColor, timeUsed

def timed_solve(state): 
    start = time.process_time()
    wins = negamaxBooleanSolveAll(state)
    timeUsed = time.process_time() - start
    return wins, timeUsed
