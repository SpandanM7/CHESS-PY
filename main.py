import pygame
import chess
import chess.engine
from tkinter import Tk, simpledialog

# Initialize Pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

# Load images
piece_images = {}
pieces = ['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']
for piece in pieces:
    piece_images[piece] = pygame.transform.scale(
        pygame.image.load(f"assets/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))

# Initialize board and engine
board = chess.Board()
try:
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
except:
    engine = None  # Fallback for no engine

def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(piece_images[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Ask user for color
root = Tk()
root.withdraw()
user_color = simpledialog.askstring("Choose Color", "Do you want to play as White or Black? (W/B)")
player_is_white = user_color.lower() == 'w'
root.destroy()

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess AI")
clock = pygame.time.Clock()
running = True

# Game loop
while running:
    screen.fill((0, 0, 0))
    draw_board(screen)
    pygame.display.flip()
    
    if (board.turn and player_is_white) or (not board.turn and not player_is_white):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass  # Handle player move here
    else:
        if engine:
            result = engine.play(board, chess.engine.Limit(time=0.5))
            board.push(result.move)
        else:
            pass  # Simple AI logic fallback
    
    if board.is_game_over():
        running = False
    
    clock.tick(30)

pygame.quit()
if engine:
    engine.quit()
