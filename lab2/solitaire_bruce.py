class Solitaire:
    def __init__(self, seed: list):
        self.cards = seed.copy()
        # 53 - white joker
        # 54 - black joker

    def set_seed(self, seed):
        self.cards = seed.copy()

    def change_the_white_black_joker_position(self):

        white_joker_index = self.cards.index(53)

        if white_joker_index == 53:
            self.cards.pop(white_joker_index)
            self.cards.insert(1, 53)
        else:
            self.cards.pop(white_joker_index)
            self.cards.insert(white_joker_index + 1, 53)

    def change_the_black_joker_position(self):

        black_joker_index = self.cards.index(54)

        if black_joker_index == 53:
            self.cards.pop(black_joker_index)
            self.cards.insert(2, 54)
        else:
            if black_joker_index == 52:
                self.cards.pop(black_joker_index)
                self.cards.insert(1, 54)
            else:
                self.cards.pop(black_joker_index)
                self.cards.insert(black_joker_index + 2, 54)

    def swap_parts(self):

        white_joker_index: int = self.cards.index(53)
        black_joker_index: int = self.cards.index(54)

        if white_joker_index < black_joker_index:
            self.cards = self.cards[black_joker_index + 1:] \
                         + self.cards[white_joker_index:black_joker_index + 1] \
                         + self.cards[:white_joker_index]
        else:
            self.cards = self.cards[white_joker_index + 1:] \
                         + self.cards[black_joker_index:white_joker_index + 1] \
                         + self.cards[:black_joker_index]

    def check_last_card(self):
        last_card = self.cards[-1]

        if last_card == 53 or last_card == 54:
            shuffled_deck = self.cards
        else:
            first_part = self.cards[:last_card]
            remaining_part = self.cards[last_card:-1]
            shuffled_deck = remaining_part + first_part + [last_card]

        self.cards = shuffled_deck

    def solitaire(self):

        self.change_the_white_black_joker_position()
        self.change_the_black_joker_position()
        self.swap_parts()
        self.check_last_card()

        return self.cards

    def get_key(self):
        self.solitaire()
        first_card = self.cards[0]
        while first_card == 53 or first_card == 54:
            self.solitaire()
            first_card = self.cards[0]
        key = self.cards[first_card]

        return key - 1

    def get_keystream(self, length):
        keystream = ''
        for _ in range(length):
            bytearray = bin(self.get_key() % 4)[2:].zfill(2) + bin(self.get_key() % 4)[2:].zfill(2) + \
                        bin(self.get_key() % 4)[2:].zfill(2) + bin(self.get_key() % 4)[2:].zfill(2)
            decimal_value = int(bytearray, 2)
            keystream += chr(decimal_value)
        return str(keystream)
