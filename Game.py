import pygame, os
import numpy as np
import random

# Position game window in center of screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

window = pygame.display.set_mode((585, 585))
pygame.display.set_caption("Tic-Tac-Toe")

background_image = pygame.image.load("game_board.jpg")
xImage = pygame.image.load("x.jpg")
oImage = pygame.image.load("o.jpg")

# Set window icon
pygame.display.set_icon(xImage)


# Represents a Tic-Tac-Toe board
class Board:
    def __init__(self):
        self.currentTurn = 1
        self.values = np.array([[None, None, None],
                               [None, None, None],
                               [None, None, None]])

    def insert_marker(self, marker):
        self.values[marker.row, marker.column] = marker
        markers.append(marker)
        if self.currentTurn == 1:
            self.currentTurn = 2
        else:
            self.currentTurn = 1

    def move_wins(self, marker):
        if self.get_winner() is None and self.move_legal(marker):
            self.values[marker.row, marker.column] = marker
            wins = self.get_winner() is not None
            self.values[marker.row, marker.column] = None
            return wins
        return False

    def move_legal(self, marker):
        return self.values[marker.row, marker.column] is None

    def get_winner(self):
        if self.column_winner() is not None:
            return self.column_winner()
        elif self.row_winner() is not None:
            return self.row_winner()
        elif self.diagonal_winner() is not None:
            return self.diagonal_winner()
        return None

    def check_column(self, column):
        return self.values[0, column] == self.values[1, column] and self.values[1, column] == self.values[2, column] \
               and self.values[0, column] is not None

    def column_winner(self):
        for column in range(3):
            if self.check_column(column) and self.values[0, column]:
                return self.values[0, column]
        return None

    def check_row(self, row):
        return self.values[row, 0] == self.values[row, 1] and self.values[row, 1] == self.values[row, 2] and \
               self.values[row, 0] is not None

    def row_winner(self):
        for row in range(3):
            if self.check_row(row) and self.values[row, 0]:
                return self.values[row, 0]
        return None

    def check_diagonal(self):
        a = self.values[0, 0]
        b = self.values[1, 1]
        c = self.values[2, 2]
        d = self.values[2, 0]
        e = self.values[0, 2]
        return ((a == b and b == c) or (d == b and b == e)) and b is not None

    def diagonal_winner(self):
        if self.check_diagonal():
            return self.values[1, 1]

    def is_full(self):
        for row in self.values:
            for column in row:
                if column is None:
                    return False
        return True

    def corner_available(self):
        return self.values[0, 0] is None or self.values[0, 2] is None or self.values[2, 0] is None or \
               self.values[2, 2] is None

    def get_open_corner(self):
        if self.values[0, 0] is None:
            return 0, 0
        elif self.values[0, 2] is None:
            return 0, 2
        elif self.values[2, 0] is None:
            return 2, 0
        else:
            return 2, 2

    # Scan left to right, starting at top right, until a square is empty
    def get_random_available(self):
        available = []
        for row in range(3):
            for column in range(3):
                if self.values[row][column] is None:
                    available.append((row, column))
        rand = available[random.randint(0, len(available) - 1)]
        return rand[0], rand[1]


class Player:
    def __init__(self, turn_order):
        # First player's marker is an X, second is O
        if turn_order == 1:
            self.shape = "x"
        else:
            self.shape = "o"


class Marker:
    def __init__(self, player, column, row):
        if player.shape == "x":
            self.image = xImage
        else:
            self.image = oImage
        self.column = column
        self.row = row
        self.row_coordinate = row_coordinates[row]
        self.column_coordinate = column_coordinates[column]
        self.player = player

    # Determine if two markers are equal by comparing players
    def __eq__(self, other):
        if other is None:
            return False
        return self.player == other.player


font = pygame.font.Font('freesansbold.ttf', 32)

# Contain coordinates of top left point of each row and column
row_coordinates = [60, 235, 415]
column_coordinates = [55, 210, 395]


# Updates all images to be displayed
def draw(markers):
    window.blit(background_image, (0, 0))
    if board.get_winner() is not None:
        display_turn_text(markers, "win")
    elif not board.is_full():
        display_turn_text(markers, "ongoing")
    else:
        display_turn_text(markers, "draw")
    if len(markers) > 0:
        for marker in markers:
            window.blit(marker.image, (marker.column_coordinate, marker.row_coordinate))

    pygame.display.update()


# Updates text to be displayed, either end of game message or current player's turn
def display_turn_text(markers, victory_status):
    if victory_status == "win":
        string = "Congratulations Player " + str(len(markers) % 2 + 1) + "! You win!"
    elif victory_status == "ongoing":
        string = "There are still moves remaining"
    else:
        string = "The game has ended in a tie"
    text = font.render(string, True, (0, 0, 0), (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (585 // 2, 25)
    window.blit(text, text_rect)


# Convert exact pixel to row or column
def coord_to_block(variable):
    if variable == "x":
        x = 0
        if column_coordinates[1] < pos[0] <= column_coordinates[2]:
            x = 1
        elif column_coordinates[2] < pos[0]:
            x = 2
        return x
    else:
        y = 0
        if row_coordinates[1] < pos[1] <= row_coordinates[2]:
            y = 1
        elif row_coordinates[2] < pos[1]:
            y = 2
        return y


# Check if either player can win on this move, make the move if so
def block_or_win():
    for row in range(3):
        for column in range(3):
            move = Marker(ai, column, row)
            player_move = Marker(player, column, row)
            if board.move_wins(move):
                board.insert_marker(move)
                return
            elif board.move_wins(player_move):
                board.insert_marker(move)
                return


running = True

while running:

    round_over = False
    markers = []
    board = Board()
    player = Player(1)
    ai = Player(2)

    while not round_over:
        draw(markers)
        if board.get_winner() is not None or board.is_full():
            round_over = True
            pygame.time.delay(3000)

        pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                round_over = True
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

        # The user's turn
        if board.currentTurn == 1:
            if pos is not None and not round_over:
                x = coord_to_block("x")
                y = coord_to_block("y")

                marker = Marker(player, x, y)

                if board.move_legal(marker):
                    board.insert_marker(marker)

        # The opponent's (AI) turn
        else:
            # First check if can win or block user's win
            block_or_win()
            # Otherwise, place in random open spot
            if board.currentTurn == 2 and not board.is_full():
                open_coords = board.get_random_available()
                move = Marker(ai, open_coords[1], open_coords[0])
                board.insert_marker(move)


pygame.quit()
