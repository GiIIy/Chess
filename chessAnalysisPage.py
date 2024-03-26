import pygame
import sys
import chess
import analysisChess

class ChessBoardApp:
    def __init__(self):
        # Constants
        self.WIDTH, self.HEIGHT = 600, 480
        self.ROWS, self.COLS = 8, 8
        self.SQUARE_SIZE = 60
        self.BOARD_WIDTH = self.COLS * self.SQUARE_SIZE
        self.SIDEBAR_WIDTH = self.WIDTH - self.BOARD_WIDTH

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Current player
        self.current_player = chess.WHITE

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Chess Board')

        # Chess Board
        self.board = [[0]*self.COLS for _ in range(self.ROWS)]

        # Load Piece Images
        self.load_piece_images()

    def load_piece_images(self):
        # Load and scale piece images
        self.piece_images = {}
        pieces = [
            ("white_king", "whiteKing.png"), ("white_queen", "whiteQueen.png"), ("white_knight", "whiteKnight.png"),
            ("white_bishop", "whiteBishop.png"), ("white_rook", "whiteRook.png"), ("white_pawn", "whitePawn.png"),
            ("black_king", "blackKing.png"), ("black_queen", "blackQueen.png"), ("black_knight", "blackKnight.png"),
            ("black_bishop", "blackBishop.png"), ("black_rook", "blackRook.png"), ("black_pawn", "blackPawn.png")
        ]
        for name, filename in pieces:
            img = pygame.image.load(f'assets/{filename}')
            img = pygame.transform.scale(img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
            self.piece_images[name] = img

    def draw_board(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = self.WHITE if (row + col) % 2 == 0 else "brown"
                pygame.draw.rect(self.screen, color, (col*self.SQUARE_SIZE, row*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    img_name = "white_" if piece < 7 else "black_"
                    piece_name = {1: "king", 2: "queen", 3: "rook", 4: "bishop", 5: "knight", 0: "pawn"}[piece % 6]
                    img_name += piece_name
                    img = self.piece_images[img_name]
                    self.screen.blit(img, (col*self.SQUARE_SIZE, row*self.SQUARE_SIZE))

    def get_square(self, mouse_pos):
        col = mouse_pos[0] // self.SQUARE_SIZE
        row = mouse_pos[1] // self.SQUARE_SIZE
        return row, col

    def get_sidebar_piece(self, mouse_pos):
        if mouse_pos[0] >= self.BOARD_WIDTH:
            row = (mouse_pos[1] - (self.HEIGHT - self.BOARD_WIDTH)) // self.SQUARE_SIZE
            return row + 1
        return None

    def draw_button(self):
        pygame.draw.rect(self.screen, self.WHITE, (self.BOARD_WIDTH, self.HEIGHT - 100, 120, 40))
        font = pygame.font.Font(None, 32)
        text = font.render("Analyse", True, self.BLACK)
        self.screen.blit(text, (self.BOARD_WIDTH + 20, self.HEIGHT - 90))


    def output_fen_position(self):
        fen_position = self.board_to_fen(self.board)
        chess_game = analysisChess.ChessGame(fen=fen_position)
        chess_game.run_game()

    def board_to_fen(self, board):
        fen_parts = []
        for row in range(self.ROWS):
            fen_row = ''
            empty_counter = 0
            for col in range(self.COLS):
                piece = board[row][col]
                if piece == 0:
                    empty_counter += 1
                else:
                    if empty_counter > 0:
                        fen_row += str(empty_counter)
                        empty_counter = 0
                    fen_row += self.get_piece_from_code(piece).symbol()
            if empty_counter > 0:
                fen_row += str(empty_counter)
            fen_parts.append(fen_row)
        
        if self.current_player == chess.WHITE:
            fen_position = '/'.join(fen_parts) + ' w - - 1 0 '  # white to move
        else:
            fen_position = '/'.join(fen_parts) + ' b - - 1 0 ' # black to move
        return fen_position

    def get_piece_from_code(self, code):
        # Map piece code to chess piece
        piece_map = {
            1: 'K', 2: 'Q', 3: 'R', 4: 'B', 5: 'N', 6: 'P',
            7: 'k', 8: 'q', 9: 'r', 10: 'b', 11: 'n', 12: 'p'
        }
        return chess.Piece.from_symbol(piece_map[code])

    def toggle_player(self):
        if self.current_player == chess.WHITE:
            self.current_player = chess.BLACK
        else:
            self.current_player = chess.WHITE



    def run(self):
        selected_piece = None
        running = True
        while running:
            self.screen.fill("grey")
            self.draw_board()
            self.draw_pieces()

            # Draw sidebar
            sidebar_rects = []
            for i, img in enumerate([self.piece_images[f"white_{piece}"] for piece in ["king", "queen", "rook", "bishop", "knight", "pawn"]]):
                rect = self.screen.blit(img, (self.BOARD_WIDTH, i * self.SQUARE_SIZE + (self.HEIGHT - self.BOARD_WIDTH)))
                sidebar_rects.append(rect)

            for i, img in enumerate([self.piece_images[f"black_{piece}"] for piece in ["king", "queen", "rook", "bishop", "knight", "pawn"]]):
                rect = self.screen.blit(img, (self.BOARD_WIDTH + self.SQUARE_SIZE, i * self.SQUARE_SIZE + (self.HEIGHT - self.BOARD_WIDTH)))
                sidebar_rects.append(rect)

            # Draw toggle button
            pygame.draw.rect(self.screen, self.WHITE, (self.BOARD_WIDTH, self.HEIGHT - 150, 120, 40))
            font = pygame.font.Font(None, 32)
            text = font.render("Toggle", True, self.BLACK)
            self.screen.blit(text, (self.BOARD_WIDTH + 20, self.HEIGHT - 140))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if selected_piece is None:
                        # Check if a piece from the sidebar is selected
                        for i, rect in enumerate(sidebar_rects):
                            if rect.collidepoint(mouse_pos):
                                selected_piece = i + 1  # Map piece index to piece type
                    else:
                        # Place the selected piece on the board
                        row, col = self.get_square(mouse_pos)
                        if 0 <= row < self.ROWS and 0 <= col < self.COLS and self.board[row][col] == 0:
                            self.board[row][col] = selected_piece
                        selected_piece = None
                    # Check if the button is clicked
                    if self.BOARD_WIDTH + 20 <= mouse_pos[0] <= self.BOARD_WIDTH + 140 and self.HEIGHT - 100 <= mouse_pos[1] <= self.HEIGHT - 60:
                        self.output_fen_position()
                    if self.BOARD_WIDTH <= mouse_pos[0] <= self.BOARD_WIDTH + 120 and self.HEIGHT - 150 <= mouse_pos[1] <= self.HEIGHT - 110:
                        self.toggle_player()
                    
            self.draw_button()
            pygame.display.flip()

        pygame.quit()
        sys.exit()



