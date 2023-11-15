import chess
 
board=chess.Board()


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

def minimax(board, depth):
    
    if board.is_game_over() or depth == 0:
        return basicEval(board), None

    if board.turn == chess.WHITE:
        best = -10000
        best_move = None

        for move in legalMoves(board):
            board.push_san(move)
            val, _ = minimax(board, depth - 1)
            board.pop()

            if val > best:
                best = val
                best_move = move

        return best, best_move

    else:
        best = 10000
        best_move = None

        for move in legalMoves(board):
            board.push_san(move)
            val, _ = minimax(board, depth - 1)
            board.pop()

            if val < best:
                best = val
                best_move = move

        return best, best_move




