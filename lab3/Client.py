import random
import sys
import socket
import json
import threading
import os

from ast import literal_eval
from pathlib import Path

import KeyServerHeader
import MerkleHellman
import logging

sys.path.append(str(Path(__file__).parent.parent.resolve()))
from lab2.stream_cipher import StreamCipher

logging.basicConfig(level=logging.INFO, format='CLIENT : %(message)s')


class Client:
    def _generate_register_client(self):
        private_key = MerkleHellman.generate_private_key()
        logging.info(f'Private key: {private_key}')

        public_key = MerkleHellman.create_public_key(private_key)
        logging.info(f'Public key: {public_key}')

        self.server_socket.sendall(f'REGISTER:{self.port, public_key}'.encode())
        data = self.server_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()

        if data == KeyServerHeader.INVALID:
            logging.info('Error: Invalid request')
            return

        logging.info(f'Received data: {data}')
        if data == KeyServerHeader.GOOD:
            logging.info('Registered successfully')
        else:
            logging.info('Error: Invalid request')
            return

        return private_key, public_key

    def _get_public_key(self):
        logging.info('Getting public key')
        self.server_socket.sendall(f'PUBLIC_KEY:{self.friend_port}'.encode())
        data = self.server_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()

        if data == KeyServerHeader.INVALID:
            logging.info('Error: Invalid request')
            exit(1)
        logging.info(f'Received friend public key: {data}')
        self.friend_public_key = literal_eval(data)

        # Close connection to key server
        self.server_socket.sendall(KeyServerHeader.END_CONN.encode())
        self.server_socket.close()

    def _start_communication(self):
        # Setup solitaire secret key
        logging.info('Setting up solitaire secret key')
        if self.state == 1:
            my_half = list(range(1, 28))
            random.shuffle(my_half)
        else:
            my_half = list(range(28, 55))
            random.shuffle(my_half)
        # Send half of solitaire secret key
        # logging.info(f'My half unencrypted: {str(my_half)}')
        sent_message = json.dumps(MerkleHellman.encrypt_mh(str(my_half), self.friend_public_key))
        # logging.info(f'Sending my half encrypted: {sent_message}')
        self.friend_socket.sendall(sent_message.encode())

        # Receive other half of solitaire secret key
        received = self.friend_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
        other_half_encrypted = json.loads(received)
        # logging.info(f'Received other half encrypted: {other_half_encrypted}')
        other_half = literal_eval(MerkleHellman.decrypt_mh(other_half_encrypted, self.private_key))
        # logging.info(f'Other half decrypted: {other_half}')

        def combine_solitaire_element(my, friend):
            return (my, friend) if self.state == 1 else (friend, my)

        # Combine the two halves by alternating elements
        [self.solitaire_seed.extend(combine_solitaire_element(m, f)) for m, f in zip(my_half, other_half)]
        logging.info(f'Solitaire seed: {self.solitaire_seed}')

    def _start_chat(self):
        stream_cipher = StreamCipher(config_dict={
            'seed': self.solitaire_seed,
            'random_generator': 'solitaire'
        })

        # Server will send first message
        if self.state == 2:
            received = self.friend_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
            print(f'Received encrypted: {received}')
            decrypted = stream_cipher.decrypt(received)
            print(f'Decrypted: {decrypted}')

            if decrypted == KeyServerHeader.END_CONN:
                print('Ending communication...')
                self.friend_socket.sendall(stream_cipher.encrypt(KeyServerHeader.END_CONN).encode())
                return

        message = input('Enter message: ')
        while message:
            # Send message
            encrypted = stream_cipher.encrypt(message)
            print(f'Sending encrypted: {encrypted}')
            self.friend_socket.sendall(encrypted.encode())

            if message == KeyServerHeader.END_CONN:
                print('Ending communication...')
                return

            # Receive message
            received = self.friend_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
            print(f'Received encrypted: {received}')
            decrypted = stream_cipher.decrypt(received)
            print(f'Decrypted: {decrypted}')

            if decrypted == KeyServerHeader.END_CONN:
                print('Ending communication...')
                self.friend_socket.sendall(stream_cipher.encrypt(KeyServerHeader.END_CONN).encode())
                return
            message = input('Enter message: ')


    def _threaded_client(self):
        self.client_server_socket.listen(1)
        logging.info(f'Waiting for other clients on port: {self.port}')

        conn, addr = self.client_server_socket.accept()
        logging.debug(f'Connected to: {addr}')

        self.friend_socket = conn

        self.state = 1  # Server
        message = self.friend_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
        logging.debug(f'Received message: {message}')
        self.friend_port = int(message)
        logging.info(f'Starting chat with {self.friend_port}...')

        self.friend_socket.sendall(KeyServerHeader.GOOD.encode())
        self.client_server_socket.close()

    def __init__(self):
        self.port = int(input('Enter own port: '))
        self.host = 'localhost'
        self.solitaire_seed: list[int] = []

        self.friend_socket = None
        self.friend_port = None
        self.friend_public_key = None
        self.state = 0

        # Own server socket
        self.client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_server_socket.bind((self.host, self.port))

        threading.Thread(target=self._threaded_client).start()

        # Register client to key server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((KeyServerHeader.SERVER_HOST, KeyServerHeader.SERVER_PORT))
        self.private_key, self.public_key = self._generate_register_client()

        try:
            self.friend_port = int(input('Enter friend port: '))
        except KeyboardInterrupt:
            ...

        if self.port == self.friend_port:
            logging.error('Error: Own port and friend port cannot be the same')
            exit(1)

        self._get_public_key()

        if self.state != 1:
            self.friend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.friend_socket.connect((self.host, self.friend_port))
            self.state = 2
            self.friend_socket.sendall(f'{self.port}'.encode())
            message = self.friend_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
            if message != KeyServerHeader.GOOD:
                logging.error(f'Unexpected response from other client: {message}')
                exit(1)

        self._start_communication()
        self._start_chat()
        self.friend_socket.close()
        logging.info('Communication overrrr! Bye!!!')
        os._exit(0)


def main():
    client = Client()


if __name__ == "__main__":
    main()
