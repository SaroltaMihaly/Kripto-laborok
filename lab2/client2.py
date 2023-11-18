import socket
from lab2.stream_cipher import StreamCipher


def main():
    stream_cipher = StreamCipher("config.json")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    while True:
        received_data = client_socket.recv(1024).decode('utf-8')
        print("Kliens 1 üzenete enkriptálva:", received_data)
        decrypted_message = stream_cipher.decrypt(received_data)
        print("Kliens 1 üzenete dekriptalva:", decrypted_message)

        message = input("Kliens 2 üzenete: ")
        encrypted_message = stream_cipher.encrypt(message)
        print("Kliens 2 üzenete enkriptálva:", encrypted_message)
        client_socket.send(encrypted_message.encode('utf-8'))

    client_socket.close()


if __name__ == "__main__":
    main()
