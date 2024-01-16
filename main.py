"""
A two player simple chess game in python using Pygame. 
Features:
    -> tells whose turn is it
    -> highlights the valid moves
    -> highlights when king is in check
    -> shows deceased pieces
    -> allows the player to Forfeit the game
    -> restart the game by pressing ENTER
"""

import pygame

# initialize pygame module
pygame.init()

# defining the screen dimensions
WIDTH = HEIGHT = 600
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION   # square size
screen = pygame.display.set_mode([800, 700])
pygame.display.set_caption("Chess")

# predifined colours and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (190, 190, 190)
D_GREY = (96, 96, 96)
font = pygame.font.Font("freesansbold.ttf", 15)
big_font = pygame.font.Font("freesansbold.ttf", 30)

IMAGES_BIG = {}
IMAGES_SMALL = {}

# defining timer and fps
timer = pygame.time.Clock()
fps = 60

# defining game variables and board
WHITE_PIECES = ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
                "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
BLACK_PIECES = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", 
                "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]

black_loactions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
white_loactions = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                   (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),]

captured_pieces_white = []
captured_pieces_black = []

# check variables / flashing counter
counter = 0
winner = " "
game_over = False

# 0: white's turn (piece not selected); 1: piece selected (piece selected)
# 2: black's turn (piece not selected); 3: piece selected (piece selected)
turn_step = 0
selection = 100
valid_moves = []

# loading game images for main board
pieces = ["bP", "bR", "bN", "bB", "bQ", "bK", "wP", "wR", "wN", "wB", "wQ", "wK"]
for piece in pieces:
      IMAGES_BIG[piece] = pygame.transform.scale( pygame.image.load("Chess/images/" + piece + ".png"), (70, 70))
      IMAGES_SMALL[piece] = pygame.transform.scale(pygame.image.load("Chess/images/" + piece + ".png"), (30, 30))
      

"""draw main board"""
# If the sum of row and column is even then the color is White, and if it is odd the color is Black
def drawBoard():
    for row in range(DIMENSION):
        # drawing black and white squares
        for col in range(DIMENSION):
            if (((row+col) % 2) == 0):
                pygame.draw.rect(screen, WHITE, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                pygame.draw.rect(screen, GREY, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # drawing lines to seperate squares
        for i in range(9):
            pygame.draw.line(screen, BLACK, (0, SQ_SIZE*i), (WIDTH, SQ_SIZE*i), 2)  # horisontal lines
            pygame.draw.line(screen, BLACK, (SQ_SIZE*i, 0), (SQ_SIZE*i, HEIGHT), 2) # vertical lines

        # drawing the area of decesed pieces and instructions
        pygame.draw.rect(screen, D_GREY, [0, WIDTH, 800, 100], 5)
        pygame.draw.rect(screen, D_GREY, [HEIGHT, 0, 200, 800], 5)
        status_text = ["White: Select a piece to move", "White: Select a destination",
                       "Black: Select a piece to move", "Black: Select a destination"]
        screen.blit(big_font.render(status_text[turn_step], True, "black"), (20, 630))

        # adding forfiet buttion
        screen.blit(big_font.render("FORFEIT", True, BLACK), (640, 640))

# draw pieces on the main board
def drawPieces():
    # white   
    for i in range(len(WHITE_PIECES)):
        if WHITE_PIECES[i] == "wP":
            screen.blit(IMAGES_BIG["wP"], (white_loactions[i][0] * SQ_SIZE, white_loactions[i][1] * SQ_SIZE + 3))
        else:
            screen.blit(IMAGES_BIG[WHITE_PIECES[i]], (white_loactions[i][0] * SQ_SIZE, white_loactions[i][1] * SQ_SIZE + 3))

    # black
    for i in range(len(BLACK_PIECES)):
        if BLACK_PIECES[i] == "bP":
            screen.blit(IMAGES_BIG["bP"], (black_loactions[i][0] * SQ_SIZE, black_loactions[i][1] * SQ_SIZE + 3))
        else:
            screen.blit(IMAGES_BIG[BLACK_PIECES[i]], (black_loactions[i][0] * SQ_SIZE, black_loactions[i][1] * SQ_SIZE + 3)) 
        
            
        # highlight selected piece
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, BLUE, [white_loactions[i][0] * SQ_SIZE +1, white_loactions[i][1] * SQ_SIZE +1, SQ_SIZE, SQ_SIZE], 2)

        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, BLUE, [black_loactions[i][0] * SQ_SIZE +1, black_loactions[i][1] * SQ_SIZE +1, SQ_SIZE, SQ_SIZE], 2)
        

