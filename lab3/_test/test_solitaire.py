# from ...lab2.stream_cipher import StreamCipher
from lab2.stream_cipher import StreamCipher


def test_create_stream_cipher():
    """
    Test creating a stream cipher: A stream cipher is created, and the
    returned value is a StreamCipher object.
    """
    stream_cipher = StreamCipher(config_dict={
        "random_generator": "solitaire",
        "seed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
    })
    assert isinstance(stream_cipher, StreamCipher)


def test_wrong_random_generator():
    """
    Test creating a stream cipher with a wrong random generator: A stream
    cipher is created, and the returned value is a StreamCipher object.
    """
    try:
        StreamCipher(config_dict={
            "random_generator": "wrong",
            "seed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                     29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
        })
    except ValueError:
        pass
    else:
        assert False


def test_encrypt():
    """
    Test encrypting a message: A message is encrypted, and the returned
    value is a string of the correct form.
    """
    stream_cipher = StreamCipher(config_dict={
        "random_generator": "solitaire",
        "seed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
    })
    encrypted = stream_cipher.encrypt('Hello, world!')
    assert isinstance(encrypted, str)
    assert encrypted == '\x8d\x9aV<\x10¯¥&ùqþ»\x05'


def test_decrypt():
    """
    Test decrypting a message: A message is decrypted, and the returned
    value is a string of the correct form.
    """
    stream_cipher = StreamCipher(config_dict={
        "random_generator": "solitaire",
        "seed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
    })
    decrypted = stream_cipher.decrypt('\x8d\x9aV<\x10¯¥&ùqþ»\x05')
    assert isinstance(decrypted, str)
    assert decrypted == 'Hello, world!'
