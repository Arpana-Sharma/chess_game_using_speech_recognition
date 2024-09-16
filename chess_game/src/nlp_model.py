import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def parse_command(command):
    doc = nlp(command)
    piece = None
    start_pos = None
    end_pos = None
    piece_map = {
        "pawn": "P",
        "rook": "R",
        "knight": "N",
        "bishop": "B",
        "queen": "Q",
        "king": "K"
    }

    for token in doc:
        if token.text.lower() in piece_map:
            piece = piece_map[token.text.lower()]
        elif token.text.lower() in ["from", "to"]:
            continue
        elif re.match(r"^[a-h][1-8]$", token.text.lower()):
            if start_pos is None:
                start_pos = token.text.lower()
            else:
                end_pos = token.text.lower()

    return piece, start_pos, end_pos


if __name__ == "__main__":
    command = "Move pawn from e2 to e4"
    piece, start_pos, end_pos = parse_command(command)
    print(f"Piece: {piece}, Start: {start_pos}, End: {end_pos}")
