import numpy as np

from board import GoBoard
from board_base import GO_POINT


class AlphaBetaForGo:
    def __init__(self, board=None, color=None, possibleMoves=None):
        self.bestPredictionMove = None
        self.boardInput: GoBoard = board
        self.board: GoBoard = board
        self.possibleMoves: list[GO_POINT] = possibleMoves
        self.color = color
        self.maxScore = None

        self.HastTable = {}

    def re(self, board, color, possibleMoves) -> None:
        self.boardInput: GoBoard = board.copy()
        self.board: GoBoard = board.copy()
        self.color = color
        self.possibleMoves: list[GO_POINT] = possibleMoves

    def getMaxScore(self):
        return self.maxScore

    def getPredictMove(self):
        return self.bestPredictionMove

    def getPredictBoard(self):
        predictBoard = self.boardInput.copy()
        predictBoard.play_move(self.bestPredictionMove, self.color)
        return predictBoard

    def run(self, depthLeft=5):
        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMoves:
            scores.append(self.HastTable.get(possibleMove))
        try:
            self.maxScore = max(scores)
            maxIndex = scores.index(self.maxScore)
            self.bestPredictionMove = self.possibleMoves[maxIndex]
            return self.bestPredictionMove
        except:
            return False

    def searcher(self, alpha, beta, depthLeft):
        bestScore = -np.Inf
        if (len(self.possibleMoves) == 0) or (depthLeft == 0):
            return True
        for possibleMove in self.possibleMoves:
            """
            try:
                score = self.HastTable.get(possibleMove)
                assert score is not None
            except AssertionError:
            """
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



