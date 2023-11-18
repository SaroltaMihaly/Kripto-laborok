import random


class BlumBlumShub:

    def __init__(self, seed):
        self.seed = seed.copy()
        self.p = self.seed[0]
        self.q = self.seed[1]
        self.s = self.seed[2]

    def set_seed(self, seed):
        self.seed = seed.copy()
        self.p = self.seed[0]
        self.q = self.seed[1]
        self.s = self.seed[2]

    def blum_blum_shub(self, seed_length):
        n = self.p * self.q
        x = pow(self.s, 2, n)

        random_bits = []

        for _ in range(seed_length):
            x = pow(x, 2, n)
            random_bits.append(x % 2)

        return ''.join(map(str, random_bits))

    def get_keystream(self, length):
        byte_array = self.blum_blum_shub(length * 8)
        bytes_list = [byte_array[i:i + 8] for i in range(0, len(byte_array), 8)]
        char_list = [chr(int(byte, 2)) for byte in bytes_list]
        return ''.join(char_list)
