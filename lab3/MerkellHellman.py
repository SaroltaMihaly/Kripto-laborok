import math
import random
from typing import Tuple

from . import utils

PrivateKey = Tuple[Tuple[int], int, int]
PublicKey = Tuple[int]

def generate_private_key(n: int = 8) -> PrivateKey:
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    assert n > 0, 'n must be a positive integer!'

    def next_superincreasing_number(total: int) -> int:
        return total + random.randint(total + 1, 2 * total)

    def superincreasing_sequence(count: int) -> Tuple[int]:
        starting_value = random.randint(2, 10)
        super_seq = [starting_value]
        sum_super_seq = starting_value
        for _ in range(count - 1):
            next_super = next_superincreasing_number(sum_super_seq)
            super_seq.append(next_super)
            sum_super_seq += next_super
        return tuple(super_seq)

    # 1.
    w = superincreasing_sequence(n)
    assert utils.is_superincreasing(w), 'The sequence is not superincreasing!'
    # 2.
    q = next_superincreasing_number(sum(w))
    # 3.
    r = random.randint(2, q - 1)
    while not math.gcd(r, q) == 1:
        r = random.randint(2, q - 1)
    return w, q, r


def create_public_key(private_key: PrivateKey) -> PublicKey:
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    w, q, r = private_key
    return tuple([r * w_i % q for w_i in w])


def encrypt_mh(message: str, public_key: PublicKey) -> list[int]:
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    # 1.
    chunks = list(message)  # Since the message size is 8 bytes, we just convert it to a list
    assert len(public_key) == 8, 'The public key must be 8 bytes long!'
    # 2.
    byte_list = [utils.byte_to_bits(ord(chunk)) for chunk in chunks]
    # 3.
    encrypted = []
    for byte in byte_list:
        encrypted.append(sum([a_i * b_i for a_i, b_i in zip(byte, public_key)]))
    # 4.
    return encrypted


def decrypt_mh(message: list[int], private_key: PrivateKey) -> str:
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    # 1.
    w, q, r = private_key
    # 2.
    s = utils.modinv(r, q)

    def decrypt_byte(byte: int) -> int:
        # 3. Calculate c' for each byte
        c_prime = byte * s % q
        # 4.
        decrypted_bits = []
        for w_k in reversed(w):
            if w_k > c_prime:
                decrypted_bits.append(0)
            else:
                decrypted_bits.append(1)
                c_prime -= w_k
        # Reverse list since we added the bits from the end
        return utils.bits_to_byte(decrypted_bits[::-1])

    decrypted_bytes = [decrypt_byte(byte) for byte in message]
    # 5.
    return ''.join([chr(byte) for byte in decrypted_bytes])
