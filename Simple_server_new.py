import socket
import threading

server_host = '127.0.0.1'
server_port = 5050


# =================================================================================================

def decrypt(ciphertext, private_key):
    """Decrypt a ciphertext using RSA."""
    d, n = private_key
    return pow(ciphertext, d, n)


def read_key_from_file(filename):
    """Read the key from a text file."""
    with open(filename, 'r') as file:
        key_values = file.read().split(',')
    return tuple(map(int, key_values))


read_private_key = read_key_from_file('E:/downloads/private_key.txt')


def check_data(user_number, user_pin, number_pin_dict):
    if user_number in number_pin_dict:
        if user_pin == number_pin_dict[user_number]:
            return True  # PIN is correct
        else:
            return False  # PIN is incorrect
    else:
        return False


def handle_client(client_socket, number_pin_dict):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            decoded_data = data.decode('utf-8')
            user_number, user_pin = map(int, decoded_data.split(','))
            decrypted_number_card = decrypt(user_number, read_private_key)
            decrypted_number_pin = decrypt(user_pin, read_private_key)
            if check_data(int(decrypted_number_card), int(decrypted_number_pin), number_pin_dict):
                response = "Transaction successful"
            else:
                response = "Transaction failed"

            # Debugging: Print the response before sending
            print(f"Sending response: {response}")

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def main():
    number_pin_dict = {
        1234567891012341: 98765,
        9876543219910012: 54325,
    }

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print(f"Server is listening on {server_host}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, number_pin_dict))
        client_handler.start()


if __name__ == '__main__':
    main()
