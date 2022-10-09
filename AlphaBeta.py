import numpy as np

import board_base
import board_util
import gtp_connection
from board import GoBoard
from board_base import GO_POINT, EMPTY
from board_util import GoBoardUtil


class AlphaBetaForGo:
    def __init__(self, board=None, color=None):
        self.inputBoard = board
        self.currentBoard = board
        self.inputColor = color
        self.currentColor = color

        self.HastTable_b = {}
        self.HastTable_w = {}
        self.possibleMovesNow = None

        self.bestMoveForCur = None
        self.bestScoreForCur = None
        self.bestMoveForOpp = None
        self.bestScoreForOpp = None

        self.possibleMovesForCur = None
        self.possibleMovesForOpp = None


    def re(self, currentBoard, currentColor) -> None:
        self.inputBoard = currentBoard.copy()
        self.currentBoard = currentBoard.copy()
        self.currentBoard2 = currentBoard.copy()
        self.inputColor = currentColor
        self.currentColor = currentColor

        self.possibleMovesForCur = GoBoardUtil.generate_legal_moves(self.inputBoard, self.inputColor)
        self.possibleMovesForOpp = None

    def run(self, depthLeft=5):
        self.run_cur()
        self.run_opp()

    def run_cur(self, depthLeft=5):
        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMovesForCur:
            if self.inputColor == 1:
                move_b = self.HastTable_b.get(possibleMove)
                scores.append(move_b)
                #print("cur move_b: ", possibleMove, move_b)
            else:
                move_w = self.HastTable_w.get(possibleMove)
                scores.append(move_w)
                #print("cur move_w: ", possibleMove, move_w)
        #print("b", self.HastTable_b)
        #print("w", self.HastTable_w)
        #self.bestScoreForCur = max(scores)
        #maxIndex = scores.index(self.bestScoreForCur)
        #self.bestMoveForCur = self.possibleMovesNow[maxIndex]
        index = 0
        for item in scores:
            if item == True:
                self.bestMoveForCur = self.possibleMovesForCur[index]
                print("\n\n????", self.bestMoveForCur)
                break
            index += 1

    def run_opp(self, depthLeft=5):
        self.currentBoard = self.currentBoard2
        self.currentBoard.play_move(self.bestMoveForCur, self.inputColor)
        self.possibleMovesForOpp = GoBoardUtil.generate_legal_moves(self.currentBoard, board_base.opponent(self.inputColor))
        print("\n\n+++++++ possibleMovesForCur", self.possibleMovesForCur)
        print("\n+++++++ possibleMovesForOpp", self.possibleMovesForOpp)
        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMovesForOpp:
            print(gtp_connection.format_point(divmod(possibleMove, self.inputBoard.size + 1)).lower())
            if self.inputColor == 1:
                move_b = self.HastTable_b.get(possibleMove)
                scores.append(move_b)
                #print("opp move_b: ", possibleMove, move_b)
            else:
                move_w = self.HastTable_w.get(possibleMove)
                scores.append(move_w)
                #print("opp move_w: ", possibleMove, move_w)
        #self.bestScoreForOpp = max(scores)
        #maxIndex = scores.index(self.bestScoreForCur)
        #self.bestMoveForOpp = self.possibleMovesNow[maxIndex]
        index = 0
        for item in scores:
            if item == True:
                self.bestMoveForCur = self.possibleMovesForOpp[index]
                break
            index += 1

    def getPredictWinner(self):
        if self.bestScoreForOpp > self.bestScoreForCur:
            return self.inputColor, self.bestScoreForOpp
        else:
            return board_base.opponent(self.inputColor), self.bestMoveForCur

    def statEvaluate(self):
        winColor = self.winner()
        if winColor == self.currentColor:
            return True
        assert winColor == board_base.opponent(self.currentColor)
        return False

    def winner(self):
        if self.currentColor == 2:
            return 1
        else:
            return 2

    def searcher(self, alpha, beta, depthLeft):
        bestScore = -np.Inf
        self.possibleMovesNow = GoBoardUtil.generate_legal_moves(self.currentBoard, self.currentColor)
        if depthLeft == 0 or len(self.possibleMovesNow) == 0:
            return self.statEvaluate()
        print("Searcher self.possibleMovesNow", self.possibleMovesNow)
        for move in self.possibleMovesNow:
            """
            try:
                score = self.HastTable.get(possibleMove)
                assert score is not None
            except AssertionError:"""
            self.currentColor = board_base.opponent(self.currentColor)
            self.currentBoard.play_move(move, self.currentColor)
            score = not self.searcher(-beta, -alpha, depthLeft - 1)
            self.currentBoard = self.inputBoard
            #self.current_player = self.inputColor
            if score >= beta:
                return score
            if score > bestScore:
                bestScore = score
                if score > alpha:
                    alpha = score
            if self.currentColor == 1:
                self.HastTable_b[move] = bestScore
            else:
                self.HastTable_w[move] = bestScore
        return bestScore

"""
    def searcher(self, alpha, beta, depthLeft, color):
        if depthLeft == 0:
            return alpha
        for possibleMove in self.possibleMoves:
            self.board.play_move(possibleMove, self.board.current_player)
            if color == 0:
                color = 1
            else:
                color = 0
            score = -self.searcher(-beta, -alpha, depthLeft - 1, color)
            if score >= beta:
                self.HastTable[possibleMove] = beta
                return beta     # fail hard beta - cutoff
            if score > alpha:
                alpha = score   # alpha acts like max in MiniMax
                self.HastTable[possibleMove] = alpha
        return alpha

    def negamaxBoolean(self):
        end = True
        empties = self.board.get_empty_points()
        for move in empties:
            if self.is_legal(move, self.color):
                end = False

                self.board[move] = self.color
                board_base.opponent()
                success = not self.negamaxBoolean()
                self.board[move] = EMPTY
                self.current_player = self.color
                if success:
                    self.current_winning_move = move
                    self.HastTable[move] = True
                    return True
        if end:
            result = self.staticallyEvaluateForPlay()
            self.HastTable[move] = result
            return result
            # return self.storeResult(tt, result)
        tt.store(codes, False)
        return False
        # return self.storeResult(tt, False)
"""

