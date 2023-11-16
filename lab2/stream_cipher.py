import random

def generate_key(length):
    key = ''
    for i in range(length):
        key += chr(random.randint(0, 255))
    return key


def stream_cipher_encrypt(plaintext, key):

    ciphertext = ''
    for i in range(len(plaintext)):
        ciphertext += chr(ord(plaintext[i]) ^ ord(key[i]))
    
    return ciphertext


def stream_cipher_decrypt(ciphertext, key):
    
    plaintext = ''
    for i in range(len(ciphertext)):
        plaintext += chr(ord(ciphertext[i]) ^ ord(key[i]))
    
    return plaintext


def _generate_key(length, type):

    if type == "binary":
        return ''.join(random.choice('01') for _ in range(length))
    elif type == "decimal":
        return ''.join(random.choice('0123456789') for _ in range(length))
    elif type == "alpabet":
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))


def _stream_cipher_encrypt(plaintext, key, type):

    encrypted_text = ""

    if type == "binary":
        for i in range(len(plaintext)):
            encrypted_text += chr((int(plaintext[i]) + int(key[i])) % 2 + ord('0'))
        return encrypted_text
    
    elif type == "decimal":
        for i in range(len(plaintext)):
            encrypted_text += chr((int(plaintext[i]) + int(key[i])) % 10 + ord('0'))
        return encrypted_text
    
    elif type == "alpabet":
        for i in range(len(plaintext)):
            encrypted_text += chr((ord(plaintext[i]) + ord(key[i]) - ord('a')) % 26 + ord('a'))
        return encrypted_text

    
def _stream_cipher_decrypt(ciphertext, key, type):

    decrypted_text = ""

    if type == "binary":
        for i in range(len(ciphertext)):
            decrypted_text += chr((int(ciphertext[i]) - int(key[i])) % 2 + ord('0'))
        return decrypted_text
    
    elif type == "decimal":
        for i in range(len(ciphertext)):
            decrypted_text += chr((int(ciphertext[i]) - int(key[i])) % 10 + ord('0'))
        return decrypted_text

    elif type == "alpabet":
        for i in range(len(ciphertext)):
            decrypted_text += chr((ord(ciphertext[i]) - ord(key[i]) - ord('a')) % 26 + ord('a'))
        return decrypted_text


if __name__ == '__main__':
    
    # plaintext = input('Enter plaintext: ')
    # key = generate_key(len(plaintext))
    # print('Key: {}'.format(key))
    # ciphertext = stream_cipher_encrypt(plaintext, key)
    # print('Ciphertext: {}'.format(ciphertext))
    # plaintext = stream_cipher_decrypt(ciphertext, key)
    # print('Plaintext: {}'.format(plaintext))

    # other version from book

    plaintext = input('Enter binary plaintext: ')
    key = _generate_key(len(plaintext), "binary")
    print('Key: {}'.format(key))
    ciphertext = _stream_cipher_encrypt(plaintext, key, "binary")
    print('Ciphertext: {}'.format(ciphertext))
    plaintext = _stream_cipher_decrypt(ciphertext, key, "binary")
    print('Plaintext: {}'.format(plaintext))

    plaintext = input('Enter decimal plaintext: ')
    key = _generate_key(len(plaintext), "decimal")
    print('Key: {}'.format(key))
    ciphertext = _stream_cipher_encrypt(plaintext, key, "decimal")
    print('Ciphertext: {}'.format(ciphertext))
    plaintext = _stream_cipher_decrypt(ciphertext, key, "decimal")
    print('Plaintext: {}'.format(plaintext))

    plaintext = input('Enter alpabet plaintext: ')
    key = _generate_key(len(plaintext), "alpabet")
    print('Key: {}'.format(key))
    ciphertext = _stream_cipher_encrypt(plaintext, key, "alpabet")
    print('Ciphertext: {}'.format(ciphertext))
    plaintext = _stream_cipher_decrypt(ciphertext, key, "alpabet")
    print('Plaintext: {}'.format(plaintext))





