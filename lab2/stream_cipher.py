import json
import random

from lab2.blum_blum_shub import BlumBlumShub
from lab2.solitaire_bruce import Solitaire


def is_prime(n, k=10):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True
def generate_prime():
    while True:
        p = random.randint(2 ** 10, 2 ** 16)
        if p % 4 == 3 and is_prime(p):
            return p

class StreamCipher:
    def __init__(self, config: str):
        with open(config, 'r') as f:
            self.config = json.load(f)
        self.seed = self.config['seed']
        random_gen = self.config['random_generator']
        if random_gen == 'solitaire':
            self.random_generator = Solitaire(self.seed)
        elif random_gen == 'blum_blum_shub':
            self.random_generator = BlumBlumShub(self.seed)
        else:
            raise ValueError('Invalid random generator')

    def encrypt(self, plaintext: str):
        ciphertext = ''
        self.random_generator.set_seed(self.seed)
        keystream = self.random_generator.get_keystream(len(plaintext))
        for i in range(len(plaintext)):
            ciphertext += chr(ord(plaintext[i]) ^ ord(keystream[i]))
        return ciphertext

    def decrypt(self, ciphertext: str):
        plaintext = ''
        self.random_generator.set_seed(self.seed)
        keystream = self.random_generator.get_keystream(len(ciphertext))
        for i in range(len(ciphertext)):
            plaintext += chr(ord(ciphertext[i]) ^ ord(keystream[i]))
        return plaintext

    def get_key(self, length: int):
        self.random_generator.set_seed(self.seed)
        return self.random_generator.get_keystream(length)


# def _generate_key(length, type):
#
#     if type == "binary":
#         return ''.join(random.choice('01') for _ in range(length))
#     elif type == "decimal":
#         return ''.join(random.choice('0123456789') for _ in range(length))
#     elif type == "alpabet":
#         return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))
#
#
# def _stream_cipher_encrypt(plaintext, key, type):
#
#     encrypted_text = ""
#
#     if type == "binary":
#         for i in range(len(plaintext)):
#             encrypted_text += chr((int(plaintext[i]) + int(key[i])) % 2 + ord('0'))
#         return encrypted_text
#
#     elif type == "decimal":
#         for i in range(len(plaintext)):
#             encrypted_text += chr((int(plaintext[i]) + int(key[i])) % 10 + ord('0'))
#         return encrypted_text
#
#     elif type == "alpabet":
#         for i in range(len(plaintext)):
#             encrypted_text += chr((ord(plaintext[i]) + ord(key[i]) - ord('a')) % 26 + ord('a'))
#         return encrypted_text
#
#
# def _stream_cipher_decrypt(ciphertext, key, type):
#
#     decrypted_text = ""
#
#     if type == "binary":
#         for i in range(len(ciphertext)):
#             decrypted_text += chr((int(ciphertext[i]) - int(key[i])) % 2 + ord('0'))
#         return decrypted_text
#
#     elif type == "decimal":
#         for i in range(len(ciphertext)):
#             decrypted_text += chr((int(ciphertext[i]) - int(key[i])) % 10 + ord('0'))
#         return decrypted_text
#
#     elif type == "alpabet":
#         for i in range(len(ciphertext)):
#             decrypted_text += chr((ord(ciphertext[i]) - ord(key[i]) - ord('a')) % 26 + ord('a'))
#         return decrypted_text


if __name__ == '__main__':
    plaintext = "Hello world!"

    print("Solitaire")
    stream_cipher = StreamCipher("config.json")
    print("Plaintext: {}", plaintext)
    encrypted = stream_cipher.encrypt(plaintext)
    print("Encrypted text: {}", encrypted)
    decrypted = stream_cipher.decrypt(encrypted)
    print("Decrypted text: {}", decrypted)

    # p = generate_prime()
    # q = generate_prime()
    # n = p * q
    # s = random.randint(1, n - 1)
    # print(p)
    # print(q)
    # print(n)
    print("\nBlum Blum Shub")
    stream_cipher_blum = StreamCipher("config_blum.json")
    print("Plaintext: {}", plaintext)
    encrypted = stream_cipher_blum.encrypt(plaintext)
    print("Encrypted text: {}", encrypted)
    decrypted = stream_cipher_blum.decrypt(encrypted)
    print("Decrypted text: {}", decrypted)
