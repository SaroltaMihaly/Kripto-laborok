from ast import literal_eval

import lab3.KeyServerHeader as KeyServerHeader
import socket
import threading
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

    def get_public_key(self, port: int) -> KeyServerHeader.PublicKeyType:
        return self.registered_clients[port] if port in self.registered_clients else None

    def socket_communication(self, conn: socket.socket):
        data = conn.recv(KeyServerHeader.MESSAGE_SIZE)

        if not data:
            logging.info('')
            return
        request = data.decode()
        logging.info(f'Decoded request: {request}')

        while KeyServerHeader.END_CONN not in request:
            if 'PUBLIC_KEY' in request:
                try:
                    port = int(request.split(':')[1])
                    public_key = self.get_public_key(port)
                    if public_key:
                        logging.info(f'Sending public key: {public_key}')
                        conn.sendall(str(public_key).encode())
                    else:
                        logging.info('Error: Invalid request: No such client')
                        conn.sendall(KeyServerHeader.INVALID.encode())
                except ValueError:
                    logging.info('Error: Invalid request')
                    conn.sendall(KeyServerHeader.INVALID.encode())
            elif 'REGISTER' in request:
                try:
                    port, public_key = literal_eval(request.split(':')[1])
                    self.register_client((port, public_key))
                    logging.info(f'Registered client: {port=}, {public_key=}')
                    conn.sendall(KeyServerHeader.GOOD.encode())
                except SyntaxError:
                    logging.info('Error: Invalid request')
                    conn.sendall(KeyServerHeader.INVALID.encode())

            data = conn.recv(KeyServerHeader.MESSAGE_SIZE)
            if not data:
                logging.info('No data received, closing client socketo!')
                break
            request = data.decode()
            logging.info(f'Decoded request: {request}')

        conn.close()
        logging.info('Closed connection with client')

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ser_socket:
            ser_socket.bind((KeyServerHeader.SERVER_HOST, KeyServerHeader.SERVER_PORT))
            ser_socket.listen(self.max_clients)
            logging.info('Server listening...')

            while True:
                conn, address = ser_socket.accept()
                logging.info(f'Connected to {address}...')
                threading.Thread(target=self.socket_communication, args=(conn,)).start()


if __name__ == '__main__':
    server = KeyServer()
    server.start_server()

