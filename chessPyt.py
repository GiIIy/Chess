import chess
 
board=chess.Board()

class Evaluate():
    def __init__(self):
        self.board=chess.Board()
        self.moveCount=0
        self.moveList=[]

    def legalMoves(board):
        moves = [board.san(move) for move in board.legal_moves]
        return moves


    def basicEval(board):
            
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]

        if board.turn == chess.WHITE and board.is_checkmate():
            return -1000
        elif board.turn == chess.BLACK and board.is_checkmate():
            return 1000
        elif board.is_stalemate() or board.is_fivefold_repetition() or board.is_insufficient_material():
            return 0 

        else:

            return (
                chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
            )

    def minimax(board, depth, alpha=-float('inf'), beta=float('inf')):
        if board.is_game_over() or depth == 0:
            return Evaluate.basicEval(board), None

        if board.turn == chess.WHITE:
            best = -float('inf')
            best_move = None

            for move in legalMoves(board):
                board.push_san(move)
                val, _ = minimax(board, depth - 1, alpha, beta)
                board.pop()  

                if val > best:
                    best = val
                    best_move = move

                alpha = max(alpha, best)

                if beta <= alpha:
                    break

            return best, best_move

        else:
            best = float('inf')
            best_move = None

            for move in legalMoves(board):
                board.push_san(move)
                val, _ = minimax(board, depth - 1, alpha, beta)
                board.pop()

                if val < best:
                    best = val
                    best_move = move

                beta = min(beta, best)

                if beta <= alpha:
                    break

            return best, best_move





