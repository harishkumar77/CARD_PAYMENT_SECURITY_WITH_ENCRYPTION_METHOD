from flask import Flask, redirect, url_for, render_template, request
import socket
import random

app = Flask(__name__)


def encrypt(message, public_key):
    """Encrypt a message using RSA."""
    e, n = public_key
    return pow(message, e, n)


def read_key_from_file(filename):
    """Read the key from a text file."""
    with open(filename, 'r') as file:
        key_values = file.read().split(',')
    return tuple(map(int, key_values))


read_public_key = read_key_from_file('public_key.txt')


def send_server(card_number, pin):
    server_host = '127.0.0.1' 
    server_port = 5050  
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        encrypted_number_card = encrypt(int(card_number), read_public_key)
        encrypted_number_pin = encrypt(int(pin), read_public_key)
        data = f"{encrypted_number_card},{encrypted_number_pin}"
        client_socket.send(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

        if response == "Transaction successful":
            return redirect(url_for("success"))
        else:
            return redirect(url_for("failure"))
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for("failure"))
    finally:
        client_socket.close()


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        card_number = request.form["card_number"]
        pin = request.form["pin"]
        return send_server(card_number, pin)
    else:
        return render_template("index(1).html")


@app.route("/success")
def success():
    return render_template("success(1).html")


@app.route("/failure")
def failure():
    return render_template("failure (1).html")


if __name__ == "__main__":
    app.run(debug=True)