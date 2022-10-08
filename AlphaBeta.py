import numpy as np

from board import GoBoard
from board_base import GO_POINT
import gtp_connection


class AlphaBetaForGo:
    def __init__(self, board=None, color=None, possibleMoves=None):
        self.boardInput: GoBoard = board
        self.board: GoBoard = board
        self.possibleMoves: list[GO_POINT] = possibleMoves
        self.color = color
        self.maxScore = None

        self.HastTable = {}

    def re(self, board, color, possibleMoves) -> None:
        self.boardInput: GoBoard = board
        self.board: GoBoard = board
        self.color = color
        self.possibleMoves: list[GO_POINT] = possibleMoves

    def run(self, depthLeft=6):
        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMoves:
            scores.append(self.HastTable.get(possibleMove))
        try:
            self.maxScore = max(scores)
            maxIndex = scores.index(self.maxScore)
            move = divmod(self.possibleMoves[maxIndex], self.board.size + 1)
            return gtp_connection.format_point(move)
        except:
            return False

    def getMaxScore(self):
        return self.maxScore

    def searcher(self, alpha, beta, depthLeft):
        bestScore = -np.Inf
        if (depthLeft == 0) or (len(self.possibleMoves) == 0):
            return True
        for possibleMove in self.possibleMoves:
            try:
                score = self.HastTable.get(possibleMove)
                assert score is not None
            except AssertionError:
                self.board.play_move(possibleMove, self.color)
                score = -self.searcher(-beta, -alpha, depthLeft - 1)
                self.board = self.boardInput
            if score >= beta:
                return score
            if score > bestScore:
                bestScore = score
                if score > alpha:
                    alpha = score
            self.HastTable[possibleMove] = bestScore
        return bestScore



