import socket
import KeyServerHeader
import logging
from lab1.crypto import generate_private_key, create_public_key, encrypt_mh, decrypt_mh


logging.basicConfig(level=logging.DEBUG, format='CLIENT : %(message)s')

class Client:

    def _generate_register_client(self):
        logging.info('Generating register request')
        private_key = generate_private_key()
        logging.info(f'Private key: {private_key}')

        logging.info('Create public key')
        public_key = create_public_key(private_key)
        logging.info(f'Public key: {public_key}')

        self.client_server_socket.sendall(f'REGISTER:{self.port, public_key}'.encode())
        data = self.client_server_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
        logging.info(f'Received data: {data}')
        if data == KeyServerHeader.GOOD:
            logging.info('Registered successfully')
        else:
            logging.info('Error: Invalid request')
            return

        return private_key, public_key

    def _get_public_key(self, port: int):
        logging.info('Getting public key')
        self.client_server_socket.sendall(f'PUBLIC_KEY:{port}'.encode())
        data = self.client_server_socket.recv(KeyServerHeader.MESSAGE_SIZE).decode()
        logging.info('Received data: ', data)
        return data

    def __init__(self):
        port = input('Enter port: ')
        self.port = int(port)
        self.client_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_server_socket.connect((KeyServerHeader.SERVER_HOST, KeyServerHeader.SERVER_PORT))

        private_key, public_key = self._generate_register_client()

        friend_port = input('Enter friend port: ')
        friend_port = int(friend_port)
        friend_public_key = self._get_public_key(friend_port)
        logging.info('Friend public key: ', friend_public_key)



def main():
    client = Client()


if __name__ == "__main__":
    main()
