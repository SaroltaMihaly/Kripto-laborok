import socket
from lab2.stream_cipher import StreamCipher


def main():
    stream_cipher = StreamCipher("config_blum.json")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Várakozás a kapcsolatra...")
    client_socket, addr = server_socket.accept()
    print("Kapcsolat létrejött:", addr)

    while True:
        message = input("Kliens 1 üzenete: ")
        encrypted_message = stream_cipher.encrypt(message)
        print("Kliens 1 üzenete enkriptalva:", encrypted_message)
        client_socket.send(encrypted_message.encode('utf-8'))

        received_data = client_socket.recv(1024).decode('utf-8')
        print("Kliens 2 üzenete enkriptalva:", received_data)
        decrypted_message = stream_cipher.decrypt(received_data)
        print("Kliens 2 üzenete dekriptalva:", decrypted_message)

    server_socket.close()


if __name__ == "__main__":
    main()
