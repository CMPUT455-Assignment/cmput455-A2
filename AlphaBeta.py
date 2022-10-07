import numpy as np

from board import GoBoard
from board_base import GO_POINT


class AlphaBetaForGo:
    def __init__(self, board=None, color=None, possibleMoves=None):
        self.boardInput: GoBoard = board
        self.board: GoBoard = board
        self.possibleMoves: list[GO_POINT] = possibleMoves
        self.color = color

        self.HastTable = {}

    """    
    def re(self, GTP) -> None:
        self.boardInput: GoBoard = GTP.board
        self.board: GoBoard = self.board
        self.possibleMoves: list[GO_POINT] = GoBoardUtil.generate_legal_moves(self.board, self.board.current_player)
        self.color = self.board.current_player
    """

    def re(self, board, color, possibleMoves) -> None:
        self.boardInput: GoBoard = board
        self.board: GoBoard = board.copy()
        self.color = color
        self.possibleMoves: list[GO_POINT] = possibleMoves

    def run(self, depthLeft=6) -> str:
        self.searcher(alpha=-np.Inf, beta=np.Inf, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMoves:
            scores.append(self.HastTable.get(possibleMove))

        maxIndex = scores.index(max(scores))
        return self.possibleMoves[maxIndex]

    def searcher(self, alpha, beta, depthLeft) -> None | int:
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
