from random import shuffle

def init_solitaire_cards():
    cards = list(range(1,55))
    shuffle(cards)
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
    return key

def encrypt(message, keystream):
    message = message.replace(" ", "").upper()
    message_groups = [message[i:i+5].ljust(5, 'X') for i in range(0, len(message), 5)]

    keystream_numbers = [ord(char) - ord('A') + 1 for char in keystream]
    
    encrypted_message = ""
    for group, key in zip(message_groups, keystream_numbers):
        group_numbers = [ord(char) - ord('A') + 1 for char in group]
        encrypted_numbers = [(m + k - 1) % 26 + 1 for m, k in zip(group_numbers, keystream_numbers)]
        encrypted_chars = [chr(num + ord('A') - 1) for num in encrypted_numbers]
        encrypted_message += "".join(encrypted_chars)

    return encrypted_message

def decrypt(ciphertext, keystream):

    ciphertext_numbers = [ord(char) - ord('A') + 1 for char in ciphertext]
    keystream_numbers = [ord(char) - ord('A') + 1 for char in keystream]
    decrypted_numbers = [(c - k + 26) % 26 for c, k in zip(ciphertext_numbers, keystream_numbers)]
    decrypted_message = "".join(chr(num + ord('A') - 1) for num in decrypted_numbers)

    return decrypted_message

if __name__ == '__main__':

    cards = init_solitaire_cards()

    cards = solitaire(cards)

    keystream = ''.join([chr(get_key(cards) + ord('A') - 1) for _ in range(10)])

    plaintext = "DO NOT USE PC"

    ciphertext = encrypt(plaintext, keystream)

    print("Plaintext:", plaintext)
    print("Ciphertext:", ciphertext)

    decrypted_message = decrypt(ciphertext, keystream)

    print("Decrypted message:", decrypted_message)