"""Functions for valid moves of each piece on board"""               
# check valid moves of all pieces
def checkOptions(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == "wP" or piece == "bP":
            moves_list = checkPawn(location, turn)
        elif piece == "wR" or piece == "bR":
            moves_list = checkRook(location, turn)
        elif piece == "wN" or piece == "bN":
            moves_list = checkKnight(location, turn)
        elif piece == "wB" or piece == "bB":
            moves_list = checkBishop(location, turn)
        elif piece == "wQ" or piece == "bQ":
            moves_list = checkQueen(location, turn)
        elif piece == "wK" or piece == "bK":
            moves_list = checkKing(location, turn)
        
        all_moves_list.append(moves_list)
    return all_moves_list


# checking valid Pawn moves
def checkPawn(position, color):
    moves_list = []
    if color == "white":
        # forward 1 square move
        if (position[0], position[1]-1) not in white_loactions and \
            (position[0], position[1]-1) not in black_loactions and \
                position[1] > 0:
            moves_list.append((position[0], position[1]-1))
        
            # forward 2 squares move
            if (position[0], position[1]-2) not in white_loactions and \
                (position[0], position[1]-2) not in black_loactions and \
                    position[1] == 6:
                moves_list.append((position[0], position[1]-2))

        # diagonal attack move
        if (position[0]+1, position[1]-1) in black_loactions:
            moves_list.append((position[0]+1, position[1]-1))
        if (position[0]-1, position[1]-1) in black_loactions:
            moves_list.append((position[0]-1, position[1]-1))
    
    else:
        # forward 1 square move
        if (position[0], position[1]+1) not in white_loactions and \
            (position[0], position[1]+1) not in black_loactions and \
                position[1] < 7:
            moves_list.append((position[0], position[1]+1))
        
            # forward 2 squares move
            if (position[0], position[1]+2) not in white_loactions and \
                (position[0], position[1]+2) not in black_loactions and \
                    position[1] == 1:
                moves_list.append((position[0], position[1]+2))

        # diagonal attack move
        if (position[0]+1, position[1]+1) in white_loactions:
            moves_list.append((position[0]+1, position[1]+1))
        if (position[0]-1, position[1]+1) in white_loactions:
            moves_list.append((position[0]-1, position[1]+1))
        
    return moves_list


# checking valid Rook moves
def checkRook(position, color):
    moves_list = []
    if color == "white":
        enemies_list = black_loactions
        firends_list = white_loactions
    else:
        enemies_list = white_loactions
        firends_list = black_loactions
    
    for i in range(4):
        path = True
        chain = 1
        if i == 0:      # down
            x = 0
            y = 1
        elif i == 1:    # up
            x = 0
            y = -1
        elif i == 2:    # right
            x = 1
            y = 0
        else:           # left
            x = -1
            y = 0

        while path:
            if (position[0] + (chain*x), position[1] + (chain*y)) not in firends_list and \
                0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain*y) <= 7:
                moves_list.append((position[0]+(chain*x), position[1]+(chain*y)))
                if (position[0] + (chain*x), position[1] + (chain*y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    
    return moves_list


# checking valid Knight moves
def checkKnight(position, color):
    moves_list = []
    if color == "white":
        enemies_list = black_loactions
        firends_list = white_loactions
    else:
        enemies_list = white_loactions
        firends_list = black_loactions

    # knight moves: 2 squares in one direction and 1 square, either left ot right in another direction
    targets = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])             # index
        if target not in firends_list and 0 <= target[0] <=7 and 0 <= target[1] <=7:
            moves_list.append(target)
    
    return moves_list


