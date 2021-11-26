"""
Solitaire clone: From python arcade wiki https://api.arcade.academy/en/latest/tutorials/card_game/index.html adapted for our use
"""
from typing import Optional

import random
import arcade
from collections import deque

new_reachable_talon = deque([])
new_unreachable_talon = deque([])
new_foundation = deque([deque([]),deque([]),deque([]),deque([])])
new_tableau = deque([[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])]])

lookup_dict = {
    'H': 'Hearts',
    'D': 'Diamonds',
    'C': 'Clubs',
    'S': 'Spades',
    1: 'A',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'J',
    12: 'Q',
    13: 'K'
}

def load_stacks(reachable_talon, unreachable_talon, foundation, tableau):
    new_reachable_talon = deque([])
    new_unreachable_talon = deque([])
    new_foundation = deque([deque([]),deque([]),deque([]),deque([])])
    new_tableau = deque([[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])]])
    for x in reachable_talon:
        new_reachable_talon.append([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
    for x in unreachable_talon:
        new_unreachable_talon.append([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
    for y in range(4):
        for x in foundation[y]:
            new_foundation[y].append([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
            print(new_foundation[y])
    for y in range(7):
        for z in range(2):
            for x in tableau[y][z]:
                new_tableau[y][z].appendleft([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
    return new_reachable_talon, new_unreachable_talon, new_foundation, new_tableau
def initGame(reachable_talon, unreachable_talon, foundation, tableau):
    for x in reachable_talon:
        new_reachable_talon.append([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
    for x in unreachable_talon:
        new_unreachable_talon.append([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
    for y in range(4):
        for x in foundation[y]:
            new_foundation[y].append([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
            print(new_foundation[y])
    for y in range(7):
        for z in range(2):
            for x in tableau[y][z]:
                new_tableau[y][z].appendleft([lookup_dict.get(x[0]),lookup_dict.get(x[1])])
    main()

def update(reachable_talon, unreachable_talon, foundation, tableau):
    new_reachable_talon = deque([])
    new_unreachable_talon = deque([])
    new_foundation = deque([deque([]),deque([]),deque([]),deque([])])
    new_tableau = deque([[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])],[deque([]), deque([])]])
    new_reachable_talon, new_unreachable_talon, new_foundation, new_tableau = load_stacks(reachable_talon,unreachable_talon,foundation,tableau)
    main()

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Searching Solitaire in Real Time"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# If we fan out cards stacked on each other, how far apart to fan them?
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

# Face down image
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

# Constants that represent "what pile is what" for the game
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12
K_PLUS_TALON = 14


class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        """ Turn card face-down """
        #self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.texture = arcade.load_texture(self.image_file_name)
        self.color = [120,120,120]
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list: Optional[arcade.SpriteList] = None

        arcade.set_background_color(arcade.color.AMAZON)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        # Create a list of lists, each holds a pile of cards.
        self.piles = None

    def setup1(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for the bottom face down and face up piles
        pile = arcade.SpriteSolidColor(1000, MAT_HEIGHT, arcade.csscolor.DARK_GREEN)
        pile.position = 512, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create the seven middle piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create the top "play" piles
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards
    def setup2(self):
        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]

        #draw tableau
        for x in range(7):
            #unreachable cards
            card_no = 0
            for y in new_tableau[x][1]:
                card = Card(y[0], y[1], CARD_SCALE)
                card.position = START_X + x*X_SPACING, MIDDLE_Y - CARD_VERTICAL_OFFSET * card_no
                self.card_list.append(card)
                self.piles[x+2].append(card)
                self.pull_to_top(card)
                self.piles[x+2][-1].face_down()
                card_no += 1
            for y in new_tableau[x][0]:
                card = Card(y[0], y[1], CARD_SCALE)
                card.position = START_X + x*X_SPACING, MIDDLE_Y - CARD_VERTICAL_OFFSET * card_no
                self.card_list.append(card)
                self.piles[x+2].append(card)
                self.pull_to_top(card)
                self.piles[x+2][-1].face_up()
                card_no += 1
            #reachable cards
        card_no = 0
        for y in new_reachable_talon:
            card = Card(y[0], y[1], CARD_SCALE)
            card.position = START_X + card_no*X_SPACING*1/4, BOTTOM_Y
            self.card_list.append(card)
            self.piles[x+2].append(card)
            self.pull_to_top(card)
            self.piles[x+2][-1].face_up()
            card_no += 1

        card_no +=3
        for y in new_unreachable_talon:
            card = Card(y[0], y[1], CARD_SCALE)
            card.position = START_X + card_no*X_SPACING*1/4, BOTTOM_Y
            self.card_list.append(card)
            self.piles[x+2].append(card)
            self.pull_to_top(card)
            self.piles[x+2][-1].face_down()
            card_no += 1

        for x in range(4):
            if new_foundation[x]:
                card = Card(new_foundation[x][0][0], new_foundation[x][0][1], CARD_SCALE)
                card.position = START_X + x*X_SPACING, TOP_Y
                self.card_list.append(card)
                self.piles[x+2].append(card)
                self.pull_to_top(card)
                self.piles[x+2][-1].face_up()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        arcade.start_render()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()
    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)


def main():
    """ Main function """
    window = MyGame()
    window.setup1()
    window.setup2()
    arcade.run()


if __name__ == "__main__":
    main()