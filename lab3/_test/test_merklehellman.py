from ..MerkleHellman import generate_private_key, create_public_key, encrypt_mh, decrypt_mh
import math


def test_generate_private_key():
    """
    Test generating a private key: A private key is generated, and the
    returned value is a 3-tuple of the correct form.
    """
    private_key = generate_private_key()
    assert isinstance(private_key, tuple)
    assert len(private_key) == 3
    assert isinstance(private_key[0], tuple)
    assert isinstance(private_key[1], int)
    assert isinstance(private_key[2], int)

    w, q, r = private_key
    assert len(w) == 8
    assert all(isinstance(w_i, int) for w_i in w)
    assert all(w_i > 0 for w_i in w)
    assert q > 0
    assert r > 0

    assert all(w_i < q for w_i in w)
    assert math.gcd(q, r) == 1


def test_create_public_key():
    """
    Test creating a public key: A public key is created, and the returned
    value is a tuple of the correct form.
    """
    private_key = generate_private_key()
    public_key = create_public_key(private_key)
    assert isinstance(public_key, tuple)
    assert len(public_key) == 8
    assert all(isinstance(b_i, int) for b_i in public_key)

    w, q, r = private_key
    assert all(b_i == r * w_i % q for b_i, w_i in zip(public_key, w))


def test_encrypt_mh():
    """
    Test encrypting a message: A message is encrypted, and the returned
    value is a list of the correct form.
    """
    private_key = generate_private_key()
    public_key = create_public_key(private_key)
    encrypted = encrypt_mh('Hello, world!', public_key)
    assert isinstance(encrypted, list)
    assert all(isinstance(c, int) for c in encrypted)

    assert len(encrypted) == 13


def test_decrypt_mh():
    """
    Test decrypting a message: A message is decrypted, and the returned
    value is a string of the correct form.
    """
    private_key = generate_private_key()
    public_key = create_public_key(private_key)
    encrypted = encrypt_mh('Hello, world!', public_key)
    decrypted = decrypt_mh(encrypted, private_key)
    assert isinstance(decrypted, str)
    assert decrypted == 'Hello, world!'