# checking valid Bishop moves
def checkBishop(position, color):
    moves_list = []
    if color == "white":
        enemies_list = black_loactions
        firends_list = white_loactions
    else:
        enemies_list = white_loactions
        firends_list = black_loactions

    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1

        while path:
            if (position[0] + (chain*x), position[1] + (chain*y)) not in firends_list and \
                0 <= position[0] + (chain*x) <= 7 and 0 <= position[1] + (chain*y) <= 7:
                moves_list.append((position[0]+(chain*x), position[1]+(chain*y)))
                if (position[0] + (chain*x), position[1] + (chain*y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    
    return moves_list


# checking valid Queen moves
# follows the moves of Bhishop and Rook
def checkQueen(position, color):
    moves_list = checkBishop(position, color)
    second_list = checkRook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# checking valid King moves
def checkKing(position, color):
    moves_list = []
    if color == "white":
        enemies_list = black_loactions
        firends_list = white_loactions
    else:
        enemies_list = white_loactions
        firends_list = black_loactions

    # king can go 1 square in any direction: up, down, left, right, right-up, right-down, left-up, left-down
    targets = [(0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (1, 0)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])             # index
        if target not in firends_list and 0 <= target[0] <=7 and 0 <= target[1] <=7:
            moves_list.append(target)
    return moves_list


"""Tells about valid moves of a piece"""
# check for valid moves for selected piece
def checkValidMoves():
    if turn_step < 2:                   # white moves
        options_list = white_options
    else:                               # black moves
        options_list = black_options

    valid_options = options_list[selection] 
    return valid_options


# show valid moves on board
def drawValid(moves):
    for i in range(len(moves)):
        pygame.draw.rect(screen, GREEN, [moves[i][0] * SQ_SIZE+1, moves[i][1] * SQ_SIZE+1, SQ_SIZE-1, SQ_SIZE-1], 3)


"""Capturing the deceased piece on the side of the chess board"""
# draw deceased pieces
def drawCaptured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        screen.blit(IMAGES_SMALL[captured_piece], (625, 5+35*i))

    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        screen.blit(IMAGES_SMALL[captured_piece], (725, 5+35*i))


"""Checking winning conditions"""
# flasing king if in check
def drawCheck():
    check = False
    if turn_step < 2:       # white's turn (white king checked)
        if "wK" in WHITE_PIECES:
            king_index = WHITE_PIECES.index("wK")
            king_location = white_loactions[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, RED, (white_loactions[king_index][0] * SQ_SIZE + 1,
                                                    white_loactions[king_index][1] * SQ_SIZE + 1, SQ_SIZE, SQ_SIZE), 5)
    
    else:       # white's turn (white king checked)
        if "bK" in BLACK_PIECES:
            king_index = BLACK_PIECES.index("bK")
            king_location = black_loactions[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, RED, (black_loactions[king_index][0] * SQ_SIZE + 1,
                                                    black_loactions[king_index][1] * SQ_SIZE + 1, SQ_SIZE, SQ_SIZE), 5)


# game over
def drawGameOver():
    pygame.draw.rect(screen, BLACK, (200, 250, 200, 60))
    screen.blit(font.render(f"{winner} won the game!", True, WHITE), (210, 260))
    screen.blit(font.render(f"Press ENTER to Restart!", True, WHITE), (210, 285))

# main game loop
# checking pieces' valid moves at the start of the game
black_options = checkOptions(BLACK_PIECES, black_loactions, "black")
white_options = checkOptions(WHITE_PIECES, white_loactions, "white")

# game start
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0

    screen.fill(GREY)

    # calling methods
    drawBoard()
    drawPieces()
    drawCaptured()
    drawCheck()

    # draw valid moves for pieces
    if selection != 100:
        valid_moves = checkValidMoves()
        drawValid(valid_moves)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    

        # mouse event handling on board
        # while playing the game
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:  # checking for left click
            x_coordinates = event.pos[0] // SQ_SIZE
            y_coordinates = event.pos[1] // SQ_SIZE
            click_coordinates = (x_coordinates, y_coordinates)
            # print(click_coordinates)                                  # print clicked coordinates

            # White's turn
            if turn_step <= 1:
                if click_coordinates == (8, 8) or click_coordinates == (9, 8) or click_coordinates == (10, 8):
                    winner = "black"
                if click_coordinates in white_loactions:                    # white piece selected
                    selection = white_loactions.index(click_coordinates)    # selected piece's coords
                    if turn_step == 0:
                        turn_step = 1
                
                if click_coordinates in valid_moves and selection != 100:
                    white_loactions[selection] = click_coordinates
                    if click_coordinates in black_loactions:
                        black_piece = black_loactions.index(click_coordinates)  # index
                        # deceased piece caputred and removed from original pieces list and location
                        captured_pieces_white.append(BLACK_PIECES[black_piece])
                        if BLACK_PIECES[black_piece] == "bK":
                            winner = "white"
                        BLACK_PIECES.pop(black_piece)
                        black_loactions.pop(black_piece)

                    
                    # checking pieces' valid moves
                    black_options = checkOptions(BLACK_PIECES, black_loactions, "black")
                    white_options = checkOptions(WHITE_PIECES, white_loactions, "white")

                    # clearing valid moves everytime to recalculate it
                    turn_step = 2
                    selection = 100
                    valid_moves = []


            # Black's turn
            if turn_step > 1:
                if click_coordinates == (8, 8) or click_coordinates == (9, 8) or click_coordinates == (10, 8):
                    winner = "white"
                if click_coordinates in black_loactions:                    # black piece selected
                    selection = black_loactions.index(click_coordinates)    # selected piece's coords
                    if turn_step == 2:
                        turn_step = 3
                
                if click_coordinates in valid_moves and selection != 100:
                    black_loactions[selection] = click_coordinates
                    if click_coordinates in white_loactions:
                        white_piece = white_loactions.index(click_coordinates)  # index
                        # deceased piece caputred and removed from original pieces list and location
                        captured_pieces_white.append(BLACK_PIECES[white_piece])
                        if WHITE_PIECES[white_piece] == "wK":
                            winner = "black"
                        WHITE_PIECES.pop(white_piece)
                        white_loactions.pop(white_piece)
                    
                    # checking pieces' valid moves
                    black_options = checkOptions(BLACK_PIECES, black_loactions, "black")
                    white_options = checkOptions(WHITE_PIECES, white_loactions, "white")
                    
                    # clearing valid moves everytime to recalculate it
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        
        # when restating the game
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                # resetting game variables
                game_over = False
                winner = " "
                WHITE_PIECES = ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
                                "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
                BLACK_PIECES = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", 
                                "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"]

                black_loactions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                white_loactions = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
                                   (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),]

                captured_pieces_white = []
                captured_pieces_black = []

                turn_step = 0
                selection = 100
                valid_moves = []

                black_options = checkOptions(BLACK_PIECES, black_loactions, "black")
                white_options = checkOptions(WHITE_PIECES, white_loactions, "white")

    if winner != " ":
        game_over = True
        drawGameOver()

    pygame.display.flip()

pygame.quit()
