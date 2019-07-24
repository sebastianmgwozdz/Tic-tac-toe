import pygame, os
import numpy as np

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
            self.currentTurn = 2;
        else:
            self.currentTurn = 1;

    def move_legal(self, row, column):
        return self.values[row, column] is None

    def get_winner(self):
        if self.column_winner() is not None:
            return self.column_winner()
        elif self.row_winner() is not None:
            return self.row_winner()
        elif self.diagonal_winner() is not None:
            return self.diagonal_winner()
        return None

    def check_column(self, column):
        return self.values[0, column] == self.values[1, column] and self.values[1, column] == self.values[2, column] and self.values[0, column] is not None

    def column_winner(self):
        for column in range(3):
            if self.check_column(column) and self.values[0, column]:
                return self.values[0, column]
        return None

    def check_row(self, row):
        return self.values[row, 0] == self.values[row, 1] and self.values[row, 1] == self.values[row, 2] and self.values[row, 0] is not None

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
row_coordinates = [65, 235, 420]
column_coordinates = [55, 200, 395]


# Updates all images to be displayed
def draw(markers):
    window.blit(background_image, (0, 0))
    if board.get_winner() is not None:
        display_turn_text(markers, True)
    else:
        display_turn_text(markers, False)
    if len(markers) > 0:
        for marker in markers:
            window.blit(marker.image, (marker.column_coordinate, marker.row_coordinate))

    pygame.display.update()


# Updates text to be displayed, either end of game message or current player's turn
def display_turn_text(markers, victory_status):
    if victory_status:
        string = "Congratulations Player " + str(len(markers) % 2 + 1) + "! You win!"
    else:
        string = "Player " + str(len(markers) % 2 + 1) + "'s turn"
    text = font.render(string, True, (0, 0, 0), (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (585 // 2, 25)
    window.blit(text, text_rect)


# Convert exact pixel to row or column
def coord_to_block(variable):
    if variable == "x":
        x = 0
        if 200 < pos[0] <= 395:
            x = 1;
        elif 395 < pos[0]:
            x = 2;
        return x
    else:
        y = 0
        if 235 < pos[1] <= 420:
            y = 1;
        elif 420 < pos[1]:
            y = 2;
        return y

running = True

while running:

    done = False
    markers = []
    board = Board()
    player1 = Player(1)
    player2 = Player(2)

    while not done:
        draw(markers)
        if board.get_winner() is not None:
            done = True
            pygame.time.delay(3000)


        pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

        if pos is not None and done is False:
            x = coord_to_block("x")
            y = coord_to_block("y")

            marker = None
            if board.currentTurn == 1:
                marker = Marker(player1, x, y)
            else:
                marker = Marker(player2, x, y)

            if board.move_legal(y, x):
                board.insert_marker(marker)
            else:
                continue

pygame.quit()
