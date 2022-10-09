import numpy as np

import board_base
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

    def re(self, currentBoard, currentColor) -> None:
        self.inputBoard = currentBoard
        self.currentBoard = currentBoard.copy()
        self.currentBoard2 = currentBoard.copy()
        self.inputColor = currentColor
        self.currentColor = currentColor

    def run(self, depthLeft=5):
        self.run_cur()
        self.run_opp()

    def run_cur(self, depthLeft=5):
        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMovesNow:
            print(gtp_connection.format_point(divmod(possibleMove, self.inputBoard.size + 1)).lower())
            if self.inputColor == 1:
                scores.append(self.HastTable_b.get(possibleMove))
            else:
                scores.append(self.HastTable_w.get(possibleMove))
        self.bestScoreForCur = max(scores)
        maxIndex = scores.index(self.bestScoreForCur)
        self.bestMoveForCur = self.possibleMovesNow[maxIndex]

    def run_opp(self, depthLeft=5):
        self.currentBoard = self.currentBoard2
        self.currentBoard[self.bestMoveForCur] = self.inputColor

        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMovesNow:
            print(gtp_connection.format_point(divmod(possibleMove, self.inputBoard.size + 1)).lower())
            if self.inputColor == 1:
                scores.append(self.HastTable_b.get(possibleMove))
            else:
                scores.append(self.HastTable_w.get(possibleMove))
        self.bestScoreForOpp = max(scores)
        maxIndex = scores.index(self.bestScoreForCur)
        self.bestMoveForOpp = self.possibleMovesNow[maxIndex]

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
        if depthLeft == 0:
            return self.statEvaluate()
        self.possibleMovesNow = GoBoardUtil.generate_legal_moves(self.currentBoard, self.currentColor)
        for move in self.possibleMovesNow:
            """
            try:
                score = self.HastTable.get(possibleMove)
                assert score is not None
            except AssertionError:"""
            self.currentColor = board_base.opponent(self.currentColor)
            self.currentBoard[move] = self.currentColor
            score = not self.searcher(-beta, -alpha, depthLeft - 1)
            self.currentBoard[move] = EMPTY
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

