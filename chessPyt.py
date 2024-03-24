import chess
 
board=chess.Board()

class Evaluate():

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

    def minimax(board, depth, PST, alpha=-float('inf'), beta=float('inf')):
        if board.is_game_over() or depth == 0:
            return Evaluate.overallEval(board,PST), None

        if board.turn == chess.WHITE:
            best = -float('inf')
            best_move = None

            for move in Evaluate.legalMoves(board):
                board.push_san(move)
                val, _ = Evaluate.minimax(board, depth - 1,PST, alpha, beta)
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

            for move in Evaluate.legalMoves(board):
                board.push_san(move)
                val, _ = Evaluate.minimax(board, depth - 1, PST, alpha, beta)
                board.pop()

                if val < best:
                    best = val
                    best_move = move

                beta = min(beta, best)

                if beta <= alpha:
                    break

        
            return best, best_move

    def pTableEval(board, piece, square, PST, isWhite):

        if str(piece).lower() == 'p' :
            if isWhite:
                return PST[chess.PAWN][square] / 10
                
            else:
                return -PST[chess.PAWN][chess.square_mirror(square)] / 10
            
        elif str(piece).lower() == 'n':
            
            if isWhite:
                return PST[chess.KNIGHT][square] / 10
            else:
                return -PST[chess.KNIGHT][chess.square_mirror(square)] / 10
            
        elif str(piece).lower() == 'b':
            
            if isWhite:
                return PST[chess.BISHOP][square] / 10
            else:
                return -PST[chess.BISHOP][chess.square_mirror(square)] / 10
            
        elif str(piece).lower() == 'r':
    
            if isWhite:
                return PST[chess.ROOK][square] / 10
            else:
                return -PST[chess.ROOK][chess.square_mirror(square)] / 10
            
        elif str(piece).lower() == 'q':
           
            if isWhite:
                return PST[chess.QUEEN][square] / 10
            else:
                return -PST[chess.QUEEN][chess.square_mirror(square)] / 10
            
        elif str(piece).lower() == 'k':
            
            if isWhite:
                return PST[chess.KING][square] / 10
            
            else:
                return -PST[chess.KING][chess.square_mirror(square)] / 10
                
        
        else:
            return 0 
        
    
    def symbol(piece):
        if piece == 1:
            return "p"
        elif piece == 2:
            return "n"
        elif piece == 3:
            return "b"
        elif piece == 4:
            return "r"
        elif piece == 5:
            return "q"
        elif piece == 6:
            return "k"

    
    
    def pTableScore(board, PST):

        score = 0
        for i in range(64):
            piece = board.piece_at(i)
            if str(piece) == 'None':
                pass
            elif str(piece).isupper():
                isWhite = True
            else:
                isWhite = False
            
           
            

            if piece is not None:
                score += Evaluate.pTableEval(board, piece.symbol(), i, PST, isWhite)
               
               
                
        return score
    
    def overallEval(board,PST):
        return float(Evaluate.basicEval(board)) + float(Evaluate.pTableScore(board,PST))
    


def numPiecesLeft(board):
    return len(board.piece_map())

pawn_table = [

    0, 0, 0, 0, 0, 0, 0, 0,
    5, 5, 5, 5, 5, 5 ,5 ,5,
    1, 1, 2, 3, 3, 2, 1, 1,
    0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
    0, 0, 0, 2, 2, 0, 0, 0,
    0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
    0.5, 1, 1, -2, -2, 1, 1, 0.5,
    0, 0, 0, 0, 0, 0, 0, 0
]

knights_table = [
    -5, -4, -3, -3, -3, -3, -4, -5,
    -4, -2, 0, 0, 0, 0, -2, -4,
    -3, 0, 1, 1.5, 1.5, 1, 0, -3,
    -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
    -3, 0, 1.5, 2, 2, 1.5, 0, -3,
    -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
    -4, -2, 0, 0.5, 0.5, 0, -2, -4,
    -5, -4, -3, -3, -3, -3, -4, -5
]

bishops_table = [
    -2, -1, -1, -1, -1, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 1, 1, 0.5, 0, -1,
    -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
    -1, 0, 1, 1, 1, 1, 0, -1,
    -1, 1, 1, 1, 1, 1, 1, -1,
    -1, 0.5, 0, 0, 0, 0, 0.5, -1,
    -2, -1, -1, -1, -1, -1, -1, -2
]

rooks_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0.5, 1, 1, 1, 1, 1, 1, 0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    -0.5, 0, 0, 0, 0, 0, 0, -0.5,
    0, 0, 0, 0.5, 0.5, 0, 0, 0
]

queens_table = [
    -2, -1, -1, -0.5, -0.5, -1, -1, -2,
    -1, 0, 0, 0, 0, 0, 0, -1,
    -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
    -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
    -1, 0, 0.5, 0, 0, 0, 0, -1,
    -2, -1, -1, -0.5, -0.5, -1, -1, -2
]

kings_table = [
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -3, -4, -4, -5, -5, -4, -4, -3,
    -2, -3, -3, -4, -4, -3, -3, -2,
    -1, -2, -2, -2, -2, -2, -2, -1,
    2, 2, 0, 0, 0, 0, 2, 2,
    2, 3, 1, 0, 0, 1, 3, 2
]


PST = {
    chess.PAWN: list(reversed(pawn_table)),
    chess.KNIGHT: list(reversed(knights_table)),
    chess.BISHOP: list(reversed(bishops_table)),
    chess.ROOK: list(reversed(rooks_table)),
    chess.QUEEN: list(reversed(queens_table)),
    chess.KING: list(reversed(kings_table))
}





