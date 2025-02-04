import tkinter as tk
from tkinter import messagebox
import chess
import chess.engine
import os

# Load Stockfish Engine
STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Ask user for side choice
player_color = input("Do you want to play as White or Black? (w/b): ").strip().lower()
player_is_white = player_color == 'w'

# Initialize Chess Board
board = chess.Board()

# Tkinter GUI
root = tk.Tk()
root.title("Chess Game with AI")

# Board canvas
canvas_size = 512
square_size = canvas_size // 8
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
canvas.pack()

# Load piece images
ASSETS_PATH = "assets"
piece_images = {}
for color, folder in [("w", "white"), ("b", "black")]:
    for piece in ["P", "R", "N", "B", "Q", "K"]:
        img = tk.PhotoImage(file=os.path.join(ASSETS_PATH, folder, piece + ".png"))
        piece_images[color + piece] = img

# Draw Chessboard
def draw_board():
    for row in range(8):
        for col in range(8):
            color = "#EEEED2" if (row + col) % 2 == 0 else "#769656"
            x1, y1 = col * square_size, row * square_size
            x2, y2 = x1 + square_size, y1 + square_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

# Draw Pieces
def draw_pieces():
    canvas.delete("pieces")
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_symbol = piece.symbol().upper()
            color = "w" if piece.color == chess.WHITE else "b"
            img = piece_images[color + piece_symbol]
            row, col = divmod(square, 8)
            if not player_is_white:  # Flip board for Black
                row, col = 7 - row, 7 - col
            canvas.create_image(col * square_size, row * square_size, anchor="nw", image=img, tags="pieces")

# Convert mouse click to chess square
def get_square_from_mouse(x, y):
    col = x // square_size
    row = y // square_size
    if not player_is_white:  # Flip board for Black
        row = 7 - row
        col = 7 - col
    return chess.square(col, row)

# AI Move
def ai_move():
    if not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.5))
        board.push(result.move)
        draw_pieces()
        check_game_over()

# Check if the game is over
def check_game_over():
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        messagebox.showinfo("Game Over", f"Checkmate! {winner} wins.")
        root.quit()
    elif board.is_stalemate() or board.is_insufficient_material():
        messagebox.showinfo("Game Over", "Draw!")
        root.quit()

# Handle Piece Selection and Movement
selected_square = None

def on_canvas_click(event):
    global selected_square
    clicked_square = get_square_from_mouse(event.x, event.y)
    piece = board.piece_at(clicked_square)

    if selected_square is None:
        if piece and piece.color == (chess.WHITE if player_is_white else chess.BLACK):
            selected_square = clicked_square
    else:
        move = chess.Move(selected_square, clicked_square)
        if move in board.legal_moves:
            board.push(move)
            draw_pieces()
            check_game_over()
            ai_move()
        selected_square = None

# Bind Mouse Click
canvas.bind("<Button-1>", on_canvas_click)

# Start Game
draw_board()
draw_pieces()

if board.turn == chess.BLACK and not player_is_white:
    ai_move()

root.mainloop()
engine.quit()
