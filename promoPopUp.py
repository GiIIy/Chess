import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Function to create a popup window
def create_popup_window():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Select Tool")

    # Load images
    image1 = pygame.image.load("assets/whiteQueen.png")
    image2 = pygame.image.load("assets/whiteRook.png")
    image3 = pygame.image.load("assets/whiteBishop.png")
    image4 = pygame.image.load("assets/whiteKnight.png")

    images = [image1, image2, image3, image4]

    # Define button dimensions and positions
    button_width = 75
    button_height = 75
    button_padding = 0
    num_buttons = len(images)
    total_width = num_buttons * button_width + (num_buttons - 1) * button_padding
    start_x = (WINDOW_WIDTH - total_width) // 2
    y = (WINDOW_HEIGHT - button_height) // 2

    # Draw buttons
    for i, image in enumerate(images):
        x = start_x + (button_width + button_padding) * i
        button_rect = pygame.Rect(x, y, button_width, button_height)
        screen.blit(image, button_rect)

    pygame.display.flip()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check which button is clicked
                for i, image in enumerate(images):
                    x = start_x + (button_width + button_padding) * i
                    button_rect = pygame.Rect(x, y, button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        if i + 1 == 1:
                            return "q"
                        elif i + 1 == 2:
                            return "r"
                        elif i + 1 == 3:
                            return "b"
                        elif i + 1 == 4:
                            return "n"
