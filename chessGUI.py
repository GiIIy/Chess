import pygame
import chess
import chessPyt
import promoPopUp

WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = 60
PIECE_SIZE = 60
FPS = 60


pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

piece_images = {
    chess.Piece.from_symbol('P'): pygame.transform.scale(pygame.image.load('assets/whitePawn.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('p'): pygame.transform.scale(pygame.image.load('assets/blackPawn.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('R'): pygame.transform.scale(pygame.image.load('assets/whiteRook.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('r'): pygame.transform.scale(pygame.image.load('assets/blackRook.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('N'): pygame.transform.scale(pygame.image.load('assets/whiteKnight.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('n'): pygame.transform.scale(pygame.image.load('assets/blackKnight.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('B'): pygame.transform.scale(pygame.image.load('assets/whiteBishop.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('b'): pygame.transform.scale(pygame.image.load('assets/blackBishop.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('Q'): pygame.transform.scale(pygame.image.load('assets/whiteQueen.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('q'): pygame.transform.scale(pygame.image.load('assets/blackQueen.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('K'): pygame.transform.scale(pygame.image.load('assets/whiteKing.png'), (PIECE_SIZE, PIECE_SIZE)),
    chess.Piece.from_symbol('k'): pygame.transform.scale(pygame.image.load('assets/blackKing.png'), (PIECE_SIZE, PIECE_SIZE)),
}

board = chess.Board()


dragging = False
dragged_piece = None
start_square = None

def draw_board():
    for i in range(8):
        for j in range(8):
            color = "white" if (i + j) % 2 == 0 else "brown"
            pygame.draw.rect(screen, color, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    draw_pieces()

def draw_pieces():
    for i in range(8):
        for j in range(8):
            piece = board.piece_at(i + j * 8)
            if piece is not None:
                x = i * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
                y = (7 - j) * SQUARE_SIZE + (SQUARE_SIZE - PIECE_SIZE) // 2
                piece_image = piece_images.get(piece)
                if piece_image is not None:
                    piece_image = pygame.transform.scale(piece_image, (PIECE_SIZE, PIECE_SIZE))
                    piece_image_rect = piece_image.get_rect(center=(x + 30, y + 30))
                    screen.blit(piece_image, piece_image_rect)


run = True
timer = pygame.time.Clock()

while run:
    timer.tick(FPS)
    screen.fill("lightgray")
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif dragging or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_coord = event.pos[0] // SQUARE_SIZE
                y_coord = 7 - event.pos[1] // SQUARE_SIZE
                start_square = chess.square(x_coord, y_coord)
                piece = board.piece_at(start_square)

                if piece is not None:
                    dragging = True
                    dragged_piece = piece_images.get(piece)
                    dragged_piece = pygame.transform.scale(dragged_piece, (PIECE_SIZE, PIECE_SIZE))

            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = event.pos
                x -= PIECE_SIZE // 2  
                y -= PIECE_SIZE // 2
                screen.fill("lightgray")
                draw_board()
                screen.blit(dragged_piece, (x, y))
                pygame.display.flip()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                dragging = False
                x_coord = event.pos[0] // SQUARE_SIZE
                y_coord = 7 - event.pos[1] // SQUARE_SIZE
                end_square = chess.square(x_coord, y_coord)
                move = chess.Move(start_square, end_square)

                if board.piece_at(start_square).piece_type == chess.PAWN and chess.square_rank(end_square) in (0, 7):
                    promotionMoves = []
                    for x in board.legal_moves:
                        if str(x)[-1] in ["q", "r", "b", "n"]:
                            promotionMoves.append(x)

                    if promotionMoves != []:
                        promoPiece = promoPopUp.create_popup_window()
                        for x in promotionMoves:
                            if str(x)[-1] == promoPiece:
                                move = x
                                break


                san_move = event.dict.get('text') or board.san(move)
                try:
                    move = chess.Move.from_uci(san_move)
                except:
                    pass

                if move in board.legal_moves:
                    board.push(move)
                    

                screen.fill("lightgray")
                draw_board()
                pygame.display.flip()

                if board.turn == chess.BLACK and not board.is_game_over():
                    numLeft = chessPyt.numPiecesLeft(board)
                    if numLeft < 15:
                        depth = 4
                    elif numLeft < 10:
                        depth = 5
                    else:
                        depth = 3
                    bestValue, bestMove = chessPyt.Evaluate.minimax(board, depth, chessPyt.PST)
                    print("Evaluation: ", bestValue, "Best Move: ", bestMove)
                    board.push_san(bestMove)

                if board.is_game_over():
                    fen = board.board_fen()
                    print(fen)


    pygame.display.flip()

pygame.quit()


 