import pygame
import chess
import speech_recognition as sr
import pyttsx3
from nlp_model import parse_command

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Load piece images
piece_images = {
    'P': pygame.image.load('assets/pieces/white_pawn.png'),
    'p': pygame.image.load('assets/pieces/black_pawn.png'),
    'R': pygame.image.load('assets/pieces/white_rook.png'),
    'r': pygame.image.load('assets/pieces/black_rook.png'),
    'N': pygame.image.load('assets/pieces/white_knight.png'),
    'n': pygame.image.load('assets/pieces/black_knight.png'),
    'B': pygame.image.load('assets/pieces/white_bishop.png'),
    'b': pygame.image.load('assets/pieces/black_bishop.png'),
    'Q': pygame.image.load('assets/pieces/white_queen.png'),
    'q': pygame.image.load('assets/pieces/black_queen.png'),
    'K': pygame.image.load('assets/pieces/white_king.png'),
    'k': pygame.image.load('assets/pieces/black_king.png')
}


def draw_board(screen, board):
    white = (255, 255, 255)
    black = (0, 0, 0)
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(row * 8 + col)
            if piece:
                piece_image = piece_images.get(piece.symbol())
                if piece_image:
                    screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    pygame.display.flip()


def recognize_speech(recognizer, microphone):
    with microphone as source:
        print("Listening for your move...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print(audio)
    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


# Initialize the recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Sample board state
board = chess.Board()

# Player turn
player_turn = "white"

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(screen, board)

    # Recognize speech and convert to move
    command = recognize_speech(recognizer, microphone)
    if command:
        piece, start_pos, end_pos = parse_command(command)
        if start_pos and end_pos:
            move = chess.Move.from_uci(start_pos + end_pos)
            if move in board.legal_moves:
                if (board.turn and player_turn == "white") or (not board.turn and player_turn == "black"):
                    board.push(move)
                    engine.say(f"{player_turn} moved {piece} from {start_pos} to {end_pos}")
                    engine.runAndWait()
                    player_turn = "black" if player_turn == "white" else "white"
                else:
                    engine.say("It's not your turn")
                    engine.runAndWait()
            else:
                engine.say("Invalid move")
                engine.runAndWait()
        else:
            engine.say("Could not parse the move")
            engine.runAndWait()

pygame.quit()
