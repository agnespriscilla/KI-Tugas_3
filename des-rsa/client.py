import socket
import rsa
import des
import json

# Function to split message into smaller blocks (8 characters per block)
def split_message(message, block_size=8):
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = socket.gethostname()  # Replace with server's IP
port = 5050
client_socket.connect((host, port))

# RSA public key from Public Key Authority (PKA)
pka_public_key = {"e": 65537, "n": 1234567890123456}  # This is an example, replace it with actual PKA key
print("Public key dari PKA:", pka_public_key)

# Receive server's public key
server_public_key = json.loads(client_socket.recv(1024).decode('utf-8'))
print("Received server public key:", server_public_key)

# Input the message
message = input("Enter a message to send to the server: ")

# Split the message into blocks
blocks = split_message(message)

# Encrypt each block using RSA
for block in blocks:
    message_encrypted = rsa.encrypt(block, server_public_key)
    print(f"Encrypted block: {message_encrypted}")
    
    # Send the encrypted block to the server
    client_socket.sendall(str(message_encrypted).encode())

# Close the connection
client_socket.close()