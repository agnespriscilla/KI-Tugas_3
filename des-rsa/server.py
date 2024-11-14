import socket
import rsa
import des
import json

# Function to combine the received message blocks (server-side)
def combine_message(blocks):
    return ''.join(blocks)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = socket.gethostname()
port = 5050
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {host}:{port}...")

# Wait for a connection from a client
print("Waiting for connection...")
client_socket, addr = server_socket.accept()
print(f"Got connection from: {addr}\n")

# RSA configuration (server-side)
p, q = 982451653, 104729  # Use larger primes
n = p * q
phi_n = (p - 1) * (q - 1)
e = rsa.generate_e(phi_n)
public_key = {"e": e, "n": n}
print(f"Public key: {public_key}")

# Generate RSA private key
d = pow(e, -1, phi_n)
private_key = {"d": d, "n": n}
print(f"Private key: {private_key}\n")

# Send RSA public key to client
serialized_public_key = json.dumps(public_key).encode('utf-8')
client_socket.sendall(serialized_public_key)

# Receive encrypted message blocks
received_blocks = []
while True:
    encrypted_block = client_socket.recv(1024)
    if not encrypted_block:
        break
    encrypted_block = eval(encrypted_block.decode('utf-8'))  # Convert string back to integer
    received_blocks.append(rsa.decrypt(encrypted_block, private_key))
    print(f"Received encrypted block and decrypted: {received_blocks[-1]}")

# Combine the decrypted message blocks
decrypted_message = combine_message(received_blocks)
print(f"Decrypted message: {decrypted_message}")

# Close the connection
client_socket.close()