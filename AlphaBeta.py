from board import GoBoard
from board_base import GO_POINT


class AlphaBetaForGo:
    def __init__(self, board: GoBoard, color, possibleMoves: list[GO_POINT]):
        self.boardInput = board
        self.possibleMoves = possibleMoves
        self.board = board
        self.color = color
        self.HastTable = {}

    def run(self, depthLeft=10) -> str:
        self.searcher(alpha=-999999, beta=999999, depthLeft=depthLeft)
        scores = []
        for possibleMove in self.possibleMoves:
            scores.append(self.HastTable.get(possibleMove))

        maxIndex = scores.index(max(scores))
        return self.possibleMoves[maxIndex]

    def searcher(self, alpha, beta, depthLeft) -> None | int:
        bestScore = -9999999
        if depthLeft == 0:
            return
        for possibleMove in self.possibleMoves:
            try:
                score = self.HastTable.get(possibleMove)
            except KeyError:
                self.board[possibleMove] = self.color
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
