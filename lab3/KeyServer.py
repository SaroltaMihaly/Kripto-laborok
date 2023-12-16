from ast import literal_eval

import KeyServerHeader
import socket
import logging

logging.basicConfig(level=logging.DEBUG, format='SERVER : %(message)s')


class KeyServer(object):
    def __init__(self):
        self.max_clients = 5
        self.registered_clients = {}

    def register_client(self, register_request: KeyServerHeader.RegisterType):
        port, public_key = register_request
        if port not in self.registered_clients:
            logging.debug('Registering a new client')
        self.registered_clients[port] = public_key

    def get_public_key(self, port: int):
        return self.registered_clients[port]

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ser_socket:
            ser_socket.bind((KeyServerHeader.SERVER_HOST, KeyServerHeader.SERVER_PORT))
            ser_socket.listen(self.max_clients)
            logging.info('Server listening...')

            while True:
                conn, addr = ser_socket.accept()
                logging.info('Connected by', addr)
                data = conn.recv(KeyServerHeader.MESSAGE_SIZE)

                if not data:
                    logging.info('')
                    break

                request = data.decode()
                logging.info('Decoded request: ', request)

                if 'PUBLIC_KEY' in request:
                    try:
                        port = int(request.split(':')[1])
                        public_key = self.get_public_key(port)
                        logging.info('Sending public key: ', public_key)
                        conn.sendall(str(public_key).encode())
                    except ValueError:
                        logging.info('Error: Invalid request')
                        conn.sendall('Error: Invalid request'.encode())
                elif 'REGISTER' in request:
                    try:
                        port, public_key = literal_eval(request)
                        self.register_client((port, public_key))
                        logging.info('Registered client: ', port, public_key)
                        conn.sendall('Registered client'.encode())
                    except ValueError:
                        logging.info('Error: Invalid request')
                        conn.sendall('Error: Invalid request'.encode())

                conn.close()


if __name__ == '__main__':
    server = KeyServer()
    server.start_server()





