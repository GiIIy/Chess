import pygame
import chess
import chessPyt  # my other python file
import promoPopUp  # my other python file

class ChessGame:
    def __init__(self, fen=chess.STARTING_FEN):
        # Constants
        self.WIDTH, self.HEIGHT = 680, 480  # Adjusted width to accommodate the sidebar
        self.SQUARE_SIZE = 60
        self.PIECE_SIZE = 60
        self.FPS = 60

        # Sidebar dimensions
        self.SIDEBAR_WIDTH = 200
        self.MOVE_HISTORY_HEIGHT = self.HEIGHT

        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Chess')

        # Create a font for displaying move history
        self.font = pygame.font.SysFont('Arial', 20)

        # Dictionary to store piece images
        self.piece_images = {
            chess.Piece.from_symbol('P'): pygame.transform.scale(pygame.image.load('assets/whitePawn.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('p'): pygame.transform.scale(pygame.image.load('assets/blackPawn.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('N'): pygame.transform.scale(pygame.image.load('assets/whiteKnight.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('n'): pygame.transform.scale(pygame.image.load('assets/blackKnight.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('B'): pygame.transform.scale(pygame.image.load('assets/whiteBishop.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('b'): pygame.transform.scale(pygame.image.load('assets/blackBishop.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('R'): pygame.transform.scale(pygame.image.load('assets/whiteRook.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('r'): pygame.transform.scale(pygame.image.load('assets/blackRook.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('Q'): pygame.transform.scale(pygame.image.load('assets/whiteQueen.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('q'): pygame.transform.scale(pygame.image.load('assets/blackQueen.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('K'): pygame.transform.scale(pygame.image.load('assets/whiteKing.png'), (self.PIECE_SIZE, self.PIECE_SIZE)),
            chess.Piece.from_symbol('k'): pygame.transform.scale(pygame.image.load('assets/blackKing.png'), (self.PIECE_SIZE, self.PIECE_SIZE))
        }

        # Initialize the chess board
        self.board = chess.Board(fen)

        # Variables for dragging pieces
        self.dragging = False
        self.dragged_piece = None
        self.start_square = None

        # List to store move history
        self.move_history = []

        # starting evaluation score
        self.evaluation, self.bestMove = chessPyt.Evaluate.minimax(self.board, 3, chessPyt.PST)

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                # Alternate square colors
                color = "white" if (i + j) % 2 == 0 else "brown"
                pygame.draw.rect(self.screen, color, (i * self.SQUARE_SIZE, j * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
        self.draw_pieces()

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.piece_at(i + j * 8)
                if piece is not None:
                    x = i * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
                    y = (7 - j) * self.SQUARE_SIZE + (self.SQUARE_SIZE - self.PIECE_SIZE) // 2
                    piece_image = self.piece_images.get(piece)
                    if piece_image is not None:
                        piece_image = pygame.transform.scale(piece_image, (self.PIECE_SIZE, self.PIECE_SIZE))
                        piece_image_rect = piece_image.get_rect(center=(x + 30, y + 30))
                        self.screen.blit(piece_image, piece_image_rect)

    def draw_move_history(self):
        sidebar = pygame.Surface((self.SIDEBAR_WIDTH, self.MOVE_HISTORY_HEIGHT))
        sidebar.fill((200, 200, 200))

        # Render and blit move history
        y_offset = 10
        white_moves = []
        black_moves = []

        for i, move in enumerate(self.move_history):
            if i % 2 == 0:
                white_moves.append(move)
            else:
                black_moves.append(move)
        i = 0
        text = self.font.render("Moves: ", True, (0, 0, 0))
        sidebar.blit(text, (10, y_offset))
        y_offset += self.font.get_linesize()

        for white_move, black_move in zip(white_moves, black_moves):
            i += 1
            move_text = f"{i}.{white_move} {black_move}"
            text = self.font.render(move_text, True, (0, 0, 0))
            sidebar.blit(text, (10, y_offset))
            y_offset += self.font.get_linesize()

        # Render and blit evaluation score
        text = self.font.render(f"Eval: {self.evaluation}", True, (0, 0, 0))
        sidebar.blit(text, (10, self.HEIGHT - self.font.get_linesize()))  # Placing evaluation at the bottom

        text = self.font.render(f"Best Move: {self.bestMove}", True, (0, 0, 0))
        sidebar.blit(text, (10, self.HEIGHT - self.font.get_linesize() * 2))  # Placing evaluation at the bottom

        self.screen.blit(sidebar, (self.WIDTH - self.SIDEBAR_WIDTH, 0))

    def run_game(self):
        run = True
        timer = pygame.time.Clock()
        if self.board.turn == chess.WHITE:
            player_color = chess.WHITE
        else:
            player_color = chess.BLACK

        while run:
            timer.tick(self.FPS)
            self.screen.fill("lightgray")
            self.draw_board()
            self.draw_move_history()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                elif self.dragging or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.board.turn == player_color:
                            x_coord = event.pos[0] // self.SQUARE_SIZE
                            y_coord = 7 - event.pos[1] // self.SQUARE_SIZE
                            self.start_square = chess.square(x_coord, y_coord)
                            piece = self.board.piece_at(self.start_square)

                            if piece is not None and piece.color == player_color:
                                self.dragging = True
                                self.dragged_piece = self.piece_images.get(piece)
                                self.dragged_piece = pygame.transform.scale(self.dragged_piece, (self.PIECE_SIZE, self.PIECE_SIZE))

                    elif event.type == pygame.MOUSEMOTION and self.dragging:
                        x, y = event.pos
                        x -= self.PIECE_SIZE // 2
                        y -= self.PIECE_SIZE // 2
                        self.screen.fill("lightgray")
                        self.draw_board()  
                        self.draw_move_history()
                        self.screen.blit(self.dragged_piece, (x, y))
                        pygame.display.flip()

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
                        if self.board.turn == player_color:
                            self.dragging = False
                            x_coord = event.pos[0] // self.SQUARE_SIZE
                            y_coord = 7 - event.pos[1] // self.SQUARE_SIZE
                            end_square = chess.square(x_coord, y_coord)
                            move = chess.Move(self.start_square, end_square)

                            # Handling pawn promotion
                            if self.board.piece_at(self.start_square).piece_type == chess.PAWN and chess.square_rank(end_square) in (0, 7):
                                promotionMoves = []
                                for x in self.board.legal_moves:
                                    if str(x)[-1] in ["q", "r", "b", "n"]:
                                        promotionMoves.append(x)

                                if promotionMoves != []:
                                    promoPiece = promoPopUp.create_popup_window()
                                    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                                    for x in promotionMoves:
                                        if str(x)[-1] == promoPiece:
                                            move = x
                                            break

                            san_move = event.dict.get('text') or self.board.san(move)
                            try:
                                move = chess.Move.from_uci(san_move)
                            except:
                                pass

                            if move in self.board.legal_moves:
                                self.board.push(move)
                                self.move_history.append(san_move)  # Add move to history

                                # Update evaluation score after move
                                bestValue, self.bestMove = chessPyt.Evaluate.minimax(self.board, 3, chessPyt.PST)
                                self.evaluation = bestValue

                            # Redraw only the necessary portion of the screen
                            self.draw_board()  
                            self.draw_move_history()
                            pygame.display.flip()

                            # Check if the game is over
                            if self.board.is_game_over():
                                print("Game Over")
                                print(self.board.result())

                            # Change player turn
                            player_color = not player_color

            pygame.display.flip()

        pygame.quit()


    

