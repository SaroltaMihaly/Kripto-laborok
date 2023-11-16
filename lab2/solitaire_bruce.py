from random import shuffle

def init_solitaire_cards():
    cards = list(range(1,55))
    shuffle(cards)
    print(cards)
    return cards
    # 53 - white joker
    # 54 - black joker

def change_the_white_black_joker_position(cards):

    white_joker_index = cards.index(53)

    if white_joker_index == 53:
        cards.pop(white_joker_index)
        cards.insert(1, 53)
    else:
        cards.pop(white_joker_index)
        cards.insert(white_joker_index + 1, 53)
    print(cards)
    return cards

def change_the_black_joker_position(cards):
    
    black_joker_index = cards.index(54)

    if black_joker_index == 53:
        cards.pop(black_joker_index)
        cards.insert(2, 54)
    else:
        if black_joker_index == 52:
            cards.pop(black_joker_index)
            cards.insert(1, 54)
        else:
            cards.pop(black_joker_index)
            cards.insert(black_joker_index + 2, 54)
    print(cards)
    return cards

def swap_parts(cards):

    white_joker_index = cards.index(53)
    black_joker_index = cards.index(54)

    if white_joker_index < black_joker_index:
        cards = cards[black_joker_index + 1:] + cards[white_joker_index:black_joker_index + 1] + cards[:white_joker_index]
    else:
        cards = cards[white_joker_index + 1:] + cards[black_joker_index:white_joker_index + 1] + cards[:black_joker_index]

    print(cards)
    return cards

def check_last_card(cards):

    last_card = cards[-1]
    print(last_card)

    if last_card == 53 or last_card == 54:
        return cards
    else:
        first_part = cards[:last_card]
        remaining_part = cards[last_card:-1]
        shuffled_deck = remaining_part + first_part + [last_card]
        print(shuffled_deck)

    return shuffled_deck

def solitaire(cards):
        cards = change_the_white_black_joker_position(cards)
        cards = change_the_black_joker_position(cards)
        cards = swap_parts(cards)
        cards = check_last_card(cards)
    
        return cards

def get_key(cards):
    
    first_card = cards[0]

    while first_card == 53 or first_card == 54:
        cards = solitaire(cards)
        first_card = cards[0]

    key = cards[first_card]
    print(key)


if __name__ == '__main__':

    cards = init_solitaire_cards()
    cards = change_the_white_black_joker_position(cards)
    cards = change_the_black_joker_position(cards)
    cards = swap_parts(cards)
    cards = check_last_card(cards)